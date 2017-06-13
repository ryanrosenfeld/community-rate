# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_auto_20170523_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('message', models.CharField(max_length=300)),
                ('is_read', models.BooleanField(default=False)),
                ('notification_class', models.CharField(choices=[('Follower', 'Follower')], max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='siteuser',
            name='bio',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='postal',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
