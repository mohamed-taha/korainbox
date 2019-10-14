from django.contrib import admin

from bakr_bot.football.models import (
    Competition,
    CompetitionUserMembership,
    Country,
    Fixture,
    Team,
)

class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'code', 'name', 'name_ar', 'is_real']


admin.site.register(Country, CountryAdmin)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'name_ar', 'country', 'is_supported']
    list_filter = ['is_supported', 'country']
    search_fields = ['name', 'name_ar']

admin.site.register(Competition, CompetitionAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'name', 'name_ar', 'country']
    list_filter = ['country']
    search_fields = ['name', 'name_ar']


admin.site.register(Team, TeamAdmin)


class FixtureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'event_date', 'event_time', 'status', 'api_id', 'competition']
    search_fields = ['name', 'name_ar']
    list_filter = ['event_date', 'competition']


admin.site.register(Fixture, FixtureAdmin)


class CompetitionMembershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'competition', 'created']
    list_filter = ['competition', 'user']
    search_fields = ['competition', 'user']


admin.site.register(CompetitionUserMembership, CompetitionMembershipAdmin)
