# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreAssignment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('list', models.ForeignKey(to='movies.List')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('tmdb_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('poster_path', models.CharField(max_length=100)),
                ('overview', models.TextField()),
                ('release_date', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='listentry',
            name='movie',
            field=models.ForeignKey(to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='genreassignment',
            name='movie',
            field=models.ForeignKey(to='movies.Movie'),
        ),
    ]
