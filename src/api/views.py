# -*- coding: utf-8 -*-
from datetime import datetime
from subprocess import Popen
import os
import urllib

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from rest_framework import generics

from core.utils import (validate_status, write_log, get_path_folder_run, execute_fe_command)
from gsi.models import Run, RunStep, CardSequence, OrderedCardItem, SubCardItem
from gsi.settings import EXECUTE_FE_COMMAND, KML_PATH
from cards.models import CardItem
from customers.models import CustomerPolygons, DataTerraserver, DataSet, CustomerAccess, DataPolygons
from api.serializers import CustomerPolygonsSerializer, UserSerializer, DataPolygonsSerializer


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
        
        
# def send_simple_message():
#     import requests
#     return requests.get(
#         "https://api.mailgun.net/v3/domains/indy4.epcc.ed.ac.uk",
#         auth=("api", "key-2f50cd188fd70950e5af3c9cae9aa534"))
        
        
    # import requests
    # return requests.post(
    #     "https://api.mailgun.net/v3/indy4.epcc.ed.ac.uk",
    #     auth=("api", "key-2f50cd188fd70950e5af3c9cae9aa534"),
    #     data={"from": "Excited User <mailgun@indy4.epcc.ed.ac.uk>",
    #           "to": ["favorite.69@mail.ru",],
    #           "subject": "Hello 369",
    #           "text": "NEW Testing some Mailgun awesomness!"})
    
    
    # import smtplib
    # from email.mime.text import MIMEText
    #
    # msg = MIMEText('Testing some Mailgun awesomness')
    # msg['Subject'] = "Hello"
    # msg['From']    = "artgrem@gmail.com"
    # msg['To']      = "favorite.69@mail.ru"
    #
    # s = smtplib.SMTP('smtp.mailgun.org', 587)
    #
    # s.login('postmaster@indy4.epcc.ed.ac.uk', '3050e323a97e7cd65d7ac1c760f51de1')
    # s.sendmail(msg['From'], msg['To'], msg.as_string())
    # s.quit()


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
    
    ####################### write log file
    log_file = '/home/gsi/LOGS/update_run.log'
    log_update_run = open(log_file, 'a+')
    now = datetime.now()
    log_update_run.write('NOW: '+str(now))
    log_update_run.write('\n')
    log_update_run.write('RUN ID: '+str(run_id))
    log_update_run.write('\n')
    #######################

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
    
    ####################### write log file
    log_update_run.write('STATUS: '+data['status'])
    log_update_run.write('\n')
    #######################

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
        
        
        ####################### write log file
        log_update_run.write('*************************************************\n')
        log_update_run.close()
        #######################

    return Response(data, status=status.HTTP_200_OK)
    

# Example
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        

@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def external_auth_api(request):
    url_status = status.HTTP_200_OK
    content = {'detail': 'Method "GET" not allowed.'}
    
    # if request.method == 'POST':
    #     url_status = status.HTTP_200_OK
    #     content = {'detail': 'Hello User!'}
    # else:
    #     content = {'detail': 'Method "GET" not allowed.'}
    #     return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    return Response(content, status=url_status)
        
        
# class DataSetList(TokenAuthentication):
#     def authenticate(self, request):
#         print 'request ======================== ', request
#         username = request.META.get('X_USERNAME')
#         if not username:
#             return None
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')
#
#         return (user, None)
        
        
class CustomerPolygonsList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    data = None

    def get(self, request, format=None):
        if request.auth:
            queryset = CustomerPolygons.objects.filter(user=request.user).order_by('id')
            serializer = CustomerPolygonsSerializer(queryset, many=True)
            content = serializer.data
        else:
            content = {
                'auth': 'Need YOUR ACCESS TOKEN',
            }
        
        # content = {
        #     'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        #     'auth': unicode(request.auth),  # None
        # }
        # print 'request.user ======================== ', request.user
        
        return Response(content)
    
    
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def dataset(request, ds_id):
    # print 'ds_id ================================ ', ds_id
    # print 'request ================================ ', request
    url_status = status.HTTP_200_OK
    data = DataSet.objects.get(pk=ds_id)
    serializer = DataSetSerializer(data)
    
    return Response(serializer.data, status=url_status)
    
    
@api_view(['GET',])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def terraserver(request):
    """API to get data from the terraserver."""

    data = {}
    shapefile_name = ''
    customer = request.user
    data_terraserver = DataTerraserver.objects.none()
    
    
    path_to_map_images = '/home/gsi/Web_GeoChart/GSiMaps/png'
    root_url_gsimap = 'http://indy41.epcc.ed.ac.uk/'
    url_status = status.HTTP_200_OK
    
    # token = Token.objects.get(user=request.user)
    # print 'token.key ============================= ', token.key
    
    # print 'customer ============================= ', customer

    if request.GET:
        data_get = request.GET
        # data = JSONParser().parse(request)
        
        # print 'data =================== ', data

        if data_get.get('shapefile', ''):
            data['shapefile'] = data_get.get('shapefile', '')
            shapefile_name = data['shapefile'].split('/')[-1]
            kml_name = shapefile_name.split('.kml')[0]
            print 'data[shapefile] ============================= ', data['shapefile']
            
            new_shapefile_name = KML_PATH + '/' + shapefile_name
            
            print 'new_shapefile_name ============================= ', new_shapefile_name
            
            url = data['shapefile']
            urllib.urlretrieve(url, new_shapefile_name)
            
            data_terraserver, created = DataTerraserver.objects.update_or_create(
                user=customer,
                shapefile_link=data['shapefile'],
                shapefile=shapefile_name)
            
            obj, created = CustomerPolygons.objects.update_or_create(
                user=customer,
                name=kml_name,
                kml_name=shapefile_name,
                kml_path=new_shapefile_name
            )
        else:
            data['message error shapefile'] = 'Invalid or missing the shapefile in the request.'
            url_status = status.HTTP_400_BAD_REQUEST
            
        if data_get.get('param', ''):
            data['param'] = data_get.get('param', '')
            print 'param ============================= ', data['param']
            data_terraserver.parameter = data['param']
            data_terraserver.save()
        else:
            data['message error param'] = 'Invalid or missing the parameter in the request.'
            url_status = status.HTTP_400_BAD_REQUEST
            
        if data_get.get('transaction_id', ''):
            data['transaction_id'] = data_get.get('transaction_id', '')
            data_terraserver.transaction_id = data['transaction_id']
            data_terraserver.save()
        else:
            data['message error transaction_id'] = 'Invalid or missing the transaction ID in the request.'
            url_status = status.HTTP_400_BAD_REQUEST

        # send mail
        if url_status == status.HTTP_200_OK:
            send_mail('Subject here', 'Here is the message.', 'artgrem@gmail.com',
            ['artgrem@gmail.com'], fail_silently=False)
        
        # send_simple_message()
        
        # '''send email via mailgun'''
        # subject = "Hello, its me"
        # text_content = "I was wondering if after all these years"
        # sender = "artgrem@gmail.com"
        # receipient = "artgrem@gmail.com"
        # msg = EmailMultiAlternatives(subject, text_content, sender, [receipient])
        # respone = msg.send()
        
        # artgrem@gmail.com

        

        # if url_status == status.HTTP_200_OK:
        #     try:
        #         root, dirs, files = os.walk(path_to_map_images).next()
        #         data['results'] = []
        #
        #         for f in files:
        #             dict_tmp = {}
        #             file_without_ext = f.split('.png')[0]
        #             dict_tmp['file'] = f
        #             dict_tmp['url'] = root_url_gsimap + 'GSiMap.php?q=images/{0}'.format(file_without_ext)
        #             dict_tmp['description'] = 'a brief description of the map'
        #             data['results'].append(dict_tmp)
        #     except Exception, e:
        #         data['message error'] = 'No such file or directory: {0}'.format(path_to_map_images)
        #         url_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    # elif request.POST:
    #     data_post = request.POST
    #     data = JSONParser().parse(request)
    #
    #     print 'shapefile =================== ', shapefile
    #
    #     if data_post.get('shapefile', ''):
    #
    #         print 'shapefile =================== ', shapefile
    #         url_status = status.HTTP_200_OK
        # return Response("ok")
    else:
        data['message error'] = 'Invalid or missing the parameters for request.'
        url_status = status.HTTP_400_BAD_REQUEST

    return Response(data, status=url_status)
    
        
        
