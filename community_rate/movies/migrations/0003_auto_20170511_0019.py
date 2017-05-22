# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20170510_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genreassignment',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='listentry',
            name='movie',
        ),
        migrations.AddField(
            model_name='listentry',
            name='movie_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='GenreAssignment',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
