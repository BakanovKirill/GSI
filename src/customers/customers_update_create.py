# -*- coding: utf-8 -*-
from gsi.settings import RESULTS_DIRECTORY
from customers.models import (Category, ShelfData, DataSet)


def category_update_create(form, item_id=None):
    """**Updated Category model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the item_id=None when you create a object)

    """

    if item_id:
        Category.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
        )
        category = Category.objects.get(id=item_id)
    else:
        category = Category.objects.create(
            name=form.cleaned_data["name"],
        )

    return category


def shelf_data_update_create(form, item_id=None):
    """**Updated ShelfData model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the item_id=None when you create a object)

    """

    if item_id:
        ShelfData.objects.filter(id=item_id).update(
            category=form.cleaned_data["category"],
            attribute_name=form.cleaned_data["attribute_name"],
            root_filename=form.cleaned_data["root_filename"],
            units=form.cleaned_data["units"],
            description=form.cleaned_data["description"],
        )
        shelf_data = ShelfData.objects.get(id=item_id)
    else:
        shelf_data = ShelfData.objects.create(
            category=form.cleaned_data["category"],
            attribute_name=form.cleaned_data["attribute_name"],
            root_filename=form.cleaned_data["root_filename"],
            units=form.cleaned_data["units"],
            description=form.cleaned_data["description"],
        )

    return shelf_data


def data_set_update_create(form, item_id=None):
    """**Updated DataSet model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the item_id=None when you create a object)

    """

    if item_id:
        DataSet.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            results_directory=form.cleaned_data["results_directory"],
        )
        data_set = DataSet.objects.get(id=item_id)
    else:
        data_set = DataSet.objects.create(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            results_directory=form.cleaned_data["results_directory"],
        )

    if form.cleaned_data["root_filename"] and form.cleaned_data["attribute_name"]:
        try:
            shelf_data = ShelfData.objects.get(
                            root_filename=form.cleaned_data["root_filename"],
                            attribute_name=form.cleaned_data["attribute_name"]
                        )
            data_set.shelf_data = shelf_data
            data_set.save()
        except Exception:
            pass

    return data_set
