"""
Add initial data database using api-football.com.
"""

import requests

from django.utils.dateparse import parse_datetime

from bakr_bot.football.models import *

REQUEST_HEADERS = {
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "21c4bef1damsh4ccce9c4dc1366fp18cf5bjsn91ea67ad9298"
}


def add_countries_to_db():
    url = "https://api-football-v1.p.rapidapi.com/v2/countries"

    try:
        resp = requests.get(url, headers=REQUEST_HEADERS)
        resp.raise_for_status()

        countries = resp.json()['api']['countries']
        print(len(countries))
        print(countries[0])

        for country in countries:
            c, created = Country.objects.get_or_create(code=country['code'], defaults={
                'name': country['country'],
                'data': country
            })

            if created:
                print("Country {} - {} created.".format(c.id, c.name))
            else:
                print("Country {} - {} already exists!".format(c.id, c.name))

    except requests.exceptions.HTTPError as e:
        print(e)

def add_leagues_by_season_to_db(season=2018):
    url = "https://api-football-v1.p.rapidapi.com/v2/leagues/season/{}".format(season)

    try:
        resp = requests.get(url, headers=REQUEST_HEADERS)
        resp.raise_for_status()

        leagues = resp.json()['api']['leagues']
        print('# of legues: ', len(leagues))

        for league in leagues:
            country = Country.objects.get(code=league['country_code'])
            l, created = League.objects.get_or_create(api_id=league['league_id'], defaults={
                'name': league['name'],
                'country': country,
                'data': league
            })

            if created:
                print("League {} - {} created.".format(l.id, l.name))
            else:
                print("League {} - {} already exists!".format(l.id, l.name))

    except requests.exceptions.HTTPError as e:
        print(e)


def add_leagues_to_db():
    url = "https://api-football-v1.p.rapidapi.com/v2/leagues"

    try:
        resp = requests.get(url, headers=REQUEST_HEADERS)
        resp.raise_for_status()

        leagues = resp.json()['api']['leagues']
        print('# of legues: ', len(leagues))

        for league in leagues:
            country = Country.objects.get(code=league['country_code'])
            l, created = League.objects.get_or_create(api_id=league['league_id'], defaults={
                'name': league['name'],
                'country': country,
                'data': league
            })

            if created:
                print("League {} - {} created.".format(l.id, l.name))
            else:
                print("League {} - {} already exists!".format(l.id, l.name))

    except requests.exceptions.HTTPError as e:
        print(e)


def add_teams_for_supported_leagues_to_db():
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/{league_id}"

    supported_lagues = League.objects.filter(is_supported=True)

    for league in supported_lagues:

        try:
            resp = requests.get(url.format(league_id=league.api_id), headers=REQUEST_HEADERS)
            resp.raise_for_status()

            teams = resp.json()['api']['teams']
            print('# of teams in {} is {}'.format(league.name, len(teams)))

            for team in teams:
                t, created = Team.objects.get_or_create(api_id=team['team_id'], defaults={
                    'name': team['name'],
                    'league': league,
                    'data': team
                })

                if created:
                    print("Team {} - {} created.".format(t.id, t.name))
                else:
                    print("Team {} - {} already exists!".format(t.id, t.name))

        except requests.exceptions.HTTPError as e:
            print(e)


def add_fixtures_for_supported_leagues_to_db():
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}"

    supported_lagues = League.objects.filter(is_supported=True)

    for league in supported_lagues:

        try:
            resp = requests.get(url.format(league_id=league.api_id), headers=REQUEST_HEADERS)
            resp.raise_for_status()

            fixtures = resp.json()['api']['fixtures']
            print('# of fixtures in {} is {}'.format(league.name, len(fixtures)))

            for fixture in fixtures:
                f, created = Fixture.objects.get_or_create(api_id=fixture['fixture_id'], defaults={
                    'name': fixture['event_date'] + ' ' + fixture['homeTeam']['team_name'] + ' Vs. ' + fixture['awayTeam']['team_name'],
                    'league': league,
                    'home_team': Team.objects.get(api_id=fixture['homeTeam']['team_id']),
                    'away_team': Team.objects.get(api_id=fixture['awayTeam']['team_id']),
                    'event_date': parse_datetime(fixture['event_date']),
                    'status': fixture['status'],
                    'venue': fixture['venue'],
                    'data': fixture
                })

                if created:
                    print("Fixture {} - {} created.".format(f.id, f))
                else:
                    print("Fixture {} - {} already exists!".format(f.id, f))

        except requests.exceptions.HTTPError as e:
            print(e)
