# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-12 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_input', '0022_auto_20171012_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyuserinputstrong',
            name='number_of_alcohol_consumed_yesterday',
            field=models.CharField(blank=True, choices=[('', '-'), ('0', '0'), ('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5'), ('5.5', '5.5'), ('6', '6'), ('6.5', '6.5'), ('7', '7'), ('7.5', '7.5'), ('8', '8'), ('8.5', '8.5'), ('9', '9'), ('9.5', '9.5'), ('10', '10'), ('10+', 'More than 10')], max_length=3, null=True),
        ),
    ]
