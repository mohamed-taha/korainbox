# Generated by Django 2.1.8 on 2019-10-03 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0025_auto_20191003_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='name_ar',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
