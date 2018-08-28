# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-06 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0054_auto_20180806_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyuserinputoptional',
            name='nap_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='dailyuserinputoptional',
            name='nap_duration',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='dailyuserinputoptional',
            name='nap_end_time',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='dailyuserinputoptional',
            name='nap_start_time',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='dailyuserinputoptional',
            name='took_nap',
            field=models.CharField(blank=True, choices=[('', '-'), ('yes', 'Yes'), ('no', 'No')], max_length=10),
        ),
    ]
