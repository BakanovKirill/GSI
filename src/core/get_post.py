# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from gsi.models import Area


def get_post(request, item_form, item, reverse_ulr, func, args=False, item_id=None):
    response = None

    # import pdb;pdb.set_trace()
    if request.POST.get('save_button') is not None:
        form = item_form(request.POST)

        if form.is_valid():
            if item_id:
                if request.POST.getlist('available_tiles'):
                    multiple = '_'.join(request.POST.getlist('available_tiles'))
                    obj = func(form, multiple=multiple, item_id=item_id)
                else:
                    obj = func(form, item_id=item_id)
            else:
                if request.POST.getlist('available_tiles'):
                    multiple = '_'.join(request.POST.getlist('available_tiles'))
                    obj = func(form, multiple=multiple)
                else:
                    obj = func(form)

            if args:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button'][0],
                                                       args=reverse_ulr['save_button'][1]),
                    (u"The {0} {1} created successfully".format(item, obj.name)))
                )
            else:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button']),
                    (u"The {0} {1} created successfully".format(item, obj.name)))
                )
        else:
            return form
    elif request.POST.get('save_and_another_button') is not None:
        form = item_form(request.POST)

        if form.is_valid():
            if item_id:
                if request.POST.getlist('available_tiles'):
                    multiple = '_'.join(request.POST.getlist('available_tiles'))
                    obj = func(form, multiple=multiple, item_id=item_id)
                else:
                    obj = func(form, item_id=item_id)
            else:
                if request.POST.getlist('available_tiles'):
                    multiple = '_'.join(request.POST.getlist('available_tiles'))
                    obj = func(form, multiple=multiple)
                else:
                    obj = func(form)

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another'][0],
                                                           args=reverse_ulr['save_and_another'][1]),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} below".format(item, obj.name, item)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another']),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} below".format(item, obj.name, item)))
                )
        else:
            return form
    elif request.POST.get('save_and_continue_editing_button') is not None or request.POST.get('add_button') is not None:
        form = item_form(request.POST)

        if form.is_valid():
            if item_id:
                if request.POST.getlist('available_tiles'):
                    multiple = '_'.join(request.POST.getlist('available_tiles'))
                    obj = func(form, multiple=multiple, item_id=item_id)
                else:
                    obj = func(form, item_id=item_id)
            else:
                if request.POST.getlist('available_tiles'):
                    multiple = '_'.join(request.POST.getlist('available_tiles'))
                    obj = func(form, multiple=multiple)
                else:
                    obj = func(form)

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'][0],
                                                           args=reverse_ulr['save_and_continue'][1]+[obj.id]),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} below".format(item, obj.name, item)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                           args=[obj.id]),
                        (u"The {0} {1} was added successfully. \
                        You may add another {2} below".format(item, obj.name, item)))
                )
        else:
            return form
    elif request.POST.get('delete_button') is not None:
        form = item_form(request.POST)

        if form.is_valid():
            if item_id:
                if request.POST.getlist('chosen_tiles'):
                    multiple = '_'.join(request.POST.getlist('chosen_tiles'))
                    obj = func(form, multiple=multiple, item_id=item_id, delete=True)

                if args:
                    response = HttpResponseRedirect(
                            u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another'][0],
                                                               args=reverse_ulr['save_and_continue'][1]+[obj.id]),
                            (u"The {0} {1} was deleted successfully. \
                            You may add another {2} below".format(item, obj.name, item)))
                    )
                else:
                    response = HttpResponseRedirect(
                            u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                               args=[obj.id]),
                            (u"The {0} {1} was deleted successfully. \
                            You may add another {2} below".format(item, obj.name, item)))
                    )
        else:
            return form
    elif request.POST.get('cancel_button') is not None:
        if args:
            response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['cancel_button'][0],
                                                       args=reverse_ulr['cancel_button'][1]),
                    (u"The {0} created canceled".format(item)))
            )
        else:
            response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['cancel_button']),
                    (u"The {0} created canceled".format(item)))
            )

    return response