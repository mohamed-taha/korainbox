import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from bakr_bot.football.models import Country, Competition


class Command(BaseCommand):
    help = "Insert Competition model seed data to database from the football API"

    def handle(self, *args, **kwargs):
        resp = requests.get(settings.LIVESCORE_COMPETITIONS_LIST_API_URL).json()
        competitions = resp['data']['competition']
        new_competitions = 0

        for comp in competitions:
            if comp.get('countries') and len(comp['countries']) > 0:
                country = Country.objects.get(api_id=comp['countries'][0]['id'])
            else:
                country = None
            db_comp, created = Competition.objects.get_or_create(api_id=comp['id'], defaults={
                "name": comp['name'],
                "country": country,
                "data": comp
            })

            if created:
                new_competitions += 1
                self.stdout.write("Competition %d: %s inserted to DB" %(db_comp.id, db_comp.name))
            else:
                self.stdout.write("Competition %d: %s already exists in DB" %(db_comp.id, db_comp.name))

        self.stdout.write(self.style.SUCCESS("Summary: %d new competitions added to DB" % new_competitions))
