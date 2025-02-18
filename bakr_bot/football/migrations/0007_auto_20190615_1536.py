# Generated by Django 2.1.8 on 2019-06-15 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0006_team'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='livescore_id',
            new_name='api_id',
        ),
        migrations.RenameField(
            model_name='league',
            old_name='livescore_country_id',
            new_name='api_country_id',
        ),
        migrations.RenameField(
            model_name='league',
            old_name='livescore_id',
            new_name='api_id',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='livescore_id',
            new_name='api_id',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='livescore_league_id',
            new_name='api_league_id',
        ),
    ]
