# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20170110_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelfdata',
            name='attribute_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Attribute Name', blank=True),
        ),
    ]
