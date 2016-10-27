# -*- coding: utf-8 -*-
from datetime import datetime
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


from gsi.models import (Tile, Area, RunBase, Run, CardSequence,
                        InputDataDirectory, HomeVariables)
from log.logger import log_it
from core.utils import update_list_files


@receiver(post_save, sender=Tile)
def added_update_area_for_each_tile(sender, instance, **kwargs):
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
    Area.objects.filter(tiles__isnull=True).delete()


@receiver(post_save, sender=RunBase)
def log_it_runbase(sender, instance, created, **kwargs):
    # log_it(user, element, element_id, message)
    if created:
        massage = 'Run created: ID - {0}'.format(instance.id)
        log_it(instance.author, 'RunBase', instance.id, massage)
    else:
        massage = 'Edited Run: ID - {0}'.format(instance.id)
        log_it(instance.author, 'RunBase', instance.id, massage)


@receiver(post_save, sender=RunBase)
def create_cs(sender, instance, created, **kwargs):
    cs_name = 'CS{0}'.format(instance.id)

    if not CardSequence.objects.filter(name=cs_name).exists():
        cs_new = CardSequence.objects.create(name=cs_name)
        instance.card_sequence = cs_new
        instance.save()
        cs_new.save()


@receiver(post_save, sender=Run)
def log_it_run(sender, instance, **kwargs):
    # log_it(user, element, element_id, message)
    if instance.state == 'success' or instance.state == 'fail':
        message = 'Run executed: Run ID - {0}; status - {1}'.format(
            instance.run_base.id, instance.state.capitalize())
        log_it(instance.user, 'Run', instance.run_base.id, message)


@receiver(post_save, sender=InputDataDirectory)
def mkdir(sender, instance, **kwargs):
    update_list_files(instance)
