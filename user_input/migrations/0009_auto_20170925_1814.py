# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0008_auto_20170925_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdailyinput',
            name='created_at',
            field=models.DateField(unique=True),
        ),
    ]