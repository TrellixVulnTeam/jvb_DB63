# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-14 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hrr',
            old_name='HRR_activity_start_time',
            new_name='hrr_activity_start_time',
        ),
        migrations.RenameField(
            model_name='hrr',
            old_name='No_beats_recovered',
            new_name='no_beats_recovered',
        ),
    ]
