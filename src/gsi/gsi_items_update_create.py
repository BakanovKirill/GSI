# -*- coding: utf-8 -*-
from gsi.models import (VariablesGroup, Area, Tile)
from django.shortcuts import get_object_or_404


def var_group_update_create(form, item_id=None):
    if item_id:
        VariablesGroup.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            environment_variables=form.cleaned_data["environment_variables"],
        )
        result = VariablesGroup.objects.get(id=item_id)
    else:
        result = VariablesGroup.objects.create(
            name=form.cleaned_data["name"],
            environment_variables=form.cleaned_data["environment_variables"],
        )

    return result


def area_update_create(form, multiple=None, item_id=None, delete=False):
    # import pdb;pdb.set_trace()
    if item_id:
        Area.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        result = Area.objects.get(id=item_id)
    else:
        result = Area.objects.create(
            name=form.cleaned_data["name"],
        )

    if multiple:
        list_id = multiple.split('_')
        for tile_id in list_id:
            if delete:
                Area.tiles.through.objects.filter(
                    area_id=result.id,
                    tile_id=tile_id
                ).delete()
            else:
                Area.tiles.through.objects.create(
                    area_id=result.id,
                    tile_id=tile_id
                )

    return result



