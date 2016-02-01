# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def get_cards_post(request, card_form, card, reverse_ulr, func, args=False, card_id=None):
    response = None

    # import pdb;pdb.set_trace()
    if request.POST.get('save_button') is not None:
        form = card_form(request.POST)

        if form.is_valid():
            if card_id:
                card_item = func(form, card_id)
            else:
                card_item = func(form)

            if args:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button'][0],
                                                       args=reverse_ulr['save_button'][1]),
                    (u"The {0} {1} created successfully".format(card, card_item.name)))
                )
            else:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button']),
                    (u"The {0} {1} created successfully".format(card, card_item.name)))
                )
        else:
            return form
    elif request.POST.get('save_and_another_button') is not None:
        form = card_form(request.POST)

        if form.is_valid():
            if card_id:
                card_item = func(form, card_id)
            else:
                card_item = func(form)

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another'][0],
                                                           args=reverse_ulr['save_and_another'][1]),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} below".format(card, card_item.name, card)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another']),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} below".format(card, card_item.name, card)))
                )
        else:
            return form
    elif request.POST.get('save_and_continue_editing_button') is not None:
        form = card_form(request.POST)

        if form.is_valid():
            if card_id:
                card_item = func(form, card_id)
            else:
                card_item = func(form)

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'][0],
                                                           args=reverse_ulr['save_and_continue'][1]+[card_item.id]),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} Card below".format(card, card_item.name, card)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                           args=[card_item.id]),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} Card below".format(card, card_item.name, card)))
                )
        else:
            return form
    elif request.POST.get('cancel_button') is not None:
        if args:
            response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['cancel_button'][0],
                                                       args=reverse_ulr['cancel_button'][1]),
                    (u"The {0} Card created canceled".format(card)))
            )
        else:
            response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['cancel_button']),
                    (u"The {0} Card created canceled".format(card)))
            )

    return response