# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_list_listentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('poster_path', models.TextField()),
                ('release_year', models.IntegerField()),
            ],
        ),
    ]
