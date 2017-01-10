# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType


def cs_cards_update(form, cs_card, card_item):
    """**The method updates the value of the cards in CardSequence object.**

    :Arguments:
        * *form*: The form object
        * *cs_card*: The OrderedCardItem object
        * *card_item*: The Card object

    """

    cs_card.order = form.cleaned_data["order"]
    cs_card.card_item = card_item
    cs_card.save()

    return cs_card


def add_card_in_cardsequence(card, cs_id):
    """**The method added the new Card object and its order in the CardSequence object.**

    :Arguments:
        * *card*: The Card object
        * *cs_id*: The CardSequence object ID

    """

    from gsi.models import CardSequence
    from cards.models import CardItem

    order_num = 0

    try:
        card_model = ContentType.objects.get_for_model(card.__class__).model
        content_type = get_object_or_404(ContentType, app_label='cards', model=card_model)
        cs = get_object_or_404(CardSequence, pk=cs_id)
        card_item = get_object_or_404(
                CardItem,
                content_type=content_type,
                object_id=card.id
        )
        cs_all = CardSequence.cards.through.objects.filter(
                    sequence=cs,
                ).count()

        if cs_all:
            order_num = cs_all

        CardSequence.cards.through.objects.create(
            order=order_num,
            sequence=cs,
            card_item=card_item,
        )
    except Exception, e:
        pass


def get_post(request, item_form, item, reverse_ulr, func, args=False, item_id=None, cs_form=False, cs_id=None):
    """**The method processes the POST request and sends a response from the server.**

    :Arguments:
        * *request*: The request to the server
        * *item_form*: The Card form
        * *item*: The Card object
        * *reverse_ulr*: The URL redirection
        * *func*: The function to create or update Card
        * *args*: Additional options: Run ID, CardSequence ID, Card ID
        * *item_id*: The Card object ID (if the object is created the value default "None")
        * *cs_form*: If an object is created or updated in CardSequence object, the value is "True". Default is "False"
        * *cs_id*: If an object is created or updated in CardSequence object, the value is CardSequence object ID. Default is "None"

    """

    response = None

    # process the POST request by pressing a button "Save"
    if request.POST.get('save_button') is not None:
        form_1 = item_form(request.POST)

        if cs_form:
            form_2 = cs_form[0](request.POST)

        if form_1.is_valid():
            if item_id:
                if request.POST.getlist('available'):
                    multiple = '_'.join(request.POST.getlist('available'))
                    obj = func(form_1, multiple=multiple, item_id=item_id)
                else:
                    obj = func(form_1, item_id=item_id)
                if obj == None:
                    return None
            else:
                if request.POST.getlist('available'):
                    multiple = '_'.join(request.POST.getlist('available'))
                    obj = func(form_1, multiple=multiple)
                else:
                    obj = func(form_1)
                    add_card_in_cardsequence(obj, cs_id)
                if obj == None:
                    return None

            if cs_form:
                if form_2.is_valid():
                    cs_obj = cs_cards_update(form_2, cs_form[1], cs_form[2])

            if args:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button'][0],
                                                       args=reverse_ulr['save_button'][1]),
                    (u'The {0} "{1}" was edited.'.format(item, obj)))
                )
            else:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button']),
                    (u'The {0} "{1}" created successfully.'.format(item, obj)))
                )
        else:
            return form_1
    # process the POST request by pressing a button "Save and create another object"
    elif request.POST.get('save_and_another_button') is not None:
        form_1 = item_form(request.POST)

        if form_1.is_valid():
            if item_id:
                if request.POST.getlist('available'):
                    multiple = '_'.join(request.POST.getlist('available'))
                    obj = func(form_1, multiple=multiple, item_id=item_id)
                else:
                    obj = func(form_1, item_id=item_id)

                if obj == None:
                    return None
            else:
                if request.POST.getlist('available'):
                    multiple = '_'.join(request.POST.getlist('available'))
                    obj = func(form_1, multiple=multiple)
                    add_card_in_cardsequence(obj, cs_id)
                else:
                    obj = func(form_1)
                    add_card_in_cardsequence(obj, cs_id)
                if obj == None:
                    return None

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another'][0],
                                                           args=reverse_ulr['save_and_another'][1]),
                        (u'The {0} "{1}" was added successfully. \
                        You may add another {2} below'.format(item, obj, item)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another']),
                        (u'The {0} "{1}" was added successfully. \
                        You may add another {2} below'.format(item, obj, item)))
                )
        else:
            return form_1
    # process the POST request by pressing a button "Delete"
    elif request.POST.get('delete_button') is not None:
        form_1 = item_form(request.POST)

        if form_1.is_valid():
            if item_id:
                if request.POST.getlist('chosen'):
                    multiple = '_'.join(request.POST.getlist('chosen'))
                    obj = func(form_1, multiple=multiple, item_id=item_id, delete=True)

                    if obj == None:
                        return None

                if args:
                    response = HttpResponseRedirect(
                            u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'][0],
                                                               args=reverse_ulr['save_and_continue'][1]+[obj.id]),
                            (u'The {0} "{1}" was deleted successfully.'.format(item, obj)))
                    )
                else:
                    response = HttpResponseRedirect(
                            u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                               args=[obj.id]),
                            (u'The {0} "{1}" was deleted successfully.'.format(item, obj)))
                    )
        else:
            return form_1
    # process the POST request by pressing a button "Cancel"
    elif request.POST.get('cancel_button') is not None:
        if args:
            response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['cancel_button'][0],
                                                       args=reverse_ulr['cancel_button'][1]),
                    (u'The "{0}" created canceled'.format(item)))
            )
        else:
            response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['cancel_button']),
                    (u'The "{0}" created canceled'.format(item)))
            )
    # process the POST request by pressing other buttons
    else:
        form_1 = item_form(request.POST)

        if cs_form:
            form_2 = cs_form[0](request.POST)

        if form_1.is_valid():
            if item_id:
                if request.POST.getlist('available'):
                    multiple = '_'.join(request.POST.getlist('available'))
                    obj = func(form_1, multiple=multiple, item_id=item_id)
                else:
                    obj = func(form_1, item_id=item_id)

                if obj == None:
                    return None
            else:
                if request.POST.getlist('available'):
                    multiple = '_'.join(request.POST.getlist('available'))
                    obj = func(form_1, multiple=multiple)
                    add_card_in_cardsequence(obj, cs_id)
                else:
                    obj = func(form_1)
                    add_card_in_cardsequence(obj, cs_id)

                if obj == None:
                    return None

            if cs_form:
                if form_2.is_valid():
                    cs_obj = cs_cards_update(form_2, cs_form[1], cs_form[2])

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'][0],
                                                           args=reverse_ulr['save_and_continue'][1]+[obj.id]),
                        (u'The {0} "{1}" will be saved. \
                        You can continue editing.'.format(item, obj)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                           args=[obj.id]),
                        (u'The {0} "{1}" will be saved. \
                        You can continue editing.'.format(item, obj)))
                )
        else:
            return form_1

    return response
