# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0025_configfile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configfile',
            options={'ordering': ('pathname',), 'verbose_name': 'Configuration Files'},
        ),
        migrations.AddField(
            model_name='cardsequence',
            name='configfile',
            field=models.ForeignKey(blank=True, to='gsi.ConfigFile', null=True),
        ),
    ]
