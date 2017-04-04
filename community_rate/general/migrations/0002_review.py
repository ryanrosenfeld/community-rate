# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('rating', models.IntegerField()),
                ('reaction', models.CharField(max_length=100)),
                ('movie_id', models.IntegerField()),
                ('thoughts', models.CharField(max_length=10000)),
            ],
        ),
    ]
