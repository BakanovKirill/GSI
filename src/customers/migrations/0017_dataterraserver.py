# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0016_auto_20170401_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataTerraserver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, null=True, blank=True)),
                ('shapefile', models.CharField(max_length=250, null=True, blank=True)),
                ('parameter', models.CharField(max_length=250, null=True, blank=True)),
                ('transaction_id', models.CharField(max_length=250, null=True, blank=True)),
                ('user', models.ForeignKey(verbose_name=b'User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Data from Terraserver',
            },
        ),
    ]
