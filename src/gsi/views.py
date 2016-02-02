# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.conf import settings

# from gsi.models import RunBase, Resolution, CardSequence, OrderedCardItem
# from cards.models import CardItem
from gsi.gsi_forms import *

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
