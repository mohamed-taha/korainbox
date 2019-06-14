# Generated by Django 2.1.8 on 2019-06-14 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='facebook_psid',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='FB Page-Scoped ID'),
        ),
    ]
