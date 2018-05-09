# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-08 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garmin', '0025_auto_20180508_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='garminpingnotification',
            name='state',
            field=models.CharField(choices=[('unprocessed', 'Unprocessed'), ('processing', 'Processing'), ('processed', 'Processed'), ('failed', 'Failed')], default='unprocessed', max_length=100),
            preserve_default=False,
        ),
    ]
