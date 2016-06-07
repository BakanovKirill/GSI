# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from cards.models import Collate


def delete_other_dir_files(sender, instance, **kwargs):
    print 'instance ======================= ', instance
    print 'instance input_data_directory ======================= ', instance.input_data_directory

m2m_changed.connect(delete_other_dir_files, sender=Collate.input_files.through)


# @receiver(m2m_changed, sender=Collate.input_files.through)
# def delete_other_dir_files(sender, instance, **kwargs):
#     print 'instance ======================= ', instance
#     print 'instance input_data_directory ======================= ', instance.input_data_directory
#     # try:
#     #     area = Area.objects.get(tiles=instance)
#     #     area.name = instance.name
#     # except ObjectDoesNotExist:
#     #     area = Area(name=instance.name)
#     # finally:
#     #     area.save()
#     #     area.tiles.add(instance)
