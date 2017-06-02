# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0038_attributesreport_statisctic'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(verbose_name=b'User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
