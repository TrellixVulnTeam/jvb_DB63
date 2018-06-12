# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-15 09:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hrr', '0004_auto_20180515_0922'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='hrr',
            name='hrr_hrr_user_id_10ca40_idx',
        ),
        migrations.RenameField(
            model_name='hrr',
            old_name='user',
            new_name='user_hrr',
        ),
        migrations.AlterUniqueTogether(
            name='hrr',
            unique_together=set([('user_hrr', 'created_at')]),
        ),
        migrations.AddIndex(
            model_name='hrr',
            index=models.Index(fields=['user_hrr', '-created_at'], name='hrr_hrr_user_hr_91f46b_idx'),
        ),
    ]