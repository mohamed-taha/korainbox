import logging
from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from model_utils.models import TimeStampedModel

from bakr_bot.football.utils import competition_directory_path

logger = logging.getLogger(__name__)
User = get_user_model()


class Country(TimeStampedModel):
    api_id = models.CharField(max_length=250, unique=True, null=True)  # ID on the API provider
    name = models.CharField(max_length=150)
    name_ar = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_real = models.CharField(max_length=1, default='1')  # TODO: remove this or change to Boolean

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Competition(TimeStampedModel):
    country = models.ForeignKey(Country, related_name='competitions', on_delete=models.CASCADE, blank=True, null=True)
    api_id = models.CharField(max_length=250, unique=True)  # ID on the API provider
    name = models.CharField(max_length=250)
    name_ar = models.CharField(max_length=250, blank=True, null=True)
    is_supported = models.BooleanField(_('Is competition supported by KoraInbox?'), default=False)

    logo = models.FileField(upload_to=competition_directory_path)
    followers = models.ManyToManyField(User, through='CompetitionUserMembership')

    data = JSONField(null=True, blank=True)

    def fetch_and_update_fixtures(self, date: str = None):
        """Get competition fixtures (matches) on a date and save them to DB.
        Args:
            - data: :String date string of format `yyyy-mm-dd` ex: 2019-07-09
                    if not provided all the competition fixtures will be fetched
        """
        logger.info("Started fetching and updating compteition %s fixtures for date: %s",
                    self.name, date)

        api_fixtures_url_extra_params = f"&competition_id={self.api_id}"
        api_fixtures_url_extra_params += f"&date={date}" if date is not None else ''
        api_fixtures_url = settings.LIVESCORE_FIXTURES_LIST_API_URL + api_fixtures_url_extra_params
        session = requests.Session()

        while api_fixtures_url:
            resp = session.get(api_fixtures_url)
            resp.raise_for_status()
            data = resp.json()
            fixtures = data['data']['fixtures']

            for fixture in fixtures:
                home_team = Team.objects.get(api_id=fixture['home_id'])
                away_team = Team.objects.get(api_id=fixture['away_id'])
                db_fixture, created = Fixture.objects.update_or_create(api_id=fixture['id'], defaults={
                    'name_ar': fixture['away_name'] + "  -  " + fixture['home_name'],
                    'competition': self,
                    'event_date': fixture['date'],
                    'event_time': fixture['time'] if fixture['time'] != "00:00" else None,
                    'round': fixture['round'] if str(fixture['round']) != "999" else None,
                    'venue': fixture['location'],
                    'home_team': home_team,
                    'away_team': away_team,
                    'name': home_team.name + " Vs. " + away_team.name,
                    'data': fixture
                })
                if created:
                    logger.info("Fixture %d inserted to DB", db_fixture.id)
                else:
                    logger.info("Fixture %d updated in DB", db_fixture.id)

            api_fixtures_url = data['data']['next_page']

        logger.info("Finished fetching and updating comptetition %s fixtures for date: %s", self.name, date)

    def next_30_days_fixtures(self):
        """
        Return nearst 10 fixtures in the coming 30 days including today.
        """
        # TODO: Enhance to return today's matches and then next days (annotation)
        today = timezone.now().date()
        fixtures = self.fixtures.filter(
            event_date__gte=today, event_date__lte=today + timedelta(days=30)).order_by('event_date', 'event_time')[:10]
        return fixtures if fixtures.exists() else None

    def __str__(self):
        if getattr(self, 'country'):
            return f"{self.name} - {self.country.name}"
        else:
            return self.name


class Team(TimeStampedModel):
    country = models.ForeignKey(Country, related_name='teams', on_delete=models.CASCADE, null=True, blank=True)
    api_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    name_ar = models.CharField(max_length=250, blank=True, null=True)

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Fixture(TimeStampedModel):
    """Fixtures = Matches"""
    competition = models.ForeignKey(Competition, related_name='fixtures', on_delete=models.CASCADE)
    api_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    name_ar = models.CharField(max_length=250, null=True, blank=True)
    event_date = models.DateField()
    event_time = models.TimeField(null=True, blank=True)
    round = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, null=True, blank=True)
    elapsed = models.SmallIntegerField(default=0)
    venue = models.CharField(_('Venue / Stadium'), max_length=250, null=True, blank=True)

    home_team = models.ForeignKey(Team, related_name='home_fixtures', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_fixures', on_delete=models.CASCADE)

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return "%s %s Vs. %s" %(str(self.event_date), self.home_team.name, self.away_team.name)


class CompetitionUserMembership(TimeStampedModel):
    """
    A `through` class for many-to-many relationship between users and competitions.
    User can follow multiple competitions and competitions can be followed by multiple users.
    """
    user = models.ForeignKey(User, related_name="leagues", on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name="users", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'competition')
