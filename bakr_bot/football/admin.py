from django.contrib import admin
from bakr_bot.football.models import Country, Fixture, League, Team

class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'is_real']


admin.site.register(Country, CountryAdmin)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'country']


admin.site.register(League, LeagueAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'league']


admin.site.register(Team, TeamAdmin)


class FixtureAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_date', 'name', 'status', 'api_id', 'league']


admin.site.register(Fixture, FixtureAdmin)
