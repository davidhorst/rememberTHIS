# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='comment',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='name',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
