from django.contrib import admin
from bakr_bot.football.models import Country, League, Team

class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'is_real']


admin.site.register(Country, CountryAdmin)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'country']


admin.site.register(League, LeagueAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'league']


admin.site.register(Team, TeamAdmin)
