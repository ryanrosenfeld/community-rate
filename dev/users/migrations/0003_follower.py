# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20170523_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date_followed', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(related_name='follower_set', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(related_name='following_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
