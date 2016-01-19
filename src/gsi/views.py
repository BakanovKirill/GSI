from annoying.decorators import render_to
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .utils import validate_status
from .models import Run, RunStep


@render_to('gsi/blocking.html')
def blocking(request):
    data = {}
    return data


@login_required
@render_to('gsi/index.html')
def index(request):
    data = {}
    return data


@login_required
@render_to('gsi/setup_new_run.html')
def setup_new_run(request):
    data = {}
    return data


@api_view(['GET'])
def update_run(request, run_id):
    """ update the status of the runs """

    data = validate_status(request.query_params.get('status', False))

    if data['status']:
        try:
            current_run = Run.objects.get(id=run_id)
            current_run.state = data['status']
            current_run.save()
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
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

