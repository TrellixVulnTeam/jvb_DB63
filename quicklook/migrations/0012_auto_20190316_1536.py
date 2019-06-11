# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-03-16 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quicklook', '0011_sleep_restless_sleep'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseandreporting',
            name='avg_non_strength_heartrate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exerciseandreporting',
            name='total_exercise_activities',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exerciseandreporting',
            name='total_strength_activities',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]