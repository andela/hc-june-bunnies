# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-11 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_remove_check_profile'),
        ('accounts', '0011_remove_profile_profile_checks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='check_assigned',
        ),
        migrations.AddField(
            model_name='member',
            name='check_assigned',
            field=models.ManyToManyField(null=True, to='api.Check'),
        ),
    ]
