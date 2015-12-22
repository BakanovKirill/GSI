from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import Tile, Area


@receiver(post_save, sender=Tile)
def added_update_area_for_each_tile(sender, instance, **kwargs):
    try:
        area = Area.objects.get(tiles=instance)
        area.name = instance.name
    except ObjectDoesNotExist:
        area = Area(name=instance.name)
    finally:
        area.save()
        area.tiles.add(instance)

