from django.db.models.signals import post_save, post_delete
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


@receiver(post_delete, sender=Tile)
def remove_empty_area_by_removing_tile(sender, instance, **kwargs):
    areas = Area.objects.all()

    for area in areas:
        if not area.tiles.through.objects.filter(area_id=area.id):
            Area.objects.get(name=area.name).delete()

