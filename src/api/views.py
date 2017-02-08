# -*- coding: utf-8 -*-
from datetime import datetime
from subprocess import Popen
import os

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import (validate_status, write_log, get_path_folder_run, execute_fe_command)
from gsi.models import Run, RunStep, CardSequence, OrderedCardItem, SubCardItem
from gsi.settings import EXECUTE_FE_COMMAND
from cards.models import CardItem


def is_finished(run_id, card_id, cur_counter, last, run_parallel):
    """Function to determine the last card in a running list of cards.

    :Arguments:
        * *run_id*: run id
        * *card_id*: card id
        * *cur_counter*: the current cards position in the running list of cards
        * *last*: the last position in the running list of cards
        * *run_parallel*: boolean value that parallel card opledelyaet running or sequentially

    """

    # if the card is running in parallel
    if run_parallel:
        # get all the sub-cards for the card
        sub_card_item = SubCardItem.objects.filter(
                run_id=int(run_id),
                card_id=int(card_id)
        ).values_list('state', flat=True)

        # if there is no "running" status and the "pending" in the list of sub-cards, the card is finished the Run
        if 'running' not in sub_card_item and 'pending' not in sub_card_item:
            return True
    # if the card is running in successively
    else:
        # if the current number of card coincides with the latter number, the card is finished the Run
        if cur_counter == last:
            return True

    return False


def set_state_fail(obj, state):
    """Set a card execution status if it does not 'fail'.

    :Arguments:
        * *obj*: card object
        * *state*: the current status of the card

    """

    if obj.state != 'fail':
        obj.state = state
        obj.save()


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def update_run(request, run_id):
    """Update the status of the card.

    The function receives the request and the card data. If the launched the card is last, the process stops.

    :Arguments:
        * *request*: request
        * *run_id*: card details. Presented as a string: <run_id>.<card_sequence_id>.<order_card_item_id>.<current_position>.<the_last_card_number>

    """

    data = validate_status(request.query_params.get('status', False))
    value_list = str(run_id).split('.')
    run_card_id = value_list[0]
    card_sequence_id = value_list[1]
    order_card_item_id = value_list[2]
    last = value_list[-1]
    last_but_one = value_list[-2:-1]
    cur_counter = last_but_one[0]
    name_sub_card = '{0}_{1}'.format(order_card_item_id, cur_counter)
    finished = False

    # if the status is valid
    if data['status']:
        state = data['status']

        # get the data of Run
        try:
            run = Run.objects.get(id=run_card_id)
            sequence = CardSequence.objects.get(id=card_sequence_id)
            card = OrderedCardItem.objects.get(id=order_card_item_id)
            step = RunStep.objects.get(
                parent_run=run,
                card_item=card)
            cur_state = step.state
            run_parallel = False

            # if the run is parallel
            # get name of sub-card
            try:
                if card.run_parallel:
                    run_parallel = True
                    name_sub_card = '{0}_{1}'.format(card.id, cur_counter)
            except Exception, e:
                pass

            # check the status and perform card processing
            if state == 'fail':
                params = []

                if run_parallel:
                    sub_card_item = SubCardItem.objects.filter(
                            name=name_sub_card,
                            run_id=int(run_card_id),
                            card_id=int(order_card_item_id)
                    )
                    for n in sub_card_item:
                        n.state = state
                        n.save()

                step.state = state
                step.save()
                run.state = state
                run.save()
            elif state == 'running':
                if run_parallel:
                    sub_card_item = SubCardItem.objects.filter(
                            name=name_sub_card,
                            run_id=int(run_card_id),
                            card_id=int(order_card_item_id)
                    )
                    for n in sub_card_item:
                        if n.state == 'running':
                            n.state = 'fail'
                            n.save()
                        else:
                            n.state = state
                            n.save()

                run_state = set_state_fail(run, state)
                step_state = set_state_fail(step, state)
            elif state == 'success':
                next_step, is_last_step = step.get_next_step()
                new_sub_card_item = None
                params = []

                if run_parallel:
                    sub_card_item = get_object_or_404(
                            SubCardItem,
                            name=name_sub_card,
                            run_id=int(run_card_id),
                            card_id=int(order_card_item_id)
                    )
                    sub_card_item.state = state
                    sub_card_item.save()

                if next_step:
                    data['next_step'] = next_step.id
                    run_parallel_next_step = next_step.card_item.run_parallel

                    # CHECK ALL THE SUB CARDS!!!!!!!
                    finished = is_finished(int(run_card_id), int(order_card_item_id), cur_counter, last, run_parallel)

                    if finished:
                        step_state = set_state_fail(step, state)

                        if run_parallel_next_step:
                            master_script_name = '{0}_master'.format(next_step.card_item.id)
                            ex_fe_com = Popen(
                                'nohup {0} {1} {2} &'.format(
                                    EXECUTE_FE_COMMAND,
                                    next_step.parent_run.id,
                                    master_script_name
                                ),
                                shell=True,
                            )
                        else:
                            ex_fe_com = Popen(
                                'nohup {0} {1} {2} &'.format(
                                    EXECUTE_FE_COMMAND,
                                    next_step.parent_run.id,
                                    next_step.card_item.id
                                ),
                                shell=True,
                            )

                    log_name = '{0}_{1}.log'.format(value_list[0], value_list[2])
                    path_log = get_path_folder_run(run)['path_runs_logs']
                    write_log(log_name, run, path_log)

                # this end
                if is_last_step:
                    data['is_last_step'] = True
                    finished = is_finished(int(run_card_id), int(order_card_item_id), cur_counter, last, run_parallel)

                    if finished:
                        if run_parallel:
                            sub_card_item = get_object_or_404(
                                    SubCardItem,
                                    name=name_sub_card,
                                    run_id=int(run_card_id),
                                    card_id=int(order_card_item_id)
                            )

                            sub_card_item.state = 'success'
                            sub_card_item.save()
                        run_state = set_state_fail(run, state)
                        step_state = set_state_fail(step, state)
            else:
                if run_parallel:
                    sub_card_item = SubCardItem.objects.filter(
                            name=name_sub_card,
                            run_id=int(run_card_id),
                            card_id=int(order_card_item_id)
                    )

                    for n in sub_card_item:
                        n.state = state
                        n.save()

                run_state = set_state_fail(run, state)
                step_state = set_state_fail(step, state)
        except Exception, e:
            data['status'] = False
            data['message'] = str(e)
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_gsi_maps(request):
    """API to get ready card images."""

    data = {}
    path_to_map_images = '/home/gsi/Web_GeoChart/GSiMaps/png'
    root_url_gsimap = 'http://indy41.epcc.ed.ac.uk/'
    url_status = status.HTTP_200_OK

    if request.GET:
        data_get = request.GET

        if data_get.get('param1', ''):
            data['param 1'] = data_get.get('param1', '')
        else:
            data['message error param1'] = 'Invalid or missing the param1 in the request GET.'
            url_status = status.HTTP_400_BAD_REQUEST

        if data_get.get('param2', ''):
            data['param 2'] = data_get.get('param2', '')
        else:
            data['message error param2'] = 'Invalid or missing the param2 in the request GET.'
            url_status = status.HTTP_400_BAD_REQUEST

        if data_get.get('param3', ''):
            data['param 3'] = data_get.get('param3', '')
        else:
            data['message error param3'] = 'Invalid or missing the param3 in the request GET.'
            url_status = status.HTTP_400_BAD_REQUEST

        if url_status == status.HTTP_200_OK:
            try:
                root, dirs, files = os.walk(path_to_map_images).next()
                data['results'] = []

                for f in files:
                    dict_tmp = {}
                    file_without_ext = f.split('.png')[0]
                    dict_tmp['file'] = f
                    dict_tmp['url'] = root_url_gsimap + 'GSiMap.php?q=images/{0}'.format(file_without_ext)
                    dict_tmp['description'] = 'a brief description of the map'
                    data['results'].append(dict_tmp)
            except Exception, e:
                data['message error'] = 'No such file or directory: {0}'.format(path_to_map_images)
                url_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        data['message error'] = 'Invalid or missing the parameters for request GET.'
        url_status = status.HTTP_400_BAD_REQUEST

    return Response(data, status=url_status)
