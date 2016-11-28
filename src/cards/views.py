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


def processing_card_menu(request, rev_url, args=False):
    """The function to receive a response depending on the type of card.

    :Arguments:
        **request:** The request is sent to the server when processing the page

        **rev_url:** Dictionary. It contains values for reverse after processing of form.

            *rev_url[<name_card>][0]*: url for reverse,

            If the element to edit, then the variable is its id:

            *rev_url[<name_card>][1]*: id of element,

        **args:** Boolean. If the value is True, then edit the element and contains id

    """

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
        elif request.POST.get('randomforest_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['randomforest_button'][0], args=rev_url['randomforest_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['randomforest_button']))
        elif request.POST.get('calcstats_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['calcstats_button'][0], args=rev_url['calcstats_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['calcstats_button']))
        elif request.POST.get('cancel_button') is not None:
            if args:
                response = HttpResponseRedirect(reverse(rev_url['cancel_button'][0], args=rev_url['cancel_button'][1]))
            else:
                response = HttpResponseRedirect(reverse(rev_url['cancel_button']))

    return response


@login_required
@render_to('cards/processing_card_new_run.html')
def proces_card_new_run(request):
    """View at the creation of new cards.

    :When choosing a new card in "processing_card_menu" function transferred dictionary "rev_url" values:
        {<button_a_new_card>: <url_to_create_a_new_card>}

    """

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
