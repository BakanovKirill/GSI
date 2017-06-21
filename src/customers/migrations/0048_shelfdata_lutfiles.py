# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0047_auto_20170620_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelfdata',
            name='lutfiles',
            field=models.ForeignKey(related_name='lut_files', verbose_name=b'LUTFiles', blank=True, to='customers.LutFiles', null=True),
        ),
    ]
