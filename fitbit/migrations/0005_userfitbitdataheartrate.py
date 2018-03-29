# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-29 04:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fitbit', '0004_userfitbitdatasleep'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFitbitDataHeartRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_heartrate', models.TextField()),
                ('data', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fitbit_heartrate_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
