# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-13 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datefile',
            name='archivo',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='datefile',
            name='fecha',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
