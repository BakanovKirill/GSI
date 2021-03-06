# -*- coding: utf-8 -*-
from gsi.models import (VariablesGroup, Area, Tile, Resolution,
						YearGroup, CardSequence, Satellite,
                        InputDataDirectory, ConfigFile, Year,
                        DevelopmentPage)


def development_page_update(form, item_id):
    DevelopmentPage.objects.filter(id=item_id).update(
        title=form.cleaned_data["title"],
        is_development=form.cleaned_data["is_development"]
    )
    result = DevelopmentPage.objects.get(id=item_id)

    return result


def configfile_update_create(pathname):
    """**Updated ConfigFile model.**

    :Arguments:
        * *pathname*: Path name

    """

    if not ConfigFile.objects.filter(pathname=pathname).exists():
        configfile = ConfigFile.objects.create(pathname=pathname,)
    else:
        configfile = ConfigFile.objects.get(pathname=pathname,)

    return configfile


def var_group_update_create(form, item_id=None):
    """**Updated VariablesGroup model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)

    """

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
    """**Updated Area model.**

    :Arguments:
        * *form*: Object of the form
        * *multiple*: Transmited a list of objects
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)
        * *delete*: Boolean value determine the remove objects or not

    """

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
    """**Updated YearGroup model.**

    :Arguments:
        * *form*: Object of the form
        * *multiple*: Transmited a list of objects
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)
        * *delete*: Boolean value determine the remove objects or not

    """

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


def create_update_card_sequence(form, configfile=None, cs_id=None):
    """**Updated CardSequence model.**

    :Arguments:
        * *form*: Object of the form
        * *multiple*: Transmited a list of objects
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)
        * *delete*: Boolean value determine the remove objects or not

    """

    if cs_id:
		card_sequence = CardSequence.objects.get(id=cs_id)
		card_sequence.environment_override = form.cleaned_data["environment_override"]
		card_sequence.environment_base = form.cleaned_data["environment_base"]

		if configfile:
			configfile = configfile_update_create(configfile)
			card_sequence.configfile = configfile
		card_sequence.save()
    else:
		card_sequence = CardSequence.objects.create(
			environment_override=form.cleaned_data["environment_override"],
			environment_base=form.cleaned_data["environment_base"],
		)

		if configfile:
			configfile = configfile_update_create(configfile)
			card_sequence.configfile = configfile
		card_sequence.save()

    if form.cleaned_data["card_item"]:
		CardSequence.cards.through.objects.create(
			sequence=card_sequence,
			card_item=form.cleaned_data["card_item"],
			order=form.cleaned_data["order"],
		)

    return card_sequence


def satellite_update_create(form, multiple=None, item_id=None, delete=False):
    """**Updated Satellite model.**

    :Arguments:
        * *form*: Object of the form
        * *multiple*: Transmited a list of objects
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)
        * *delete*: Boolean value determine the remove objects or not

    """

    if item_id:
		Satellite.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
		result = Satellite.objects.get(id=item_id)
    else:
		result = Satellite.objects.create(
            name=form.cleaned_data["name"],
        )

    if multiple:
		list_id = multiple.split('_')
		for satellite_id in list_id:
			if delete:
				Satellite.objects.filter(
                    pk=satellite_id
                ).delete()
			else:
				Satellite.objects.create(
                    pk=satellite_id
                )

    return result


def data_dir_update_create(form, item_id=None):
    """**Updated InputDataDirectory model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)

    """

    if item_id:
        InputDataDirectory.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        result = InputDataDirectory.objects.get(id=item_id)
    else:
        result = InputDataDirectory.objects.create(
            name=form.cleaned_data["name"],
        )

    return result


def resolution_update_create(form, item_id=None):
    """**Updated Resolution model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)

    """

    if item_id:
        Resolution.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            value=form.cleaned_data["value"],
        )
        resolution = Resolution.objects.get(id=item_id)
    else:
        resolution = Resolution.objects.create(
            name=form.cleaned_data["name"],
            value=form.cleaned_data["value"],
        )

    return resolution


def tile_update_create(form, item_id=None):
    """**Updated Tile model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)

    """

    if item_id:
        Tile.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        tile = Tile.objects.get(id=item_id)
    else:
        tile = Tile.objects.create(
            name=form.cleaned_data["name"],
        )

    return tile


def year_update_create(form, item_id=None):
    """**Updated Year model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)

    """

    if item_id:
        Year.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        year = Year.objects.get(id=item_id)
    else:
        year = Year.objects.create(
            name=form.cleaned_data["name"],
        )

    return year
