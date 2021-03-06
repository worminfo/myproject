# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-25 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class_assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Class_code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(default='', max_length=2)),
                ('class_description', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Parent_contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_name', models.CharField(default='', max_length=255)),
                ('parent_type', models.CharField(choices=[('F', 'Father'), ('M', 'Mother'), ('G', 'Guardian'), ('O', 'Other')], default='', max_length=1)),
                ('parent_phone', models.CharField(default='', max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Permission_meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_key', models.CharField(default='', max_length=255)),
                ('permission_description', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='student', max_length=24)),
                ('level', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=255, unique=True)),
                ('firstname', models.CharField(default='', max_length=255)),
                ('lastname', models.CharField(default='', max_length=255)),
                ('password_hash', models.CharField(default='', max_length=96)),
                ('sex_code', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1)),
                ('card_id', models.CharField(blank=True, default='', max_length=20)),
                ('strn_code', models.CharField(blank=True, default='', max_length=12)),
                ('sams_code', models.CharField(blank=True, default='', max_length=12)),
                ('jupas_app_code', models.CharField(blank=True, default='', max_length=32)),
                ('barcode', models.CharField(blank=True, default='', max_length=32)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('hkid_card', models.CharField(blank=True, default='', max_length=12)),
                ('address', models.TextField(blank=True, default='')),
                ('phone', models.CharField(blank=True, default='', max_length=24)),
                ('mobile', models.CharField(blank=True, default='', max_length=24)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('national', models.CharField(blank=True, default='', max_length=24)),
                ('location_of_birth', models.CharField(blank=True, default='', max_length=24)),
                ('intake_date', models.CharField(blank=True, default='', max_length=24)),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Role')),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Permission_meta'),
        ),
        migrations.AddField(
            model_name='permission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='parent_contact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='class_assignment',
            name='class_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Class_code'),
        ),
        migrations.AddField(
            model_name='class_assignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
