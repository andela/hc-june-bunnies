# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-18 11:22
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0015_profile_scheduled_task_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.CharField(default='* * * * *', max_length=100)),
                ('time_created', models.DateTimeField(default=datetime.datetime(2018, 7, 18, 11, 22, 3, 524851, tzinfo=utc))),
                ('subject', models.CharField(blank=True, max_length=1000)),
                ('body', models.CharField(blank=True, max_length=30)),
                ('task_scheduler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='scheduled_task_date_time',
        ),
    ]