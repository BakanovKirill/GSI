# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings

from customers.models import DataPolygons


class Command(BaseCommand):
    def handle(self, *args, **options):
        for dp in DataPolygons.objects.all():
            dp.statistic = 'mean_ConditionalMean'
            dp.save()
            
