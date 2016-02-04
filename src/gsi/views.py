# -*- coding: utf-8 -*-
import datetime

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.conf import settings

from gsi.models import (Run, RunStep, HomeVariables,
						VariablesGroup)
# from cards.models import CardItem
from gsi.gsi_forms import *
from core.utils import make_run

TITLES = {
	'home': ['Home', 'index'],
	'setup_run': ['GSI Run Setup', 'run_setup'],
	'edit_run': ['GSI Edit Run', 'run_update'],
	'new_run': ['GSI New Run', 'new_run'],
	'card_sequence': ['GSI Card Sequence', 'card_sequence'],
	'add_card_sequence': ['GSI New Card Sequence', 'new_card_sequence'],
	'card_item_update': ['GSI Card Item', 'card_item_update'],
}


@render_to('gsi/blocking.html')
def blocking(request):
	data = {}
	return data


@login_required
@render_to('gsi/index.html')
def index(request):
	title = 'GSI Main Menu'
	data = {'title': title}
	return data


@login_required
@render_to('gsi/run_setup.html')
def run_setup(request):
	title = 'GSI Run Setup'
	run_bases = RunBase.objects.all()
	data = {
		'title': title,
		'run_bases': run_bases,
	}

	return data


@login_required
@render_to('gsi/new_run.html')
def new_run(request):
	title = 'GSI New Run'
	form = None

	if request.method == "POST":
		form = RunForm(request.POST)

		if form.is_valid():
			new_run_base = RunBase.objects.create(
				name=form.cleaned_data["name"],
				description=form.cleaned_data["description"],
				purpose=form.cleaned_data["purpose"],
				card_sequence=form.cleaned_data["card_sequence"],
				directory_path=form.cleaned_data["directory_path"],
				resolution=form.cleaned_data["resolution"],
			)

			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('run_setup'),
					(u"RunID {0} created successfully".format(new_run_base.id)))
			)
	else:
		form = RunForm()

	data = {
		'title': title,
		'form': form,
	}

	return data


@login_required
@render_to('gsi/run_update.html')
def run_update(request, run_id):
	title = 'GSI Edit RunID {0}'.format(run_id)
	run_base = get_object_or_404(RunBase, pk=run_id)
	form = None

	if request.method == "POST":
		if request.POST.get('save_button') is not None:
			form = RunForm(request.POST)

			if form.is_valid():
				run_base.name = form.cleaned_data["name"]
				run_base.description = form.cleaned_data["description"]
				run_base.purpose = form.cleaned_data["purpose"]
				run_base.card_sequence = form.cleaned_data["card_sequence"]
				run_base.directory_path = form.cleaned_data["directory_path"]
				run_base.resolution = form.cleaned_data["resolution"]
				run_base.save()

				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('run_setup'),
						(u"Run {0} updated successfully".format(run_base.name)))
				)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('run_setup'),
					(u"Run {0} updated canceled".format(run_base.name)))
			)
	else:
		form = RunForm(instance=run_base)

	data = {
		'title': title,
		'run_base': run_base,
		'form': form
	}

	return data


@login_required
@render_to('gsi/card_sequence.html')
def card_sequence(request, run_id):
	card_sequences = CardSequence.objects.all()
	title = 'GSI Card Sequence'

	data = {
		'title': title,
		'card_sequences': card_sequences,
		'run_id': run_id,
	}

	return data


def create_update_card_sequence(form, cs_id=None):
	if cs_id:
		card_sequence = CardSequence.objects.get(id=cs_id)
		card_sequence.name=form.cleaned_data["name"]
		card_sequence.environment_override=form.cleaned_data["environment_override"]
		card_sequence.environment_base=form.cleaned_data["environment_base"]
		card_sequence.save()
	else:
		card_sequence = CardSequence.objects.create(
			name=form.cleaned_data["name"],
			environment_override=form.cleaned_data["environment_override"],
			environment_base=form.cleaned_data["environment_base"],
		)

	if form.cleaned_data["card_item"]:
		CardSequence.cards.through.objects.create(
			sequence=card_sequence,
			card_item=form.cleaned_data["card_item"],
			order=form.cleaned_data["order"],
		)

	return card_sequence


@login_required
@render_to('gsi/add_card_sequence.html')
def run_new_card_sequence_add(request):
	title = 'GSI New Card Sequence'
	href = 'run_new_card_sequence_add'
	form = None

	if request.method == "POST":
		if request.POST.get('create_processing_card') is not None:
			return HttpResponseRedirect(reverse('proces_card_new_run'))
		elif request.POST.get('add_card_items_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('run_new_card_sequence_update', args=[card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".\
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_and_continue_editing_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form)

				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('run_new_card_sequence_update',
														   args=[card_sequence.id]),
						(u"The card sequence '{0}' created successfully. You may edit it again below.".
						 format(card_sequence.name)))
				)
		elif request.POST.get('save_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form)

				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('new_run'),
						(u"The card sequence '{0}' created successfully.".
						 format(card_sequence.name)))
				)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('new_run'),
					(u"Card Sequence created canceled"))
			)
	else:
		form = CardSequenceCreateForm()

	data = {
		'title': title,
		'form': form,
		'href': href,
	}

	return data


@login_required
@render_to('gsi/card_sequence_update.html')
def run_new_card_sequence_update(request, cs_id):
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)
	card_sequence_cards = CardSequence.cards.through.objects.filter(sequence_id=cs_id)
	title = 'GSI Card Sequence {0}'.format(card_sequence.name)
	url_process_card = 'proces_card_sequence_card_edit'
	form = None

	if request.method == "POST":
		pass
		if request.POST.get('create_processing_card') is not None:
			return HttpResponseRedirect(
					reverse('proces_card_new_run_new_sc', args=[card_sequence.id])
				)
		elif request.POST.get('add_card_items_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('run_new_card_sequence_update',
													   args=[card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_and_continue_editing_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('run_new_card_sequence_update',
													   args=[card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('new_run'),
						(u"The card sequence '{0}' created successfully.".
						 format(card_sequence.name)))
				)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('new_run'),
					(u"Card Sequence created canceled"))
			)
	else:
		form = CardSequenceCreateForm(instance=card_sequence)

	data = {
		'title': title,
		'form': form,
		'cs_id': cs_id,
		'card_sequence_cards': card_sequence_cards,
		'card_sequence': card_sequence,
		'url_process_card': url_process_card,
	}

	return data


@login_required
@render_to('gsi/add_card_sequence.html')
def add_card_sequence(request, run_id):
	card_items = CardItem.objects.all()
	title = 'GSI New Card Sequence'
	href = 'add_card_sequence {0}'.format(run_id)
	form = None

	if request.method == "POST":
		if request.POST.get('create_processing_card') is not None:
			return HttpResponseRedirect(
					reverse('proces_card_runid', args=[run_id])
				)
		elif request.POST.get('add_card_items_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".\
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_and_continue_editing_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form)

				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, card_sequence.id]),
						(u"The card sequence '{0}' created successfully. You may edit it again below.".
						 format(card_sequence.name)))
				)
		elif request.POST.get('save_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form)

			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence', args=[run_id]),
					(u"The card sequence '{0}' created successfully.".
					 format(card_sequence.name)))
			)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence', args=[run_id]),
					(u"Card Sequence created canceled"))
			)
	else:
		form = CardSequenceCreateForm()

	data = {
		'title': title,
		'form': form,
		'run_id': run_id,
		'card_items': card_items,
		'href': href,
	}

	return data


@login_required
@render_to('gsi/card_sequence_update.html')
def card_sequence_update(request, run_id, cs_id):
	card_sequence = get_object_or_404(CardSequence, pk=cs_id)
	card_sequence_cards = CardSequence.cards.through.objects.filter(sequence_id=cs_id)
	title = 'GSI Card Sequence {0}'.format(card_sequence.name)
	url_process_card = 'proces_card_sequence_card_edit'
	form = None

	if request.method == "POST":
		if request.POST.get('create_processing_card') is not None:
			return HttpResponseRedirect(
					reverse('proces_card_runid_csid', args=[run_id, cs_id])
				)

		elif request.POST.get('add_card_items_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_and_continue_editing_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence', args=[run_id]),
					(u"The card sequence '{0}' created successfully.".
					 format(card_sequence.name)))
			)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence', args=[run_id]),
					(u'Card Sequence "{0}" created canceled'.format(card_sequence.name)))
			)
	else:
		form = CardSequenceCreateForm(instance=card_sequence)

	data = {
		'title': title,
		'form': form,
		'run_id': run_id,
		'cs_id': cs_id,
		'card_sequence_cards': card_sequence_cards,
		'card_sequence': card_sequence,
		'url_process_card': url_process_card,
	}

	return data


@login_required
@render_to('gsi/card_item_update.html')
def card_item_update(request, run_id, cs_id, card_item_id):
	card_sequence_card = get_object_or_404(CardSequence.cards.through, pk=card_item_id)
	title = 'GSI Card ItemID {0}'.format(card_item_id)
	form = None

	if request.method == "POST":
		if request.POST.get('save_button') is not None:
			form = CardSequenceCardForm(request.POST, instance=card_sequence_card)

			if form.is_valid():
				for card in CardItem.objects.filter(id=form.cleaned_data["card_item"].id):
					card_sequence_card.card_item = card
				card_sequence_card.order = form.cleaned_data["order"]
				card_sequence_card.save()

				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
						(u"Card Item {0} updated successfully".format(card_sequence_card.card_item)))
				)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
					(u"Card Item {0} updated canceled".format(card_sequence_card.card_item)))
			)
	else:
		form = CardSequenceCardForm(instance=card_sequence_card)

	data = {
		'title': title,
		'card_sequence_card': card_sequence_card,
		'cs_id': cs_id,
		'form': form,
		'run_id': run_id,
	}

	return data

# submit a run
@login_required
@render_to('gsi/submit_run.html')
def submit_run(request):
	run_bases = RunBase.objects.all()
	title = 'GSI Submit a Run'
	name_runs = ''

	if request.method == "POST":
		if request.POST.getlist('execute_runs'):
			for run_id in request.POST.getlist('execute_runs'):
				rb = get_object_or_404(RunBase, pk=run_id)
				name_runs += '"' + str(rb.name) + '", '
				execute_run = make_run(rb, request.user)

			runs_id = '_'.join(request.POST.getlist('execute_runs'))
			now_date = datetime.datetime.now()
			now_date_formating = now_date.strftime("%d/%m/%Y")
			now_time = now_date.strftime("%H:%M")

			return HttpResponseRedirect(u'%s?status_message=%s' %
						(reverse('execute_runs', args=[runs_id]),
						 (u"Runs: {0} has been submitted to back end and {1} on {2}".
						  format(name_runs, now_time, now_date_formating)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('submit_run'),
										 (u"Fof start choose Run."))
			)
	data = {
		'title': title,
		'run_bases': run_bases,
	}

	return data


# execute run
@login_required
@render_to('gsi/execute_run.html')
def execute_runs(request, run_id):
	title = 'GSI Execute Run'
	list_run_id = run_id.split('_')
	name_runs = ''
	messages = []

	for run in list_run_id:
		name_runs += '"' + str(get_object_or_404(RunBase, pk=int(run)).name) + '", '
		messages.append('It has been assigned unique run ID:{0}. To view progress of this run use \
						the view progress otion on the main menu.\n'.format(run))

	data = {
		'title': title,
		'run_id': run_id,
		'messages': messages,
	}

	return data


# run progress
@login_required
@render_to('gsi/run_progress.html')
def run_progress(request):
	runs = Run.objects.all()
	title = 'GSI Run Progress'

	if request.method == "POST":
		if request.POST.get('run_progress'):
			run_id = request.POST.get('run_progress')
			run = get_object_or_404(Run, pk=run_id)

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('run_details', args=[run_id]),
										 (u'Run: "{0}" selected for viewing log file.'.
										  format(run.run_base)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_progress'),
										 (u"To view the log, select Run."))
			)
	data = {
		'title': title,
		'runs': runs,
	}

	return data


# execute run
@login_required
@render_to('gsi/run_details.html')
def run_details(request, run_id):
	title = 'GSI Run Details'
	sub_title = 'The View Log file select and hit view'
	runs_step = RunStep.objects.filter(parent_run=run_id)

	# for run in list_run_id:
	# 	name_runs += '"' + str(get_object_or_404(RunBase, pk=int(run)).name) + '", '
	# 	messages.append('It has been assigned unique run ID:{0}. To view progress of this run use \
	# 					the view progress otion on the main menu.\n'.format(run))

	data = {
		'title': title,
		'sub_title': sub_title,
		'run_id': run_id,
		'runs_step': runs_step,
	}

	return data


# setup static data
@login_required
@render_to('gsi/static_data_setup.html')
def static_data_setup(request):
	title = 'GSI Setup Static Data'
	data = {
		'title': title,
	}

	return data


# setup home variable
@login_required
@render_to('gsi/home_variable_setup.html')
def home_variable_setup(request):
	title = 'GSI Home Variables'
	variables = get_object_or_404(HomeVariables, pk=1)
	form = None

	if request.method == "POST":
		form = HomeVariablesForm(request.POST)

		if form.is_valid():
				variables.SAT_TIF_DIR_ROOT = form.cleaned_data["SAT_TIF_DIR_ROOT"]
				variables.RF_DIR_ROOT = form.cleaned_data["RF_DIR_ROOT"]
				variables.USER_DATA_DIR_ROOT = form.cleaned_data["USER_DATA_DIR_ROOT"]
				variables.MODIS_DIR_ROOT = form.cleaned_data["MODIS_DIR_ROOT"]
				variables.RF_AUXDATA_DIR = form.cleaned_data["RF_AUXDATA_DIR"]
				variables.SAT_DIF_DIR_ROOT = form.cleaned_data["SAT_DIF_DIR_ROOT"]
				variables.save()

		if request.POST.get('save_button') is not None:
			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('static_data_setup'),
										 (u"Home variables successfully updated"))
			)
		if request.POST.get('save_and_continue_button') is not None:
			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('home_variable_setup'),
										 (u"Home variables successfully updated"))
			)
	else:
		form = HomeVariablesForm(instance=variables)

	data = {
		'title': title,
		'variables': variables,
		'form': form
	}

	return data


# environment group
@login_required
@render_to('gsi/environment_groups.html')
def environment_groups(request):
	title = 'GSI Environment Groups'
	environments = VariablesGroup.objects.all()
	env_name = ''

	if request.method == "POST":
		if request.POST.get('env_select'):
			for env_id in request.POST.getlist('env_select'):
				cur_env = get_object_or_404(VariablesGroup, pk=env_id)
				env_name += '"' + str(cur_env.name) + '", '
				cur_env.delete()

			envs_ids = '_'.join(request.POST.getlist('env_select'))

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('environment_groups'),
										 (u'Environment Groups: {0} ==> deleted.'.
										  format(env_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('environment_groups'),
										 (u"To delete, select Group or more Groups."))
			)

	data = {
		'title': title,
		'environments': environments,
	}

	return data