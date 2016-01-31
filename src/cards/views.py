# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings

# from cards.models import QRF, RFScore
from cards.cards_forms import *


def qrf_card_update_create(form, qrf_id=None):
    if qrf_id:
        QRF.objects.filter(id=qrf_id).update(
            name=form.cleaned_data["name"],
            interval=form.cleaned_data["interval"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            directory=form.cleaned_data["directory"],
        )
        qrf_card = QRF.objects.get(id=qrf_id)
    else:
        qrf_card = QRF.objects.create(
            name=form.cleaned_data["name"],
            interval=form.cleaned_data["interval"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            directory=form.cleaned_data["directory"],
        )

    return qrf_card


@login_required
@render_to('cards/processing_card_new_run.html')
def proces_card_new_run(request):
    title = 'Create New Processing Cards'

    if request.method == "POST":
        if request.POST.get('qrf_button') is not None:
            return HttpResponseRedirect(reverse('new_run_qrf'))
        elif request.POST.get('rfscore_button') is not None:
            return HttpResponseRedirect(reverse('new_run_rfscore'))
        elif request.POST.get('remap_button') is not None:
            return HttpResponseRedirect(reverse('new_run_remap'))
        elif request.POST.get('year_filter_button') is not None:
            return HttpResponseRedirect(reverse('new_run_year_filter'))
        elif request.POST.get('collate_button') is not None:
            return HttpResponseRedirect(reverse('new_run_collate'))
        elif request.POST.get('preproc_button') is not None:
            return HttpResponseRedirect(reverse('new_run_preproc'))
        elif request.POST.get('margecsv_button') is not None:
            return HttpResponseRedirect(reverse('new_run_mergecsv'))
        elif request.POST.get('rftrain_button') is not None:
            return HttpResponseRedirect(reverse('new_run_rftrain'))
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('new_run'))

    data = {
        'title': title,
    }

    return data


@login_required
@render_to('cards/proces_card_sequence_card_edit.html')
def proces_card_sequence_card_edit(request, run_id, cs_id):
    title = 'Create New Processing Cards'
    url_form = 'proces_card_sequence_card_edit'
    template_name = 'cards/_create_processing_card_form.html'

    if request.method == "POST":
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                reverse('card_sequence_update', args=[run_id, cs_id])
            )

    data = {
        'title': title,
        'run_id': run_id,
        'cs_id': cs_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/proces_card_sequence_card_new.html')
def proces_card_sequence_card_new(request, run_id):
    title = 'Create New Processing Cards'
    url_form = 'proces_card_sequence_card_new'
    template_name = 'cards/_create_processing_card_form.html'

    if request.method == "POST":
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                reverse('add_card_sequence', args=[run_id])
            )

    data = {
        'title': title,
        'run_id': run_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data
