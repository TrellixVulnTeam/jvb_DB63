# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-03 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress_analyzer', '0012_auto_20180327_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='metacumulative',
            name='cum_mc_recorded_days_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
