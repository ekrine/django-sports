# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0004_auto_20171205_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='date',
            field=models.BigIntegerField(blank=True),
        ),
    ]