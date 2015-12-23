from django.test import TestCase

from .models import Tile, Area

class GsiSignalsTests(TestCase):
    def test_added_update_area_for_each_tile(self):
        '''test signal added_update_area_for_each_tile'''

        tile, created = Tile.objects.get_or_create(name='test1')
        self.assertEqual(tile.name, Area.objects.get(name='test1').name)

        area = Area.objects.get(name='test1')
        self.assertEqual(tile.id, area.tiles.through.objects.get(tile_id=tile.id).id)

    def test_remove_empty_area_by_removing_tile(self):
        '''test signal remove_empty_area_by_removing_tile'''

        tile1, created1 = Tile.objects.get_or_create(name='test1')
        tile2, created2 = Tile.objects.get_or_create(name='test2')
        self.assertEqual(2, Area.objects.all().count())
        self.assertEqual(tile1.name, Area.objects.get(name='test1').name)
        self.assertEqual(tile2.name, Area.objects.get(name='test2').name)

        tile1.delete()
        self.assertEqual(1, Area.objects.all().count())
        self.assertEqual(tile2.name, Area.objects.get(name='test2').name)

        tile2.delete()
        self.assertEqual(0, Area.objects.all().count())

