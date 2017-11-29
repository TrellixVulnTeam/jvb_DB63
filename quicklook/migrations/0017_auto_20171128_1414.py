# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-28 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quicklook', '0016_auto_20171127_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciseandreporting',
            name='heartrate_variability_grade',
        ),
        migrations.AddField(
            model_name='exerciseandreporting',
            name='heartrate_variability_stress',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
