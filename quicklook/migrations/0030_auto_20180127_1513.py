# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-27 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quicklook', '0029_auto_20180126_0746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grades',
            old_name='exercise_consistency_gpa',
            new_name='exercise_consistency_score',
        ),
        migrations.AddField(
            model_name='exerciseandreporting',
            name='avg_exercise_heartrate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
