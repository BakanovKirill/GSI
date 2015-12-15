# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('cards', '0001_initial'),
        ('gsi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='yearfilter',
            name='area',
            field=models.ForeignKey(to='gsi.Area'),
        ),
        migrations.AddField(
            model_name='rftrain',
            name='tile_type',
            field=models.ForeignKey(to='gsi.TileType'),
        ),
        migrations.AddField(
            model_name='rfscore',
            name='area',
            field=models.ForeignKey(to='gsi.Area'),
        ),
        migrations.AddField(
            model_name='rfscore',
            name='year_group',
            field=models.ForeignKey(to='gsi.YearGroup'),
        ),
        migrations.AddField(
            model_name='preproc',
            name='area',
            field=models.ForeignKey(to='gsi.Area'),
        ),
        migrations.AddField(
            model_name='preproc',
            name='year_group',
            field=models.ForeignKey(to='gsi.YearGroup'),
        ),
        migrations.AddField(
            model_name='orderedcarditem',
            name='card_item',
            field=models.ForeignKey(to='cards.CardItem'),
        ),
        migrations.AddField(
            model_name='collate',
            name='area',
            field=models.ForeignKey(to='gsi.Area'),
        ),
        migrations.AddField(
            model_name='carditem',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AlterUniqueTogether(
            name='carditem',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
