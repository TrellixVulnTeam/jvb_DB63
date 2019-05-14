# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-30 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0059_auto_20190430_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyuserinputencouraged',
            name='hr_down_99',
            field=models.CharField(blank=True, choices=[('', ''), ('', '-'), ('yes', 'Yes'), ('yes', 'yes'), ('no', 'no'), ('no', 'No')], max_length=4),
        ),
        migrations.AlterField(
            model_name='dailyuserinputencouraged',
            name='measured_hr',
            field=models.CharField(blank=True, choices=[('', ''), ('', '-'), ('yes', 'Yes'), ('yes', 'yes'), ('no', 'no'), ('no', 'No')], max_length=4),
        ),
    ]
