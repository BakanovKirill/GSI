# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0020_datapolygons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datapolygons',
            old_name='name',
            new_name='attribute',
        ),
    ]
