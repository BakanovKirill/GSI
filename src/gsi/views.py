# -*- coding: utf-8 -*-
from datetime import datetime
import os
import shutil

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.contenttypes.models import ContentType

from gsi.settings import PATH_RUNS_SCRIPTS, CONFIGFILE_PATH, GOOGLE_MAP_ZOOM
from gsi.models import (Run, RunStep, RunBase, Log, OrderedCardItem, HomeVariables,
                        VariablesGroup, YearGroup, Year, Satellite, Area, CardSequence,
                        InputDataDirectory, SubCardItem, Resolution, Tile)
from gsi.gsi_forms import (RunForm, CardSequenceForm, CardSequenceCardForm, CardSequenceCreateForm, HomeVariablesForm,
                            EnvironmentGroupsForm, AreasForm, YearGroupForm, SatelliteForm, UploadFileForm,
                            InputDataDirectoryForm, ConfigFileForm, ResolutionForm, TileForm, YearForm)
from gsi.gsi_update_create import (configfile_update_create, var_group_update_create, area_update_create,
                                        yg_update_create, create_update_card_sequence, satellite_update_create,
                                        data_dir_update_create, resolution_update_create, tile_update_create,
                                        year_update_create)
from cards.models import (QRF, RFScore, Remap, YearFilter, Collate, PreProc, CardItem,
                          MergeCSV, RFTrain, RandomForest, CalcStats, FILTER_OUT, PERIOD)
from cards.cards_forms import (QRFForm, RFScoreForm, RemapForm, YearFilterForm, CollateForm, PreProcForm,
                                MergeCSVForm, RFTrainForm, RandomForestForm, CalcStatsForm)
from cards.card_update_create import (qrf_update_create, rfscore_update_create, remap_update_create,
                                    year_filter_update_create, collate_update_create, preproc_update_create,
                                    mergecsv_update_create, rftrain_update_create, randomforest_update_create,
                                    calcstats_update_create)
from core.utils import (make_run, get_dir_root_static_path, get_path_folder_run, slash_remove_from_path,
                        get_files_dirs, create_sub_dir, get_copy_name, get_files)
from core.get_post import get_post
from core.copy_card import create_copycard
from core.paginations import paginations
from log.logger import get_logs


def handle_uploaded_file(f, path):
    """**Upload file on the server.**

    :Arguments:
        * *f*: File name
        * *path*: Path where to save the file

    """

    with open(path, 'a') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def update_qrf_rftrain_card(cs, cs_cards):
    """**Update the QRF and RFtrain cards.**

    :Functions:
        The method takes the CardSequence model object and list of cards of CardSequence object.
        If the card QRF, it is written to the path of configfile CardSequence object.
        If the card RFtrain, it is written the name of the configfile of the CardSequence object.

    :Arguments:
        * *cs*: The CardSequence object
        * *cs_cards*: List of the cards from the CardSequence object

    """

    from cards.models import QRF, RFTrain

    configfile = cs.configfile
    qrf_directory = str(configfile).split('.cfg')[0]
    rftrain_configfile = '{0}{1}'.format(CONFIGFILE_PATH, configfile)

    for n in cs_cards:
        card_model = n.card_item.content_type.model

        if card_model == 'qrf':
            data_card = QRF.objects.get(name=n.card_item.content_object)
            data_card.directory = qrf_directory
            data_card.save()
        elif card_model == 'rftrain':
            data_card = RFTrain.objects.get(name=n.card_item.content_object)
            data_card.config_file = rftrain_configfile
            data_card.save()


def write_card_to_cs(card_sequence, query):
    """**Update the QRF and RFtrain cards.**

    :Functions:
        Method writes an object CardSequence card objects.

    :Arguments:
        * *card_sequence*: The CardSequence object
        * *query*: request POST

    """

    dict_carditem_order = {}
    carditem_select = query.getlist('carditem_select')
    carditem_order = query.getlist('carditem_order')
    num_card = len(carditem_select)

    for n in xrange(num_card):
        card_item = get_object_or_404(CardItem, pk=int(carditem_select[n]))

        CardSequence.cards.through.objects.create(
            sequence=card_sequence,
            card_item=card_item,
            order=int(carditem_order[n]), )


def copy_runbase(request, name):
    """**Copy the RunBase object.**

    :Functions:
        The method creates a copy of an existing of the RunBase object.

    :Arguments:
        * *name*: The RunBase object name
        * *request:* The request is sent to the server when processing the page

    """

    new_rb = None
    rb = get_object_or_404(RunBase, name=name)
    rb_count = RunBase.objects.all().count()
    copy_name_rb = get_copy_name(name)
    new_name_rb = '{0}*cp{1}'.format(copy_name_rb, rb_count)

    if RunBase.objects.filter(name=new_name_rb).exists():
        try:
            new_name_rb = '{0}_{1}'.format(new_name_rb, 1)
        except ValueError:
            num = int(rb_count) + 1
            new_name_rb = '{0}*cp{1}'.format(new_name_rb, num)

    try:
        new_rb = RunBase.objects.create(
            name=new_name_rb,
            author=request.user,
            description=rb.description,
            purpose=rb.purpose,
            directory_path=rb.directory_path,
            resolution=rb.resolution, )
        new_rb_cs = get_object_or_404(CardSequence, pk=new_rb.card_sequence.id)

        new_rb_cs.environment_base = rb.card_sequence.environment_base
        new_rb_cs.environment_override = rb.card_sequence.environment_override
        new_rb_cs.save()

        new_rb_cs_cards = CardSequence.cards.through.objects.filter(
            sequence_id=new_rb_cs.id)
        card_sequence = CardSequence.objects.get(id=new_rb_cs.id)
        copy_rb_cs_cards = CardSequence.cards.through.objects.filter(
            sequence_id=rb.card_sequence.id)

        for n in copy_rb_cs_cards:
            card_model = n.card_item.content_type.model
            new_copy_card = create_copycard(str(n.card_item), card_model)
            content_type = get_object_or_404(
                ContentType, app_label='cards', model=card_model)
            card_item = get_object_or_404(
                CardItem,
                content_type=content_type,
                object_id=new_copy_card.id)

            CardSequence.cards.through.objects.create(
                sequence=card_sequence,
                card_item=card_item,
                order=n.order, )
    except Exception, e:
        pass

    return new_rb


def get_number_cards(rb, user):
    """**Get the number of cards in the object RunBase.**

    :Functions:
        The method creates a copy of an existing of the CardSequence object.

    :Arguments:
        * *rb*: The RunBase object
        * *user*: Current the user

    """

    num_card = 0
    all_card = OrderedCardItem.objects.filter(sequence__runbase=rb.run_base)

    for card in all_card:
        if card.run_parallel:
            num_card += card.number_sub_cards
        else:
            num_card += 1

    return num_card


@user_passes_test(lambda u: u.is_superuser)
@render_to('gsi/upload_file.html')
def upload_file(request):
    """**View for the "Upload Test Data" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Upload Test Data'
    url_name = 'upload_file'

    try:
        home_var = HomeVariables.objects.all()[0]
    except IndexError:
        home_var = ''

    # Handling POST request
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            if home_var:
                file_name = str(request.FILES['test_data']).decode('utf-8')
                path_test_data = os.path.join(home_var.RF_AUXDATA_DIR,
                                              file_name)
                handle_uploaded_file(request.FILES['test_data'],
                                     path_test_data)

                return HttpResponseRedirect(u'%s?status_message=%s' % (
                    reverse('upload_file'),
                    (u'Test data "{0}" is loaded'.format(file_name))))
            else:
                return HttpResponseRedirect(u'%s?danger_message=%s' % (
                    reverse('index'), (u'Please fill the Home Variables.')))
        else:
            return HttpResponseRedirect(u'%s?danger_message=%s' % (
                reverse('upload_file'), (u'Sorry. Upload error: {0}'.format(
                    form['test_data'].errors.as_text()))))
    else:
        form = UploadFileForm()
    data = {'title': title, 'form': form, 'url_name': url_name}

    return data


@login_required
@render_to('gsi/index.html')
def index(request):
    """**View for the Main page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Main Menu'
    url_name = 'home'
    is_homevar = False

    try:
        home_var = HomeVariables.objects.all()[0]
        if home_var.RF_AUXDATA_DIR:
            is_homevar = True
    except IndexError:
        home_var = ''

    # Handling POST request
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            if home_var:
                file_name = str(request.FILES['test_data']).decode('utf-8')
                path_test_data = os.path.join(home_var.RF_AUXDATA_DIR,
                                              file_name)
                # type_file = str(request.FILES['test_data'].content_type).split('/')[0]
                handle_uploaded_file(request.FILES['test_data'],
                                     path_test_data)

                return HttpResponseRedirect(u'%s?status_message=%s' % (
                    reverse('index'),
                    (u'Test data "{0}" is loaded'.format(file_name))))
            else:
                return HttpResponseRedirect(u'%s?danger_message=%s' % (
                    reverse('index'), (u'Please fill the Home Variables.')))
        else:
            return HttpResponseRedirect(u'%s?danger_message=%s' % (
                reverse('index'), (u'Upload error: {0}'.format(form[
                    'test_data'].errors.as_text()))))
    else:
        form = UploadFileForm()
    data = {'title': title, 'form': form, 'url_name': url_name, 'is_homevar': is_homevar}

    return data


@login_required
@render_to('gsi/run_setup.html')
def run_setup(request):
    """**View for the "Setup New Run" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Run Setup'
    run_bases = RunBase.objects.all().order_by('-date_modified')
    run_name = ''
    url_name = 'run_setup'

    # Sorted by name, author, date_created, date_modified
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')
        if order_by in ('name', 'author', 'date_created', 'date_modified'):
            run_bases = run_bases.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                run_bases = run_bases.reverse()

    # Ajax when deleting objects
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

    # Handling POST request
    if request.method == "POST":
        data_post = request.POST

        if data_post.get('copy_btn'):
            run_bases_current = get_object_or_404(
                RunBase, pk=data_post.get('copy_btn'))
            run_name += '"' + run_bases_current.name + '"'
            new_rb = copy_runbase(request, run_bases_current.name)

            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                'run_setup'
            ), (u'Run the {0} has been successfully copied. Creates a copy of the "{1}".'.
                format(run_name, new_rb.name))))
        elif data_post.get('run_select') and not data_post.get('copy_btn'):
            for run_id in data_post.getlist('run_select'):
                cur_run = get_object_or_404(RunBase, pk=run_id)
                run_name += '"' + cur_run.name + '", '
                rb_cs = get_object_or_404(
                    CardSequence, id=cur_run.card_sequence.id)
                cur_run.delete()
                rb_cs.delete()
            run_name = run_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('run_setup'),
                (u'Run(s): {0} ==> deleted.'.format(run_name))))
        elif data_post.get('delete_button'):
            run_bases_current = get_object_or_404(
                RunBase, pk=data_post.get('delete_button'))
            run_name += '"' + run_bases_current.name + '"'
            rb_cs = get_object_or_404(
                CardSequence, id=run_bases_current.card_sequence.id)
            run_bases_current.delete()
            rb_cs.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('run_setup'),
                (u'Run: {0} ==> deleted.'.format(run_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('run_setup'),
                (u"To delete, select Run or more Runs.")))

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
    """**View for the "New Run" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'New Run'
    form = None
    cards_item = CardItem.objects.all()

    # Handling POST request
    if request.method == "POST":
        form = RunForm(request.POST)

        if form.is_valid():
            if not RunBase.objects.filter(name=form.cleaned_data["name"]).exists():
                new_run_base = RunBase.objects.create(
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    purpose=form.cleaned_data["purpose"],
                    directory_path=form.cleaned_data["directory_path"],
                    resolution=form.cleaned_data["resolution"],
                    author=request.user, )

                path_dir = os.path.join(
                    str(new_run_base.resolution),
                    str(new_run_base.directory_path))
                error_message = create_sub_dir(path_dir)
                card_sequence = new_run_base.card_sequence

                if request.POST.get('save_button') is not None:
                    if request.POST.get('carditem_select'):
                        write_card_to_cs(card_sequence, request.POST)

                    if error_message:
                        return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_setup'),
                                (u'''RunID {0} created successfully.
                                But an error occurred while creating a sub-directory: "{1}"'''.format(new_run_base.id, error_message))))

                    return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_setup'),
                            (u"RunID {0} created successfully".format(new_run_base.id))))
                if request.POST.get('save_update_button') is not None:
                    if request.POST.get('carditem_select'):
                        write_card_to_cs(card_sequence, request.POST)

                    if error_message:
                        return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_update', args=[new_run_base.id]),
                                    (u'''RunID {0} created successfully. You may edit it again below.
                                    But an error occurred while creating a sub-directory: "{1}"'''.format(new_run_base.id, error_message))))

                    return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_update', args=[new_run_base.id]),
                                (u"RunID {0} created successfully. You may edit it again below.".
                                format(new_run_base.id))))
            else:
                return HttpResponseRedirect(u'%s?warning_message=%s' % (
                    reverse('new_run'), (
                        u'Run with the name "{0}" already exists.'.format(
                            form.cleaned_data["name"]))))
    else:
        form = RunForm()

    data = {'title': title, 'form': form, 'cards_item': cards_item}

    return data


@login_required
@render_to('gsi/run_update.html')
def run_update(request, run_id):
    """**View for the "Upload Test Data" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *run_id:* The RunBase object ID

    """

    run_base = get_object_or_404(RunBase, pk=run_id)
    title = 'Edit "{0}"'.format(run_base.name)
    form = None
    cur_run = None

    # Handling POST request
    if request.method == "POST":
        form = RunForm(request.POST)

        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?info_message=%s' % (
                reverse('run_setup'),
                (u"Run {0} updated canceled".format(run_base.name))))
        else:
            if form.is_valid():
                if RunBase.objects.filter(
                        name=form.cleaned_data["name"]).exists():
                    cur_run = RunBase.objects.get(
                        name=form.cleaned_data["name"])

                if cur_run is None or cur_run.id == int(run_id):
                    if request.POST.get('save_button') is not None:
                        run_base.name = form.cleaned_data["name"]
                        run_base.description = form.cleaned_data["description"]
                        run_base.purpose = form.cleaned_data["purpose"]
                        run_base.directory_path = form.cleaned_data[
                            "directory_path"]
                        run_base.resolution = form.cleaned_data["resolution"]
                        run_base.save()

                        path_dir = os.path.join(
                            str(run_base.resolution),
                            str(run_base.directory_path))
                        error_message = create_sub_dir(path_dir)

                        if error_message:
                            return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse('run_setup'),
                                    (u'''Run {0} updated successfully.
                                    But an error occurred while creating a sub-directory: "{1}"'''.format(run_base.name, error_message))))

                        return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('run_setup'),
                                (u"Run {0} updated successfully".format(run_base.name))))
                    if request.POST.get('edit_run_details_button') is not None:
                        return HttpResponseRedirect(u'%s?info_message=%s' % (
                            reverse('card_sequence_update', args=[run_id, run_base.card_sequence.id]), (
                                    u"Edit Card Sequence {0}".format(run_base.card_sequence))))
                else:
                    return HttpResponseRedirect(u'%s?status_message=%s' % (
                        reverse(
                            'run_update', args=[run_id]),
                        (u'Run with the name "{0}" already exists.'.format(
                            form.cleaned_data["name"]))))
    else:
        form = RunForm(instance=run_base)

    data = {'title': title, 'run_base': run_base, 'form': form}

    return data


@login_required
@render_to('gsi/card_sequence_update.html')
def card_sequence_update(request, run_id, cs_id):
    """**View the CardSequence object for editing in the creation of the Run.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

	    * *run_id:* The RunBase object ID

        * *cs_id:* The CardSequence object ID

    """

    home_var = HomeVariables.objects.all()
    rf_auxdata_path = home_var[0].RF_AUXDATA_DIR
    files, error = get_files(rf_auxdata_path, '.cfg')
    card_sequence = get_object_or_404(CardSequence, pk=cs_id)
    card_sequence_cards = CardSequence.cards.through.objects.filter(
        sequence_id=cs_id)
    title = 'Card Sequence {0}'.format(card_sequence.name)
    url_process_card = 'proces_card_sequence_card_edit'
    cs_configfile = card_sequence.configfile
    form = None

    REVERCE_URL = {
        'qrf': ['runid_csid_qrf_add', [run_id, cs_id]],
        'rfscore': ['runid_csid_rfscore_add', [run_id, cs_id]],
        'remap': ['runid_csid_remap_add', [run_id, cs_id]],
        'yearfilter': ['runid_csid_year_filter_add', [run_id, cs_id]],
        'collate': ['runid_csid_collate_add', [run_id, cs_id]],
        'preproc': ['runid_csid_preproc_add', [run_id, cs_id]],
        'mergecsv': ['runid_csid_mergecsv_add', [run_id, cs_id]],
        'rftrain': ['runid_csid_rftrain_add', [run_id, cs_id]],
        'randomforest': ['runid_csid_randomforest_add', [run_id, cs_id]],
        'calcstats': ['runid_csid_calcstats_add', [run_id, cs_id]],
        'cancel': ['card_sequence_update', [run_id, cs_id]]
    }

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            cs_id = data_post.getlist('run_id[]')

            for r in cs_id:
                cur_cs = get_object_or_404(
                    CardSequence.cards.through, pk=int(r))
                data += '"' + str(cur_cs) + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            cs_id = data_post['cur_run_id']
            cur_cs = get_object_or_404(
                CardSequence.cards.through, pk=int(cs_id))
            data = '<b>"' + str(cur_cs) + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        data_post = request.POST
        data_configfile = data_post.get('configfile', '')

        if data_post.get('new_card'):
            new_card = data_post.get('new_card')
            return HttpResponseRedirect(
                reverse(REVERCE_URL[new_card][0], args=REVERCE_URL[new_card][1]))
        elif data_post.get('add_card_items_button') is not None:
            form = CardSequenceCreateForm(data_post, instance=card_sequence)

            if form.is_valid():
                card_sequence = create_update_card_sequence(form, cs_id=cs_id)

                return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                    'card_sequence_update', args=[run_id, card_sequence.id]
                ), (u"The new card item '{0}' was changed successfully. You may edit it again below.".
                    format(card_sequence.name))))
        elif data_post.get('save_and_continue_editing_button') is not None:
            form = CardSequenceCreateForm(data_post, instance=card_sequence)

            if form.is_valid():
                if data_configfile:
                    card_sequence = create_update_card_sequence(
                        form, configfile=data_configfile, cs_id=cs_id)
                    update_qrf_rftrain_card(card_sequence, card_sequence_cards)
                else:
                    card_sequence = create_update_card_sequence(
                        form, cs_id=cs_id)

                return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                    'card_sequence_update', args=[run_id, card_sequence.id]
                ), (u"The new card item '{0}' was update successfully. You may edit it again below.".
                    format(card_sequence.name))))
        elif data_post.get('save_button') is not None:
            form = CardSequenceCreateForm(data_post, instance=card_sequence)

            if form.is_valid():
                if data_configfile:
                    card_sequence = create_update_card_sequence(
                        form, configfile=data_configfile, cs_id=cs_id)
                    update_qrf_rftrain_card(card_sequence, card_sequence_cards)
                else:
                    card_sequence = create_update_card_sequence(
                        form, cs_id=cs_id)

            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                'run_update', args=[run_id]), (
                    u"The card sequence '{0}' update successfully.".format(
                        card_sequence.name))))
        elif data_post.get('delete_button') is not None:
            form = CardSequenceCreateForm(data_post, instance=card_sequence)

            if form.is_valid():
                card_sequence = create_update_card_sequence(form, cs_id=cs_id)

                if data_post.get('cs_select'):
                    cs_name = ''
                    for cs_card_id in data_post.getlist('cs_select'):
                        cur_cs = get_object_or_404(
                            CardSequence.cards.through, pk=cs_card_id)
                        cs_name += '"' + str(cur_cs.card_item) + '", '
                        cur_cs.delete()

                    return HttpResponseRedirect(u'%s?status_message=%s' % (
                        reverse(
                            'card_sequence_update', args=[run_id, cs_id]),
                        (u'Card Items: {0} deleted.'.format(cs_name))))
                else:
                    return HttpResponseRedirect(u'%s?warning_message=%s' % (
                        reverse(
                            'card_sequence_update', args=[run_id, cs_id]),
                        (u"To delete, select Card Item or more Card Items.")))
        elif data_post.get('del_current_btn'):
            card_id = data_post.get('del_current_btn')
            cur_cs = get_object_or_404(CardSequence.cards.through, pk=card_id)
            cs_name = '"' + str(cur_cs.card_item) + '", '
            cur_cs.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse(
                    'card_sequence_update', args=[run_id, cs_id]),
                (u'Card Item: {0} deleted.'.format(cs_name))))
        elif data_post.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?info_message=%s' % (reverse(
                'run_update', args=[run_id]), (
                    u'Card Sequence "{0}" created canceled'.format(
                        card_sequence.name))))
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
        'files': files,
        'cs_configfile': cs_configfile
    }

    return data


# submit a run
@login_required
@render_to('gsi/submit_run.html')
def submit_run(request):
    """**View for the "Submit a Run" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    run_bases = RunBase.objects.all().order_by('-date_modified')
    title = 'Submit a Run'
    name_runs = ''
    url_name = 'submit_run'

    # Sorted by name, author, date_created, date_modified
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')
        if order_by in ('name', 'author', 'date_created', 'date_modified'):
            run_bases = run_bases.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                run_bases = run_bases.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        try:
            if 'cur_run_id' in data_post:
                run_id = data_post['cur_run_id']
                rb = get_object_or_404(RunBase, pk=run_id)
                execute_run = make_run(rb, request.user)

                if not execute_run:
                    data = u'Unable to execute the Run. Please contact the administrator!'
                    return HttpResponse(data)

                if execute_run['error']:
                    data = u'<b>ERROR</b>: {0}'.format(execute_run['error'])
                    return HttpResponse(data)

                num_cards = get_number_cards(execute_run['run'], request.user)
                now_date = datetime.now()
                now_date_formating = now_date.strftime("%d/%m/%Y")
                now_time = now_date.strftime("%H:%M")
                data = u'Run "{0}" has been submitted to back end and {1} on {2}<br>Processed {3} Cards'.\
                 format(rb.name, now_time, now_date_formating, num_cards)

                return HttpResponse(data)
            else:
                data = u"For start choose Run"
                return HttpResponse(data)
        except Exception, e:
            pass

    # paginations
    model_name = paginations(request, run_bases)

    data = {
        'title': title,
        'run_bases': model_name,
        'model_name': model_name,
        'url_name': url_name,
    }

    return data


# run progress
@login_required
@render_to('gsi/run_progress.html')
def run_progress(request):
    """**View for the "View Run Progress" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    runs = Run.objects.all().order_by('-id')
    title = 'Run Progress'
    url_name = 'run_progress'
    run_name = ''

    # Sorted by run_base, id, run_date, state, user
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')
        if order_by in ('run_base', ):
            runs = runs.order_by('run_base__name')

            if request.GET.get('reverse', '') == '1':
                runs = runs.reverse()

        if order_by in ('id', 'run_date', 'state', 'user'):
            runs = runs.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                runs = runs.reverse()

    # Ajax when deleting objects
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

    # Handling POST request
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

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('run_progress'),
                (u'Run(s): {0} ==> deleted.'.format(run_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('run_progress'),
                (u"To delete, select Run or more Runs.")))

    # paginations
    model_name = paginations(request, runs)

    data = {
        'title': title,
        'runs': model_name,
        'url_name': url_name,
        'model_name': model_name,
    }

    return data


# details run
@login_required
@render_to('gsi/run_details.html')
def run_details(request, run_id):
    """**View the details executed of run of the cards.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

	    * *run_id:* The RunStep object ID

    """

    sub_title = 'The View Log file select and hit view'
    runs_step = RunStep.objects.filter(parent_run=run_id)
    runs_step.order_by('card_item__order')
    url_name = 'run_details'

    if runs_step:
        title = 'Run "{0}" Details'.format(runs_step[0].parent_run)
    else:
        title = 'No data to display'

    # Sorted by id, name, order, start_date, state
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')
        if order_by in ('card_item_id', ):
            runs_step = runs_step.order_by('card_item__id')

            if request.GET.get('reverse', '') == '1':
                runs_step = runs_step.reverse()

        if order_by in ('card_item', ):
            runs_step = runs_step.order_by('card_item__card_item__name')

            if request.GET.get('reverse', '') == '1':
                runs_step = runs_step.reverse()

        if order_by in ('order', ):
            runs_step = runs_step.order_by('card_item__order')

            if request.GET.get('reverse', '') == '1':
                runs_step = runs_step.reverse()

        if order_by in ('start_date', 'state'):
            runs_step = runs_step.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                runs_step = runs_step.reverse()

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('details_file'):
            step = get_object_or_404(
                RunStep, pk=request.POST.get('details_file'))

            if request.POST.get('out_button', ''):
                return HttpResponseRedirect(u'%s?status_message=%s' % (
                    reverse(
                        'view_log_file',
                        args=[run_id, step.card_item.id, 'Out']),
                    (u'Log Out file for the Card "{0}".'.format(step.card_item)
                     )))
            elif request.POST.get('err_button', ''):
                return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                    'view_log_file',
                    args=[run_id, step.card_item.id, 'Error']), (
                        u'Log Error file for the Card "{0}".'.format(
                            step.card_item))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (reverse(
                'run_details',
                args=[run_id]), (u"To view the Card Log, select Card.")))

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
def view_log_file(request, run_id, card_id, status):
    """**View details of the files *.err and *.out  of the cards.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

	    * *run_id:* The RunStep object ID

        * *card_id:* The Card object ID

        * *status:* Status executed to work of the cards

    """

    log_info = ''
    run = get_object_or_404(Run, pk=run_id)
    runs_step = RunStep.objects.filter(parent_run=run_id).first()
    run_step_card = RunStep.objects.filter(card_item__id=card_id).first()

    title = 'Log {0} file for the Card Item "{1}"'.format(status, run)
    sub_title = 'The View Log file select and hit view'

    try:
        log = get_object_or_404(Log, pk=run.log.id)
        log_path = log.log_file_path
    except Exception:
        log_name = '{}_{}.log'.format(run.id, run_step_card.card_item.id)
        log_path = get_path_folder_run(run)
        log = Log.objects.create(
            name=log_name, log_file=log_name, log_file_path=log_path)
        run.log = log
        run.save()

    if status == 'Out':
        try:
            card_name = 'runcard_{0}.out'.format(card_id)
            path_log_file = os.path.join(str(log_path), str(card_name))
            fd = open(path_log_file, 'r')
            for line in fd.readlines():
                log_info += line + '<br />'
        except Exception, e:
            return HttpResponseRedirect(u'%s?danger_message=%s' % (
                reverse('run_details', args=[run_id]),
                    (u'Log Out file "{0}" not found.'.format(card_name))))
    elif status == 'Error':
        try:
            card_name = 'runcard_{0}.err'.format(card_id)
            path_log_file = os.path.join(str(log_path), str(card_name))
            fd = open(path_log_file, 'r')
            for line in fd.readlines():
                log_info += line + '<br />'
        except Exception, e:
            return HttpResponseRedirect(u'%s?danger_message=%s' % (
                reverse('run_details', args=[run_id]),
                    (u'Log Error file "{0}" not found.'.format(card_name))))

    data = {
        'title': title,
        'run_id': run_id,
        'card_id': card_id,
        'log_info': log_info,
    }

    return data


# view out/error log files for cards
@login_required
@render_to('gsi/view_log_file_sub_card.html')
def view_log_file_sub_card(request, run_id, card_id, count, status):
    """**View details of the files *.err and *.out  of the sub-cards.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

	    * *run_id:* The RunStep object ID

        * *card_id:* The Card object ID

        * *count:* The number of sub-cards

        * *status:* Status executed to work of the cards

    """

    log_info = ''
    runs_step = RunStep.objects.filter(parent_run=run_id).first()
    run_step_card = RunStep.objects.filter(card_item__id=card_id).first()

    title = 'Log {0} file for the Sub Card "{1}"'.format(
        status, run_step_card.card_item)
    sub_title = 'The View Log file select and hit view'

    run = get_object_or_404(Run, pk=run_id)

    try:
        log = get_object_or_404(Log, pk=run.log.id)
        log_path = log.log_file_path
    except Exception:
        log_name = '{}_{}.log'.format(run.id, run_step_card.card_item.id)
        log_path = get_path_folder_run(run)
        log = Log.objects.create(
            name=log_name, log_file=log_name, log_file_path=log_path)
        run.log = log
        run.save()

    if status == 'Out':
        card_name = 'runcard_{0}_{1}.out'.format(card_id, count)
        path_log_file = os.path.join(str(log_path), str(card_name))
        try:
            fd = open(path_log_file, 'r')
            for line in fd.readlines():
                log_info += line + '<br />'
        except Exception, e:
            print 'ERROR Out view_log_file_sub_card: ', e
            return HttpResponseRedirect(u'%s?danger_message=%s' % (
                reverse(
                    'sub_card_details', args=[run_id, card_id]),
                (u'Log Out file "{0}" not found.'.format(card_name))))
    elif status == 'Error':
        card_name = 'runcard_{0}_{1}.err'.format(card_id, count)
        path_log_file = os.path.join(str(log_path), str(card_name))
        try:
            fd = open(path_log_file, 'r')
            for line in fd.readlines():
                log_info += line + '<br />'
        except Exception, e:
            print 'ERROR Error view_log_file_sub_card: ', e
            return HttpResponseRedirect(u'%s?danger_message=%s' % (
                reverse(
                    'sub_card_details', args=[run_id, card_id]),
                (u'Log Error file "{0}" not found.'.format(card_name))))

    data = {
        'title': title,
        'run_id': run_id,
        'card_id': card_id,
        'log_info': log_info,
    }

    return data


# details parallel card of run
@login_required
@render_to('gsi/sub_card_details.html')
def sub_card_details(request, run_id, card_id):
    """**View the details executed of run of the cards.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

	    * *run_id:* The RunStep object ID

        * *card_id:* The CardItem object ID

    """

    url_name = 'sub_card_details'
    sub_cards = SubCardItem.objects.filter(run_id=run_id, card_id=card_id)
    sub_cards.order_by('sub_cards.start_time')
    # runs_step = RunStep.objects.filter(parent_run=run_id).first()
    run_step_card = RunStep.objects.filter(card_item__id=card_id).first()
    title = 'Sub Cards of Card "{0}" Details'.format(run_step_card.card_item)
    sub_title = 'The View Log file select and hit view'

    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'start_date', 'start_time', 'state'):
            sub_cards = sub_cards.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                sub_cards = sub_cards.reverse()

    if request.method == "POST":
        if request.POST.get('details_file'):

            if request.POST.get('err_button', ''):
                log_err = request.POST.get('details_file')
                count = log_err.split('_')[1]
                return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                    'view_log_file_sub_card',
                    args=[run_id, card_id, count, 'Error']), (
                        u'Log Error file for the Card "{0}".'.format(
                            run_step_card.card_item))))
            elif request.POST.get('out_button', ''):
                log_err = request.POST.get('details_file')
                count = log_err.split('_')[1]
                return HttpResponseRedirect(u'%s?status_message=%s' % (reverse(
                    'view_log_file_sub_card',
                    args=[run_id, card_id, count, 'Out']), (
                        u'Log Out file for the Card "{0}".'.format(
                            run_step_card.card_item))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse(
                    'sub_card_details', args=[run_id, card_id]),
                (u"To view the Card Log, select Card.")))

    # paginations
    model_name = paginations(request, sub_cards)

    data = {
        'title': title,
        'sub_title': sub_title,
        'run_id': run_id,
        'card_id': card_id,
        'sub_cards': model_name,
        'card_name': run_step_card.card_item,
        'model_name': model_name,
        'url_name': url_name,
        'obj_id': run_id,
    }

    return data


# setup home variable
@login_required
@render_to('gsi/home_variable_setup.html')
def home_variable_setup(request):
    """**View for the "Home Variables Setup" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Home Variables'
    form = None
    url_name = 'home_variable'
    but_name = 'static_data'

    try:
        variables = HomeVariables.objects.get(pk=1)
    except HomeVariables.DoesNotExist:
        variables = ''

    # Handling POST request
    if request.method == "POST":
        form = HomeVariablesForm(request.POST)

        if form.is_valid():
            if variables:
                variables.SAT_TIF_DIR_ROOT = form.cleaned_data["SAT_TIF_DIR_ROOT"]
                variables.RF_DIR_ROOT = form.cleaned_data["RF_DIR_ROOT"]
                variables.USER_DATA_DIR_ROOT = form.cleaned_data["USER_DATA_DIR_ROOT"]
                variables.MODIS_DIR_ROOT = form.cleaned_data["MODIS_DIR_ROOT"]
                variables.RF_AUXDATA_DIR = form.cleaned_data["RF_AUXDATA_DIR"]
                variables.SAT_DIF_DIR_ROOT = form.cleaned_data["SAT_DIF_DIR_ROOT"]
                variables.save()
            else:
                variables = HomeVariables.objects.create(
                        SAT_TIF_DIR_ROOT = form.cleaned_data["SAT_TIF_DIR_ROOT"],
                        RF_DIR_ROOT = form.cleaned_data["RF_DIR_ROOT"],
                        USER_DATA_DIR_ROOT = form.cleaned_data["USER_DATA_DIR_ROOT"],
                        MODIS_DIR_ROOT = form.cleaned_data["MODIS_DIR_ROOT"],
                        RF_AUXDATA_DIR = form.cleaned_data["RF_AUXDATA_DIR"],
                        SAT_DIF_DIR_ROOT = form.cleaned_data["SAT_DIF_DIR_ROOT"]
                    )

            if request.POST.get('save_button') is not None:
                return HttpResponseRedirect(u'%s?status_message=%s' % (
                    reverse('home_variable_setup'),
                    (u"Home variables successfully updated")))
            if request.POST.get('save_and_continue_button') is not None:
                return HttpResponseRedirect(u'%s?status_message=%s' % (
                    reverse('home_variable_setup'),
                    (u"Home variables successfully updated")))
    else:
        if variables:
            form = HomeVariablesForm(instance=variables)
        else:
            form = HomeVariablesForm()

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
    """**View for the "Environment Groups" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Environment Groups'
    environments = VariablesGroup.objects.all()
    env_name = ''
    url_name = 'environment_groups'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            environments = environments.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                environments = environments.reverse()

    # Ajax when deleting objects
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

    # Handling POST request
    if request.method == "POST":
        # if request.POST.get('delete_button'):
        if request.POST.get('env_select'):
            for env_id in request.POST.getlist('env_select'):
                cur_env = get_object_or_404(VariablesGroup, pk=env_id)
                env_name += '"' + str(cur_env.name) + '", '
                cur_env.delete()

            envs_ids = '_'.join(request.POST.getlist('env_select'))
            env_name = env_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('environment_groups'), (
                    u'Environment Groups: {0} ==> deleted.'.format(env_name))))
        elif request.POST.get('delete_button'):
            cur_env = get_object_or_404(
                VariablesGroup, pk=request.POST.get('delete_button'))
            env_name += '"' + str(cur_env.name) + '", '
            cur_env.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('environment_groups'), (
                    u'Environment Group: {0} ==> deleted.'.format(env_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('environment_groups'),
                (u"To delete, select Group or more Groups.")))

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
    """**View for the "Environment Group Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

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

    # Handling POST request
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
    """**View for the "Environment Group "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *env_id:* The VariablesGroup object ID

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            EnvironmentGroupsForm,
            'Environment Group',
            reverse_url,
            func,
            item_id=env_id)

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
    """**View for the "Areas" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Areas'
    areas = Area.objects.all()
    area_name = ''
    url_name = 'areas'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            areas = areas.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                areas = areas.reverse()

    # Ajax when deleting objects
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

    # Handling POST request
    if request.method == "POST":
        # if request.POST.get('delete_button'):
        if request.POST.get('area_select'):
            for area_id in request.POST.getlist('area_select'):
                cur_area = get_object_or_404(Area, pk=area_id)
                area_name += '"' + cur_area.name + '", '
                cur_area.delete()

            area_ids = '_'.join(request.POST.getlist('env_select'))

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('areas'),
                (u'Areas: {0} ==> deleted.'.format(area_name))))
        elif request.POST.get('delete_button'):
            cur_area = get_object_or_404(
                Area, pk=request.POST.get('delete_button'))
            area_name += '"' + cur_area.name + '", '
            cur_area.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('areas'),
                (u'Areas: {0} ==> deleted.'.format(area_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('areas'), (u"To delete, select Area or more Areas.")))

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
    """**View for the "Area Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, AreasForm, 'Area', reverse_url, func)

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
    """**View for the "Area "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *area_id:* The Area object ID

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request, AreasForm, 'Area', reverse_url, func, item_id=area_id)

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


# years_group
@login_required
@render_to('gsi/years_group_list.html')
def years_group(request):
    """**View for the "Years Groups" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Years Groups'
    years_groups = YearGroup.objects.all()
    yg_name = ''
    url_name = 'years_group'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            years_groups = years_groups.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                years_groups = years_groups.reverse()

    # Ajax when deleting objects
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

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('yg_select'):
            for yg_id in request.POST.getlist('yg_select'):
                cur_yg = get_object_or_404(YearGroup, pk=yg_id)
                yg_name += '"' + cur_yg.name + '", '
                cur_yg.delete()
            yg_name = yg_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('years_group'),
                (u'Years Groups: {0} ==> deleted.'.format(yg_name))))
        elif request.POST.get('delete_button'):
            cur_yg = get_object_or_404(
                YearGroup, pk=request.POST.get('delete_button'))
            yg_name += '"' + cur_yg.name + '"'
            cur_yg.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('years_group'),
                (u'Years Group: {0} ==> deleted.'.format(yg_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('years_group'),
                (u"To delete, select Years Group or more Years Groups.")))

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
    """**View for the "Years Group Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, YearGroupForm, 'Year Group', reverse_url,
                            func)

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
    """**View for the "Years Group "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *yg_id:* The YearGroup object ID

    """

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
    available_years = Year.objects.exclude(
        id__in=years_group.years.values_list(
            'id', flat=True))

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            YearGroupForm,
            'Year Group',
            reverse_url,
            func,
            item_id=yg_id)

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
    """**View for the "Satellite" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Satellites'
    satellites = Satellite.objects.all()
    satellite_name = ''
    url_name = 'satellite'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            satellites = satellites.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                satellites = satellites.reverse()

    # Ajax when deleting objects
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

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('satellite_select'):
            for satellite_id in request.POST.getlist('satellite_select'):
                cur_satellite = get_object_or_404(Satellite, pk=satellite_id)
                satellite_name += '"' + cur_satellite.name + '", '
                cur_satellite.delete()

            satellite_name = satellite_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('satellite'),
                (u'Satellites: {0} ==> deleted.'.format(satellite_name))))
        elif request.POST.get('delete_button'):
            cur_satellite = get_object_or_404(
                Satellite, pk=request.POST.get('delete_button'))
            satellite_name += '"' + cur_satellite.name + '"'
            cur_satellite.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('satellite'),
                (u'Satellite: {0} ==> deleted.'.format(satellite_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('satellite'),
                (u"To delete, select Satellite or more Satellites.")))

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
    """**View for the "Satellites Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, SatelliteForm, 'Satellite', reverse_url,
                            func)

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
    """**View for the "Satellite Edit '<name>' page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *satellite_id:* The Satellite object ID

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            SatelliteForm,
            'Satellite',
            reverse_url,
            func,
            item_id=satellite_id)

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
    """**View for the "Input Data Directory" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Input Data Directory'
    input_data_dirs = InputDataDirectory.objects.all()
    home_var = HomeVariables.objects.all()
    input_data_dir_name = ''
    url_name = 'input_data_dir_list'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            input_data_dirs = input_data_dirs.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                input_data_dirs = input_data_dirs.reverse()

    # Ajax when deleting objects
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

    # Handling POST reques
    if request.method == "POST":
        # if request.POST.get('delete_button'):
        if request.POST.get('input_data_dirs_select'):
            for dir_id in request.POST.getlist('input_data_dirs_select'):
                cur_dir = get_object_or_404(InputDataDirectory, pk=dir_id)
                input_data_dir_name += '"' + cur_dir.name + '", '
                cur_dir.delete()

                dir_path = os.path.join(home_var[0].RF_AUXDATA_DIR,
                                        cur_dir.name)
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)

            input_data_dir_name = input_data_dir_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('input_data_dir_list'), (
                    u'Input Data Directorys "{0}": deleted.'.format(
                        input_data_dir_name))))
        elif request.POST.get('delete_button'):
            cur_dir = get_object_or_404(
                InputDataDirectory, pk=request.POST.get('delete_button'))
            input_data_dir_name += '"' + cur_dir.name + '"'
            cur_dir.delete()
            dir_path = os.path.join(home_var[0].RF_AUXDATA_DIR, cur_dir.name)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('input_data_dir_list'), (
                    u'Input Data Directory "{0}": deleted.'.format(
                        input_data_dir_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('input_data_dir_list'),
                (u"To delete, select Directory or more Directorys.")))

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
    """**View for the "Input Data Directory Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, InputDataDirectoryForm,
                            'Input Data Directory', reverse_url, func)

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
    """**View for the "Input Data Directory Edit "<name>"" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *dir_id:* The InputDataDirectory object ID

    """

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

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            InputDataDirectoryForm,
            'Input Data Directory',
            reverse_url,
            func,
            item_id=dir_id)

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


# Cards List
@login_required
@render_to('gsi/cards_list.html')
def cards_list(request, *args, **kwargs):
    """**View for the "Cards List" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Cards List'
    cards_all = CardItem.objects.all()
    card_list = []
    cards_name = ''
    url_name = 'cards_list'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'content_type__model'):
            cards_all = cards_all.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                cards_all = cards_all.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            card_id = data_post.getlist('run_id[]')

            for c in card_id:
                cur_card = get_object_or_404(CardItem, pk=int(c))
                data += '"' + str(cur_card) + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            card_id = data_post['cur_run_id']
            cur_card = get_object_or_404(CardItem, pk=int(card_id))
            data = '<b>"' + str(cur_card) + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('card_select'):
            for card_id in request.POST.getlist('card_select'):
                cur_card = get_object_or_404(CardItem, pk=card_id)
                cards_name += '"' + str(cur_card) + '", '
                content_type_card = ContentType.objects.get(
                    id=cur_card.content_type_id)
                class_obj = content_type_card.get_object_for_this_type(
                    name=str(cur_card))
                cur_card.delete()
                class_obj.delete()

            cards_name = cards_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('cards_list'), (u'Cards: {0} ==> deleted.'.format(cards_name))))
        elif request.POST.get('delete_button'):
            cur_card = get_object_or_404(
                CardItem, pk=request.POST.get('delete_button'))
            cards_name += '"' + str(cur_card) + '"'
            content_type_card = ContentType.objects.get(
                id=cur_card.content_type_id)
            class_obj = content_type_card.get_object_for_this_type(
                name=str(cur_card))
            cur_card.delete()
            class_obj.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('cards_list'),
                (u'Card: {0} deleted.'.format(cards_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('cards_list'),
                (u"To delete, select Card or more Cards.")))

    # paginations
    model_name = paginations(request, cards_all)

    data = {
        'title': title,
        'cards': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# audit history
@login_required
@render_to('gsi/audit_history.html')
def audit_history(request, run_id):
    """**View for the "Audit record for '<name>'" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *run_id:* The RunBase object

    """

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


# view results
@login_required
@render_to('gsi/view_results.html')
def view_results(request, run_id):
    """**View for the "View results '<name>'" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *run_id:* The RunBase object ID

    """

    run_base = get_object_or_404(RunBase, pk=run_id)
    title = 'View results "{0}"'.format(run_base.name)
    dir_root = get_dir_root_static_path()
    resolution = run_base.resolution
    folder = run_base.directory_path
    static_dir_root_path = str(dir_root['static_dir_root_path']) + '/' + str(
        resolution) + '/' + str(folder)
    static_dir_root_path = slash_remove_from_path(static_dir_root_path)
    static_dir_root = str(dir_root['static_dir_root']) + '/' + str(
        resolution) + '/' + str(folder)
    static_dir_root = slash_remove_from_path(static_dir_root)

    dirs, files, info_message = get_files_dirs(static_dir_root,
                                               static_dir_root_path)

    if info_message:
        info_message = u'For run "{0}" there are no results to show.'.format(
            run_base.name)

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
    """**View for the "View results '<name>'" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *run_id:* The RunBase object ID

        * *prev_dir:* The prev directory

        * *dir:* The current directory

    """

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


# Resolution list
@login_required
@render_to('gsi/resolution_list.html')
def resolution(request):
    """**View for the "Resolutions" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Resolutions'
    resolution = Resolution.objects.all()
    resolution_name = ''
    url_name = 'resolution'
    but_name = 'static_data'

    # Sorted by name, value
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'value'):
            resolution = resolution.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                resolution = resolution.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(Resolution, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(Resolution, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('resolution_select'):
            for satellite_id in request.POST.getlist('resolution_select'):
                cur_resolution = get_object_or_404(Resolution, pk=satellite_id)
                resolution_name += '"' + cur_resolution.name + '", '
                cur_resolution.delete()

            resolution_name = resolution_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('resolution'),
                (u'Resolutions "{0}" deleted.'.format(resolution_name))))
        elif request.POST.get('delete_button'):
            cur_resolution = get_object_or_404(
                Resolution, pk=request.POST.get('delete_button'))
            resolution_name += '"' + cur_resolution.name + '"'
            cur_resolution.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('resolution'),
                (u'Resolution "{0}" deleted.'.format(resolution_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('resolution'),
                (u"To delete, select Resolution or more Resolutions.")))

    # paginations
    model_name = paginations(request, resolution)

    data = {
        'title': title,
        'resolutions': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# Resolution add
@login_required
@render_to('gsi/static_data_item_edit.html')
def resolution_add(request):
    """**View for the 'Resolution Add' page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Resolution Add'
    url_form = 'resolution_add'
    url_name = 'resolution'
    but_name = 'static_data'
    template_name = 'gsi/_resolution_form.html'
    reverse_url = {
        'save_button': 'resolution',
        'save_and_another': 'resolution_add',
        'save_and_continue': 'resolution_edit',
        'cancel_button': 'resolution'
    }
    func = resolution_update_create
    form = None
    available_resolution = Resolution.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, ResolutionForm, 'Resolution', reverse_url,
                            func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ResolutionForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_resolution': available_resolution,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# Resolution edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def resolution_edit(request, resolution_id):
    """**View for the "Resolution Edit '<name>'" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *resolution_id:* The Resolution object ID

    """

    resolution = get_object_or_404(Resolution, pk=resolution_id)
    title = 'Resolution Edit "%s"' % (resolution.name)
    url_name = 'resolution'
    but_name = 'static_data'
    url_form = 'resolution_edit'
    template_name = 'gsi/_resolution_form.html'
    reverse_url = {
        'save_button': 'resolution',
        'save_and_another': 'resolution_add',
        'save_and_continue': 'resolution_edit',
        'cancel_button': 'resolution'
    }
    func = resolution_update_create
    form = None

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            ResolutionForm,
            'Resolution',
            reverse_url,
            func,
            item_id=resolution_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ResolutionForm(instance=resolution)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': resolution_id,
    }

    return data


# Tiles list
@login_required
@render_to('gsi/tiles_list.html')
def tiles(request):
    """**View for the "Tiles" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Tiles'
    tile = Tile.objects.all()
    tile_name = ''
    url_name = 'tiles'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name',):
            tile = tile.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                tile = tile.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(Tile, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(Tile, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('tile_select'):
            for tile_id in request.POST.getlist('tile_select'):
                cur_tile = get_object_or_404(Tile, pk=tile_id)
                tile_name += '"' + cur_tile.name + '", '
                cur_tile.delete()

            tile_name = tile_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('tiles'),
                (u'Tiles "{0}" deleted.'.format(tile_name))))
        elif request.POST.get('delete_button'):
            cur_tile = get_object_or_404(
                Tile, pk=request.POST.get('delete_button'))
            tile_name += '"' + cur_tile.name + '"'
            cur_tile.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('tiles'),
                (u'Tile "{0}" deleted.'.format(tile_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('tiles'),
                (u"To delete, select Tile or more Tiles.")))

    # paginations
    model_name = paginations(request, tile)

    data = {
        'title': title,
        'tiles': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# Tiles add
@login_required
@render_to('gsi/static_data_item_edit.html')
def tile_add(request):
    """**View for the "Tile Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Tile Add'
    url_form = 'tile_add'
    url_name = 'tiles'
    but_name = 'static_data'
    template_name = 'gsi/_tile_form.html'
    reverse_url = {
        'save_button': 'tiles',
        'save_and_another': 'tile_add',
        'save_and_continue': 'tile_edit',
        'cancel_button': 'tiles'
    }
    func = tile_update_create
    form = None
    available_tiles = Tile.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, TileForm, 'Tile', reverse_url,
                            func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = TileForm()

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


# Tiles edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def tile_edit(request, tile_id):
    """**View for the "Tile Edit '<name>'" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *tile_id:* The Tile object ID

    """

    tile = get_object_or_404(Tile, pk=tile_id)
    title = 'Tile Edit "%s"' % (tile.name)
    url_name = 'tiles'
    but_name = 'static_data'
    url_form = 'tile_edit'
    template_name = 'gsi/_tile_form.html'
    reverse_url = {
        'save_button': 'tiles',
        'save_and_another': 'tile_add',
        'save_and_continue': 'tile_edit',
        'cancel_button': 'tiles'
    }
    func = tile_update_create
    form = None

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            TileForm,
            'Tile',
            reverse_url,
            func,
            item_id=tile_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = TileForm(instance=tile)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': tile_id,
    }

    return data


# Years list
@login_required
@render_to('gsi/years_list.html')
def years(request):
    """**View for the "Years" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Years'
    years = Year.objects.all().order_by('name')
    year_name = ''
    url_name = 'years'
    but_name = 'static_data'

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name',):
            years = years.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                years = years.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(Year, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(Year, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('year_select'):
            for year_id in request.POST.getlist('year_select'):
                cur_year = get_object_or_404(Year, pk=year_id)
                year_name += '"' + cur_year.name + '", '
                cur_year.delete()

            year_name = year_name[:-2]

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('years'),
                (u'Tiles "{0}" deleted.'.format(year_name))))
        elif request.POST.get('delete_button'):
            cur_year = get_object_or_404(
                Year, pk=request.POST.get('delete_button'))
            year_name += '"' + cur_year.name + '"'
            cur_year.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('years'),
                (u'Year "{0}" deleted.'.format(year_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('years'),
                (u"To delete, select Year or more Years.")))

    # paginations
    model_name = paginations(request, years)

    data = {
        'title': title,
        'years': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# Year add
@login_required
@render_to('gsi/static_data_item_edit.html')
def year_add(request):
    """**View for the "Year Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Year Add'
    url_form = 'year_add'
    url_name = 'years'
    but_name = 'static_data'
    template_name = 'gsi/_year_form.html'
    reverse_url = {
        'save_button': 'years',
        'save_and_another': 'year_add',
        'save_and_continue': 'year_edit',
        'cancel_button': 'years'
    }
    func = year_update_create
    form = None
    available_years = Year.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, YearForm, 'Year', reverse_url,
                            func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = YearForm()

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


# Year edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def year_edit(request, year_id):
    """**View for the "Year Edit '<name>'" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

        * *year_id:* The Year object ID

    """

    year = get_object_or_404(Year, pk=year_id)
    title = 'Year Edit "%s"' % (year.name)
    url_name = 'years'
    but_name = 'static_data'
    url_form = 'year_edit'
    template_name = 'gsi/_year_form.html'
    reverse_url = {
        'save_button': 'years',
        'save_and_another': 'year_add',
        'save_and_continue': 'year_edit',
        'cancel_button': 'years'
    }
    func = year_update_create
    form = None

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            YearForm,
            'Year',
            reverse_url,
            func,
            item_id=year_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = YearForm(instance=year)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': year_id,
    }

    return data


# view Customer section
@login_required
@render_to('gsi/customer_section.html')
def customer_section(request):
    """**View for the "Customer '<user>' section" page.**

    :Functions:
        When you load the page is loaded map with Google MAP. Initial coordinates: eLat = 0, eLng = 0.
        Zoom map is variable GOOGLE_MAP_ZOOM, whose value is in the project settings.
        Code view allows to change position when you enter values in the fields on the page "Enter Lat" and "Enter Log".

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    customer = request.user
    title = 'Customer {0} section'.format(customer)
    url_name = 'customer_section'
    eLat = 0
    eLng = 0

    # Handling POST request
    if request.method == "POST":
        data_request = request.POST

        if data_request.get('eLat', ''):
            eLat = data_request.get('eLat', '')

        if data_request.get('eLng', ''):
            eLng = data_request.get('eLng', '')


    data = {
        'title': title,
        'customer': customer,
        'url_name': url_name,
        'eLat': eLat,
        'eLng': eLng,
        'GOOGLE_MAP_ZOOM': GOOGLE_MAP_ZOOM
    }

    return data
