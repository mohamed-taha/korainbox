from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.fields import BooleanField, SmallIntegerField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Country(TimeStampedModel):
    # api_id = models.CharField(max_length=250, unique=True, null=True)  # ID on the API provider
    name = models.CharField(max_length=150)
    name_ar = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_real = models.CharField(max_length=1, default='1')  # TODO: remove this or change to Boolean

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class League(TimeStampedModel):
    country = models.ForeignKey(Country, related_name='leagues', on_delete=models.CASCADE)
    api_id = models.CharField(max_length=250, unique=True)  # ID on the API provider
    name = models.CharField(max_length=250)
    name_ar = models.CharField(max_length=250, blank=True, null=True)
    is_supported = models.BooleanField(_('Is league supported by KoraInbox?'), default=False)

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.country.name)


class Team(TimeStampedModel):
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    api_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    name_ar = models.CharField(max_length=250, blank=True, null=True)

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.league.country.name)


class Fixture(TimeStampedModel):
    league = models.ForeignKey(League, related_name='fixtures', on_delete=models.CASCADE)
    api_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    event_date = models.DateTimeField()
    status = models.CharField(max_length=150)
    elapsed = models.SmallIntegerField(default=0)
    venue = models.CharField(_('Venue / Stadium'), max_length=250, null=True, blank=True)

    home_team = models.ForeignKey(Team, related_name='home_fixtures', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_fixures', on_delete=models.CASCADE)

    data = JSONField(null=True, blank=True)

    def __str__(self):
        return "%s %s Vs. %s" %(str(self.event_date), self.home_team.name, self.away_team.name)
