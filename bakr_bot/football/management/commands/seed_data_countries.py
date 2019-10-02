import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from bakr_bot.football.models import Country


class Command(BaseCommand):
    help = "Insert Country model seed data to database from the football API"

    def handle(self, *args, **kwargs):
        resp = requests.get(settings.LIVESCORE_COUNTRIES_LIST_API_URL).json()
        countries = resp['data']['country']
        new_countries = 0

        for country in countries:
            # Remove `leagues` and `scores` from country dict since they contain API and SECRET KEYS
            if 'leagues' in country:
                del country['leagues']
            if 'scores' in country:
                del country['scores'] 

            db_country, created = Country.objects.get_or_create(api_id=country['id'], defaults={
                "name": country['name'],
                "is_real": country['is_real'],
                "data": country
            })

            if created:
                new_countries += 1
                self.stdout.write("Country %d: %s inserted to DB" %(db_country.id, db_country.name))
            else:
                self.stdout.write("Country %d: %s already exists in DB" %(db_country.id, db_country.name))

        self.stdout.write(self.style.SUCCESS("Summary: %d new countries added to DB" % new_countries))
