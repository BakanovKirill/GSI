# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0014_customerpolygons_kml_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelfdata',
            name='show_totals',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shelfdata',
            name='attribute_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Attribute Names', blank=True),
        ),
        migrations.AlterField(
            model_name='shelfdata',
            name='root_filename',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Root Filenames', blank=True),
        ),
    ]
