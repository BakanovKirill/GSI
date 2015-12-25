from annoying.decorators import render_to
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .utils import validate_status
from .models import Run


@render_to('index.html')
def index(request):
    data = {}
    return data


@api_view(['GET'])
def update_status_of_runs(request, run_id):
    """ update the status of the runs"""

    data = validate_status(request.query_params.get('status', False))

    if data['status']:
        try:
            current_run = Run.objects.get(id=run_id)
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def update_status_of_cards(request, run_id, card_id):
    """ update the status of the cards"""

    data = validate_status(request.query_params.get('status', False))

    if data['status']:
        try:
            update_card = Run.objects.get(
                    id=run_id,
                    run_base__card_sequence__cards__id=card_id)
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)