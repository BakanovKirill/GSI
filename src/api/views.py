# -*- coding: utf-8 -*-
from datetime import datetime
from subprocess import Popen

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from core.utils import (validate_status, write_log,
                        get_path_folder_run, execute_fe_command)
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

    if run_parallel:
        sub_card_item = SubCardItem.objects.filter(
                run_id=int(run_id),
                card_id=int(card_id)
        ).values_list('state', flat=True)

        is_finish = ('running' not in sub_card_item and 'pending' not in sub_card_item)

        if 'running' not in sub_card_item and 'pending' not in sub_card_item:
            return True
    else:
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

    if data['status']:
        state = data['status']

        try:
            run = Run.objects.get(id=run_card_id)
            sequence = CardSequence.objects.get(id=card_sequence_id)
            card = OrderedCardItem.objects.get(id=order_card_item_id)
            step = RunStep.objects.get(
                parent_run=run,
                card_item=card)
            cur_state = step.state
            run_parallel = False

            try:
                if card.run_parallel:
                    run_parallel = True
                    name_sub_card = '{0}_{1}'.format(card.id, cur_counter)
            except Exception, e:
                pass

            # for step in steps:
            # Go to the next step only on success state
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
                    path_log = get_path_folder_run(run)
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
            pass
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)
