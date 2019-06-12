# Generated by Django 2.1.8 on 2019-06-11 20:30

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('livescore_id', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
                ('is_real', models.SmallIntegerField(default=1, max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
