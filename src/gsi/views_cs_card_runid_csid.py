# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings

from cards.cards_forms import *
from cards.card_update_create import *
# from .get_card_post import *
from core.get_post import *
from gsi.models import CardSequence
from cards.models import CardItem
from gsi.gsi_forms import CardSequenceCardForm

REVERSE_URL = {
	'qrf': {'save_button': ['card_sequence_update'],
	        'save_and_continue': ['cs_runid_csid_qrf_edit'],
	        'cancel_button': ['card_sequence_update']},

	'rfscore': {'save_button': ['card_sequence_update'],
	            'save_and_continue': ['cs_runid_csid_rfscore_edit'],
	            'cancel_button': ['card_sequence_update']},

	'remap': {'save_button': ['card_sequence_update'],
	          'save_and_continue': ['cs_runid_csid_remap_edit'],
	          'cancel_button': ['card_sequence_update']},

	'year_filter': {'save_button': ['card_sequence_update'],
	                'save_and_continue': ['cs_runid_csid_year_filter_edit'],
	                'cancel_button': ['card_sequence_update']},

	'collate': {'save_button': ['card_sequence_update'],
	            'save_and_continue': ['cs_runid_csid_collate_edit'],
	            'cancel_button': ['card_sequence_update']},

	'preproc': {'save_button': ['card_sequence_update'],
	            'save_and_continue': ['cs_runid_csid_preproc_edit'],
	            'cancel_button': ['card_sequence_update']},

	'mergecsv': {'save_button': ['card_sequence_update'],
	             'save_and_continue': ['cs_runid_csid_mergecsv_edit'],
	             'cancel_button': ['card_sequence_update']},

	'rftrain': {'save_button': ['card_sequence_update'],
	            'save_and_continue': ['cs_runid_csid_rftrain_edit'],
	            'cancel_button': ['card_sequence_update']}
}


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_qrf_edit(request, run_id, cs_id, qrf_id):
	# print 'RUN ====================== ', run_id
	# print 'CS ====================== ', cs_id
	title = 'QRF Card Edit'
	qrf_card = get_object_or_404(QRF, pk=qrf_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='qrf')
	card_item = get_object_or_404(CardItem, object_id=qrf_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card = get_object_or_404(
		CardSequence.cards.through,
		card_item=card_item,
		sequence=card_sequence
	)

	url_form = 'cs_runid_csid_qrf_edit'
	template_name = 'gsi/_cs_qrf_form.html'
	func = qrf_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['qrf']['save_button'].append([run_id, cs_id])
	REVERSE_URL['qrf']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['qrf']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, QRFForm, 'QRF Card', REVERSE_URL['qrf'],
							func, args=True, item_id=qrf_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = QRFForm(instance=qrf_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': qrf_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_rfscore_edit(request, run_id, cs_id, rfscore_id):
	title = 'RFScore Card Edit'
	rfscore_card = get_object_or_404(RFScore, pk=rfscore_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='rfscore')
	card_item = get_object_or_404(CardItem, object_id=rfscore_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_rfscore_edit'
	template_name = 'gsi/_cs_rfscore_form.html'
	func = rfscore_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['rfscore']['save_button'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['rfscore']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, RFScoreForm, 'RFScore Card', REVERSE_URL['rfscore'],
							func, args=True, item_id=rfscore_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RFScoreForm(instance=rfscore_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': rfscore_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_remap_edit(request, run_id, cs_id, remap_id):
	title = 'Remap Card Edit'
	remap_card = get_object_or_404(Remap, pk=remap_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='remap')
	card_item = get_object_or_404(CardItem, object_id=remap_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_remap_edit'
	template_name = 'gsi/_cs_remap_form.html'
	func = remap_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['remap']['save_button'].append([run_id, cs_id])
	REVERSE_URL['remap']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['remap']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, RemapForm, 'Remap Card', REVERSE_URL['remap'],
							func, args=True, item_id=remap_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RemapForm(instance=remap_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': remap_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_year_filter_edit(request, run_id, cs_id, yf_id):
	title = 'YearFilter Card Edit'
	year_filter_card = get_object_or_404(YearFilter, pk=yf_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='yearfilter')
	card_item = get_object_or_404(CardItem, object_id=yf_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_year_filter_edit'
	template_name = 'gsi/_cs_year_filter_form.html'
	func = year_filter_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['year_filter']['save_button'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['year_filter']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, YearFilterForm, 'YearFilter Card', REVERSE_URL['year_filter'],
							func, args=True, item_id=yf_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = YearFilterForm(instance=year_filter_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': yf_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_collate_edit(request, run_id, cs_id, collate_id):
	title = 'Collate Card Edit'
	collate_card = get_object_or_404(Collate, pk=collate_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='collate')
	card_item = get_object_or_404(CardItem, object_id=collate_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_collate_edit'
	template_name = 'gsi/_cs_collate_form.html'
	func = collate_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['collate']['save_button'].append([run_id, cs_id])
	REVERSE_URL['collate']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['collate']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, CollateForm, 'Collate Card', REVERSE_URL['collate'],
							func, args=True, item_id=collate_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = CollateForm(instance=collate_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': collate_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_preproc_edit(request, run_id, cs_id, preproc_id):
	title = 'PreProc Card Edit'
	preproc_card = get_object_or_404(PreProc, pk=preproc_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='preproc')
	card_item = get_object_or_404(CardItem, object_id=preproc_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_preproc_edit'
	template_name = 'gsi/_cs_preproc_form.html'
	func = preproc_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['preproc']['save_button'].append([run_id, cs_id])
	REVERSE_URL['preproc']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['preproc']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, PreProcForm, 'PreProc Card',
							REVERSE_URL['preproc'],
							func, args=True, item_id=preproc_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = PreProcForm(instance=preproc_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': preproc_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_mergecsv_edit(request, run_id, cs_id, mcsv_id):
	title = 'MergeCSV Card Edit'
	mergecsv_card = get_object_or_404(MergeCSV, pk=mcsv_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='mergecsv')
	card_item = get_object_or_404(CardItem, object_id=mcsv_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_mergecsv_edit'
	template_name = 'gsi/_cs_mergecsv_form.html'
	func = mergecsv_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['mergecsv']['save_button'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['mergecsv']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, MergeCSVForm, 'MergeCSV Card', REVERSE_URL['mergecsv'],
							func, args=True, item_id=mcsv_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = MergeCSVForm(instance=mergecsv_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': mcsv_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data


@login_required
@render_to('cards/new_runid_csid_card.html')
def cs_runid_csid_rftrain_edit(request, run_id, cs_id, rftrain_id):
	title = 'RFTrain Card Edit'
	rftrain_card = get_object_or_404(RFTrain, pk=rftrain_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='rftrain')
	card_item = get_object_or_404(CardItem, object_id=rftrain_id, content_type=content_type)
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	card_sequence_card_all = CardSequence.cards.through.objects.filter(
							card_item=card_item,
							sequence=card_sequence
						)
	card_sequence_card = card_sequence_card_all[0]
	url_form = 'cs_runid_csid_rftrain_edit'
	template_name = 'gsi/_cs_rftrain_form.html'
	func = rftrain_update_create
	form_1 = None
	form_2 = None
	REVERSE_URL['rftrain']['save_button'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['save_and_continue'].append([run_id, cs_id])
	REVERSE_URL['rftrain']['cancel_button'].append([run_id, cs_id])

	if request.method == "POST":
		cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
		response = get_post(request, RFTrainForm, 'RFTrain Card', REVERSE_URL['rftrain'],
							func, args=True, item_id=rftrain_id, cs_form=cs_form)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form_2 = response
	else:
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RFTrainForm(instance=rftrain_card)

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': rftrain_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
	}

	return data
