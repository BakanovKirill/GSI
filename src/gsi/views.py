# -*- coding: utf-8 -*-
import datetime
import os
import getpass
from datetime import datetime

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import filesizeformat
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.conf import settings

from gsi.models import (Run, RunStep, Log, OrderedCardItem,
						HomeVariables, VariablesGroup, YearGroup,
						Year)
from gsi.gsi_items_update_create import *
from gsi.gsi_forms import *
from core.utils import make_run
from core.get_post import get_post

TITLES = {
	'home': ['Home', 'index'],
	'setup_run': ['GSI Run Setup', 'run_setup'],
	'edit_run': ['GSI Edit Run', 'run_update'],
	'new_run': ['GSI New Run', 'new_run'],
	'card_sequence': ['GSI Card Sequence', 'card_sequence'],
	'add_card_sequence': ['GSI New Card Sequence', 'new_card_sequence'],
	'card_item_update': ['GSI Card Item', 'card_item_update'],
}


def handle_uploaded_file(f, path):
    with open(path, 'a') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@render_to('gsi/blocking.html')
def blocking(request):
	data = {}
	return data


@login_required
@render_to('gsi/index.html')
def index(request):
	title = 'GSI Main Menu'
	home_var = HomeVariables.objects.all()[0]

	# log error permission
	err_file = '/home/gsi/logs/perm_log.err'
	now = datetime.now()
	log_file = open(err_file, 'a')

	log_file.writelines('Fail' + '\n')
	log_file.writelines(str(now) + '\n')
	log_file.writelines('USER: ' + getpass.getuser() + '\n')
	log_file.close()

	# ens log error permission

	if request.POST:
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			file_name = str(request.FILES['test_data'])
			path_test_data = str(os.path.join(home_var.RF_AUXDATA_DIR, file_name))
			type_file = str(request.FILES['test_data'].content_type).split('/')[0]

			if type_file != 'image':
				handle_uploaded_file(request.FILES['test_data'], path_test_data)
				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('index'),
						(u'Test data "{0}" is loaded'.format(file_name)))
				)
			else:
				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('index'),
						(u'To download the test data needs text format'))
				)
	else:
		form = UploadFileForm()
	data = {'title': title, 'form': form}

	return data


@login_required
@render_to('gsi/run_setup.html')
def run_setup(request):
	title = 'GSI Run Setup'
	run_bases = RunBase.objects.all()
	run_name = ''

	if request.method == "POST":
		if request.POST.get('run_select'):
			for run_id in request.POST.getlist('run_select'):
				cur_run = get_object_or_404(RunBase, pk=run_id)
				run_name += '"' + cur_run.name + '", '
				cur_run.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('run_setup'),
										 (u'Run(s): {0} ==> deleted.'.
										  format(run_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_setup'),
										 (u"To delete, select Run or more Runs."))
			)

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
				author=request.user,
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
	run_base = get_object_or_404(RunBase, pk=run_id)
	title = 'GSI Edit "{0}"'.format(run_base.name)
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
				run_base.author = request.user
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
	cs_name = ''

	if request.method == "POST":
		if request.POST.get('cs_select'):
			for cs_id in request.POST.getlist('cs_select'):
				cur_cs = get_object_or_404(CardSequence, pk=cs_id)
				cs_name += '"' + cur_cs.name + '", '
				cur_cs.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('card_sequence', args=[run_id]),
										 (u'Card Sequence: {0} ==> deleted.'.
										  format(cs_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('card_sequence', args=[run_id]),
										 (u"To delete, select Card Sequence or more Card Sequences."))
			)

	data = {
		'title': title,
		'card_sequences': card_sequences,
		'run_id': run_id,
	}

	return data


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
			# import pdb;pdb.set_trace()
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
	url_process_card = 'run_new_card_sequence_update'
	form = None

	if request.method == "POST":
		if request.POST.get('create_processing_card') is not None:
			return HttpResponseRedirect(
					reverse('proces_card_run_new_csid', args=[cs_id])
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
		elif request.POST.get('delete_button') is not None:
			form = CardSequenceCreateForm(request.POST)

			if form.is_valid():
				# card_sequence = create_update_card_sequence(form, cs_id)

				if request.POST.get('cs_select'):
					cs_name = ''
					for card_id in request.POST.getlist('cs_select'):
						cur_cs = get_object_or_404(CardSequence.cards.through, pk=card_id)
						cs_name += '"' + str(cur_cs.card_item) + '", '
						cur_cs.delete()

					return HttpResponseRedirect(u'%s?status_message=%s' %
												(reverse('run_new_card_sequence_update', args=[cs_id]),
												 (u'Card Sequence: {0} ==> deleted.'.
												  format(cs_name)))
					)
				else:
					return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_new_card_sequence_update',
																				   args=[cs_id]),
																		   (u"To delete, select Card Sequence \
																		   or more Card Sequences."))
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
			form = CardSequenceCreateForm(request.POST, instance=card_sequence)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_and_continue_editing_button') is not None:
			form = CardSequenceCreateForm(request.POST, instance=card_sequence)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence_update', args=[run_id, card_sequence.id]),
					(u"The new card item '{0}' was changed successfully. You may edit it again below.".
					 format(card_sequence.name)))
				)
		elif request.POST.get('save_button') is not None:
			form = CardSequenceCreateForm(request.POST, instance=card_sequence)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('card_sequence', args=[run_id]),
					(u"The card sequence '{0}' created successfully.".
					 format(card_sequence.name)))
			)
		elif request.POST.get('delete_button') is not None:
			form = CardSequenceCreateForm(request.POST, instance=card_sequence)

			if form.is_valid():
				card_sequence = create_update_card_sequence(form, cs_id)

				if request.POST.get('cs_select'):
					cs_name = ''
					for cs_card_id in request.POST.getlist('cs_select'):
						# import pdb;pdb.set_trace()
						cur_cs = get_object_or_404(CardSequence.cards.through, pk=cs_card_id)
						cs_name += '"' + str(cur_cs.card_item) + '", '
						cur_cs.delete()

					return HttpResponseRedirect(u'%s?status_message=%s' %
												(reverse('card_sequence_update', args=[run_id, cs_id]),
												 (u'Card Item: {0} ==> deleted.'.
												  format(cs_name)))
					)
				else:
					return HttpResponseRedirect(u'%s?status_message=%s' %
												(reverse('card_sequence_update',
														 args=[run_id, cs_id]),
												 (u"To delete, select Card Item \
												 or more Card Items."))
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


# card item edit for card sequence
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
				execute_run = make_run(rb, request.user)
				name_runs += '"' + str(execute_run['run'].run_base.name) + '", '

			runs_id = '_'.join(request.POST.getlist('execute_runs'))
			now_date = datetime.now()
			now_date_formating = now_date.strftime("%d/%m/%Y")
			now_time = now_date.strftime("%H:%M")

			return HttpResponseRedirect(u'%s?status_message=%s' %
						(reverse('execute_runs', args=[execute_run['run'].id]),
						 (u"Runs: {0} has been submitted to back end and {1} on {2}".
						  format(name_runs, now_time, now_date_formating)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('submit_run'),
										 (u"For start choose Run(s)"))
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
		name_runs += '"' + str(get_object_or_404(Run, pk=int(run)).run_base.name) + '", '
		messages.append('It has been assigned unique run ID: {0}. To view progress of this run use \
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
	runs = Run.objects.all().order_by('id')
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
	runs_step.order_by('card_item.card_item.order')

	if request.method == "POST":
		if request.POST.get('details_file'):
			step = get_object_or_404(RunStep, pk=request.POST.get('details_file'))
			return HttpResponseRedirect(u'%s?status_message=' %
										(reverse('view_log_file', args=[run_id, step.id])))
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_details', args=[run_id]),
																   (u"To view the Log, select Card.")))

	data = {
		'title': title,
		'sub_title': sub_title,
		'run_id': run_id,
		'runs_step': runs_step,
	}

	return data


@login_required
@render_to('gsi/view_log_file.html')
def view_log_file(request, run_id, card_id):
	title = 'GSI View Log Details for Cards'
	run_step = get_object_or_404(RunStep, pk=card_id)
	run = get_object_or_404(Run, pk=run_id)
	log = get_object_or_404(Log, pk=run.log.id)
	log_path = log.log_file_path
	log_info = ''

	try:
		fd = open(log_path, 'r')
		# log_info = fd.readlines()
		for line in fd.readlines():
			log_info += line + '<br />'
	except Exception, e:
		print 'ERROR view_log_file: ', e
		return HttpResponseRedirect(u'%s?status_message=%s' %
									(reverse('run_details', args=[run_id]),
									 (u'Log File for card "{0}" not found!').
									 format(run_step.card_item)))

	data = {
		'title': title,
		'run_id': run_id,
		'log_info': log_info,
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
@render_to('gsi/environment_groups_list.html')
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


# environment group add
@login_required
@render_to('gsi/static_data_item_edit.html')
def environment_group_add(request):
	title = 'GSI Environment Group Add'
	url_form = 'environment_group_add'
	template_name = 'gsi/_env_group_form.html'
	reverse_url = {
		'save_button': 'environment_groups',
		'save_and_another': 'environment_group_add',
		'save_and_continue': 'environment_group_edit',
		'cancel_button': 'environment_groups'
	}
	func = var_group_update_create
	form = None

	if request.method == "POST":
		response = get_post(request, EnvironmentGroupsForm,
							'Environment Group', reverse_url, func)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = EnvironmentGroupsForm()

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
	}

	return data


# environment group add
@login_required
@render_to('gsi/static_data_item_edit.html')
def environment_group_edit(request, env_id):
	env_item = get_object_or_404(VariablesGroup, pk=env_id)
	title = 'GSI Environment Group "{0}" Edit'.format(env_item.name)
	url_form = 'environment_group_edit'
	template_name = 'gsi/_env_group_form.html'
	reverse_url = {
		'save_button': 'environment_groups',
		'save_and_another': 'environment_group_add',
		'save_and_continue': 'environment_groups',
		'cancel_button': 'environment_groups'
	}
	func = var_group_update_create
	form = None

	if request.method == "POST":
		# import pdb;pdb.set_trace()
		response = get_post(request, EnvironmentGroupsForm, 'Environment Group',
							reverse_url, func, item_id=env_id)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = EnvironmentGroupsForm(instance=env_item)

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'item_id': env_id,
	}

	return data


# area
@login_required
@render_to('gsi/areas_list.html')
def areas(request):
	title = 'GSI Areas'
	areas = Area.objects.all()
	area_name = ''

	if request.method == "POST":
		if request.POST.get('area_select'):
			for area_id in request.POST.getlist('area_select'):
				cur_area = get_object_or_404(Area, pk=area_id)
				area_name += '"' + cur_area.name + '", '
				cur_area.delete()

			area_ids = '_'.join(request.POST.getlist('env_select'))

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('areas'),
										 (u'Environment Groups: {0} ==> deleted.'.
										  format(area_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('areas'),
										 (u"To delete, select Area or more Areas."))
			)

	data = {
		'title': title,
		'areas': areas,
	}

	return data


# area add
@login_required
@render_to('gsi/static_data_item_edit.html')
def area_add(request):
	title = 'GSI Area Add'
	url_form = 'area_add'
	template_name = 'gsi/_area_form.html'
	reverse_url = {
		'save_button': 'areas',
		'save_and_another': 'area_add',
		'save_and_continue': 'area_edit',
		'cancel_button': 'areas'
	}
	func = area_update_create
	form = None
	available_tiles = Tile.objects.all()

	if request.method == "POST":
		response = get_post(request, AreasForm, 'Area',
							reverse_url, func)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = AreasForm()

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'available_tiles': available_tiles
	}

	return data


# area edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def area_edit(request, area_id):
	area = get_object_or_404(Area, pk=area_id)
	title = 'GSI Area Edit "%s"' % (area.name)
	url_form = 'area_edit'
	template_name = 'gsi/_area_form.html'
	reverse_url = {
		'save_button': 'areas',
		'save_and_another': 'area_add',
		'save_and_continue': 'area_edit',
		'cancel_button': 'areas'
	}
	func = area_update_create
	form = None
	chosen_tiles = area.tiles.all()
	available_tiles = Tile.objects.exclude(id__in=area.tiles.values_list('id', flat=True))

	if request.method == "POST":
		response = get_post(request, AreasForm, 'Area',
							reverse_url, func, item_id=area_id)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = AreasForm(instance=area)

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'item_id': area_id,
		'available_tiles': available_tiles,
		'chosen_tiles': chosen_tiles,
	}

	return data


# year group group
@login_required
@render_to('gsi/years_group_list.html')
def years_group(request):
	title = 'GSI Years Groups'
	years_groups = YearGroup.objects.all()
	yg_name = ''

	if request.method == "POST":
		if request.POST.get('yg_select'):
			for yg_id in request.POST.getlist('yg_select'):
				cur_yg = get_object_or_404(YearGroup, pk=yg_id)
				yg_name += '"' + cur_yg.name + '", '
				cur_yg.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('years_group'),
										 (u'Environment Groups: {0} ==> deleted.'.
										  format(yg_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('years_group'),
										 (u"To delete, select Area or more Areas."))
			)

	data = {
		'title': title,
		'years_groups': years_groups,
	}

	return data


# year group add
@login_required
@render_to('gsi/static_data_item_edit.html')
def years_group_add(request):
	title = 'GSI Years Groups Add'
	url_form = 'years_group_add'
	template_name = 'gsi/_years_group_form.html'
	reverse_url = {
		'save_button': 'years_group',
		'save_and_another': 'years_group_add',
		'save_and_continue': 'years_group_edit',
		'cancel_button': 'years_group'
	}
	func = yg_update_create
	form = None
	available_years = Year.objects.all()

	if request.method == "POST":
		response = get_post(request, YearGroupForm, 'Year Group',
							reverse_url, func)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = AreasForm()

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'available_years': available_years
	}

	return data


# year group edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def years_group_edit(request, yg_id):
	years_group = get_object_or_404(YearGroup, pk=yg_id)
	title = 'GSI YearGroup Edit "%s"' % (years_group.name)
	url_form = 'years_group_edit'
	template_name = 'gsi/_years_group_form.html'
	reverse_url = {
		'save_button': 'years_group',
		'save_and_another': 'years_group_add',
		'save_and_continue': 'years_group_edit',
		'cancel_button': 'years_group'
	}
	func = yg_update_create
	form = None
	chosen_years = years_group.years.all()
	available_years = Year.objects.exclude(id__in=years_group.years.values_list('id', flat=True))

	if request.method == "POST":
		response = get_post(request, YearGroupForm, 'Year Group',
							reverse_url, func, item_id=yg_id)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = AreasForm(instance=years_group)

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'item_id': yg_id,
		'available_years': available_years,
		'chosen_years': chosen_years,
	}

	return data
