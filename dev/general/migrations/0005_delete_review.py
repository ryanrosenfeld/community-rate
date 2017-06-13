# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_review_date_added'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
