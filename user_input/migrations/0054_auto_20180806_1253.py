# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-06 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import user_input.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0053_dailyuserinputstrong_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyuserinputencouraged',
            name='hr_level',
            field=models.CharField(blank=True, max_length=10, validators=[user_input.models.CharMinValueValidator(45), user_input.models.CharMaxValueValidator(220)]),
        ),
        migrations.AlterField(
            model_name='dailyuserinputencouraged',
            name='lowest_hr_during_hrr',
            field=models.CharField(blank=True, max_length=10, validators=[user_input.models.CharMinValueValidator(45), user_input.models.CharMaxValueValidator(220)]),
        ),
        migrations.AlterField(
            model_name='dailyuserinputencouraged',
            name='lowest_hr_first_minute',
            field=models.CharField(blank=True, max_length=10, validators=[user_input.models.CharMinValueValidator(45), user_input.models.CharMaxValueValidator(220)]),
        ),
    ]
