# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-06 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quicklook', '0004_auto_20171106_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steps',
            name='movement_consistency',
            field=models.TextField(blank=True),
        ),
    ]