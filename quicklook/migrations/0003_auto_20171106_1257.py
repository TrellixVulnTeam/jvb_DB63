# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-06 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quicklook', '0002_auto_20171106_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grades',
            old_name='movement_non_exercise_grade',
            new_name='movement_non_exercise_steps_grade',
        ),
    ]