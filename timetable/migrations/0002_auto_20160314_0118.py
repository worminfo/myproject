# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-13 17:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time_meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_obj', models.DateTimeField(default=datetime.datetime(2016, 3, 14, 1, 18, 27, 462607), unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='activity_event',
            name='end_date',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='end_time_profile', to='timetable.Time_meta'),
        ),
        migrations.AddField(
            model_name='activity_event',
            name='start_date',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='start_time_profile', to='timetable.Time_meta'),
        ),
    ]
