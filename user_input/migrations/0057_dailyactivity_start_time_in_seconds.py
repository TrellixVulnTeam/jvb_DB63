# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-22 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0056_auto_20181004_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyactivity',
            name='start_time_in_seconds',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
