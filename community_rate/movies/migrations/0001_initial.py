# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('rating', models.IntegerField()),
                ('reaction', models.CharField(max_length=100)),
                ('movie_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('thoughts', models.CharField(max_length=10000)),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
