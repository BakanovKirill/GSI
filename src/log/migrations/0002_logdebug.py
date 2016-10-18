# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDebug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('log', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
