# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-27 04:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelplan', '0002_auto_20171027_0449'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='travel_date_to',
            new_name='traveldateto',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='trip_creater',
            new_name='tripcreater',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='trip_joiners',
            new_name='tripjoiners',
        ),
    ]
