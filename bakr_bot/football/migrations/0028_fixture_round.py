# Generated by Django 2.1.8 on 2019-10-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0027_auto_20191003_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='round',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
