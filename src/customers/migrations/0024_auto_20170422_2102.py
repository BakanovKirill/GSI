# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0023_auto_20170422_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerpolygons',
            old_name='url',
            new_name='kml_url',
        ),
    ]
