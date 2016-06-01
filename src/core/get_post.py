# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from gsi.models import Area
from gsi.update_create import cs_cards_update


def get_post(request, item_form, item, reverse_ulr, func, args=False, item_id=None, cs_form=False):
    response = None

    # import pdb;pdb.set_trace()
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

                if obj == None:
                    return None

            if cs_form:
                if form_2.is_valid():
                    cs_obj = cs_cards_update(form_2, cs_form[1], cs_form[2])

            if args:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button'][0],
                                                       args=reverse_ulr['save_button'][1]),
                    (u'The {0} "{1}" was edited.'.format(item, obj.name)))
                )
            else:
                response = HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse(reverse_ulr['save_button']),
                    (u'The {0} "{1}" created successfully.'.format(item, obj.name)))
                )
        else:
            return form_1
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
                else:
                    obj = func(form_1)

                if obj == None:
                    return None

            if args:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another'][0],
                                                           args=reverse_ulr['save_and_another'][1]),
                        (u'The {0} "{1}" was added successfully. \
                        You may add another {2} below'.format(item, obj.name, item)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_another']),
                        (u'The {0} "{1}" was added successfully. \
                        You may add another {2} below'.format(item, obj.name, item)))
                )
        else:
            return form_1
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
                            (u'The {0} "{1}" was deleted successfully.'.format(item, obj.name)))
                    )
                else:
                    response = HttpResponseRedirect(
                            u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                               args=[obj.id]),
                            (u'The {0} "{1}" was deleted successfully.'.format(item, obj.name)))
                    )
        else:
            return form_1
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
                else:
                    obj = func(form_1)

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
                        You can continue editing.'.format(item, obj.name)))
                )
            else:
                response = HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
                                                           args=[obj.id]),
                        (u'The {0} "{1}" will be saved. \
                        You can continue editing.'.format(item, obj.name)))
                )
        else:
            return form_1
    # elif request.POST.get('save_and_continue_editing_button') is not None or request.POST.get('add_button') is not None:
    #     form_1 = item_form(request.POST)
    #
    #     if cs_form:
    #         form_2 = cs_form[0](request.POST)
    #
    #     if form_1.is_valid():
    #         if item_id:
    #             if request.POST.getlist('available'):
    #                 multiple = '_'.join(request.POST.getlist('available'))
    #                 obj = func(form_1, multiple=multiple, item_id=item_id)
    #             else:
    #                 obj = func(form_1, item_id=item_id)
    #
    #             if obj == None:
    #                 return None
    #         else:
    #             if request.POST.getlist('available'):
    #                 multiple = '_'.join(request.POST.getlist('available'))
    #                 obj = func(form_1, multiple=multiple)
    #             else:
    #                 obj = func(form_1)
    #
    #             if obj == None:
    #                 return None
    #
    #         if cs_form:
    #             if form_2.is_valid():
    #                 cs_obj = cs_cards_update(form_2, cs_form[1], cs_form[2])
    #
    #         if args:
    #             response = HttpResponseRedirect(
    #                     u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'][0],
    #                                                        args=reverse_ulr['save_and_continue'][1]+[obj.id]),
    #                     (u'The {0} "{1}" will be saved. \
    #                     You can continue editing.'.format(item, obj.name)))
    #             )
    #         else:
    #             response = HttpResponseRedirect(
    #                     u'%s?status_message=%s' % (reverse(reverse_ulr['save_and_continue'],
    #                                                        args=[obj.id]),
    #                     (u'The {0} "{1}" will be saved. \
    #                     You can continue editing.'.format(item, obj.name)))
    #             )
    #     else:
    #         return form_1

    return response