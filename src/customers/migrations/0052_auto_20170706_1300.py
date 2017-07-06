# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0051_auto_20170706_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerinfopanel',
            name='tif_path2',
        ),
        migrations.AlterField(
            model_name='customerinfopanel',
            name='attribute_name',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customerinfopanel',
            name='file_area_name',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customerinfopanel',
            name='png_path',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customerinfopanel',
            name='statisctic',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customerinfopanel',
            name='url_png',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
