# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-11 11:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_check_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='profile',
        ),
    ]
