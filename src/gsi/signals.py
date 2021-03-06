# -*- coding: utf-8 -*-
from datetime import datetime
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from gsi.models import Tile, Area, RunBase, Run, CardSequence, InputDataDirectory
from customers.models import DataSet, CustomerAccess
from log.logger import log_it
from core.utils import update_list_files


from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_users_folders(sender, instance=None, created=False, **kwargs):
    if created:
        path_ftp_user = os.path.join(settings.FTP_PATH, instance.username)
        user_kml_dir = os.path.join(settings.KML_PATH, instance.username)
        user_remap_dir = os.path.join(settings.REMAP_PATH, instance.username)

        try:
            os.makedirs(path_ftp_user, 0755)
        except OSError:
            pass

        try:
            os.makedirs(user_kml_dir, 0755)
        except OSError:
            pass
        
        try:
            os.makedirs(user_remap_dir, 0755)
        except OSError:
            pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_default_datasets(sender, instance=None, created=False, **kwargs):
    if created:
        default_datasets = DataSet.objects.filter(is_default=True)

        if default_datasets:
            access = CustomerAccess.objects.create(
                    user=instance
                )
            for n in default_datasets:
                # print '!!!!!!!!!!!!!! N DS ========================== ', n
                # print '!!!!!!!!!!!!!! N ID DS ========================== ', n.id
                CustomerAccess.data_set.through.objects.create(
                    customeraccess_id=access.id,
                    dataset_id=n.id
                )


@receiver(post_save, sender=Tile)
def added_update_area_for_each_tile(sender, instance, **kwargs):
    """**When created new Tile object then creating a new Area object
    and in the field "tile" of Area models added the new Tiles object**.

    """

    try:
        area = Area.objects.get(tiles=instance)
        area.name = instance.name
    except Exception:
        area = Area(name=instance.name)
    finally:
        area.save()
        area.tiles.add(instance)


@receiver(post_delete, sender=Tile)
def remove_empty_area_by_removing_tile(sender, instance, **kwargs):
    """**When removing Tiles object then removed Area object**."""
    Area.objects.filter(tiles__isnull=True).delete()


@receiver(post_save, sender=RunBase)
def log_it_runbase(sender, instance, created, **kwargs):
    """**Write to log information about the change in RunBase object.**"""

    if created:
        massage = 'Run created: ID - {0}'.format(instance.id)
        log_it(instance.author, 'RunBase', instance.id, massage)
    else:
        massage = 'Edited Run: ID - {0}'.format(instance.id)
        log_it(instance.author, 'RunBase', instance.id, massage)


@receiver(post_save, sender=RunBase)
def create_cs(sender, instance, created, **kwargs):
    """**When created the new RunBase object  than creating new the CardSequence object.**"""
    cs_name = 'CS{0}'.format(instance.id)

    if not CardSequence.objects.filter(name=cs_name).exists():
        cs_new = CardSequence.objects.create(name=cs_name)
        instance.card_sequence = cs_new
        instance.save()
        cs_new.save()


@receiver(post_save, sender=Run)
def log_it_run(sender, instance, **kwargs):
    """**Writes the log information on the status of the object Run.**"""
    if instance.state == 'success' or instance.state == 'fail':
        message = 'Run executed: Run ID - {0}; status - {1}'.format(
            instance.run_base.id, instance.state.capitalize())
        log_it(instance.user, 'Run', instance.run_base.id, message)


# @receiver(post_save, sender=InputDataDirectory)
# def mkdir(sender, instance, **kwargs):
#     """**When created new InputDataDirectory object then creating new directory with name new_object.name .**"""
#     update_list_files(instance)
