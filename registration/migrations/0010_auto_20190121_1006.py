# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-01-21 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_auto_20190121_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_age',
            field=models.PositiveIntegerField(),
        ),
    ]
