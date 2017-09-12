# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-07 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garmin', '0004_auto_20170907_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergarmindataactivity',
            name='record_date_in_seconds',
            field=models.IntegerField(default=1504636200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergarmindatabodycomposition',
            name='record_date_in_seconds',
            field=models.IntegerField(default=1504636200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergarmindatadaily',
            name='record_date_in_seconds',
            field=models.IntegerField(default=1504636200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergarmindataepoch',
            name='record_date_in_seconds',
            field=models.IntegerField(default=1504636200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergarmindatamanuallyupdated',
            name='record_date_in_seconds',
            field=models.IntegerField(default=1504636200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergarmindatasleep',
            name='record_date_in_seconds',
            field=models.IntegerField(default=1504636200),
            preserve_default=False,
        ),
    ]