# -*- coding: utf-8 -*-
from gsi.models import (VariablesGroup)


def var_group_update_create(form, vg_id=None):
    if vg_id:
        VariablesGroup.objects.filter(id=vg_id).update(
            name=form.cleaned_data["name"],
            environment_variables=form.cleaned_data["environment_variables"],
        )
        var_group = VariablesGroup.objects.get(id=vg_id)
    else:
        var_group = VariablesGroup.objects.create(
            name=form.cleaned_data["name"],
            environment_variables=form.cleaned_data["environment_variables"],
        )

    return var_group

