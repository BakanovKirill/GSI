# -*- coding: utf-8 -*-
from customers.models import (Category, ShelfData, DataSet, CustomerAccess, LutFiles)


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
            show_totals=form.cleaned_data["show_totals"],
            scale=form.cleaned_data["scale"],
            lutfiles=form.cleaned_data["lutfiles"],
        )
        shelf_data = ShelfData.objects.get(id=item_id)
    else:
        shelf_data = ShelfData.objects.create(
            category=form.cleaned_data["category"],
            attribute_name=form.cleaned_data["attribute_name"],
            root_filename=form.cleaned_data["root_filename"],
            units=form.cleaned_data["units"],
            description=form.cleaned_data["description"],
            show_totals=form.cleaned_data["show_totals"],
            scale=form.cleaned_data["scale"],
            lutfiles=form.cleaned_data["lutfiles"],
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
            is_ts=form.cleaned_data["is_ts"],
            name_ts=form.cleaned_data["name_ts"],
            shelf_data=form.cleaned_data["shelf_data"],
        )
        data_set = DataSet.objects.get(id=item_id)
    else:
        data_set = DataSet.objects.create(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            results_directory=form.cleaned_data["results_directory"],
            is_ts=form.cleaned_data["is_ts"],
            name_ts=form.cleaned_data["name_ts"],
            shelf_data=form.cleaned_data["shelf_data"],
        )

    if form.cleaned_data["root_filename"] and form.cleaned_data["attribute_name"]:
        try:
            shelf_data = ShelfData.objects.get(
                            root_filename=form.cleaned_data["root_filename"],
                            attribute_name=form.cleaned_data["attribute_name"],
                            is_ts=form.cleaned_data["is_ts"],
                            name_ts=form.cleaned_data["name_ts"],
                            shelf_data=form.cleaned_data["shelf_data"],
                        )
            data_set.shelf_data = shelf_data
            data_set.save()
        except Exception:
            pass

    return data_set


def customer_access_update_create(form, multiple=None, item_id=None, delete=False):
    """**Updated CustomerAccess model.**

    :Arguments:
        * *form*: Object of the form
        * *multiple*: Transmited a list of objects
        * *item_id*: ID of the object. Set when editing (the default=None when you create a card)
        * *delete*: Boolean value determine the remove objects or not

    """

    if item_id:
        CustomerAccess.objects.filter(id=item_id).update(
            user=form.cleaned_data["user"],
        )
        result = CustomerAccess.objects.get(id=item_id)
    else:
        result = CustomerAccess.objects.create(
            user=form.cleaned_data["user"],
        )

    if multiple:
        list_id = multiple.split('_')

        for data_set_id in list_id:
            if delete:
                CustomerAccess.data_set.through.objects.filter(
                    customeraccess_id=result.id,
                    dataset_id=data_set_id
                ).delete()
            else:
                CustomerAccess.data_set.through.objects.create(
                    customeraccess_id=result.id,
                    dataset_id=data_set_id
                )

    return result


def lutfile_update_create(form, item_id=None):
    """**Updated LutFiles model.**

    :Arguments:
        * *form*: Object of the form
        * *item_id*: ID of the object. Set when editing (the item_id=None when you create a object)

    """

    lut_filename = ''

    if form.cleaned_data["lut_file"] != 'select':
        lut_filename = form.cleaned_data["lut_file"]

    if item_id:
        LutFiles.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            lut_file=lut_filename,
            max_val=form.cleaned_data["max_val"],
            legend=form.cleaned_data["legend"],
            units=form.cleaned_data["units"],
            val_scale=form.cleaned_data["val_scale"],
        )
        lut_file = LutFiles.objects.get(id=item_id)
    else:
        lut_file = LutFiles.objects.create(
            name=form.cleaned_data["name"],
            lut_file=lut_filename,
            max_val=form.cleaned_data["max_val"],
            legend=form.cleaned_data["legend"],
            units=form.cleaned_data["units"],
            val_scale=form.cleaned_data["val_scale"],
        )

    return lut_file
