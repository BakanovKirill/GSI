# -*- coding: utf-8 -*-
from datetime import datetime
from subprocess import Popen, PIPE

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from core.utils import validate_status, write_log, create_scripts
from gsi.models import Run, RunStep, CardSequence, OrderedCardItem
from gsi.settings import EXECUTE_FE_COMMAND
from cards.models import CardItem

# update the status of the runs
# <RUN_ID>.<SEQUENCE_ID>.<CARD_ID>
# example:
# http://indy4.epcc.ed.ac.uk:/run/20.5.1/?status=running

@api_view(['GET'])
def update_run(request, run_id):
    """ update the status cards of the runs """

    data = validate_status(request.query_params.get('status', False))
    value_list = run_id.split('.')
    run_card_id = value_list[0]
    card_sequence_id = value_list[1]
    order_card_item_id = value_list[2]

    if data['status']:
        state = data['status']

        try:
            run = Run.objects.get(id=run_card_id)
            sequence = CardSequence.objects.get(id=card_sequence_id)
            card = OrderedCardItem.objects.get(id=order_card_item_id)
            step = RunStep.objects.get(
                parent_run=run,
                card_item=card)

            # logs for api
            path_file = '/home/gsi/logs/runcards_status.log'
            now = datetime.now()
            log_file = open(path_file, 'a')
            log_file.writelines('RUNCARDS_{0}:\n'.format(card.id))
            log_file.writelines('STATUS:\n')
            log_file.writelines(str(now) + '\n')
            log_file.writelines(str(state) + '\n')
            log_file.writelines('====== RUN_ID:\n')
            log_file.writelines('run_id => {0}\n'.format(str(run_id)))
            log_file.writelines('====== Run:\n')
            log_file.writelines('name => {0} :: id => {1}\n'.format(str(run_card_id), str(run_card_id.id)))
            log_file.writelines('====== OrderedCardItem:\n')
            log_file.writelines('name => {0} :: id => {1}\n\n\n'.format(str(card), str(card.id)))
            log_file.writelines('====== RunStep:\n')
            log_file.writelines('name => {0} :: id => {1}\n'.format(str(step), str(step.id)))
            # log_file.close()

            # for step in steps:
            # Go to the next step only on success state
            if state == 'running':
                pass
            elif state == 'fail':
                log_file.writelines('FAIL: ' + str(state) + '\n')
                step.state = 'fail'
                run.state = 'fail'
                step.save()
                run.save()
                # break
            elif state == 'success':
                log_file.writelines('SUCCESS: ' + str(state) + '\n')
                next_step, is_last_step = step.get_next_step()

                if next_step:
                    data['next_step'] = next_step.id
                    script = create_scripts(run, sequence, card, step)
                    ex_fe_com = Popen(
                        'nohup {0} {1} {2} &'.format(
                            EXECUTE_FE_COMMAND,
                            value_list[0],
                            value_list[2]
                        ),
                        shell=True,
                        # stdout=PIPE,
                        # stderr=PIPE
                    )

                    log_name = '{0}_{1}.log'.format(value_list[0], value_list[2])
                    path_log = script['path_runs_logs']
                    write_log(log_name, run, path_log)

                if is_last_step:
                    data['is_last_step'] = True
                    step.state = 'success'
                    # run = step.parent_run
                    run.state = 'success'
                    step.save()
                    run.save()
            else:
                log_file.writelines('ELSE: ' + str(state) + '\n')
                step.state = state
                step.save()
                # run = step.parent_run
                # run.state = state
                # run.save()

            log_file.close()

        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)

            # error for api
            path_file = '/home/gsi/logs/runcards_status.err'
            now = datetime.now()
            log_file = open(path_file, 'a')
            log_file.writelines('ERRROR runcards_{0}:'.format(card.id) + '\n')
            log_file.writelines(str(now) + '\n')
            log_file.writelines(str(e) + '\n')
        log_file.writelines('\n\n\n')
        log_file.close()
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def update_step(request, step_id):
    """ update the status of the cards """

    data = validate_status(request.query_params.get('status', False))
    if data['status']:
        state = data['status']
        try:
            step = RunStep.objects.get(pk=step_id)
            step.state = state
            step.save()
            # Go to the next step only on success state
            if state == 'success':
                next_step, is_last_step = step.get_next_step()
                if next_step:
                    data['next_step'] = next_step.id
                if is_last_step:
                    data['is_last_step'] = True
                    # TODO: possibly finish the run (discuss)
                    # run = step.parent_run
                    # run.status = 'success'
                    # run.save()
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)