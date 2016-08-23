# -*- coding: utf-8 -*-
from datetime import datetime
from subprocess import Popen, PIPE

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from core.utils import (validate_status, write_log, create_scripts,
                        get_path_folder_run, execute_fe_command)
from gsi.models import Run, RunStep, CardSequence, OrderedCardItem, SubCardItem
from gsi.settings import EXECUTE_FE_COMMAND, FE_SUBMIT
from cards.models import CardItem

# update the status of the runs
# <RUN_ID>.<SEQUENCE_ID>.<CARD_ID>
# example:
# http://indy4.epcc.ed.ac.uk:/run/20.5.1/?status=running


def is_finished(run_id, card_id, cur_counter, last, run_parallel):
    # ***********************************************************************
    # logs for api
    path_file = '/home/gsi/LOGS/is_finished.log'
    now = datetime.now()
    api_run = open(path_file, 'a')
    api_run.writelines('RUN: {0}\n'.format(run_id))
    api_run.writelines('CARD: {0}\n'.format(card_id))
    # ***********************************************************************

    if run_parallel:
        sub_card_item = SubCardItem.objects.filter(
                run_id=int(run_id),
                card_id=int(card_id)
        ).values_list('state', flat=True)

        is_finish = ('running' not in sub_card_item and 'pending' not in sub_card_item)

        # ***********************************************************************
        # api_run.writelines('ALL STATUSES: {0}\n'.format(sub_card_item))
        api_run.writelines('SUB CARD: {0}\n'.format(sub_card_item))
        api_run.writelines('IS FINISH: {0}\n'.format(is_finish))
        # ***********************************************************************

        if 'running' not in sub_card_item and 'pending' not in sub_card_item:
            return True
    else:
        if cur_counter == last:
            return True

    # ***********************************************************************
    api_run.writelines('\n\n\n')
    api_run.close
    # ***********************************************************************

    return False


def get_state_fail(obj, state):
    if obj.state != 'fail':
        obj.state = state
        obj.save()


@api_view(['GET'])
def update_run(request, run_id):
    """ update the status cards of the runs """

    # ************************* logs for api
    path_file = '/home/gsi/LOGS/api_run.log'
    now = datetime.now()
    api_run = open(path_file, 'a')
    # ***********************************************************************


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

    # ***********************************************************************
    api_run.writelines('RUN: {0}\n'.format(run_id))
    api_run.writelines('STATUS: {0}\n'.format(data['status']))
    api_run.writelines('\n\n\n')
    api_run.close()
    # ***********************************************************************

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

            # ************************* logs for api
            path_file = '/home/gsi/LOGS/api_status.log'
            now = datetime.now()
            log_file = open(path_file, 'a')
            log_file.writelines(str(now) + '\n')
            log_file.writelines('RUN-{0}:\n'.format(str(run_id)))
            log_file.writelines('STATUS: {0}\n'.format(str(state)))
            # ***********************************************************************

            try:
                if card.run_parallel:
                    run_parallel = True
                    name_sub_card = '{0}_{1}'.format(card.id, cur_counter)
            except Exception, e:
                log_file.writelines('ERROR RUN PARALLEL: {0}\n\n'.format(e))

            # if run_parallel:
            #     new_sub_card_item = SubCardItem.objects.filter(
            #                             run_id=int(run_card_id),
            #                             card_id=int(order_card_item_id),
            #                             state='pending'
            #                         ).order_by('start_date')[:6]

            # ***********************************************************************
            log_file.writelines('RUN PARALLEL: {0}\n'.format(run_parallel))
            # ***********************************************************************

            # for step in steps:
            # Go to the next step only on success state
            if state == 'fail':
                # ***********************************************************************
                log_file.writelines('FAIL state: ' + str(state) + '\n')
                # ***********************************************************************

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

                # ***********************************************************************
                # write log file
                # path_file = '/home/gsi/LOGS/api_fail.log'
                # now = datetime.now()
                # api_fail = open(path_file, 'a')
                # api_fail.writelines('{0}\n'.format(now))
                # api_fail.writelines('RUN-{0}:\n'.format(run_card_id))
                # api_fail.writelines('CARDS-{0}:\n'.format(card.id))
                # api_fail.writelines('LAST ==> {0}\n'.format(last))
                # api_fail.writelines('LAST BUT ONE ==> {0}\n'.format(last_but_one[0]))
                # api_fail.writelines('CUR_counter => {0}\n'.format(cur_counter))
                # api_fail.writelines('LAST => {0}\n'.format(last))
                # api_fail.writelines('state ==> {0}\n\n\n'.format(step.state))
                # api_fail.close()
                # ***********************************************************************
            elif state == 'running':
                log_file.writelines('RUNNING state: ' + str(state) + '\n')

                # ***********************************************************************
                # write log file
                path_file = '/home/gsi/LOGS/api_running.log'
                now = datetime.now()
                api_running = open(path_file, 'a')
                api_running.writelines('{0}\n'.format(now))
                api_running.writelines('RUN: {0}:\n'.format(run_id))
                # ***********************************************************************

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

                run_state = get_state_fail(run, state)
                step_state = get_state_fail(step, state)

                # ***********************************************************************
                # write log file
                # api_running.writelines('LAST ==> {0}\n'.format(last))
                # api_running.writelines('LAST BUT ONE ==> {0}\n'.format(last_but_one[0]))
                # api_running.writelines('CUR_counter => {0}\n'.format(cur_counter))
                api_running.writelines('STATE: {0}\n\n\n'.format(step.state))
                api_running.close()
                # ***********************************************************************
            elif state == 'success':
                next_step, is_last_step = step.get_next_step()
                new_sub_card_item = None
                params = []

                # ********** WRITE LOG *****************************
                log_file.writelines('SUCCESS state: ' + str(state) + '\n')
                # log_file.writelines('get_next_step => {0}\n'.format(step.get_next_step()))
                log_file.writelines('NEXT STEP: {0}\n'.format(next_step))
                log_file.writelines('LAST STEP: {0}\n'.format(is_last_step))
                log_file.writelines('cur_counter: {0}\n'.format(cur_counter))
                log_file.writelines('last: {0}\n'.format(last))
                log_file.writelines('cur_counter & last == {0}\n'.format(cur_counter == last))
                # *************************************************

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

                    # ********** WRITE LOG *****************************
                    log_file.writelines('NEXT CARD run_parallel => {0}\n'.format(run_parallel_next_step))
                    # *************************************************

                    # CHECK ALL THE SUB CARDS!!!!!!!
                    finished = is_finished(int(run_card_id), int(order_card_item_id), cur_counter, last, run_parallel)

                    # *************************************************
                    log_file.writelines('finished => {0}\n'.format(finished))
                    # *************************************************

                    if finished:
                        step_state = get_state_fail(step, state)

                        if run_parallel_next_step:
                            # next_sub_cards_item = SubCardItem.objects.filter(
                            #         run_id=next_step.parent_run.id,
                            #         card_id=next_step.card_item.id
                            # ).order_by('start_date')
                            # # count = 1
                            #
                            # for n in next_sub_cards_item:
                            #     name_card = '{0}%{1}'.format(n.run_id, n.name)
                            #     params.append(name_card)
                            #
                            # execute_fe_command(params)

                            master_script_name = '{0}_master.sh'.format(next_step.card_item.id)
                            ex_fe_com = Popen(
                                'nohup {0} {1} {2} &'.format(
                                    EXECUTE_FE_COMMAND,
                                    next_step.parent_run.id,
                                    master_script_name
                                ),
                                shell=True,
                            )
                            # *************************************************
                            log_file.writelines('MASTER SCRIPT {0}\n'.format(master_script_name))
                            # *************************************************
                        else:
                            # *************************************************
                            log_file.writelines('next RUN => {0}\n'.format(next_step.parent_run.id))
                            log_file.writelines('card_item.id => {0}\n'.format(next_step.card_item.id))
                            # *************************************************
                            ex_fe_com = Popen(
                                'nohup {0} {1} {2} &'.format(
                                    EXECUTE_FE_COMMAND,
                                    next_step.parent_run.id,
                                    next_step.card_item.id
                                ),
                                shell=True,
                            )

                        # ***********************************************************************
                        # write log file
                        path_file = '/home/gsi/LOGS/api_success_next_step.log'
                        now = datetime.now()
                        log_api_file = open(path_file, 'a')
                        log_api_file.writelines('{0}\n'.format(now))
                        log_api_file.writelines('RUN-{0}:\n'.format(run_card_id))
                        log_api_file.writelines('CARDS-{0}:\n'.format(card.id))
                        log_api_file.writelines('SCRIPTS: \n')
                        log_api_file.writelines('LAST ==> {0}\n'.format(last))
                        log_api_file.writelines('LAST BUT ONE ==> {0}\n'.format(last_but_one[0]))
                        log_file.writelines('CUR_counter => {0}\n'.format(cur_counter))
                        log_file.writelines('LAST => {0}\n'.format(last))
                        log_api_file.writelines('state ==> {0}\n\n\n'.format(step.state))
                        log_api_file.close()
                        # ***********************************************************************
                    # else:
                    #     if new_sub_card_item:
                    #         name_card = '{0}%{1}'.format(
                    #                 new_sub_card_item[0].run_id,
                    #                 new_sub_card_item[0].name)
                    #         params.append(name_card)
                    #         new_sub_card_item[0].state = 'running'
                    #         new_sub_card_item[0].save()
                    #         execute_fe_command(params)

                    log_name = '{0}_{1}.log'.format(value_list[0], value_list[2])
                    path_log = get_path_folder_run(run)
                    # path_log = script['path_runs_logs']
                    write_log(log_name, run, path_log)

                # this end
                if is_last_step:
                    data['is_last_step'] = True
                    finished = is_finished(int(run_card_id), int(order_card_item_id), cur_counter, last, run_parallel)

                    # if new_sub_card_item:
                    #     name_card = '{0}%{1}'.format(
                    #             new_sub_card_item[0].run_id,
                    #             new_sub_card_item[0].name)
                    #     params.append(name_card)
                    #     new_sub_card_item[0].state = 'running'
                    #     new_sub_card_item[0].save()
                    #     execute_fe_command(params)

                    # *************************************************
                    log_file.writelines('Finished Last Step => {0}\n'.format(finished))
                    # *************************************************

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
                        run_state = get_state_fail(run, state)
                        step_state = get_state_fail(step, state)

                        # ***********************************************************************
                        # write log file
                        path_file = '/home/gsi/LOGS/api_success_last_step.log'
                        now = datetime.now()
                        log_api_file = open(path_file, 'a')
                        log_api_file.writelines('{0}\n'.format(now))
                        log_api_file.writelines('RUN-{0}:\n'.format(run_card_id))
                        log_api_file.writelines('CARDS-{0}:\n'.format(card.id))
                        log_api_file.writelines('PARALLEL: {0}\n'.format(run_parallel))
                        log_api_file.writelines('LAST ==> {0}\n'.format(last))
                        log_api_file.writelines('LAST BUT ONE ==> {0}\n'.format(last_but_one[0]))
                        log_file.writelines('CUR_counter => {0}\n'.format(cur_counter))
                        log_file.writelines('LAST => {0}\n'.format(last))
                        log_api_file.writelines('state ==> {0}\n\n\n'.format(step.state))
                        log_api_file.close()
                        # ***********************************************************************

                        # ***********************************************************************
                        log_file.writelines('RUN finished State => {0}\n'.format(run_state))
                        log_file.writelines('Step finished State => {0}\n'.format(step_state))
                        # ***********************************************************************

                    # ***********************************************************************
                    log_file.writelines('RUN last_step State => {0}\n'.format(run.state))
                    log_file.writelines('Step last_step State => {0}\n'.format(step.state))
                    # ***********************************************************************
            else:
                # ***********************************************************************
                log_file.writelines('ELSE: ' + str(state) + '\n')
                # ***********************************************************************

                if run_parallel:
                    sub_card_item = SubCardItem.objects.filter(
                            name=name_sub_card,
                            run_id=int(run_card_id),
                            card_id=int(order_card_item_id)
                    )

                    for n in sub_card_item:
                        n.state = state
                        n.save()

                run_state = get_state_fail(run, state)
                step_state = get_state_fail(step, state)

            # ***********************************************************************
            log_file.writelines('RUN END State => {0}\n'.format(run.state))
            log_file.writelines('Step END State => {0}\n'.format(step.state))
            log_file.writelines('\n\n\n')
            log_file.close()
            # ***********************************************************************
        except Exception, e:
            # ***********************************************************************
            # error for api
            path_file = '/home/gsi/LOGS/api_error.err'
            now = datetime.now()
            log_file1 = open(path_file, 'a')
            log_file1.writelines('ERRROR API-{0}:'.format(run_id) + '\n')
            log_file1.writelines(str(now) + '\n')
            log_file1.writelines('Error Status: {0}\n'.format(str(e)))

            # log_file1.writelines('RUN-{0}:\n'.format(run_card_id))
            # log_file1.writelines('CARDS-{0}:\n'.format(order_card_item_id))
            log_file1.writelines('STATUS: {0}\n'.format(str(state)))

            log_file1.writelines('\n\n\n')
            log_file1.close()
            # ***********************************************************************
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)

            # run.state = state
            # step.state = state
            # run.save()
            # step.save()



            # ***********************************************************************
            # error for api
            path_file = '/home/gsi/LOGS/api_status.err'
            now = datetime.now()
            log_file2 = open(path_file, 'a')
            log_file2.writelines('ERRROR runcards_{0}:'.format(run_card_id) + '\n')
            log_file2.writelines(str(now) + '\n')
            log_file2.writelines(str(e) + '\n')

            log_file2.writelines('\n\n\n')
            log_file2.close()
            # ***********************************************************************
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
