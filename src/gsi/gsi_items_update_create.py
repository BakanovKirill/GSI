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


def area_update_create(form, multiple, item_id=None):
    list_id = multiple.split('_')

    if item_id:
        Area.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        result = Area.objects.get(id=item_id)
    else:
        result = Area.objects.create(
            name=form.cleaned_data["name"],
        )
    result.tiles.through.objects.filter(area_id=result.id).delete()
    for tile_id in list_id:
        Area.tiles.through.objects.create(
            area_id=result.id,
            tile_id=tile_id
        )

    return result




# if cs_id:
# 		card_sequence = CardSequence.objects.get(id=cs_id)
# 		card_sequence.name=form.cleaned_data["name"]
# 		card_sequence.environment_override=form.cleaned_data["environment_override"]
# 		card_sequence.environment_base=form.cleaned_data["environment_base"]
# 		card_sequence.save()
# 	else:
# 		card_sequence = CardSequence.objects.create(
# 			name=form.cleaned_data["name"],
# 			environment_override=form.cleaned_data["environment_override"],
# 			environment_base=form.cleaned_data["environment_base"],
# 		)
#
# 	if form.cleaned_data["card_item"]:
# 		CardSequence.cards.through.objects.create(
# 			sequence=card_sequence,
# 			card_item=form.cleaned_data["card_item"],
# 			order=form.cleaned_data["order"],
# 		)