# Generated by Django 2.1.8 on 2019-06-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0016_auto_20190620_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='name_ar_eg',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='league',
            name='name_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='name_ar_eg',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='name_en',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
