# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-03 03:03
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0004_newtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_char', models.CharField(max_length=30)),
                ('test_number', models.IntegerField()),
            ],
        ),
    ]
