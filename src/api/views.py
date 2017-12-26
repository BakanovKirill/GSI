# -*- coding: utf-8 -*-
from datetime import datetime, date
from subprocess import Popen
import os
import urllib
import requests
import zipfile

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
# from geoip import geolite2

from django.core.files import File
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser, FileUploadParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, viewsets

from rest_framework.authtoken import views


# from rest_framework import parsers, renderers
# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView

from core.utils import (validate_status, write_log, get_path_folder_run, execute_fe_command,
                        handle_uploaded_file, getLogDataRequest)
from gsi.models import Run, RunStep, CardSequence, OrderedCardItem, SubCardItem
from gsi.settings import (EXECUTE_FE_COMMAND, KML_PATH, FTP_PATH, KML_DIRECTORY,
                            REMAP_DIRECTORY, REMAP_PATH, STATISTICS)
from cards.models import CardItem
from customers.models import (CustomerPolygons, DataTerraserver, DataSet, CustomerAccess,
                                DataPolygons, CustomerInfoPanel, TimeSeriesResults, Reports,
                                ShelfData, Log)
from api.serializers import (CustomerPolygonsSerializer, CustomerPolygonSerializer, 
                            DataPolygonsSerializer, DataSetsSerializer, DataSetSerializer,
                            TimeSeriesResultSerializer, ReportsSerializer, LogSerializer)
from api.pagination import CustomPagination
from core.get_coordinate_aoi import (get_coord_aoi, get_coord_document_placemark_polygon_outerboundaryIs,
                                    get_coord_document_placemark_multigeometry_polygon_outerboundaryIs,
                                    get_coord_document_folder_placemark_multigeometry_polygon_outerboundaryIs,
                                    get_coord_placemark_polygon_outerboundaryIs,
                                    get_coord_placemark_multigeometry_polygon_outerboundaryIs,
                                    get_coord_document_placemark_polygon_innerboundaryIs,
                                    get_coord_placemark_polygon_innerboundaryIs)
from core.editor_shapefiles import (get_count_color, copy_file_kml, get_data_kml, delete_empty_lines,
                                    validation_kml, is_calculation_aoi, get_info_window,
                                    create_new_calculations_aoi, createUploadTimeSeriesResults,
                                    addPolygonToDB)
from core.functions_customer import (getResultDirectory, getTsResultDirectory,
                                    getCountTs, createKml, addPolygonToDB)


# in_path = '/home/grigoriy/test/TMP/1_test.txt'
# out_path = '/home/grigoriy/test/TMP/11'
# command_line = 'cp {0} {1}'.format(in_path, out_path)
# proc = Popen(command_line, shell=True)
# proc.wait()
# 
# generics.ListAPIView


def get_curent_dataset(user):
    try:
        cip = CustomerInfoPanel.objects.get(user=user, is_show=True)
        dataset = cip.data_set
    except CustomerInfoPanel.DoesNotExist:
        dataset = None

    return dataset


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


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
    log_update_run.write('STATUS: '+str(data['status']))
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
    

# *********** Ethos API *********************************************************************
# Example
# class UserListAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class GetAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        dataset = get_curent_dataset(user)
        message = getLogDataRequest(request)
        Log.objects.create(user=user, mode='api', dataset=dataset, action='auth_token', message=message)

        return Response({'token': token.key})

obtain_auth_token = GetAuthToken.as_view()


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



class DataSetList(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StoreItems to be retrieved.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    # serializer_class = DataSetsSerializer
    serializer_class = DataSetSerializer

    def get_queryset(self):
        queryset = DataSet.objects.none()
        # data = {'auth': 'Need YOUR ACCESS TOKEN'}
        # url_status = status.HTTP_400_BAD_REQUEST
        # queryset = ['Need YOUR ACCESS TOKEN']

        if self.request.auth:
            try:
                customer_access = CustomerAccess.objects.get(user=self.request.user)
                queryset = DataSet.objects.filter(customer_access=customer_access).order_by('id')

                dataset = get_curent_dataset(self.request.user)
                message = getLogDataRequest(self.request)
                Log.objects.create(user=self.request.user, mode='api', dataset=dataset, action='dataset list', message=message)
            except Exception:
                pass

        return queryset


# class DataSetList(APIView):
#     """
#     List DataSets ...
#     """

#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     # authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)

#     # pagination
#     pagination_class = StandardResultsSetPagination
#     # paginate_by_param = 'page_size'
#     # max_paginate_by = 500
#     # paginate_by = 10

#     def get(self, request, format=None):
#         data = {'auth': 'Need YOUR ACCESS TOKEN'}

#         # if request.auth:
#         customer_access = CustomerAccess.objects.get(user=request.user)
#         queryset = DataSet.objects.filter(customer_access=customer_access).order_by('id')
#         pagination_class = PageNumberPagination()
#         serializer = DataSetSerializer(queryset, many=True)
#         data = serializer.data

#         return Response(data)


class DataSetDetail(APIView):
    """
    Retrieve a DataSet instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, ds_id, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}

        if request.auth:
            try:
                queryset = DataSet.objects.get(pk=ds_id)
                # serializer = DataSetsSerializer(queryset)
                serializer = DataSetSerializer(queryset)
                data = serializer.data

                dataset = get_curent_dataset(request.user)
                message = 'DATASET DETAIL: {}; '.format(queryset)
                message += getLogDataRequest(request)
                Log.objects.create(user=request.user, mode='api', dataset=dataset, action='dataset detail', message=message)
            except DataSet.DoesNotExist:
                return Response({'error': 'DataSet Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class ShapeFileList(viewsets.ReadOnlyModelViewSet):
    """
    List ShapeFiles
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerPolygonSerializer

    def get_queryset(self):
        # queryset = {'auth': 'Need YOUR ACCESS TOKEN'}
        queryset = CustomerPolygons.objects.none()

        if self.request.auth:
            queryset = CustomerPolygons.objects.filter(user=self.request.user).order_by('id')

            dataset = get_curent_dataset(self.request.user)
            message = getLogDataRequest(self.request)
            Log.objects.create(user=self.request.user, mode='api', dataset=dataset, action='shapefiles list', message=message)

        return queryset


class ShapeFileDetail(APIView):
    """
    Retrieve a ShapeFile instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, sf_id, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}

        if request.auth:
            try:
                queryset = CustomerPolygons.objects.get(pk=sf_id)
                serializer = CustomerPolygonSerializer(queryset)
                data = serializer.data

                dataset = get_curent_dataset(request.user)
                message = 'SHAPEFILE DETAIL: {}; '.format(queryset)
                message += getLogDataRequest(request)
                Log.objects.create(user=request.user, mode='api', dataset=dataset, action='shapefile detail', message=message)
            except CustomerPolygons.DoesNotExist:
                return Response({'error': 'ShapeFile Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class ShapeFileNameDetail(APIView):
    """
    Retrieve a ShapeFile instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, user, name):
        try:
            return CustomerPolygons.objects.get(user=user, name=name)
        except CustomerPolygons.DoesNotExist:
            # raise Http404
            return {'error': 'Invalid ShapeFile Name'}

    def get(self, request, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}

        if request.auth:
            try:
                queryset = CustomerPolygons.objects.get(
                                user=request.user, name=request.GET['name'])
                serializer = CustomerPolygonSerializer(queryset)
                data = serializer.data

                dataset = get_curent_dataset(request.user)
                message = 'SHAPEFILE NAME DETAIL: {}; '.format(queryset)
                message += getLogDataRequest(request)
                Log.objects.create(user=request.user, mode='api', dataset=dataset, action='shapefile name detail', message=message)
            except Exception:
                return Response({'error': 'Invalid ShapeFile Name'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class TimeSeriesList(viewsets.ReadOnlyModelViewSet):
    """
    List TimeSeries
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TimeSeriesResultSerializer

    def get_queryset(self):
        # queryset = {'auth': 'Need YOUR ACCESS TOKEN'}
        queryset = TimeSeriesResults.objects.none()
        statistics = STATISTICS

        if self.request.auth:
            if 'statistics' in self.request.GET:
                statistics = self.request.GET['statistics'].split(',')

            queryset = TimeSeriesResults.objects.filter(
                            user=self.request.user,
                            stat_code__in=statistics,
                            ).order_by('id')

            dataset = get_curent_dataset(self.request.user)

            message = 'TIMESERIES STATISTIC: {}; '.format(statistics)
            message += getLogDataRequest(self.request)
            Log.objects.create(user=self.request.user, mode='api', dataset=dataset, action='timeseries list', message=message)

        return queryset


# class TimeSeriesList(APIView):
#     """
#     List TimeSeries.
#     """

#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     # authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         data = {'auth': 'Need YOUR ACCESS TOKEN'}

#         if request.auth:
#             queryset = TimeSeriesResults.objects.filter(user=request.user).order_by('id')
#             serializer = TimeSeriesResultSerializer(queryset, many=True)
#             data = serializer.data

#         return Response(data)


class TimeSeriesDetail(APIView):
    """
    Retrieve a DataSet instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, shapefile_id, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}
        statistics = STATISTICS

        if request.auth:
            if 'statistics' in request.GET:
                statistics = request.GET['statistics'].split(',')

            try:
                # dataset = DataSet.objects.get(pk=ds_id)
                queryset = TimeSeriesResults.objects.filter(
                                user=request.user,
                                stat_code__in=statistics,
                                customer_polygons__id=shapefile_id).order_by('id')
                serializer = TimeSeriesResultSerializer(queryset, many=True)
                data = serializer.data

                dataset = get_curent_dataset(request.user)
                message = 'TIMESERIES DETAIL: {} elements; '.format(queryset.count())
                message += 'TIMESERIES STATISTIC: {}; '.format(statistics)
                message += getLogDataRequest(request)
                Log.objects.create(user=request.user, mode='api', dataset=dataset, action='timeseries detail', message=message)
            except TimeSeriesResults.DoesNotExist:
                return Response({'error': 'TimeSeries Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class TimeSeriesNameDetail(APIView):
    """
    Retrieve a DataSet instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}
        statistics = STATISTICS
        queryset = None
        shapefile_name = None
        start_date = None
        end_date = None
        start_date_log = None
        end_date_log = None

        if request.auth:
            if 'statistics' in request.GET:
                statistics = request.GET['statistics'].split(',')
            
            if 'shapefile_name' in request.GET:
                shapefile_name = request.GET['shapefile_name']
                try:
                    queryset = TimeSeriesResults.objects.filter(
                                    user=request.user,
                                    stat_code__in=statistics,
                                    customer_polygons__name=shapefile_name).order_by('id')
                    # serializer = TimeSeriesResultSerializer(queryset, many=True)
                    # data = serializer.data
                # except KeyError:
                except Exception, e:
                    return Response({'error': 'Invalid ShapeFile Name'},
                                    status=status.HTTP_400_BAD_REQUEST)

            if 'start_date' in request.GET:
                start = request.GET['start_date'].split('-')
                start_date_log = request.GET['start_date']
                start_date = date(int(start[0]), int(start[1]), int(start[2]))

            if 'end_date' in request.GET:
                end = request.GET['end_date'].split('-')
                end_date_log = request.GET['end_date']
                end_date = date(int(end[0]), int(end[1]), int(end[2]))

            
            if start_date and end_date:
                try:
                    queryset = queryset.filter(
                                result_date__gte=start_date,
                                result_date__lte=end_date).order_by('result_date')

                    if queryset:
                        serializer = TimeSeriesResultSerializer(queryset, many=True)
                        data = serializer.data
                    else:
                        data = {'status_message': 'Nothing found in this interval'}
                except Exception, e:
                    return Response({'error': e},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif start_date and not end_date:
                return Response({'error': 'The argument "end_date" is not specified'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif not start_date and end_date:
                return Response({'error': 'The argument "start_date" is not specified'},
                                    status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     return Response({'error': 'Invalid attributes in the query'},
            #                         status=status.HTTP_400_BAD_REQUEST)

            dataset = get_curent_dataset(request.user)

            message = 'TIMESERIES NAME DETAIL: {}; '.format(shapefile_name)
            message += 'TIMESERIES STATISTIC: {}; '.format(statistics)

            if start_date_log and end_date_log:
                message += 'TIMESERIES TIME INTERVAL: [from: {} to: {}]; '.format(start_date_log, end_date_log)

            message += getLogDataRequest(request)
            Log.objects.create(user=request.user, mode='api', dataset=dataset, action='timeseries name detail', message=message)

        return Response(data)


class ReportsList(viewsets.ReadOnlyModelViewSet):
    """
    ReportsList List
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportsSerializer

    def get_attributes(self, user):
        list_dirs = []
        shelfdata = ShelfData.objects.all()
        customer_access = CustomerAccess.objects.get(
                            user=self.request.user)
        datasets = DataSet.objects.filter(
                    customer_access=customer_access).order_by('id')
        Reports.objects.filter(user=user).delete()

        for ds in datasets:
            if ds.is_ts:
                list_dirs = getTsResultDirectory(ds)

                for ld in list_dirs:
                    Reports.objects.create(
                        name=ld,
                        user=user,
                        dataset=ds,
                        shelfdata=ds.shelf_data)
            else:
                list_dirs = getResultDirectory(ds, shelfdata)

                for ld in list_dirs:
                    Reports.objects.create(
                        name=ld.attribute_name,
                        user=user,
                        dataset=ds,
                        shelfdata=ld)

    def get_queryset(self):
        queryset = Reports.objects.none()
        self.get_attributes(self.request.user)

        if self.request.auth:
            queryset = Reports.objects.filter(user=self.request.user).order_by('id')

            dataset = get_curent_dataset(self.request.user)
            message = getLogDataRequest(self.request)
            Log.objects.create(user=self.request.user, mode='api', dataset=dataset, action='report list', message=message)

        return queryset


class ReportsDetail(APIView):
    """
    Retrieve a ReportsDetail instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_attributes(self, user):
        list_dirs = []
        shelfdata = ShelfData.objects.all()
        customer_access = CustomerAccess.objects.get(
                            user=self.request.user)
        datasets = DataSet.objects.filter(
                    customer_access=customer_access).order_by('id')
        Reports.objects.filter(user=user).delete()

        for ds in datasets:
            if ds.is_ts:
                list_dirs = getTsResultDirectory(ds)

                for ld in list_dirs:
                    Reports.objects.create(
                        name=ld,
                        user=user,
                        dataset=ds,
                        shelfdata=ds.shelf_data)
            else:
                list_dirs = getResultDirectory(ds, shelfdata)

                for ld in list_dirs:
                    Reports.objects.create(
                        name=ld.attribute_name,
                        user=user,
                        dataset=ds,
                        shelfdata=ld)

    def get(self, request, ds_id, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}
        self.get_attributes(request.user)

        # if request.auth:
        try:
            dataset = DataSet.objects.get(pk=ds_id)
            queryset = Reports.objects.filter(
                        user=request.user,
                        dataset=dataset).order_by('id')
            serializer = ReportsSerializer(queryset, many=True)
            data = serializer.data

            dataset = get_curent_dataset(request.user)
            message = 'DATASET REPORTS DETAIL: {}; '.format(dataset)
            message += getLogDataRequest(request)
            Log.objects.create(user=request.user, mode='api', dataset=dataset, action='reports detail', message=message)
        except Exception, e:
            return Response({'error': 'Reports DataSet Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class UploadFileAoiView(APIView):
    """
    Upload AOI file to the USER KML and User FTP directorys.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    # parser_classes = (FileUploadParser,)

    # def get_object(self, ds_id):
    #     try:
    #         return DataSet.objects.get(pk=ds_id)
    #     except DataSet.DoesNotExist:
    #         return 'Invalid Dataset ID'

    def post(self, request, ds_id, format=None):
        error = ''
        file_name = None
        reports = []
        reports_names = []
        statistic = 'Mean'
        doc_kml = None
        data_queryset = None
        customer_polygon = CustomerPolygons.objects.none()
        urls = []
        data = {'auth error': 'Need YOUR ACCESS TOKEN'}

        if request.auth:
            try:
                dataset = DataSet.objects.get(pk=ds_id)
            except DataSet.DoesNotExist:
                data = {
                    'error': 'DataSet Does Not Exist',
                    'status': status.HTTP_400_BAD_REQUEST
                }
                return Response(data)

            try:
                file_obj = request.FILES['file']
                
                dataset_name = dataset.name.replace(' ', '-')
                file_name = '{}_{}'.format(dataset.name, file_obj.name)
                fl, ext = os.path.splitext(file_name)
                # ds_file_name = '{}_{}'.format(dataset.name, fl)

                scheme = '{0}://'.format(request.scheme)
                absolute_kml_url = os.path.join(scheme, request.get_host(), KML_DIRECTORY, request.user.username)
                absolute_remap_url = os.path.join(scheme, request.get_host(), REMAP_DIRECTORY, request.user.username)

                kml_path_user = os.path.join(KML_PATH, request.user.username)
                ftp_path_user = os.path.join(FTP_PATH, request.user.username)

                path_test_data = os.path.join(ftp_path_user, file_name)

                if not os.path.exists(ftp_path_user):
                    os.makedirs(ftp_path_user)

                if not os.path.exists(kml_path_user):
                    os.makedirs(kml_path_user)

                if os.path.exists(path_test_data):
                    os.remove(path_test_data)
                
                handle_uploaded_file(file_obj, path_test_data)

                # DataPolygons.objects.filter(user=request.user, data_set=dataset,
                #         customer_polygons__name=fl).delete()

                CustomerPolygons.objects.filter(user=request.user,
                        name=fl).delete()

                if 'reports' in request.GET:
                    # reports_list = request.GET['reports'].replace(' ', '')
                    reports_list = request.GET['reports'].replace('+', ' ')
                    reports_list = reports_list.split(',')
                    reports_names = reports_list
                    new_rep = ''

                    # data = {
                    #     'REP GET': request.GET['reports'],
                    #     'REP LIST': reports_list,
                    #     'REP NAME': reports_names,
                    #     'status': status.HTTP_400_BAD_REQUEST,
                    # }

                    # return Response(data)

                    for report in reports_list:
                        if dataset.is_ts:
                            rep_ts = report.split(' ')[:-1]
                            rep_ts = (' ').join(rep_ts)

                            if ShelfData.objects.filter(attribute_name=rep_ts).exists():
                                new_rep = '{0}_'.format(report)
                            else:
                                data = {
                                    'error': 'Attribute does not match selected ShelfData',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                }

                                return Response(data)
                        else:
                            if ShelfData.objects.filter(attribute_name=report).exists():
                                shd_id = ShelfData.objects.filter(attribute_name=report)[0].id
                                new_rep = '{0}_{1}'.format(report, shd_id)
                            else:
                                data = {
                                    'error': 'Attribute does not match selected ShelfData',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                }

                                return Response(data)

                        reports.append(new_rep)
                else:
                    data = {
                        'error': 'For calculations in the body of the request, you must specify a list of reports',
                        'status': status.HTTP_400_BAD_REQUEST,
                    }

                    return Response(data)

                if 'statistic' in request.GET:
                    statistic = request.GET['statistic']

                    # data = {
                    #     'statistic': statistic,
                    #     'status': status.HTTP_400_BAD_REQUEST,
                    # }

                    # return Response(data)

                if ext == '.kmz':
                    zip_file = '{0}.zip'.format(fl)
                    new_kml_file = '{0}.kml'.format(fl)
                    path_zip_file = os.path.join(ftp_path_user, zip_file)
                    path_doc_kml = os.path.join(ftp_path_user, 'doc.kml')
                    path_new_kml = os.path.join(ftp_path_user, new_kml_file)

                    command_copy_to_zip = 'cp {0} {1}'.format(path_test_data, path_zip_file)
                    proc_copy_kml = Popen(command_copy_to_zip, shell=True)
                    proc_copy_kml.wait()

                    zip_create = zipfile.ZipFile(path_zip_file)  
                    zip_create.extractall(ftp_path_user)

                    os.rename(path_doc_kml, path_new_kml)
                    os.remove(path_zip_file)
                    os.remove(path_test_data)

                    # copy new kml file to dataset
                    kml_url = os.path.join(absolute_kml_url, new_kml_file)
                    new_path = os.path.join(kml_path_user, new_kml_file)
                    doc_kml, error = copy_file_kml(path_new_kml, new_path)

                    if error:
                        data = {
                            'filename': file_name,
                            'error': 'Error in the shapefile structure',
                            'status': status.HTTP_400_BAD_REQUEST,
                        }

                        return Response(data)

                    try:
                        count_color = get_count_color()
                        upload_file = new_kml_file
                        calculation_aoi = is_calculation_aoi(doc_kml)
                        info_window = get_info_window(doc_kml, fl, path_new_kml)
                    except Exception, e:
                        data = {
                            'filename': file_name,
                            'error': 'Error in the shapefile structure',
                            'status': status.HTTP_400_BAD_REQUEST,
                        }

                        return Response(data)

                    load_aoi = addPolygonToDB(
                                    fl, new_kml_file, request.user,
                                    new_path, kml_url,
                                    dataset, text_kml=info_window
                                )

                if ext == '.kml':
                    kml_url = os.path.join(absolute_kml_url, file_name)
                    kml_path_file = os.path.join(kml_path_user, file_name)
                    doc_kml, error = copy_file_kml(path_test_data, kml_path_file)

                    if error:
                        data = {
                            'filename': file_name,
                            'error': 'Error in the shapefile structure',
                            'status': status.HTTP_400_BAD_REQUEST,
                        }

                        return Response(data)

                    if not error:
                        count_color = get_count_color()
                        upload_file = file_name
                        calculation_aoi = is_calculation_aoi(doc_kml)
                        info_window = get_info_window(doc_kml, fl, path_test_data)

                    load_aoi = addPolygonToDB(fl, file_name, request.user,
                                    kml_path_file, kml_url,
                                    dataset, text_kml=info_window)

                # Calculations
                if not error and file_name and reports:
                    count_color = get_count_color()
                    data_args = {
                            'upload_file': file_name,
                            'statistic': statistic,
                            'attr': reports
                        }
                    new_info_window, list_attr, list_units,\
                    list_value, list_total, list_total_area = create_new_calculations_aoi(
                                                                request.user, doc_kml, dataset, data_args)
                    area_name = fl
                    outer_coord, inner_coord = get_coord_aoi(doc_kml)
                    data_coord = {
                        'outer_coord': outer_coord,
                        'inner_coord': inner_coord
                    }
                    cur_polygon = createKml(request.user, area_name, new_info_window,
                                            absolute_kml_url, dataset, count_color, data_coord)
                    len_attr = len(reports)

                    DataPolygons.objects.filter(user=request.user, data_set=dataset,
                            customer_polygons=cur_polygon).delete()

                    for n in xrange(len_attr):
                        DataPolygons.objects.create(
                            user=request.user,
                            customer_polygons=cur_polygon,
                            data_set=dataset,
                            attribute=list_attr[n],
                            statistic=statistic,
                            value=list_value[n],
                            units=list_units[n],
                            total=list_total[n],
                            total_area=list_total_area[n]+' ha'
                        )

                    path_kml = os.path.join(KML_PATH, request.user.username, file_name)
                    command_line_copy_kml = 'cp {0} {1}'.format(path_kml, ftp_path_user)
                    proc_copy_kml = Popen(command_line_copy_kml, shell=True)
                    proc_copy_kml.wait()

                    try:
                        if dataset.is_ts:
                            TimeSeriesResults.objects.filter(user=request.user, data_set=dataset,
                                                            customer_polygons=cur_polygon).delete()
                            createUploadTimeSeriesResults(request.user, cur_polygon, reports, dataset)
                    except Exception, e:
                        ###########   log ###############################################################
                        # error_save_kml.write('ERROR GEO: {0}\n'.format(e))
                        # error_save_kml.close()
                        ############################################################################

                        data = {
                            'error': 'Please add the GEO data to create Time Series.',
                            'status': status.HTTP_400_BAD_REQUEST
                        }

                        return Response(data)
                        # return HttpResponseRedirect(u'%s?danger_message=%s' % (
                        #             reverse('files_lister'),
                        #             (u'Please add the GEO data to create Time Series.')))
                

                for n in reports_names:
                    ds_name = dataset.name.replace(' ', '-')
                    report_name = n.replace(' ', '-')
                    file_name = '{0}_{1}_{2}.tif'.format(request.user, ds_name, report_name)
                    absolute_tif_url = os.path.join(absolute_remap_url, file_name)
                    user_remap_path = os.path.join(REMAP_PATH, request.user.username, file_name)

                    if os.path.exists(user_remap_path):
                        urls.append(absolute_tif_url)
                    
            except Exception, e:
                data = {
                    'filename': file_name,
                    'error': 'Error in the shapefile structure',
                    'status': status.HTTP_400_BAD_REQUEST,
                }

                return Response(data)

            try:
                shapefile_name = '{0}.kml'.format(fl)
                queryset_cp = CustomerPolygons.objects.get(
                                user=request.user,
                                name=fl,
                                data_set=dataset,
                                kml_name=shapefile_name
                            )
                customer_polygon = queryset_cp
                if dataset.is_ts:
                    try:
                        queryset_tsr = TimeSeriesResults.objects.filter(
                                        user=request.user,
                                        customer_polygons=queryset_cp).order_by('id')
                        serializer = TimeSeriesResultSerializer(queryset_tsr, many=True)
                        data_queryset = serializer.data
                    except TimeSeriesResults.DoesNotExist:
                        pass
                else:
                    try:
                        serializer = CustomerPolygonSerializer(queryset_cp)
                        data_queryset = serializer.data
                    except Exception:
                        pass
            except CustomerPolygons.DoesNotExist:
                pass

        dataset = get_curent_dataset(request.user)
        message = 'UPLOAD SHAPEFILE: {}'.format(file_name)
        message += getLogDataRequest(request)
        Log.objects.create(user=request.user, mode='api',
            dataset=dataset, action='shapefile created', customer_polygons=customer_polygon, message=message)
            
        
        data = {
            'download links': urls,
            'status': status.HTTP_201_CREATED,
            'result': data_queryset
        }

        return Response(data)


class UploadFileFtpView(APIView):
    """
    Upload file to User FTP directory.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}

        if request.auth:
            file_obj = request.FILES['file']
            file_name = file_obj.name
            ftp_path = os.path.join(FTP_PATH, request.user.username, file_name)
            
            with open(ftp_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    ch = chunk
                    destination.write(chunk)

            dataset = get_curent_dataset(request.user)
            message = 'UPLOAD FILE: {}'.format(file_name)
            message += getLogDataRequest(request)
            Log.objects.create(user=request.user, mode='api', dataset=dataset, action='file uploaded', message=message)
            
            data = {
                'file_name': file_obj.name,
                'status': status.HTTP_201_CREATED,
            }

            return Response(data)


class LogsList(viewsets.ReadOnlyModelViewSet):
    """
    Get Logs list
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = LogSerializer

    def get_queryset(self):
        message = ''
        queryset = Log.objects.none()

        if self.request.auth:
            queryset = Log.objects.filter(user=self.request.user).order_by('at')

            if 'mode' in self.request.GET:
                queryset = queryset.filter(mode=self.request.GET['mode'])
                message += 'MODE: {}; '.format(self.request.GET['mode'])

            if 'action' in self.request.GET:
                queryset = queryset.filter(action=self.request.GET['action'])
                message += 'ACTION: {}; '.format(self.request.GET['action'])

            if 'dataset' in self.request.GET:
                queryset = queryset.filter(dataset__name=self.request.GET['dataset'])
                message += 'DATASET: {}; '.format(self.request.GET['dataset'])

            dataset = get_curent_dataset(self.request.user)
            message += getLogDataRequest(self.request)
            Log.objects.create(user=self.request.user, mode='api', dataset=dataset, action='logs list', message=message)

        return queryset


class LogDetail(APIView):
    """
    Retrieve a ShapeFile instance.
    mode
    dataset
    action
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, log_id, format=None):
        data = {'auth': 'Need YOUR ACCESS TOKEN'}

        if request.auth:
            try:
                queryset = Log.objects.get(pk=log_id)
                serializer = LogSerializer(queryset)
                data = serializer.data

                dataset = get_curent_dataset(request.user)
                message = 'LOG DETAIL: {}; '.format(queryset)
                message += getLogDataRequest(request)
                Log.objects.create(user=request.user, mode='api', dataset=dataset, action='log detail', message=message)
            except CustomerPolygons.DoesNotExist:
                return Response({'error': 'Log Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


        
        
# @api_view(['GET',])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# def terraserver(request):
#     """API to get data from the terraserver."""

#     data = {}
#     shapefile_name = ''
#     customer = request.user
#     data_terraserver = DataTerraserver.objects.none()
    
    
#     path_to_map_images = '/home/gsi/Web_GeoChart/GSiMaps/png'
#     root_url_gsimap = 'http://indy41.epcc.ed.ac.uk/'
#     url_status = status.HTTP_200_OK
    
#     # token = Token.objects.get(user=request.user)
#     # print 'token.key ============================= ', token.key
    
#     # print 'customer ============================= ', customer

#     if request.GET:
#         data_get = request.GET
#         # data = JSONParser().parse(request)
        
#         # print 'data =================== ', data

#         if data_get.get('shapefile', ''):
#             data['shapefile'] = data_get.get('shapefile', '')
#             shapefile_name = data['shapefile'].split('/')[-1]
#             kml_name = shapefile_name.split('.kml')[0]
#             print 'data[shapefile] ============================= ', data['shapefile']
            
#             new_shapefile_name = KML_PATH + '/' + shapefile_name
            
#             print 'new_shapefile_name ============================= ', new_shapefile_name
            
#             url = data['shapefile']
#             urllib.urlretrieve(url, new_shapefile_name)
            
#             data_terraserver, created = DataTerraserver.objects.update_or_create(
#                 user=customer,
#                 shapefile_link=data['shapefile'],
#                 shapefile=shapefile_name)
            
#             obj, created = CustomerPolygons.objects.update_or_create(
#                 user=customer,
#                 name=kml_name,
#                 kml_name=shapefile_name,
#                 kml_path=new_shapefile_name
#             )
#         else:
#             data['message error shapefile'] = 'Invalid or missing the shapefile in the request.'
#             url_status = status.HTTP_400_BAD_REQUEST
            
#         if data_get.get('param', ''):
#             data['param'] = data_get.get('param', '')
#             print 'param ============================= ', data['param']
#             data_terraserver.parameter = data['param']
#             data_terraserver.save()
#         else:
#             data['message error param'] = 'Invalid or missing the parameter in the request.'
#             url_status = status.HTTP_400_BAD_REQUEST
            
#         if data_get.get('transaction_id', ''):
#             data['transaction_id'] = data_get.get('transaction_id', '')
#             data_terraserver.transaction_id = data['transaction_id']
#             data_terraserver.save()
#         else:
#             data['message error transaction_id'] = 'Invalid or missing the transaction ID in the request.'
#             url_status = status.HTTP_400_BAD_REQUEST

#         # send mail
#         if url_status == status.HTTP_200_OK:
#             send_mail('Subject here', 'Here is the message.', 'artgrem@gmail.com',
#             ['artgrem@gmail.com'], fail_silently=False)
        
#         # send_simple_message()
        
#         # '''send email via mailgun'''
#         # subject = "Hello, its me"
#         # text_content = "I was wondering if after all these years"
#         # sender = "artgrem@gmail.com"
#         # receipient = "artgrem@gmail.com"
#         # msg = EmailMultiAlternatives(subject, text_content, sender, [receipient])
#         # respone = msg.send()
        
#         # artgrem@gmail.com

        

#         # if url_status == status.HTTP_200_OK:
#         #     try:
#         #         root, dirs, files = os.walk(path_to_map_images).next()
#         #         data['results'] = []
#         #
#         #         for f in files:
#         #             dict_tmp = {}
#         #             file_without_ext = f.split('.png')[0]
#         #             dict_tmp['file'] = f
#         #             dict_tmp['url'] = root_url_gsimap + 'GSiMap.php?q=images/{0}'.format(file_without_ext)
#         #             dict_tmp['description'] = 'a brief description of the map'
#         #             data['results'].append(dict_tmp)
#         #     except Exception, e:
#         #         data['message error'] = 'No such file or directory: {0}'.format(path_to_map_images)
#         #         url_status = status.HTTP_500_INTERNAL_SERVER_ERROR
#     # elif request.POST:
#     #     data_post = request.POST
#     #     data = JSONParser().parse(request)
#     #
#     #     print 'shapefile =================== ', shapefile
#     #
#     #     if data_post.get('shapefile', ''):
#     #
#     #         print 'shapefile =================== ', shapefile
#     #         url_status = status.HTTP_200_OK
#         # return Response("ok")
#     else:
#         data['message error'] = 'Invalid or missing the parameters for request.'
#         url_status = status.HTTP_400_BAD_REQUEST

#     return Response(data, status=url_status)
    
        
        
