# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0027_developmentpage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='developmentpage',
            old_name='is_active',
            new_name='is_development',
        ),
    ]
