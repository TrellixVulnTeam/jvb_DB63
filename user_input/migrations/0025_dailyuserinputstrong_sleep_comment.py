# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-25 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0024_dailyuserinputstrong_workout'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyuserinputstrong',
            name='sleep_comment',
            field=models.TextField(blank=True),
        ),
    ]
