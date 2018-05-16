# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-07 12:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('progress_analyzer', '0013_metacumulative_cum_mc_recorded_days_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='SickCumulative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cum_days_sick', models.IntegerField(blank=True, null=True)),
                ('cum_reported_sick_days_count', models.IntegerField(blank=True, null=True)),
                ('user_cum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sick_cum', to='progress_analyzer.CumulativeSum')),
            ],
        ),
        migrations.CreateModel(
            name='StandingCumulative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cum_days_stand_three_hour', models.IntegerField(blank=True, null=True)),
                ('cum_reported_stand_three_hours_days_count', models.IntegerField(blank=True, null=True)),
                ('user_cum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='standing_cum', to='progress_analyzer.CumulativeSum')),
            ],
        ),
        migrations.CreateModel(
            name='StressCumulative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cum_days_low_stress', models.IntegerField(blank=True, null=True)),
                ('cum_days_medium_stress', models.IntegerField(blank=True, null=True)),
                ('cum_days_high_stress', models.IntegerField(blank=True, null=True)),
                ('cum_reported_stress_days_count', models.IntegerField(blank=True, null=True)),
                ('user_cum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stress_cum', to='progress_analyzer.CumulativeSum')),
            ],
        ),
        migrations.CreateModel(
            name='TravelCumulative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cum_days_travel_away_from_home', models.IntegerField(blank=True, null=True)),
                ('user_cum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='travel_cum', to='progress_analyzer.CumulativeSum')),
            ],
        ),
    ]
