# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0036_attributesreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributesreport',
            name='attribute',
        ),
        migrations.AddField(
            model_name='attributesreport',
            name='shelfdata',
            field=models.ForeignKey(related_name='attributes_shelfdata', verbose_name=b'ShelfData', blank=True, to='customers.ShelfData', null=True),
        ),
    ]
