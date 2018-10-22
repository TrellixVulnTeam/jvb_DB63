# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-09 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress_analyzer', '0021_stresscumulative_cum_days_garmin_stress_lvl'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementconsistencycumulative',
            name='cum_exercise_active_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movementconsistencycumulative',
            name='cum_sleep_active_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movementconsistencycumulative',
            name='cum_total_active_min',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
