# -*- coding: utf-8 -*-
from datetime import datetime

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from  django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from gsi.models import CardSequence, ListTestFiles
from gsi.gsi_forms import CardSequenceCardForm
from cards.models import (QRF, RFScore, Remap, YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain, RandomForest, CalcStats, CardItem)
from cards.cards_forms import (QRFForm, RFScoreForm, RemapForm, YearFilterForm, CollateForm,
								PreProcForm, MergeCSVForm, RFTrainForm, RandomForestForm, CalcStatsForm)
from cards.card_update_create import (qrf_update_create, rfscore_update_create, remap_update_create,
										year_filter_update_create, collate_update_create, preproc_update_create,
										mergecsv_update_create, rftrain_update_create, randomforest_update_create,
										calcstats_update_create)
from core.get_post import get_post
from core.utils import update_list_files


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_qrf_edit(request, run_id, cs_id, card_id, qrf_id):
	"""**View for to edit QRF card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *qrf_id*: ID of the object of the CardItem model

	"""

	title = 'QRF Card Edit'
	qrf_card = get_object_or_404(QRF, pk=qrf_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='qrf')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=qrf_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_qrf_edit'
		template_name = 'gsi/_cs_qrf_form.html'
		func = qrf_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = QRFForm(instance=qrf_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'qrf': {'save_button': ['card_sequence_update', [run_id, cs_id]],
					'save_and_continue': ['cs_runid_csid_qrf_edit', [run_id, cs_id, card_id]],
	        		'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, QRFForm, 'QRF Card', REVERSE_URL['qrf'],
								func, args=True, item_id=qrf_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_qrf_edit', args=[run_id, cs_id, card_id, qrf_id]),
											   (u"QRF Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   qrf_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': qrf_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_rfscore_edit(request, run_id, cs_id, card_id, rfscore_id):
	"""**View for to edit RFScore card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *rfscore_id*: ID of the object of the CardItem model

	"""

	title = 'RFScore Card Edit'
	rfscore_card = get_object_or_404(RFScore, pk=rfscore_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='rfscore')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=rfscore_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_rfscore_edit'
		template_name = 'gsi/_cs_rfscore_form.html'
		func = rfscore_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RFScoreForm(instance=rfscore_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'rfscore': {'save_button': ['card_sequence_update', [run_id, cs_id]],
						'save_and_continue': ['cs_runid_csid_rfscore_edit', [run_id, cs_id, card_id]],
	            		'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, RFScoreForm, 'RFScore Card', REVERSE_URL['rfscore'],
								func, args=True, item_id=rfscore_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_rfscore_edit', args=[run_id, cs_id, card_id, rfscore_id]),
											   (u"RFScore Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   rfscore_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': rfscore_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_remap_edit(request, run_id, cs_id, card_id, remap_id):
	"""**View for to edit Remap card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *remap_id*: ID of the object of the CardItem model

	"""

	title = 'Remap Card Edit'
	remap_card = get_object_or_404(Remap, pk=remap_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='remap')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=remap_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_remap_edit'
		template_name = 'gsi/_cs_remap_form.html'
		func = remap_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RemapForm(instance=remap_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'remap': {'save_button': ['card_sequence_update', [run_id, cs_id]],
					  'save_and_continue': ['cs_runid_csid_remap_edit', [run_id, cs_id, card_id]],
					  'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, RemapForm, 'Remap Card', REVERSE_URL['remap'],
								func, args=True, item_id=remap_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_remap_edit', args=[run_id, cs_id, card_id, remap_id]),
											   (u"Remap Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   remap_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': remap_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_year_filter_edit(request, run_id, cs_id, card_id, yf_id):
	"""**View for to edit YearFilter card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *yf_id*: ID of the object of the CardItem model

	"""

	title = 'YearFilter Card Edit'
	year_filter_card = get_object_or_404(YearFilter, pk=yf_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='yearfilter')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=yf_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_year_filter_edit'
		template_name = 'gsi/_cs_year_filter_form.html'
		func = year_filter_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = YearFilterForm(instance=year_filter_card)

		REVERSE_URL = {
			'year_filter': {'save_button': ['card_sequence_update', [run_id, cs_id]],
							'save_and_continue': ['cs_runid_csid_year_filter_edit', [run_id, cs_id, card_id]],
	                		'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, YearFilterForm, 'YearFilter Card', REVERSE_URL['year_filter'],
								func, args=True, item_id=yf_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_year_filter_edit', args=[run_id, cs_id, card_id, yf_id]),
											   (u"YearFilter Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   year_filter_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': yf_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_collate_edit(request, run_id, cs_id, card_id, collate_id):
	"""**View for to edit Collate card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *collate_id*: ID of the object of the CardItem model

	"""

	title = 'Collate Card Edit'
	collate_card = get_object_or_404(Collate, pk=collate_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='collate')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	update_list_files(collate_card.input_data_directory)
	input_files_list = collate_card.input_files.values_list('id', flat=True)

	available_files = ListTestFiles.objects.filter(
			input_data_directory=collate_card.input_data_directory).exclude(
			id__in=input_files_list)
	chosen_files = collate_card.input_files.filter(input_data_directory=collate_card.input_data_directory)

	available_files = available_files.order_by('name')
	chosen_files = chosen_files.order_by('name')

	try:
		card_item = get_object_or_404(CardItem, object_id=collate_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_collate_edit'
		template_name = 'gsi/_cs_collate_form.html'
		func = collate_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = CollateForm(instance=collate_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'collate': {'save_button': ['card_sequence_update', [run_id, cs_id]],
						'save_and_continue': ['cs_runid_csid_collate_edit', [run_id, cs_id, card_id]],
						'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			if request.POST.get('update_data') is not None:
				update_list_files(collate_card.input_data_directory)

			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, CollateForm, 'Collate Card', REVERSE_URL['collate'],
								func, args=True, item_id=collate_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_collate_edit', args=[run_id, cs_id, card_id, collate_id]),
											   (u"Collate Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   collate_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': collate_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
		'available_files': available_files,
		'chosen_files': chosen_files,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_preproc_edit(request, run_id, cs_id, card_id, preproc_id):
	"""**View for to edit PreProc card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *preproc_id*: ID of the object of the CardItem model

	"""

	title = 'PreProc Card Edit'
	preproc_card = get_object_or_404(PreProc, pk=preproc_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='preproc')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=preproc_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_preproc_edit'
		template_name = 'gsi/_cs_preproc_form.html'
		func = preproc_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = PreProcForm(instance=preproc_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'preproc': {'save_button': ['card_sequence_update', [run_id, cs_id]],
						'save_and_continue': ['cs_runid_csid_preproc_edit', [run_id, cs_id, card_id]],
	            		'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, PreProcForm, 'PreProc Card',
								REVERSE_URL['preproc'],
								func, args=True, item_id=preproc_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_preproc_edit', args=[run_id, cs_id, card_id, preproc_id]),
											   (u"PreProc Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   preproc_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': preproc_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_mergecsv_edit(request, run_id, cs_id, card_id, mcsv_id):
	"""**View for to edit MergeCSV card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *mcsv_id*: ID of the object of the CardItem model

	"""

	title = 'MergeCSV Card Edit'
	mergecsv_card = get_object_or_404(MergeCSV, pk=mcsv_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='mergecsv')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=mcsv_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_mergecsv_edit'
		template_name = 'gsi/_cs_mergecsv_form.html'
		func = mergecsv_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = MergeCSVForm(instance=mergecsv_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'mergecsv': {'save_button': ['card_sequence_update',[run_id, cs_id]],
						 'save_and_continue': ['cs_runid_csid_mergecsv_edit', [run_id, cs_id, card_id, mcsv_id]],
						 'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, MergeCSVForm, 'MergeCSV Card', REVERSE_URL['mergecsv'],
								func, args=True, item_id=mcsv_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_mergecsv_edit', args=[run_id, cs_id, card_id, mcsv_id]),
											   (u"MergeCSV Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   mergecsv_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': mcsv_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_rftrain_edit(request, run_id, cs_id, card_id, rftrain_id):
	"""**View for to edit RFTrain card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *rftrain_id*: ID of the object of the CardItem model

	"""

	title = 'RFTrain Card Edit'
	rftrain_card = get_object_or_404(RFTrain, pk=rftrain_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='rftrain')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=rftrain_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)

		url_form = 'cs_runid_csid_rftrain_edit'
		template_name = 'gsi/_cs_rftrain_form.html'
		func = rftrain_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RFTrainForm(instance=rftrain_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'rftrain': {'save_button': ['card_sequence_update', [run_id, cs_id]],
						'save_and_continue': ['cs_runid_csid_rftrain_edit', [run_id, cs_id, card_id]],
						'cancel_button': ['card_sequence_update', [run_id, cs_id]]},
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, RFTrainForm, 'RFTrain Card', REVERSE_URL['rftrain'],
								func, args=True, item_id=rftrain_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_rftrain_edit', args=[run_id, cs_id, card_id, rftrain_id]),
											   (u"RFTrain Card with the same name already exists"))
				)
			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   rftrain_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': rftrain_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_randomforest_edit(request, run_id, cs_id, card_id, rf_id):
	"""**View for to edit RandomForest card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *rf_id*: ID of the object of the CardItem model

	"""

	title = 'RandomForest Card Edit'
	randomforest_card = get_object_or_404(RandomForest, pk=rf_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='randomforest')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=rf_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)
		url_form = 'cs_runid_csid_randomforest_edit'
		template_name = 'gsi/_cs_randomforest_form.html'
		func = randomforest_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = RandomForestForm(instance=randomforest_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'randomforest': {'save_button': ['card_sequence_update', [run_id, cs_id]],
							 'save_and_continue': ['cs_runid_csid_randomforest_edit', [run_id, cs_id, card_id]],
							 'cancel_button': ['card_sequence_update', [run_id, cs_id]]}
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, RandomForestForm, 'RandomForest Card', REVERSE_URL['randomforest'],
								func, args=True, item_id=rf_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_randomforest_edit', args=[run_id, cs_id, card_id, rf_id]),
											   (u"RandomForest Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The RFTrain Card "{0}" was removed from Card Sequence "{1}"'.format(
										   randomforest_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': rf_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data


@login_required
@render_to('cards/runid_csid_card.html')
def cs_runid_csid_calcstats_edit(request, run_id, cs_id, card_id, calcstats_id):
	"""**View for to edit CalcStats card of the CardSequence model.**

	:Arguments:

		* *request:* The request is sent to the server when processing the page
		* *run_id*: ID of the RunBase
		* *cs_id*: ID of the CardSequence
		* *card_id*: ID of the card of the CardSequence model
		* *calcstats_id*: ID of the object of the CardItem model

	"""

	title = 'CalcStats Card Edit'
	calcstats_card = get_object_or_404(CalcStats, pk=calcstats_id)
	content_type = get_object_or_404(ContentType, app_label='cards', model='calcstats')
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)

	try:
		card_item = get_object_or_404(CardItem, object_id=calcstats_id, content_type=content_type)
		card_sequence_card = CardSequence.cards.through.objects.get(id=card_id)
		url_form = 'cs_runid_csid_calcstats_edit'
		template_name = 'gsi/_cs_calcstats_form.html'
		func = calcstats_update_create

		# add two forms
		form_1 = CardSequenceCardForm(instance=card_sequence_card)
		form_2 = CalcStatsForm(instance=calcstats_card)

		# create a variable dictionary REVERSE_URL which keep: name of card, the button name and url forwarding
		REVERSE_URL = {
			'calcstats': {'save_button': ['card_sequence_update', [run_id, cs_id]],
							 'save_and_continue': ['cs_runid_csid_calcstats_edit', [run_id, cs_id, card_id]],
							 'cancel_button': ['card_sequence_update', [run_id, cs_id]]}
		}

		# Handling POST request
		if request.method == "POST":
			cs_form = [CardSequenceCardForm, card_sequence_card, card_item]
			response = get_post(request, CalcStatsForm, 'CalcStats Card', REVERSE_URL['calcstats'],
								func, args=True, item_id=calcstats_id, cs_form=cs_form)

			if response == None:
				return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('cs_runid_csid_calcstats_edit', args=[run_id, cs_id, card_id, calcstats_id]),
											   (u"CalcStats Card with the same name already exists"))
				)

			if isinstance(response, HttpResponseRedirect):
				return response
			else:
				form_2 = response
	except ObjectDoesNotExist:
		return HttpResponseRedirect(
			u'%s?danger_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
									   (u'The CalcStats Card "{0}" was removed from Card Sequence "{1}"'.format(
										   randomforest_card.name, card_sequence.name)
									   )))

	data = {
		'title': title,
		'form_1': form_1,
		'form_2': form_2,
		'card_id': calcstats_id,
		'url_form': url_form,
		'template_name': template_name,
		'run_id': run_id,
		'cs_id': cs_id,
		'card': card_id,
	}

	return data
