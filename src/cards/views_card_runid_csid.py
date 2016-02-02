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
	'qrf': {'save_button': ['proces_card_runid_csid'],
	        'save_and_another': ['new_runid_csid_qrf'],
	        'save_and_continue': ['new_runid_csid_qrf_edit'],
	        'cancel_button': ['proces_card_runid_csid']},
	'rfscore': {'save_button': ['proces_card_runid_csid'],
	            'save_and_another': ['new_runid_csid_rfscore'],
	            'save_and_continue': ['new_runid_csid_rfscore_edit'],
	            'cancel_button': ['proces_card_runid_csid']},
	'remap': {'save_button': ['proces_card_runid_csid'],
	          'save_and_another': ['new_runid_csid_remap'],
	          'save_and_continue': ['new_runid_csid_remap_edit'],
	          'cancel_button': ['proces_card_runid_csid']},
	'year_filter': {'save_button': ['proces_card_runid_csid'],
	                'save_and_another': ['new_runid_csid_year_filter'],
	                'save_and_continue': ['new_runid_csid_year_filter_edit'],
	                'cancel_button': ['proces_card_runid_csid']},
	'collate': {'save_button': ['proces_card_runid_csid'],
	            'save_and_another': ['new_runid_csid_collate'],
	            'save_and_continue': ['new_runid_csid_collate_edit'],
	            'cancel_button': ['proces_card_runid_csid']},
	'preproc': {'save_button': ['proces_card_runid_csid'],
	            'save_and_another': ['new_runid_csid_preproc'],
	            'save_and_continue': ['new_runid_csid_preproc_edit'],
	            'cancel_button': ['proces_card_runid_csid']},
	'mergecsv': {'save_button': ['proces_card_runid_csid'],
	             'save_and_another': ['new_runid_csid_mergecsv'],
	             'save_and_continue': ['new_runid_csid_mergecsv_edit'],
	             'cancel_button': ['proces_card_runid_csid']},
	'rftrain': {'save_button': ['proces_card_runid_csid'],
	            'save_and_another': ['new_runid_csid_rftrain'],
	            'save_and_continue': ['new_runid_csid_rftrain_edit'],
	            'cancel_button': ['proces_card_runid_csid']}
}


# cards for run/card-sequence/processing-card
@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_qrf(request, run_id, cs_id):
	# import pdb;pdb.set_trace()
	title = 'New QRF Card'
	url_form = 'new_runid_csid_qrf'
	template_name = 'cards/_qrf_form.html'
	func = qrf_update_create
	form = None
	REVERSE_URL['qrf']['save_button'].append([run_id, cs_id])
	REVERSE_URL['qrf']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['qrf']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['qrf']['cancel_button'].append([run_id, cs_id])

	print

	if request.method == "POST":
		# import pdb;pdb.set_trace()
		response = get_cards_post(request, QRFForm, 'QRF',
		                          REVERSE_URL['qrf'], func,
		                          args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_qrf_edit(request, run_id, cs_id, qrf_id):
	title = 'New QRF Card'
	qrf_card = get_object_or_404(QRF, pk=qrf_id)
	url_form = 'new_runid_csid_qrf_edit'
	template_name = 'cards/_qrf_form.html'
	func = qrf_update_create
	form = None
	REVERSE_URL['qrf']['save_button'].append([run_id, cs_id])
	REVERSE_URL['qrf']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['qrf']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['qrf']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, QRFForm, 'QRF',
		                          REVERSE_URL['qrf'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_rfscore(request, run_id, cs_id):
	title = 'New RFScore Card'
	url_form = 'new_runid_csid_rfscore'
	template_name = 'cards/_rfscore_form.html'
	func = rfscore_update_create
	form = None
	REVERSE_URL['rfscore']['save_button'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, RFScoreForm, 'RFScore',
		                          REVERSE_URL['rfscore'], func,
		                          args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_rfscore_edit(request, run_id, cs_id, rfscore_id):
	title = 'New RFScore Card'
	rfscore_card = get_object_or_404(RFScore, pk=rfscore_id)
	url_form = 'new_runid_csid_rfscore_edit'
	template_name = 'cards/_rfscore_form.html'
	func = rfscore_update_create
	form = None
	REVERSE_URL['rfscore']['save_button'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, RFScoreForm, 'RFScore',
		                          REVERSE_URL['rfscore'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_remap(request, run_id, cs_id):
	title = 'New Remap Card'
	url_form = 'new_runid_csid_remap'
	template_name = 'cards/_remap_form.html'
	func = remap_update_create
	form = None
	REVERSE_URL['remap']['save_button'].append([run_id, cs_id])
	REVERSE_URL['remap']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['remap']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['remap']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, RemapForm, 'Remap',
		                          REVERSE_URL['remap'], func,
		                          args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_remap_edit(request, run_id, cs_id, remap_id):
	title = 'New Remap Card'
	remap_card = get_object_or_404(Remap, pk=remap_id)
	url_form = 'new_runid_csid_remap_edit'
	template_name = 'cards/_remap_form.html'
	func = remap_update_create
	form = None
	REVERSE_URL['remap']['save_button'].append([run_id, cs_id])
	REVERSE_URL['remap']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['remap']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['remap']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, RemapForm, 'Remap',
		                          REVERSE_URL['remap'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_year_filter(request, run_id, cs_id):
	title = 'New YearFilter Card'
	url_form = 'new_runid_csid_year_filter'
	template_name = 'cards/_year_filter_form.html'
	func = year_filter_update_create
	form = None
	REVERSE_URL['year_filter']['save_button'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, YearFilterForm, 'YearFilter',
		                          REVERSE_URL['year_filter'], func, args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_year_filter_edit(request, run_id, cs_id, yf_id):
	title = 'New YearFilter Card'
	year_filter_card = get_object_or_404(YearFilter, pk=yf_id)
	url_form = 'new_runid_csid_year_filter_edit'
	template_name = 'cards/_year_filter_form.html'
	func = year_filter_update_create
	form = None
	REVERSE_URL['year_filter']['save_button'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, YearFilterForm, 'YearFilter',
		                          REVERSE_URL['year_filter'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_collate(request, run_id, cs_id):
	title = 'New Collate Card'
	url_form = 'new_runid_csid_collate'
	template_name = 'cards/_collate_form.html'
	func = collate_update_create
	form = None
	REVERSE_URL['collate']['save_button'].append([run_id, cs_id])
	REVERSE_URL['collate']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['collate']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['collate']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, CollateForm, 'Collate',
		                          REVERSE_URL['collate'], func, args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_collate_edit(request, run_id, cs_id, collate_id):
	title = 'New Collate Card'
	collate_card = get_object_or_404(Collate, pk=collate_id)
	url_form = 'new_runid_csid_collate_edit'
	template_name = 'cards/_collate_form.html'
	func = collate_update_create
	form = None
	REVERSE_URL['collate']['save_button'].append([run_id, cs_id])
	REVERSE_URL['collate']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['collate']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['collate']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, CollateForm, 'Collate',
		                          REVERSE_URL['collate'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_preproc(request, run_id, cs_id):
	title = 'New PreProc Card'
	url_form = 'new_runid_csid_preproc'
	template_name = 'cards/_preproc_form.html'
	func = preproc_update_create
	form = None
	REVERSE_URL['preproc']['save_button'].append([run_id, cs_id])
	REVERSE_URL['preproc']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['preproc']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['preproc']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, PreProcForm, 'PreProc',
		                          REVERSE_URL['preproc'], func, args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_preproc_edit(request, run_id, cs_id, preproc_id):
	title = 'New PreProc Card'
	preproc_card = get_object_or_404(PreProc, pk=preproc_id)
	url_form = 'new_runid_csid_preproc_edit'
	template_name = 'cards/_preproc_form.html'
	func = preproc_update_create
	form = None
	REVERSE_URL['preproc']['save_button'].append([run_id, cs_id])
	REVERSE_URL['preproc']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['preproc']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['preproc']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, PreProcForm, 'PreProc',
		                          REVERSE_URL['preproc'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_mergecsv(request, run_id, cs_id):
	title = 'New MergeCSV Card'
	url_form = 'new_runid_csid_mergecsv'
	template_name = 'cards/_mergecsv_form.html'
	func = mergecsv_update_create
	form = None
	REVERSE_URL['mergecsv']['save_button'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, MergeCSVForm, 'MergeCSV',
		                          REVERSE_URL['mergecsv'], func, args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_mergecsv_edit(request, run_id, cs_id, mcsv_id):
	title = 'New MergeCSV Card'
	mergecsv_card = get_object_or_404(MergeCSV, pk=mcsv_id)
	url_form = 'new_runid_csid_mergecsv_edit'
	template_name = 'cards/_mergecsv_form.html'
	func = mergecsv_update_create
	form = None
	REVERSE_URL['mergecsv']['save_button'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, MergeCSVForm, 'MergeCSV',
		                          REVERSE_URL['mergecsv'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_rftrain(request, run_id, cs_id):
	title = 'New RFTrain Card'
	url_form = 'new_runid_csid_rftrain'
	template_name = 'cards/_rftrain_form.html'
	func = rftrain_update_create
	form = None
	REVERSE_URL['rftrain']['save_button'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, RFTrainForm, 'RFTrain',
		                          REVERSE_URL['rftrain'], func, args=True)

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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def new_runid_csid_rftrain_edit(request, run_id, cs_id, rftrain_id):
	title = 'New RFTrain Card'
	rftrain_card = get_object_or_404(RFTrain, pk=rftrain_id)
	url_form = 'new_runid_csid_rftrain_edit'
	template_name = 'cards/_rftrain_form.html'
	func = rftrain_update_create
	form = None
	REVERSE_URL['rftrain']['save_button'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['save_and_another'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		response = get_cards_post(request, RFTrainForm, 'RFTrain',
		                          REVERSE_URL['rftrain'], func, args=True,
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
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data