# -*- coding: utf-8 -*-
import datetime
import os
import shutil
import getpass
from datetime import datetime
import magic

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import filesizeformat
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.conf import settings

from gsi.models import (Run, RunStep, Log, OrderedCardItem,
						HomeVariables, VariablesGroup, YearGroup,
						Year, Satellite, InputDataDirectory, ListTestFiles)
from gsi.gsi_items_update_create import *
from gsi.gsi_forms import *
from core.utils import (make_run, get_dir_root_static_path,
                        slash_remove_from_path, get_files_dirs)
from core.get_post import get_post
from log.logger import get_logs
from gsi.settings import (NUM_PAGINATIONS, PATH_RUNS_SCRIPTS, BASE_DIR,
						  STATIC_ROOT, STATIC_DIR)
from core.paginations import paginations

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


class UploadStaticDataView(FormView):
	success_url = 'index.html'
	form_class = UploadFileForm
	template_name = 'gsi/upload_file.html'

	def get_context_data(self, **kwargs):
		context = super(UploadStaticDataView, self).get_context_data(**kwargs)
		title = 'Upload Test Data'
		url_name = 'upload_file'
		context.update({
            'title': title,
			'url_name': url_name,
        })

		return context

	def form_valid(self, form):
		home_var = HomeVariables.objects.all()[0]
		file_name = str(self.request.FILES['test_data']).decode('utf-8')
		path_test_data = os.path.join(home_var.RF_AUXDATA_DIR, file_name)
		# type_file = str(request.FILES['test_data'].content_type).split('/')[0]
		handle_uploaded_file(self.request.FILES['test_data'], path_test_data)
		message = u'Test data "{0}" is loaded'.format(file_name)

		return HttpResponseRedirect(
                '%s?status_message=%s' % (reverse('index'), message))


# upload_static_data_view = user_passes_test(login_url='/', redirect_field_name='')(UploadStaticDataView.as_view())


@login_required
@render_to('gsi/upload_file.html')
def upload_file(request):
	title = 'Upload Test Data'
	home_var = HomeVariables.objects.all()[0]
	url_name = 'upload_file'

	if request.POST:
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			file_name = str(request.FILES['test_data']).decode('utf-8')
			path_test_data = os.path.join(home_var.RF_AUXDATA_DIR, file_name)
			handle_uploaded_file(request.FILES['test_data'], path_test_data)

			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('upload_file'),
					(u'Test data "{0}" is loaded'.format(file_name)))
			)

			# type_file = str(request.FILES['test_data'].content_type).split('/')[0]
			# if type_file != 'image':
			# 	handle_uploaded_file(request.FILES['test_data'], path_test_data)
			# 	return HttpResponseRedirect(
			# 			u'%s?status_message=%s' % (reverse('index'),
			# 			(u'Test data "{0}" is loaded'.format(file_name)))
			# 	)
			# else:
			# 	return HttpResponseRedirect(
			# 			u'%s?status_message=%s' % (reverse('index'),
			# 			(u'The file "{0}" can not be loaded. \
			# 			To download using a text file format'.format(file_name)))
			# 	)
		else:
			return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('upload_file'),
					(u'Sorry. Upload error: {0}'.format(form['test_data'].errors.as_text())))
			)
	else:
		form = UploadFileForm()
	data = {
		'title': title,
		'form': form,
		'url_name': url_name
	}

	return data


@login_required
@render_to('gsi/index.html')
def index(request):
	title = 'Main Menu'
	home_var = HomeVariables.objects.all()[0]
	url_name = 'home'

	if request.POST:
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			file_name = str(request.FILES['test_data']).decode('utf-8')
			path_test_data = os.path.join(home_var.RF_AUXDATA_DIR, file_name)
			# type_file = str(request.FILES['test_data'].content_type).split('/')[0]
			handle_uploaded_file(request.FILES['test_data'], path_test_data)

			return HttpResponseRedirect(
					u'%s?status_message=%s' % (reverse('index'),
					(u'Test data "{0}" is loaded'.format(file_name)))
			)

			# if type_file != 'image':
			# 	handle_uploaded_file(request.FILES['test_data'], path_test_data)
			# 	return HttpResponseRedirect(
			# 			u'%s?status_message=%s' % (reverse('index'),
			# 			(u'Test data "{0}" is loaded'.format(file_name)))
			# 	)
			# else:
			# 	return HttpResponseRedirect(
			# 			u'%s?status_message=%s' % (reverse('index'),
			# 			(u'The file "{0}" can not be loaded. \
			# 			To download using a text file format'.format(file_name)))
			# 	)
		else:
			return HttpResponseRedirect(
					u'%s?danger_message=%s' % (reverse('index'),
					(u'Upload error: {0}'.format(form['test_data'].errors.as_text())))
			)
	else:
		form = UploadFileForm()
	data = {
		'title': title,
		'form': form,
		'url_name': url_name
	}

	return data


@login_required
@render_to('gsi/run_setup.html')
def run_setup(request):
	title = 'Run Setup'
	run_bases = RunBase.objects.all().order_by('-date_modified')
	run_name = ''
	url_name = 'run_setup'

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(RunBase, pk=int(r))
				data += '"' + cur_run.name + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		if 'cur_run_id' in data_post:
			message = u'Are you sure you want to remove this objects:'
			run_id = data_post['cur_run_id']
			cur_run = get_object_or_404(RunBase, pk=int(run_id))
			data = '<b>"' + cur_run.name + '"</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		if request.POST.get('run_select'):
			for run_id in request.POST.getlist('run_select'):
				cur_run = get_object_or_404(RunBase, pk=run_id)
				run_name += '"' + cur_run.name + '", '
				cur_run.delete()
			run_name = run_name[:-2]

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_setup'),
										 (u'Run(s): {0} ==> deleted.'.format(run_name)))
			)
		elif request.POST.get('delete_button'):
			run_bases_current = get_object_or_404(RunBase, pk=request.POST.get('delete_button'))
			run_name += '"' + run_bases_current.name + '"'
			run_bases_current.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('run_setup'), (u'Run: {0} ==> deleted.'.format(run_name)))
										)
		else:
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_setup'),
										 (u"To delete, select Run or more Runs."))
			)

	# paginations
	model_name = paginations(request, run_bases)

	data = {
		'title': title,
		'run_bases': model_name,
		'model_name': model_name,
		'url_name': url_name,
	}

	return data


@login_required
@render_to('gsi/new_run.html')
def new_run(request):
	title = 'New Run'
	form = None

	if request.method == "POST":
		form = RunForm(request.POST)

		if form.is_valid():
			new_run_base = RunBase.objects.create(
				name=form.cleaned_data["name"],
				description=form.cleaned_data["description"],
				purpose=form.cleaned_data["purpose"],
				# card_sequence=form.cleaned_data["card_sequence"],
				directory_path=form.cleaned_data["directory_path"],
				resolution=form.cleaned_data["resolution"],
				author=request.user,
			)

			if request.POST.get('save_button') is not None:
				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('run_setup'),
						(u"RunID {0} created successfully".format(new_run_base.id)))
				)
			if request.POST.get('save_update_button') is not None:
				return HttpResponseRedirect(
						u'%s?status_message=%s' % (reverse('run_update', args=[new_run_base.id]),
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
	title = 'Edit "{0}"'.format(run_base.name)
	form = None

	if request.method == "POST":
		form = RunForm(request.POST)

		if request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?info_message=%s' % (reverse('run_setup'),
					(u"Run {0} updated canceled".format(run_base.name)))
			)
		else:
			if form.is_valid():
				run_base.name = form.cleaned_data["name"]
				run_base.description = form.cleaned_data["description"]
				run_base.purpose = form.cleaned_data["purpose"]
				# run_base.card_sequence = form.cleaned_data["card_sequence"]
				run_base.directory_path = form.cleaned_data["directory_path"]
				run_base.resolution = form.cleaned_data["resolution"]
				# run_base.author = request.user
				run_base.save()

				if request.POST.get('save_button') is not None:
					return HttpResponseRedirect(
							u'%s?status_message=%s' % (reverse('run_setup'),
							(u"Run {0} updated successfully".format(run_base.name)))
					)
				if request.POST.get('edit_run_details_button') is not None:
					return HttpResponseRedirect(
							u'%s?info_message=%s' % (reverse('card_sequence_update', args=[run_id, run_base.card_sequence.id]),
							(u"Update Card Sequence {0}".format(run_base.card_sequence)))
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
@render_to('gsi/run_new_card_sequence_list.html')
def run_new_card_sequence_list(request):
	title = 'Card Sequences'
	card_sequences = CardSequence.objects.all()
	cs_name = ''

	if request.method == "POST":
		if request.POST.get('cs_select'):
			for cs_id in request.POST.getlist('cs_select'):
				cur_cs = get_object_or_404(CardSequence, pk=cs_id)
				cs_name += '"' + cur_cs.name + '", '
				cur_cs.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('run_new_card_sequence_list'),
										 (u'Card Sequence: {0} ==> deleted.'.
										  format(cs_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_new_card_sequence_list'),
										 (u"To delete, select Card Sequence or more Card Sequences."))
			)

	data = {
		'title': title,
		'card_sequences': card_sequences,
	}

	return data


@login_required
@render_to('gsi/card_sequence.html')
def card_sequence(request, run_id):
	card_sequences = CardSequence.objects.all()
	title = 'Card Sequences'
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
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('card_sequence', args=[run_id]),
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
	title = 'New Card Sequence'
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
					u'%s?info_message=%s' % (reverse('run_new_card_sequence_list'),
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
	title = 'Card Sequence %s' % (card_sequence.name)
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
					return HttpResponseRedirect(u'%s?warning_message=%s' %
												(reverse('run_new_card_sequence_update', args=[cs_id]),
												 (u"To delete, select Card Sequence or more Card Sequences."))
					)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?info_message=%s' % (reverse('run_new_card_sequence_list'),
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
	title = 'New Card Sequence'
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
					u'%s?info_message=%s' % (reverse('card_sequence', args=[run_id]),
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
	title = 'Card Sequence {0}'.format(card_sequence.name)
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
					u'%s?status_message=%s' % (reverse('run_update', args=[run_id]),
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
												 (u'Card Items: {0} ==> deleted.'.format(cs_name)))
					)
				else:
					return HttpResponseRedirect(u'%s?warning_message=%s' %
												(reverse('card_sequence_update', args=[run_id, cs_id]),
												 (u"To delete, select Card Item or more Card Items."))
					)
		elif request.POST.get('del_current_btn'):
			card_id = request.POST.get('del_current_btn')
			cur_cs = get_object_or_404(CardSequence.cards.through, pk=card_id)
			cs_name = '"' + str(cur_cs.card_item) + '", '
			cur_cs.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('card_sequence_update', args=[run_id, cs_id]),
										 (u'Card Item: {0} ==> deleted.'.format(cs_name)))
										)
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(
					u'%s?info_message=%s' % (reverse('run_update', args=[run_id]),
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
	title = 'Card ItemID {0}'.format(card_item_id)
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
					u'%s?info_message=%s' % (reverse('card_sequence_update', args=[run_id, cs_id]),
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
	run_bases = RunBase.objects.all().order_by('-date_modified')
	title = 'Submit a Run'
	name_runs = ''
	url_name = 'submit_run'

	if request.method == "POST":
		if request.POST.getlist('execute_runs'):
			for run_id in request.POST.getlist('execute_runs'):
				rb = get_object_or_404(RunBase, pk=run_id)
				execute_run = make_run(rb, request.user)

				if not execute_run:
					return HttpResponseRedirect(u'%s?danger_message=%s' %
												(reverse('submit_run'),
												 (u'Unable to execute the Run. \
												 Please contact the administrator!'))
												)
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
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('submit_run'),
										 (u"For start choose Run(s)"))
			)

	# paginations
	model_name = paginations(request, run_bases)

	data = {
		'title': title,
		'run_bases': model_name,
		'model_name': model_name,
		'url_name': url_name,
	}

	return data


# execute run
@login_required
@render_to('gsi/execute_run.html')
def execute_runs(request, run_id):
	title = 'Execute Run'
	list_run_id = run_id.split('_')
	name_runs = ''
	messages = []

	for run in list_run_id:
		name_runs += '"' + str(get_object_or_404(Run, pk=int(run)).run_base.name) + '", '
		messages.append('It has been assigned unique run ID: {0}.\nTo view progress of this run use \
						the view progress option on the main menu.\n'.format(run))

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
	runs = Run.objects.all().order_by('-id')
	title = 'Run Progress'
	url_name = 'run_progress'
	run_name = ''

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(Run, pk=int(r))
				data += '"' + str(cur_run) + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		if request.POST.get('run_progress'):
			for run_id in request.POST.getlist('run_progress'):
				cur_run = get_object_or_404(Run, pk=run_id)
				run_name += '"' + str(cur_run) + '", '
				cur_run.delete()

				# delete folder Run(s) from server
				try:
					run_folder = 'R_{0}'.format(run_id)
					path = os.path.join(PATH_RUNS_SCRIPTS, run_folder)
					shutil.rmtree(path)
				except OSError:
					pass

			run_name = run_name[:-2]

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_progress'),
										 (u'Run(s): {0} ==> deleted.'.format(run_name)))
			)
		else:
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_progress'),
										 (u"To delete, select Run or more Runs."))
			)

	# paginations
	model_name = paginations(request, runs)

	data = {
		'title': title,
		'runs': model_name,
		'url_name': url_name,
		'model_name': model_name,
	}

	return data


# execute run
@login_required
@render_to('gsi/run_details.html')
def run_details(request, run_id):
	title = 'Run Details'
	sub_title = 'The View Log file select and hit view'
	runs_step = RunStep.objects.filter(parent_run=run_id)
	runs_step.order_by('card_item.card_item.order')
	run = get_object_or_404(Run, pk=run_id)
	url_name = 'run_details'

	if request.method == "POST":
		if request.POST.get('details_file'):
			step = get_object_or_404(RunStep, pk=request.POST.get('details_file'))

			if request.POST.get('log_out_button', ''):
				return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('view_log_file', args=[run_id, step.card_item.id]),
										 (u'Log Out file for the Card "{0}".'.format(step.card_item))))
			elif request.POST.get('log_err_button', ''):
				return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('view_log_file', args=[run_id, step.card_item.id]),
										 (u'Log Error file for the Card "{0}".'.format(step.card_item))))
		else:
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_details', args=[run_id]),
																   (u"To view the Card Log, select Card.")))

	# paginations
	model_name = paginations(request, runs_step)

	data = {
		'title': title,
		'sub_title': sub_title,
		'run_id': run_id,
		'runs_step': model_name,
		'model_name': model_name,
		'url_name': url_name,
		'obj_id': run_id,
	}

	return data


# view out/error log files for cards
@login_required
@render_to('gsi/view_log_file.html')
def view_log_file(request, run_id, card_id):
	status = ''
	log_info = ''
	run_step_card = RunStep.objects.filter(card_item__id=card_id).first()
	run = get_object_or_404(Run, pk=run_id)
	log = get_object_or_404(Log, pk=run.log.id)
	log_path = log.log_file_path

	if request.method == "GET":
		status = request.GET.get('status_message', '')

	out_ext = 'Out' in status and 'out' or ''
	err_ext = 'Error' in status and 'err' or ''
	out = 'Out' in status and 'Out' or ''
	err = 'Error' in status and 'Error' or ''
	log_file  = 'runcard_{0}.{1}'.format(card_id, out_ext or err_ext)
	log_file_path = '{0}/{1}'.format(log_path, log_file)

	try:
		fd = open(log_file_path, 'r')
		for line in fd.readlines():
			log_info += line + '<br />'
	except Exception, e:
		print 'ERROR view_log_file: ', e

		# logs for api
		path_file = '/home/gsi/LOGS/log_file.log'
		now = datetime.now()
		log_file = open(path_file, 'a')
		log_file.writelines(str(now) + '\n')
		log_file.writelines('ERROR => {0}\n\n\n'.format(e))
		log_file.close()


		mess = out or err
		return HttpResponseRedirect(u'%s?danger_message=%s' %
									(reverse('run_details', args=[run_id]),
									 (u'Log {0} for Card "{1}" not found!').
									 format(mess, run_step_card)))

	data = {
		'title': status,
		'run_id': run_id,
		'log_info': log_info
	}

	return data


# setup static data
@login_required
@render_to('gsi/static_data_setup.html')
def static_data_setup(request):
	title = 'Setup Static Data'
	data = {
		'title': title,
	}

	return data


# setup home variable
@login_required
@render_to('gsi/home_variable_setup.html')
def home_variable_setup(request):
	title = 'Home Variables'
	variables = get_object_or_404(HomeVariables, pk=1)
	form = None
	url_name = 'home_variable'
	but_name = 'static_data'

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
		'form': form,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# environment group
@login_required
@render_to('gsi/environment_groups_list.html')
def environment_groups(request):
	title = 'Environment Groups'
	environments = VariablesGroup.objects.all()
	env_name = ''
	url_name = 'environment_groups'
	but_name = 'static_data'

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(VariablesGroup, pk=int(r))
				data += '"' + cur_run.name + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		if 'cur_run_id' in data_post:
			message = u'Are you sure you want to remove this objects:'
			run_id = data_post['cur_run_id']
			cur_run = get_object_or_404(VariablesGroup, pk=int(run_id))
			data = '<b>"' + cur_run.name + '"</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		# if request.POST.get('delete_button'):
		if request.POST.get('env_select'):
			for env_id in request.POST.getlist('env_select'):
				cur_env = get_object_or_404(VariablesGroup, pk=env_id)
				env_name += '"' + str(cur_env.name) + '", '
				cur_env.delete()

			envs_ids = '_'.join(request.POST.getlist('env_select'))
			env_name = env_name[:-2]

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('environment_groups'),
										 (u'Environment Groups: {0} ==> deleted.'.
										  format(env_name)))
			)
		elif request.POST.get('delete_button'):
			cur_env = get_object_or_404(VariablesGroup, pk=request.POST.get('delete_button'))
			env_name += '"' + str(cur_env.name) + '", '
			cur_env.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' %
										(reverse('environment_groups'),
										 (u'Environment Group: {0} ==> deleted.'.
										  format(env_name))))
		else:
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('environment_groups'),
										 (u"To delete, select Group or more Groups."))
			)

	# paginations
	model_name = paginations(request, environments)

	data = {
		'title': title,
		'environments': model_name,
		'model_name': model_name,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# environment group add
@login_required
@render_to('gsi/static_data_item_edit.html')
def environment_group_add(request):
	title = 'Environment Group Add'
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
	url_name = 'environment_groups'
	but_name = 'static_data'

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
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# environment group add
@login_required
@render_to('gsi/static_data_item_edit.html')
def environment_group_edit(request, env_id):
	env_item = get_object_or_404(VariablesGroup, pk=env_id)
	title = 'Environment Group "{0}" Edit'.format(env_item.name)
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
	url_name = 'environment_groups'
	but_name = 'static_data'

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
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# area
@login_required
@render_to('gsi/areas_list.html')
def areas(request):
	title = 'Areas'
	areas = Area.objects.all()
	area_name = ''
	url_name = 'areas'
	but_name = 'static_data'

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(Area, pk=int(r))
				data += '"' + cur_run.name + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		if 'cur_run_id' in data_post:
			message = u'Are you sure you want to remove this objects:'
			run_id = data_post['cur_run_id']
			cur_run = get_object_or_404(Area, pk=int(run_id))
			data = '<b>"' + cur_run.name + '"</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		# if request.POST.get('delete_button'):
		if request.POST.get('area_select'):
			for area_id in request.POST.getlist('area_select'):
				cur_area = get_object_or_404(Area, pk=area_id)
				area_name += '"' + cur_area.name + '", '
				cur_area.delete()

			area_ids = '_'.join(request.POST.getlist('env_select'))

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('areas'),
										 (u'Areas: {0} ==> deleted.'.format(area_name)))
			)
		elif request.POST.get('delete_button'):
			cur_area = get_object_or_404(Area, pk=request.POST.get('delete_button'))
			area_name += '"' + cur_area.name + '", '
			cur_area.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('areas'),
										 (u'Areas: {0} ==> deleted.'.format(area_name)))
				)
		else:
				return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('areas'),
											 (u"To delete, select Area or more Areas."))
				)

	# paginations
	model_name = paginations(request, areas)

	data = {
		'title': title,
		'areas': model_name,
		'model_name': model_name,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# area add
@login_required
@render_to('gsi/static_data_item_edit.html')
def area_add(request):
	title = 'Area Add'
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
	url_name = 'areas'
	but_name = 'static_data'
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
		'available_tiles': available_tiles,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# area edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def area_edit(request, area_id):
	area = get_object_or_404(Area, pk=area_id)
	title = 'Area Edit "%s"' % (area.name)
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
	url_name = 'areas'
	but_name = 'static_data'
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
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# year group group
@login_required
@render_to('gsi/years_group_list.html')
def years_group(request):
	title = 'Years Groups'
	years_groups = YearGroup.objects.all()
	yg_name = ''
	url_name = 'years_group'
	but_name = 'static_data'

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(YearGroup, pk=int(r))
				data += '"' + cur_run.name + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		if 'cur_run_id' in data_post:
			message = u'Are you sure you want to remove this objects:'
			run_id = data_post['cur_run_id']
			cur_run = get_object_or_404(YearGroup, pk=int(run_id))
			data = '<b>"' + cur_run.name + '"</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		# if request.POST.get('delete_button'):
		if request.POST.get('yg_select'):
			for yg_id in request.POST.getlist('yg_select'):
				cur_yg = get_object_or_404(YearGroup, pk=yg_id)
				yg_name += '"' + cur_yg.name + '", '
				cur_yg.delete()
			yg_name = yg_name[:-2]

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('years_group'),
										 (u'Years Groups: {0} ==> deleted.'.format(yg_name)))
			)
		elif request.POST.get('delete_button'):
			cur_yg = get_object_or_404(YearGroup, pk=request.POST.get('delete_button'))
			yg_name += '"' + cur_yg.name + '"'
			cur_yg.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('years_group'),
										 (u'Years Group: {0} ==> deleted.'.format(yg_name)))
				)
		else:
			return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('years_group'),
										 (u"To delete, select Years Group or more Years Groups."))
			)

	# paginations
	model_name = paginations(request, years_groups)

	data = {
		'title': title,
		'years_groups': model_name,
		'model_name': model_name,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# year group add
@login_required
@render_to('gsi/static_data_item_edit.html')
def years_group_add(request):
	title = 'Years Groups Add'
	url_form = 'years_group_add'
	url_name = 'years_group'
	but_name = 'static_data'
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
		'available_years': available_years,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# year group edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def years_group_edit(request, yg_id):
	years_group = get_object_or_404(YearGroup, pk=yg_id)
	title = 'YearGroup Edit "%s"' % (years_group.name)
	url_name = 'years_group'
	but_name = 'static_data'
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
		'url_name': url_name,
		'but_name': but_name,
		'template_name': template_name,
		'form': form,
		'item_id': yg_id,
		'available_years': available_years,
		'chosen_years': chosen_years,
	}

	return data


# satellite list
@login_required
@render_to('gsi/satellite_list.html')
def satellite(request):
	title = 'Satellites'
	satellites = Satellite.objects.all()
	satellite_name = ''
	url_name = 'satellite'
	but_name = 'static_data'

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(Satellite, pk=int(r))
				data += '"' + cur_run.name + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		if 'cur_run_id' in data_post:
			message = u'Are you sure you want to remove this objects:'
			run_id = data_post['cur_run_id']
			cur_run = get_object_or_404(Satellite, pk=int(run_id))
			data = '<b>"' + cur_run.name + '"</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		# if request.POST.get('delete_button'):
		if request.POST.get('satellite_select'):
			for satellite_id in request.POST.getlist('satellite_select'):
				cur_satellite = get_object_or_404(Satellite, pk=satellite_id)
				satellite_name += '"' + cur_satellite.name + '", '
				cur_satellite.delete()

			satellite_name = satellite_name[:-2]

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('satellite'),
										 (u'Satellites: {0} ==> deleted.'.format(satellite_name)))
			)
		elif request.POST.get('delete_button'):
			cur_satellite = get_object_or_404(Satellite, pk=request.POST.get('delete_button'))
			satellite_name += '"' + cur_satellite.name + '"'
			cur_satellite.delete()

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('satellite'),
										 (u'Satellite: {0} ==> deleted.'.format(satellite_name)))
				)
		else:
				return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('satellite'),
											 (u"To delete, select Satellite or more Satellites."))
				)

	# paginations
	model_name = paginations(request, satellites)

	data = {
		'title': title,
		'satellites': model_name,
		'model_name': model_name,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# satellite add
@login_required
@render_to('gsi/static_data_item_edit.html')
def satellite_add(request):
	title = 'Satellites Add'
	url_form = 'satellite_add'
	url_name = 'satellite'
	but_name = 'static_data'
	template_name = 'gsi/_satellite_form.html'
	reverse_url = {
		'save_button': 'satellite',
		'save_and_another': 'satellite_add',
		'save_and_continue': 'satellite_edit',
		'cancel_button': 'satellite'
	}
	func = satellite_update_create
	form = None
	available_satellite = Satellite.objects.all()

	if request.method == "POST":
		response = get_post(request, SatelliteForm, 'Satellite',
							reverse_url, func)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = SatelliteForm()

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'available_satellite': available_satellite,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# satellite edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def satellite_edit(request, satellite_id):
	satellite = get_object_or_404(Satellite, pk=satellite_id)
	title = 'Satellite Edit "%s"' % (satellite.name)
	url_name = 'satellite'
	but_name = 'static_data'
	url_form = 'satellite_edit'
	template_name = 'gsi/_satellite_form.html'
	reverse_url = {
		'save_button': 'satellite',
		'save_and_another': 'satellite_add',
		'save_and_continue': 'satellite_edit',
		'cancel_button': 'satellite'
	}
	func = satellite_update_create
	form = None

	if request.method == "POST":
		response = get_post(request, SatelliteForm, 'Satellite',
							reverse_url, func, item_id=satellite_id)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = SatelliteForm(instance=satellite)

	data = {
		'title': title,
		'url_form': url_form,
		'url_name': url_name,
		'but_name': but_name,
		'template_name': template_name,
		'form': form,
		'item_id': satellite_id,
	}

	return data


# InputDataDirectory list
@login_required
@render_to('gsi/input_data_dir_list.html')
def input_data_dir_list(request):
	title = 'Input Data Directory'
	input_data_dirs = InputDataDirectory.objects.all()
	home_var = HomeVariables.objects.all()
	input_data_dir_name = ''
	url_name = 'input_data_dir_list'
	but_name = 'static_data'

	if request.method == "POST" and request.is_ajax():
		data_post = request.POST

		if 'run_id[]' in data_post:
			data = ''
			message = u'Are you sure you want to remove these objects:'
			run_id = data_post.getlist('run_id[]')

			for r in run_id:
				cur_run = get_object_or_404(InputDataDirectory, pk=int(r))
				data += '"' + cur_run.name + '", '

			data = data[:-2]
			data = '<b>' + data + '</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		if 'cur_run_id' in data_post:
			message = u'Are you sure you want to remove this objects:'
			run_id = data_post['cur_run_id']
			cur_run = get_object_or_404(InputDataDirectory, pk=int(run_id))
			data = '<b>"' + cur_run.name + '"</b>'
			data = '{0} {1}?'.format(message, data)

			return HttpResponse(data)
		else:
			data = ''
			return HttpResponse(data)

	if request.method == "POST":
		# if request.POST.get('delete_button'):
		if request.POST.get('input_data_dirs_select'):
			for dir_id in request.POST.getlist('input_data_dirs_select'):
				cur_dir = get_object_or_404(InputDataDirectory, pk=dir_id)
				input_data_dir_name += '"' + cur_dir.name + '", '
				cur_dir.delete()

				dir_path = os.path.join(home_var[0].RF_AUXDATA_DIR, cur_dir.name)
				if os.path.exists(dir_path):
					shutil.rmtree(dir_path)

			input_data_dir_name = input_data_dir_name[:-2]

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('input_data_dir_list'),
										 (u'Input Data Directorys "{0}": deleted.'.format(input_data_dir_name)))
			)
		elif request.POST.get('delete_button'):
			cur_dir = get_object_or_404(InputDataDirectory, pk=request.POST.get('delete_button'))
			input_data_dir_name += '"' + cur_dir.name + '"'
			cur_dir.delete()
			dir_path = os.path.join(home_var[0].RF_AUXDATA_DIR, cur_dir.name)
			if os.path.exists(dir_path):
				shutil.rmtree(dir_path)

			return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('input_data_dir_list'),
										 (u'Input Data Directory "{0}": deleted.'.format(input_data_dir_name)))
				)
		else:
				return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('input_data_dir_list'),
											 (u"To delete, select Directory or more Directorys."))
				)

	# paginations
	model_name = paginations(request, input_data_dirs)

	data = {
		'title': title,
		'input_data_dirs': model_name,
		'model_name': model_name,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# InputDataDirectory add
@login_required
@render_to('gsi/static_data_item_edit.html')
def input_data_dir_add(request):
	title = 'Input Data Directory Add'
	url_form = 'input_data_dir_add'
	url_name = 'input_data_dir_list'
	but_name = 'static_data'
	template_name = 'gsi/_input_data_dir_form.html'
	reverse_url = {
		'save_button': 'input_data_dir_list',
		'save_and_another': 'input_data_dir_add',
		'save_and_continue': 'input_data_dir_edit',
		'cancel_button': 'input_data_dir_list'
	}
	func = data_dir_update_create
	form = None
	available_files = InputDataDirectory.objects.all()

	if request.method == "POST":
		response = get_post(request, InputDataDirectoryForm, 'Input Data Directory',
							reverse_url, func)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = InputDataDirectoryForm()

	data = {
		'title': title,
		'url_form': url_form,
		'template_name': template_name,
		'form': form,
		'available_files': available_files,
		'url_name': url_name,
		'but_name': but_name,
	}

	return data


# InputDataDirectory edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def input_data_dir_edit(request, dir_id):
	data_dir = get_object_or_404(InputDataDirectory, pk=dir_id)
	title = 'Input Data Directory Edit "%s"' % (data_dir.name)
	url_name = 'input_data_dir_list'
	but_name = 'static_data'
	url_form = 'input_data_dir_edit'
	template_name = 'gsi/_input_data_dir_form.html'
	reverse_url = {
		'save_button': 'input_data_dir_list',
		'save_and_another': 'input_data_dir_add',
		'save_and_continue': 'input_data_dir_edit',
		'cancel_button': 'input_data_dir_list'
	}
	func = data_dir_update_create
	form = None

	if request.method == "POST":
		response = get_post(request, InputDataDirectoryForm, 'Input Data Directory',
							reverse_url, func, item_id=dir_id)

		if isinstance(response, HttpResponseRedirect):
			return response
		else:
			form = response
	else:
		form = InputDataDirectoryForm(instance=data_dir)

	data = {
		'title': title,
		'url_form': url_form,
		'url_name': url_name,
		'but_name': but_name,
		'template_name': template_name,
		'form': form,
		'item_id': dir_id,
	}

	return data


# audit history
@login_required
@render_to('gsi/audit_history.html')
def audit_history(request, run_id):
	# Audit record for  MATT_COLLATE_TESTR_29th_Feb
	# get_logs(element, element_id, limit=None, user=None)
	run_base = get_object_or_404(RunBase, pk=run_id)
	title = 'Audit record for "{0}"'.format(run_base.name)
	logs = []

	logs.extend(list(get_logs('RunBase', run_base.id)))
	logs.extend(list(get_logs('Run', run_base.id)))

	data = {
		'title': title,
		'run_id': run_id,
		'logs': logs,
	}

	return data


# def get_files_dirs(url_path, full_path):
# 	dict_dirs = {}
# 	all_dirs = {}
# 	dict_files = {}
# 	all_files = {}
# 	info_message = False
#
# 	try:
# 		root, dirs, files = os.walk(full_path).next()
#
# 		for d in dirs:
# 			date_modification = datetime.fromtimestamp(os.path.getmtime(full_path))
# 			format_date_modification = datetime.strftime(date_modification, "%Y/%m/%d %H:%M:%S")
#
# 			dict_dirs['name'] = d
# 			dict_dirs['date'] = format_date_modification
# 			all_dirs[d] = dict_dirs
# 			dict_dirs = {}
#
# 		for f in files:
# 			kb = 1024.0
# 			mb = 1024.0 * 1024.0
# 			type_file = ''
# 			size_file = ''
# 			file_path = os.path.join(url_path, f)
# 			full_file_path = os.path.join(full_path, f)
# 			size = os.path.getsize(full_file_path)
# 			date_modification = datetime.fromtimestamp(os.path.getmtime(full_file_path))
# 			format_date_modification = datetime.strftime(date_modification, "%Y/%m/%d %H:%M:%S")
# 			mime_type = magic.from_file(full_file_path, mime=True)
# 			type_list = mime_type.split('/')
#
# 			if size < kb:
# 				size_file = "%.2f B" % (size)
#
# 			if size > mb:
# 				size = size / mb
# 				size_file = "%.2f MB" % (size)
#
# 			if size > kb:
# 				size = float(size) / kb
# 				size_file = "%.2f KB" % (size)
#
# 			if type_list[0] == 'image':
# 				type_file = type_list[0]
# 			elif type_list[0] == 'text':
# 				type_file = type_list[0]
# 			elif type_list[0] == 'application':
# 				if type_list[1] == 'pdf':
# 					type_file = type_list[1]
# 				elif type_list[1] == 'msword':
# 					type_file = 'doc'
# 				elif type_list[1] == 'octet-stream':
# 					type_file = 'bin'
# 				else:
# 					type_file = 'archive'
#
# 			dict_files['name'] = f
# 			dict_files['path'] = file_path
# 			dict_files['size'] = size_file
# 			dict_files['date'] = format_date_modification
# 			dict_files['type'] = type_file
#
# 			all_files[f] = dict_files
# 			dict_files = {}
# 			# print 'all_dirs ===================== ', all_files
# 			print '\n\n\n'
# 	except StopIteration, e:
# 		print 'StopIteration ===================== ', e
# 		info_message = True
# 	except OSError, e:
# 		print 'OSError ===================== ', e
# 		info_message = True
#
# 	return all_dirs, all_files, info_message


# view results
@login_required
@render_to('gsi/view_results.html')
def view_results(request, run_id):
	run_base = get_object_or_404(RunBase, pk=run_id)
	title = 'View results "{0}"'.format(run_base.name)
	dir_root = get_dir_root_static_path()
	resolution = run_base.resolution
	folder = run_base.directory_path
	static_dir_root_path = str(dir_root['static_dir_root_path']) + '/' + str(resolution) + '/' + str(folder)
	static_dir_root_path = slash_remove_from_path(static_dir_root_path)
	static_dir_root = str(dir_root['static_dir_root']) + '/' + str(resolution) + '/' + str(folder)
	static_dir_root = slash_remove_from_path(static_dir_root)

	# print 'static_dir_root ============================ ', static_dir_root
	# print 'static_dir_root_path ============================ ', static_dir_root_path

	dirs, files, info_message = get_files_dirs(static_dir_root, static_dir_root_path)

	if info_message:
		info_message = u'For run "{0}" there are no results to show.'.format(run_base.name)

	data = {
		'run_id': run_id,
		'title': title,
		'info_message': info_message,
		'dirs': dirs,
		'files': files,
		'prev_dir': 'd',
	}

	return data


# view results
@login_required
@render_to('gsi/view_results_folder.html')
def view_results_folder(request, run_id, prev_dir, dir):
	run_base = get_object_or_404(RunBase, pk=run_id)
	title = 'View results "{0}"'.format(run_base.name)
	back_prev = ''
	back_cur = ''

	dir_root = get_dir_root_static_path()
	resolution = run_base.resolution
	folder = run_base.directory_path

	static_dir_root_path = str(dir_root['static_dir_root_path']) + '/' + str(resolution) + '/' + str(folder)
	static_dir_root_path = slash_remove_from_path(static_dir_root_path)
	static_dir_root = str(dir_root['static_dir_root']) + '/' + str(resolution) + '/' + str(folder)
	static_dir_root = slash_remove_from_path(static_dir_root)
	static_dir_root_path_folder = static_dir_root_path
	static_dir_root_folder = static_dir_root

	if prev_dir != 'd':
		list_dir = prev_dir.split('%')
		back_prev = '%'.join(list_dir[:-1])
		back_cur = list_dir[-1]
		if len(list_dir) == 1:
			back_prev = 'd'
			back_cur = list_dir[0]
		prev_dir += '%' + dir

		for d in list_dir:
			static_dir_root_path_folder += '/' + d
			static_dir_root_folder += '/' + d

		# for new folder
		static_dir_root_path_folder += '/' + str(dir)
		static_dir_root_path_folder = slash_remove_from_path(static_dir_root_path_folder)
		static_dir_root_folder += '/' + str(dir)
		static_dir_root_folder = slash_remove_from_path(static_dir_root_folder)
	else:
		# for new folder
		prev_dir = dir
		static_dir_root_path_folder = static_dir_root_path + '/' + str(dir)
		static_dir_root_path_folder = slash_remove_from_path(static_dir_root_path_folder)
		static_dir_root_folder = static_dir_root + '/' + str(dir)
		static_dir_root_folder = slash_remove_from_path(static_dir_root_folder)

	dirs, files, info_message = get_files_dirs(static_dir_root_folder, static_dir_root_path_folder)

	if info_message:
		info_message = u'For run "{0}" there are no results to show.'.format(run_base.name)

	data = {
		'run_id': run_id,
		'prev_dir': prev_dir,
		'title': title,
		'info_message': info_message,
		'dirs': dirs,
		'files': files,
		'back_prev': back_prev,
		'back_cur': back_cur
	}

	return data