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


def processing_card_menu(request, rev_url, args=False):
    # import pdb;pdb.set_trace()
    response = None

    if request.method == "POST":
        if request.POST.get('qrf_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['qrf_button'][0], args=rev_url['qrf_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['qrf_button']))
        elif request.POST.get('rfscore_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['rfscore_button'][0], args=rev_url['rfscore_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['rfscore_button']))
        elif request.POST.get('remap_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['remap_button'][0], args=rev_url['remap_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['remap_button']))
        elif request.POST.get('year_filter_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['year_filter_button'][0], args=rev_url['year_filter_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['year_filter_button']))
        elif request.POST.get('collate_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['collate_button'][0], args=rev_url['collate_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['collate_button']))
        elif request.POST.get('preproc_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['preproc_button'][0], args=rev_url['preproc_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['preproc_button']))
        elif request.POST.get('margecsv_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['margecsv_button'][0], args=rev_url['margecsv_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['margecsv_button']))
        elif request.POST.get('rftrain_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['rftrain_button'][0], args=rev_url['rftrain_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['rftrain_button']))
        elif request.POST.get('cancel_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['cancel_button'][0], args=rev_url['cancel_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['cancel_button']))

    return response


@login_required
@render_to('cards/processing_card_new_run.html')
def proces_card_new_run(request):
    title = 'Create New Processing Cards'
    rev_url = {
        'qrf_button': 'new_run_qrf',
        'rfscore_button': 'new_run_rfscore',
        'remap_button': 'new_run_remap',
        'year_filter_button': 'new_run_year_filter',
        'collate_button': 'new_run_collate',
        'preproc_button': 'new_run_preproc',
        'margecsv_button': 'new_run_mergecsv',
        'rftrain_button': 'new_run_rftrain',
        'cancel_button': 'run_new_card_sequence_add',
    }

    if request.method == "POST":
        return processing_card_menu(request, rev_url)

    data = {
        'title': title,
    }

    return data

@login_required
@render_to('cards/processing_card_new_run.html')
def proces_card_runid(request, run_id):
    title = 'Create New Processing Cards'
    rev_url = {
        'qrf_button': ['new_runid_qrf', [run_id]],
        'rfscore_button': ['new_runid_rfscore', [run_id]],
        'remap_button': ['new_runid_remap', [run_id]],
        'year_filter_button': ['new_runid_year_filter', [run_id]],
        'collate_button': ['new_runid_collate', [run_id]],
        'preproc_button': ['new_runid_preproc', [run_id]],
        'margecsv_button': ['new_runid_mergecsv', [run_id]],
        'rftrain_button': ['new_runid_rftrain', [run_id]],
        'cancel_button': ['add_card_sequence', [run_id]]
    }

    if request.method == "POST":
        return processing_card_menu(request, rev_url, args=True)

    data = {
        'title': title,
        'run_id': run_id,
    }

    return data











@login_required
@render_to('cards/processing_card_new_run.html')
def proces_card_new_run_new_sc(request, cs_id):
    title = 'Create New Processing Cards 22'
    rev_url = {
        'qrf_button': ['new_run_qrf'],
        'rfscore_button': ['new_run_rfscore'],
        'remap_button': ['new_run_remap'],
        'year_filter_button': ['new_run_year_filter'],
        'collate_button': ['new_run_collate'],
        'preproc_button': ['new_run_preproc'],
        'margecsv_button': ['new_run_mergecsv'],
        'rftrain_button': ['new_run_rftrain'],
        'cancel_button': ['run_new_card_sequence_update', [cs_id]]
    }

    if request.method == "POST":
        return processing_card_menu(request, rev_url, args=True)

    data = {
        'title': title,
        'cs_id': cs_id,
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
