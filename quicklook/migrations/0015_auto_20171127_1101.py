# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-27 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quicklook', '0014_auto_20171121_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleep',
            name='sleep_awake_time',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sleep',
            name='sleep_bed_time',
            field=models.CharField(max_length=20),
        ),
    ]