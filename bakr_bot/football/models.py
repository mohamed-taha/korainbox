from django.db import models
from model_utils.models import TimeStampedModel


class Country(TimeStampedModel):
    livescore_id = models.CharField(max_length=250, unique=True)  # ID on the API provider (livescore-api.com)
    name = models.CharField(max_length=150)
    is_real = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.name


class League(TimeStampedModel):
    country = models.ForeignKey(Country, related_name='leagues', on_delete=models.CASCADE)
    livescore_id = models.CharField(max_length=250, unique=True)  # ID on the API provider (livescore-api.com)
    name = models.CharField(max_length=250)
    livescore_country_id = models.CharField(max_length=250)

    def __str__(self):
        return "%s - %s" % (self.name, self.country.name)


class Team(TimeStampedModel):
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    livescore_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    livescore_league_id = models.CharField(max_length=250)

    def __str__(self):
        return "%s - %s" % (self.name, self.league.country.name)