# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-18 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_buddy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('desc', models.TextField(max_length=1000)),
                ('date_from', models.CharField(max_length=45)),
                ('date_to', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('planner', models.ManyToManyField(related_name='planned', to='travel_buddy.User')),
            ],
        ),
    ]
