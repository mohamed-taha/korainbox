from django.db import models
from django.db.models.fields import BooleanField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Country(TimeStampedModel):
    api_id = models.CharField(max_length=250, unique=True)  # ID on the API provider
    name = models.CharField(max_length=150)
    is_real = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.name


class League(TimeStampedModel):
    country = models.ForeignKey(Country, related_name='leagues', on_delete=models.CASCADE)
    api_id = models.CharField(max_length=250, unique=True)  # ID on the API provider
    name = models.CharField(max_length=250)
    is_supported = models.BooleanField(_('Is league supported by KoraInbox?'), default=False)

    def __str__(self):
        return "%s - %s" % (self.name, self.country.name)


class Team(TimeStampedModel):
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    api_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return "%s - %s" % (self.name, self.league.country.name)