# -*- coding: utf-8 -*-
import os
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings

from gsi.settings import KML_PATH, KML_DIRECTORY

from customers.models import CustomerPolygons

class Command(BaseCommand):
    def handle(self, *args, **options):
        for cp in CustomerPolygons.objects.all():
            old_path_kml = cp.kml_path
            path_kml_user = os.path.join(KML_PATH, cp.user.username, cp.kml_name)
            new_path_dir_kml_user = os.path.join(KML_PATH, cp.user.username)
            dir_kml_user = os.path.join(KML_DIRECTORY, cp.user.username, cp.kml_name)

            if not os.path.exists(new_path_dir_kml_user):
                os.makedirs(new_path_dir_kml_user)

            try:
                if not os.path.exists(old_path_kml):
                    old_path_kml = os.path.join(KML_PATH, cp.kml_name)

                shutil.move(old_path_kml, new_path_dir_kml_user)
            except Exception, e:
                pass

            cp.kml_path = path_kml_user
            kml_http = cp.kml_url.split('media')[0]
            cp.kml_url = os.path.join(kml_http, dir_kml_user)

            cp.save()

            print '******** DONE ********'
