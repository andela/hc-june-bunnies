# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-19 09:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20180719_0812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='alert_sent',
        ),
        migrations.RemoveField(
            model_name='check',
            name='prev_alert_status',
        ),
    ]
