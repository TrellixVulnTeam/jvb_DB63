# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-07 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summary', '0002_auto_20170707_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary_desktop',
            name='Movement_When_Not_Sleeping',
            field=models.IntegerField(blank=True, default=None, help_text='Number of Hours per day Moved less than 300 steps an hour'),
        ),
    ]
