# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from gsi.models import (VariablesGroup, Area,
                        Tile, YearGroup, CardSequence)


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


def yg_update_create(form, multiple=None, item_id=None, delete=False):
    # import pdb;pdb.set_trace()
    if item_id:
        YearGroup.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        result = YearGroup.objects.get(id=item_id)
    else:
        result = YearGroup.objects.create(
            name=form.cleaned_data["name"],
        )

    if multiple:
        list_id = multiple.split('_')
        for yg_id in list_id:
            if delete:
                YearGroup.years.through.objects.filter(
                    yeargroup_id=result.id,
                    year_id = yg_id
                ).delete()
            else:
                YearGroup.years.through.objects.create(
                    yeargroup_id=result.id,
                    year_id =yg_id
                )

    return result


def create_update_card_sequence(form, cs_id=None):
	if cs_id:
		card_sequence = CardSequence.objects.get(id=cs_id)
		card_sequence.name = form.cleaned_data["name"]
		card_sequence.environment_override = form.cleaned_data["environment_override"]
		card_sequence.environment_base = form.cleaned_data["environment_base"]
		card_sequence.save()
	else:
		card_sequence = CardSequence.objects.create(
			name=form.cleaned_data["name"],
			environment_override=form.cleaned_data["environment_override"],
			environment_base=form.cleaned_data["environment_base"],
		)

	if form.cleaned_data["card_item"]:
		CardSequence.cards.through.objects.create(
			sequence=card_sequence,
			card_item=form.cleaned_data["card_item"],
			order=form.cleaned_data["order"],
		)

	return card_sequence



