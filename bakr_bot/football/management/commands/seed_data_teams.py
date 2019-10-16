import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from bakr_bot.football.models import Country, Team


class Command(BaseCommand):
    help = "Insert Team model seed data to database from the football API"

    def handle(self, *args, **kwargs):
        session = requests.Session()
        teams_url = settings.LIVESCORE_TEAMS_LIST_API_URL
        new_teams = 0

        while teams_url:
            resp = session.get(teams_url)
            data = resp.json()
            teams = data['data']['teams']

            for team in teams:
                if team.get('country') and team['country'].get('id'):
                    country = Country.objects.get(api_id=team['country']['id'])
                else:
                    country = None
                db_team, created = Team.objects.get_or_create(api_id=team['id'], defaults={
                    'name': team['name'],
                    'name_ar': team['name_ar'] if team['name_ar'] else '',
                    'country': country,
                    'data': team
                })
                if created:
                    new_teams += 1
                    self.stdout.write("Team %d: %s inserted to DB" %(db_team.id, db_team.name))
                else:
                    self.stdout.write("Team %d: %s already exists in DB" %(db_team.id, db_team.name))

            teams_url = data['data']['next_page']

        self.stdout.write(self.style.SUCCESS("Summary: %d new teams added to DB" % new_teams))
