# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings

from cards.cards_forms import *
from .card_update_create import *
from .get_card_post import *


REVERSE_URL = {
    'qrf': {'save_button': 'proces_card_new_run',
            'save_and_another': 'new_run_qrf',
            'save_and_continue': 'new_run_qrf_edit',
            'cancel_button': 'proces_card_new_run'},
    'rfscore': {'save_button': 'proces_card_new_run',
                'save_and_another': 'new_run_rfscore',
                'save_and_continue': 'new_run_rfscore_edit',
                'cancel_button': 'proces_card_new_run'},
    'remap': {'save_button': 'proces_card_new_run',
              'save_and_another': 'new_run_remap',
              'save_and_continue': 'new_run_remap_edit',
              'cancel_button': 'proces_card_new_run'},
    'year_filter': {'save_button': 'proces_card_new_run',
                    'save_and_another': 'new_run_year_filter',
                    'save_and_continue': 'new_run_year_filter_edit',
                    'cancel_button': 'proces_card_new_run'},
    'collate': {'save_button': 'proces_card_new_run',
                'save_and_another': 'new_run_collate',
                'save_and_continue': 'new_run_collate_edit',
                'cancel_button': 'proces_card_new_run'},
    'preproc': {'save_button': 'proces_card_new_run',
                'save_and_another': 'new_run_preproc',
                'save_and_continue': 'new_run_preproc_edit',
                'cancel_button': 'proces_card_new_run'},
    'mergecsv': {'save_button': 'proces_card_new_run',
                 'save_and_another': 'new_run_mergecsv',
                 'save_and_continue': 'new_run_mergecsv_edit',
                 'cancel_button': 'proces_card_new_run'},
    'rftrain': {'save_button': 'proces_card_new_run',
                'save_and_another': 'new_run_rftrain',
                'save_and_continue': 'new_run_rftrain_edit',
                'cancel_button': 'proces_card_new_run'}
}


# cards for run/card-sequence/processing-card
@login_required
@render_to('cards/new_run_card.html')
def new_run_qrf(request):
    title = 'New QRF Card'
    url_form = 'new_run_qrf'
    template_name = 'cards/_qrf_form.html'
    func = qrf_update_create
    form = None

    if request.method == "POST":
        # import pdb;pdb.set_trace()
        response = get_cards_post(request, QRFForm, 'QRF',
                                 REVERSE_URL['qrf'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = QRFForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_qrf_edit(request, qrf_id):
    title = 'New QRF Card'
    qrf_card = get_object_or_404(QRF, pk=qrf_id)
    url_form = 'new_run_qrf_edit'
    template_name = 'cards/_qrf_form.html'
    func = qrf_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, QRFForm, 'QRF',
                                     REVERSE_URL['qrf'], func,
                                     card_id=qrf_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = QRFForm(instance=qrf_card)

    data = {
        'title': title,
        'form': form,
        'card_id': qrf_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_rfscore(request):
    title = 'New RFScore Card'
    url_form = 'new_run_rfscore'
    template_name = 'cards/_rfscore_form.html'
    func = rfscore_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, RFScoreForm, 'RFScore',
                                     REVERSE_URL['rfscore'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = RFScoreForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_rfscore_edit(request, rfscore_id):
    title = 'New RFScore Card'
    rfscore_card = get_object_or_404(RFScore, pk=rfscore_id)
    url_form = 'new_run_rfscore_edit'
    template_name = 'cards/_rfscore_form.html'
    func = rfscore_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, RFScoreForm, 'RFScore',
                                     REVERSE_URL['rfscore'], func,
                                     card_id=rfscore_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = RFScoreForm(instance=rfscore_card)

    data = {
        'title': title,
        'form': form,
        'card_id': rfscore_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_remap(request):
    title = 'New Remap Card'
    url_form = 'new_run_remap'
    template_name = 'cards/_remap_form.html'
    func = remap_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, RemapForm, 'Remap',
                                     REVERSE_URL['remap'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = RemapForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_remap_edit(request, remap_id):
    title = 'New Remap Card'
    remap_card = get_object_or_404(Remap, pk=remap_id)
    url_form = 'new_run_remap_edit'
    template_name = 'cards/_remap_form.html'
    func = remap_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, RemapForm, 'Remap',
                                     REVERSE_URL['remap'], func,
                                     card_id=remap_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = RemapForm(instance=remap_card)

    data = {
        'title': title,
        'form': form,
        'card_id': remap_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_year_filter(request):
    title = 'New YearFilter Card'
    url_form = 'new_run_year_filter'
    template_name = 'cards/_year_filter_form.html'
    func = year_filter_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, YearFilterForm, 'YearFilter',
                                     REVERSE_URL['year_filter'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = YearFilterForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_year_filter_edit(request, yf_id):
    title = 'New YearFilter Card'
    year_filter_card = get_object_or_404(YearFilter, pk=yf_id)
    url_form = 'new_run_year_filter_edit'
    template_name = 'cards/_year_filter_form.html'
    func = year_filter_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, YearFilterForm, 'YearFilter',
                                     REVERSE_URL['year_filter'], func,
                                     card_id=yf_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = YearFilterForm(instance=year_filter_card)

    data = {
        'title': title,
        'form': form,
        'card_id': yf_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_collate(request):
    title = 'New Collate Card'
    url_form = 'new_run_collate'
    template_name = 'cards/_collate_form.html'
    func = collate_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, CollateForm, 'Collate',
                                     REVERSE_URL['collate'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CollateForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_collate_edit(request, collate_id):
    title = 'New Collate Card'
    collate_card = get_object_or_404(Collate, pk=collate_id)
    url_form = 'new_run_collate_edit'
    template_name = 'cards/_collate_form.html'
    func = collate_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, CollateForm, 'Collate',
                                     REVERSE_URL['collate'], func,
                                     card_id=collate_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CollateForm(instance=collate_card)

    data = {
        'title': title,
        'form': form,
        'card_id': collate_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_preproc(request):
    title = 'New PreProc Card'
    url_form = 'new_run_preproc'
    template_name = 'cards/_preproc_form.html'
    func = preproc_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, PreProcForm, 'PreProc',
                                     REVERSE_URL['preproc'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = PreProcForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_preproc_edit(request, preproc_id):
    title = 'New PreProc Card'
    preproc_card = get_object_or_404(PreProc, pk=preproc_id)
    url_form = 'new_run_preproc_edit'
    template_name = 'cards/_preproc_form.html'
    func = preproc_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, PreProcForm, 'PreProc',
                                     REVERSE_URL['preproc'], func,
                                     card_id=preproc_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = PreProcForm(instance=preproc_card)

    data = {
        'title': title,
        'form': form,
        'card_id': preproc_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_mergecsv(request):
    title = 'New MergeCSV Card'
    url_form = 'new_run_mergecsv'
    template_name = 'cards/_mergecsv_form.html'
    func = mergecsv_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, MergeCSVForm, 'MergeCSV',
                                     REVERSE_URL['mergecsv'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = MergeCSVForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_mergecsv_edit(request, mcsv_id):
    title = 'New MergeCSV Card'
    mergecsv_card = get_object_or_404(MergeCSV, pk=mcsv_id)
    url_form = 'new_run_mergecsv_edit'
    template_name = 'cards/_mergecsv_form.html'
    func = mergecsv_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, MergeCSVForm, 'MergeCSV',
                                     REVERSE_URL['mergecsv'], func,
                                     card_id=mcsv_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = MergeCSVForm(instance=mergecsv_card)

    data = {
        'title': title,
        'form': form,
        'card_id': mcsv_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_rftrain(request):
    title = 'New RFTrain Card'
    url_form = 'new_run_rftrain'
    template_name = 'cards/_rftrain_form.html'
    func = rftrain_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, RFTrainForm, 'RFTrain',
                                     REVERSE_URL['rftrain'], func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = RFTrainForm()

    data = {
        'title': title,
        'form': form,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data


@login_required
@render_to('cards/new_run_card.html')
def new_run_rftrain_edit(request, rftrain_id):
    title = 'New RFTrain Card'
    rftrain_card = get_object_or_404(RFTrain, pk=rftrain_id)
    url_form = 'new_run_rftrain_edit'
    template_name = 'cards/_rftrain_form.html'
    func = rftrain_update_create
    form = None

    if request.method == "POST":
        response = get_cards_post(request, RFTrainForm, 'RFTrain',
                                     REVERSE_URL['rftrain'], func,
                                     card_id=rftrain_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = RFTrainForm(instance=rftrain_card)

    data = {
        'title': title,
        'form': form,
        'card_id': rftrain_id,
        'url_form': url_form,
        'template_name': template_name,
    }

    return data
