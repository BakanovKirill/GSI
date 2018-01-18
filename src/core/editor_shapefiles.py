# -*- coding: utf-8 -*-
import os
import re
from subprocess import check_call, Popen, PIPE
from datetime import datetime, date, timedelta

from pykml import parser
from lxml import html
from random import randint
import simplekml
from simplekml import Kml

from gsi.settings import (COLOR_HEX_NAME, PROJECTS_PATH, TMP_PATH,
                        SCRIPT_GETPOLYINFO, SCRIPT_REMAP, REMAP_PATH)
from core.get_coordinate_aoi import get_coord_aoi
from customers.models import ShelfData, TimeSeriesResults, CustomerPolygons


# SUB_DIRECTORIES = {
#     'mean_ConditionalMax': 'Max',
#     'mean_ConditionalMean': 'Mean',
#     'mean_ConditionalMedian': 'Median',
#     'mean_ConditionalMin': 'Min',
#     'mean_LowerQuartile': 'LQ',
#     'mean_Quantile': 'UQ',
# }

SUB_DIRECTORIES_REVERCE = {
    'Max': 'mean_ConditionalMax',
    'Mean': 'mean_ConditionalMean',
    'Median': 'mean_ConditionalMedian',
    'Min': 'mean_ConditionalMin',
    'LQ': 'mean_LowerQuartile',
    'UQ': 'mean_Quantile',
}


def get_count_color():
    divider = len(COLOR_HEX_NAME)
    return randint(0, divider)


def copy_file_kml(old_path, new_path):
    error = ''
    doc = ''

    try:
        error = validation_kml(old_path)

        # print '!!!!!!!!!!!!!!! COPY DOC old_path =================== ', old_path
        # print '!!!!!!!!!!!!!!! COPY DOC new_path =================== ', new_path
        # print '!!!!!!!!!!!!!!! COPY DOC ERROR 1 =================== ', error

        if error:
            # print '!!!!!!!!!!!!!!! COPY DOC ERROR 2 =================== ', error
            if os.path.exists(old_path):
                os.remove(old_path)

            return doc, error

        with open(old_path) as f:
            doc = parser.parse(f)

        doc = doc.getroot()
        # print '!!!!!!!!!!!!!!! copy_file_kml DOC =================== ', doc

        command_line = 'cp {0} {1}'.format(old_path, new_path)
        proc = Popen(command_line, shell=True)
        proc.wait()
    except Exception, e:
        error = e
        # print '!!!!!!!!!!!!!!! ERROR copy_file_kml =================== ', e
        # command_line = 'cp {0} {1}'.format(old_path, new_path)
        # proc = Popen(command_line, shell=True)
        # proc.wait()
        # error = str(e)

    return doc, error


def addPolygonToDB(name, kml_name, user, kml_path, kml_url, ds, text_kml=''):
    customer_pol = CustomerPolygons.objects.none()

    CustomerPolygons.objects.filter(
        name=name, user=user, data_set=ds).delete()

    customer_pol = CustomerPolygons.objects.create(
                        name=name,
                        kml_name=kml_name,
                        user=user,
                        data_set=ds,
                        kml_path=kml_path,
                        kml_url=kml_url,
                        text_kml=text_kml
                    )

    return customer_pol


def get_data_kml(path):
    doc = ''
    error = ''

    try:
        with open(path) as f:
            doc = parser.parse(f).getroot()
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR get_data_kml =================== ', e
        error = e

    return doc, error


def delete_empty_lines(file_path):
    # print '!!!!!!!!!!!!!!!!!! delete_empty_lines =========================== ', file_path

    error = ''

    try:
        string = open(file_path).readlines()
        os.remove(file_path)
        new_file_kml = open(file_path, 'w+')

        for i in string:
            if 'xsi:' in i:
                i = i.split('xsi:')
                i = ''.join(i)
            new_line = i

            if not i.isspace():
                new_file_kml.write(i)

        new_file_kml.close()
    except Exception, e:
        error = e

    return error


def validation_kml(kml_path):
    error_msg = ''
    file_name = kml_path.split('/')[-1]
    file_size = os.path.getsize(kml_path)
    updated_file = delete_empty_lines(kml_path)

    try:
        xml = html.parse(kml_path)
        xml_extendeddata = len(xml.xpath("//extendeddata")) / 2
        xml_coordinates = len(xml.xpath("//coordinates")) / 2
        xml_point = len(xml.xpath("//point")) / 2
        xml_polygon = len(xml.xpath("//polygon")) / 2
        xml_placemark = len(xml.xpath("//placemark")) / 2

        if file_size >= 10000000:
            error_msg = 'Error!! An error occurred while loading the file "{0}". \
                        The file size is more than 10Mb'.format(file_name)
            return error_msg

        if xml_extendeddata >= 1000 or xml_coordinates >= 1000 \
            or xml_point >= 1000 or xml_polygon >= 1000 or xml_placemark >= 1000:

            error_msg = 'Error!! An error occurred while loading the file "{0}". \
                        The file has more than 1000 objects'.format(file_name)
            return error_msg

        # try:
        #     schema_ogc = Schema("ogckml22.xsd")
        #     schema_gx = Schema("kml22gx.xsd")

        #     schema_ogc.assertValid(kml_name)
        #     schema_gx.assertValid(kml_name)
        # except Exception, e:
        #     return str(e)
    except Exception, e:
        # print '!!!!!!!!!!!!!!!!!! ERROR VALIDATION KML  =========================== ', e
        return e

    # print '!!!!!!!!!!!!!!!!!!!!!! ERR MESG validation_kml ===================== ', error_msg

    return error_msg


def is_calculation_aoi(doc_kml):
    is_calculation = False
    error = ''

    try:
        if doc_kml.Document.Placemark.Polygon.outerBoundaryIs:
            error = ''
            return True, error
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Document.Placemark.Polygon.outerBoundaryIs  ===================== ', e
        error += 'FALSE CALCULATION AOI: {}\n'.format(e)

    try:
        if doc_kml.Document.Placemark.MultiGeometry.Polygon.outerBoundaryIs:
            error = ''
            return True, error
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Document.MultiGeometry  ===================== ', e
        error += 'FALSE CALCULATION AOI: {}\n'.format(e)

    try:
        if doc_kml.Document.Folder.Placemark.MultiGeometry.Polygon.outerBoundaryIs:
            error = ''
            return True, error
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Document.MultiGeometry  ===================== ', e
        error += 'FALSE CALCULATION AOI: {}\n'.format(e)

    try:
        if doc_kml.Placemark.Polygon.outerBoundaryIs:
            error = ''
            return True, error
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Placemark  ===================== ', e
        error += 'FALSE CALCULATION AOI: {}\n'.format(e)

    try:
        if doc_kml.Placemark.MultiGeometry.Polygon.outerBoundaryIs:
            error = ''
            return True, error
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Placemark.MultiGeometry  ===================== ', e
        error += 'FALSE CALCULATION AOI: {}\n'.format(e)

    print '!!!!!!!!!!!!!!! 2 is_calculation_aoi  ===================== ', is_calculation

    return is_calculation, error


def get_info_window(doc_kml, file_name, path_to_file):
    text = ''
    error_tag_name = ''
    count_color = get_count_color()
    error = validation_kml(path_to_file)
    

    info_window = '<h4 align="center" style="color:{0};"><b>Attribute report: {1}</b></h4>\n'.format(
                        COLOR_HEX_NAME[count_color], file_name)

    if not error:
        try:
            text = doc_kml.Document.name
        except Exception, e:
            # print '!!!!!!!!!!!!!!! ERROR IW Document  ===================== ', e
            error_tag_name += 'ERROR TAG "Document.name": {}\n\n'.format(e)

            try:
                text = doc_kml.Folder.name
            except Exception, e:
                # print '!!!!!!!!!!!!!!! ERROR IW Folder  ===================== ', e
                error_tag_name += 'ERROR TAG "Folder.name": {}\n\n'.format(e)

                try:
                    text = doc_kml.Placemark.name
                except Exception, e:
                    # print '!!!!!!!!!!!!!!! ERROR IW Placemark  ===================== ', e
                    error_tag_name += 'ERROR TAG "Placemark.name": {}\n\n'.format(e)
                    pass

        if text:
            info_window += '<p align="center">{0}</p>'.format(text);

    print '!!!!!!!!!!!!!!! IW get_info_window  ===================== ', info_window

    return info_window, error, error_tag_name


def getUploadListTifFiles(customer, dataset, *args):
    # print '!!!!!!!!!!!!!!!!!!! ARGS ====================== ', args
    # print '!!!!!!!!!!!!!!!!!!! DATASET ====================== ', dataset
    list_files_tif = []
    # list_data_db = []
    # attributes_tmp = {}
    # attributes_reports = {}
    statistic = args[0]['statistic']
    attributes = args[0]['attr']
    upload_file = args[0]['upload_file']

    # for at in attributes:
    #     tmp = at.split('_')
    #     attributes_tmp[tmp[0]] = tmp[1]

    # for n in sorted(attributes_tmp.keys()):
    #     attributes_reports[n] = attributes_tmp[n]

    # attributes_reports = AttributesReport.objects.filter(
    #                         user=customer, data_set=dataset)
                            
    # print '!!!!!!!!!!!!!!!!!!! IS TS ====================== ', dataset.is_ts

    # print '!!!!!!!!!!!!!!!!!!! statistic ====================== ', statistic
    # print '!!!!!!!!!!!!!!!!!!! Attributes ====================== ', attributes
    # print '!!!!!!!!!!!!!!!!!!! attributes_reports ====================== ', attributes_reports
    # print '!!!!!!!!!!!!!!!!!!! upload_file ====================== ', upload_file

    if attributes:
        if dataset.is_ts:
            # attributes_reports = attributes_reports.order_by('attribute')
            # attributes = attributes.sort()
            # attributes_reports = sorted(attributes_reports.keys())
            shelf_data = dataset.shelf_data

            # print '!!!!!!!!!!!!!!!!!!! SHD ====================== ', shelf_data

            # print '!!!!!!!!!!!!!!!!!!! 2 attributes_reports ====================== ', attributes_reports

            for attr in attributes:
                # sub_dir = attr.shelfdata.root_filename + '/' + SUB_DIRECTORIES[attr.statistic]
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory, sub_dir)
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory)

                attr_list = attr.split('_')
                project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)

                # print '!!!!!!!!!! ATTR LIST ========================= ', attr_list
                # print '!!!!!!!!!! sub_dir_path ========================= ', sub_dir_path
                # print '!!!!!!!!!! project_directory ========================= ', project_directory

                try:
                    if os.path.exists(project_directory):
                        pr_root, pr_dirs, pr_files = os.walk(project_directory).next()
                        pr_dirs.sort()

                        # print '!!!!!!!!!! DIRS ========================= ', pr_dirs
                        # print '!!!!!!!!!! project_directory ========================= ', project_directory
                        # print '!!!!!!!!!! attr.attribute ========================= ', attr.attribute

                        for pd in pr_dirs:
                            if pd in attr_list[0]:
                                # attribute_name = attr_list[0].split(' ')[:-1]
                                # attribute_name = str((' ').join(attribute_name))

                                # print '!!!!!!!!!! PD ========================= ', pd
                                # print '!!!!!!!!!! attr.attribute TYPE ========================= ', type(attribute_name)


                                # shd_cur = ShelfData.objects.get(attribute_name=attribute_name)
                                # shd_cur = ShelfData.objects.get(attribute_name='Merchantable Volume of Timber')
                                sub_directory = os.path.join(project_directory, pd, statistic)
                                sub_root, sub_dirs, sub_files = os.walk(sub_directory).next()
                                sub_files.sort()

                                # print '!!!!!!!!!! sub_directory ========================= ', sub_directory

                                for f in sub_files:
                                    fl, ext = os.path.splitext(f)

                                    if ext == '.tif':
                                        fl_tif = os.path.join(sub_directory, f)
                                        # str_data_db = '{0}$$${1}$$$'.format(attr_list[0], fl_tif)
                                        new_fl_tif = '{0}$$${1}$$${2}$$$'.format(shelf_data.id, attr_list[0], fl_tif)
                                        # str_data_db = '{0}$$${1}$$$'.format(shd_cur, fl_tif)

                                        list_files_tif.append(new_fl_tif)
                                        # list_data_db.append(str_data_db)
                                        break
                                break
                        # print '!!!!!!!!!! list_data_db ========================= ', list_data_db
                        # print '!!!!!!!!!! list_files_tif ========================= ', list_files_tif
                except Exception, e:
                    print '!!!!!!!!!! ERROR TS ========================= ', e
        else:
            # attributes_reports = attributes_reports.order_by('shelfdata__attribute_name')
            # attributes_reports = sorted(attributes_reports.keys())

            # print '!!!!!!!!!!!!!!!!!!! 2 attributes_reports ====================== ', attributes_reports
            try:
                for attr in attributes:
                    attr_list = attr.split('_')
                    select_shd = ShelfData.objects.get(id=attr_list[1])
                    name_1 = select_shd.root_filename
                    name_2 = dataset.results_directory.split('/')[0]
                    tif_path = os.path.join(PROJECTS_PATH, dataset.results_directory, name_1)

                    # print '!!!!!!!!!!!!!!!!!!! TIF PATH ====================== ', tif_path

                    fl_tif = '{0}/{1}_{2}.{3}.tif'.format(tif_path, SUB_DIRECTORIES_REVERCE[statistic], name_1, name_2)
                    new_fl_tif = '{0}$$${1}$$${2}$$$'.format(attr_list[1], select_shd.attribute_name, fl_tif)
                    # str_data_db = '{0}$$${1}$$$'.format(attr_list[1], fl_tif)

                    # print '!!!!!!!!!!!!!!!!!!! TIF PATH NAME ====================== ', fl_tif

                    list_files_tif.append(new_fl_tif)
                    # list_data_db.append(str_data_db)
            except Exception, e:
                print '!!!!!!!!!! ERROR ATTR ========================= ', e

    # print '!!!!!!!!!! FILE ========================= ', list_files_tif
    # print '!!!!!!!!!! DATA DB ========================= ', list_data_db

    return list_files_tif


def create_new_calculations_aoi(customer, doc_kml, data_set, *args):
    # print '!!!!!!!!!! create_new_calculations_aoi =================== ', customer

    info_window = ''
    attr_name = ''
    total_area = ''
    units_per_ha = ''
    total = ''
    # count_tif = 0
    list_value = []
    list_attr = []
    list_units = []
    list_total = []
    list_total_area = []

    list_data_kml = []

    # print '!!!!!!!!!!!!!!! ARGS create_new_calculations_aoi  ===================== ', args

    is_ts = data_set.is_ts
    statistic = args[0]['statistic']
    attributes = args[0]['attr']
    upload_file = args[0]['upload_file']
    upload_file = upload_file.split('.kml')[0]
    count_color = get_count_color()
    outer_coord, inner_coord = get_coord_aoi(doc_kml)
    list_file_tif = getUploadListTifFiles(customer, data_set, *args)

    # print '!!!!!!!!!!!!!!! CREATE Outer Coord  ===================== ', outer_coord
    # print '!!!!!!!!!!!!!!! LIST TIF FILES  ===================== ', list_file_tif

    # all_coord = outer_coord + inner_coord
    kml_name ='{0} {1} AREA COORDINATE'.format(customer, data_set)

    # print '!!!!!!!!!!!!!!! ARGS  ===================== ', args
    # print '!!!!!!!!!!!!!!! outer_coord  ===================== ', len(outer_coord)
    # print '!!!!!!!!!!!!!!! all_coord  ===================== ', len(all_coord)

    # COORDINATE
    in_new_calculations_coord = str(customer) + '_in_new_calculations_coord_tmp.kml'
    out_new_calculations_coord = str(customer) + '_out_new_calculations_coord_tmp.txt'
    
    
    file_path_in_new_calculations_coord = os.path.join(TMP_PATH, in_new_calculations_coord)
    file_path_out_new_calculations_coord = os.path.join(TMP_PATH, out_new_calculations_coord)

    

    # print '!!!!!!!!!!!!!!! file_path_in_new_calculations_coord  ===================== ', file_path_in_new_calculations_coord
    # print '!!!!!!!!!!!!!!! file_path_out_new_calculations_coord  ===================== ', file_path_out_new_calculations_coord

    if os.path.exists(file_path_in_new_calculations_coord):
        os.remove(file_path_in_new_calculations_coord)

    if os.path.exists(file_path_out_new_calculations_coord):
        os.remove(file_path_out_new_calculations_coord)

    # print '!!!!!!!!!!!!!!! outer_coord  ===================== ', outer_coord
    # print '!!!!!!!!!!!!!!! LEN outer_coord  ===================== ', len(outer_coord)
    
    # print '!!!!!!!!!!!!!!! list_file_tif  ===================== ', list_file_tif
    

    # if all_coord:
    for file_tif in list_file_tif:
        # *****************************************************************************
        # print '!!!!!!!!!!!!!!! outer_coord [0]  ===================== ', outer_coord[0]

        kml = simplekml.Kml()
        pol = kml.newpolygon(name=kml_name)
        pol.outerboundaryis = outer_coord[0]

        # print '!!!!!!!!!!!!!!! 1 kml_name  ===================== ', kml_name
        # print '!!!!!!!!!!!!!!! 1 file_tif  ===================== ', file_tif
        # print '!!!!!!!!!!!!!!! 1 inner_coord  ===================== ', inner_coord

        if inner_coord:
            pol.innerboundaryis = inner_coord

        # print '!!!!!!!!!!!!!!! 2 file_tif  ===================== ', file_tif

        kml.save(file_path_in_new_calculations_coord)

        # print '!!!!!!!!!!!!!!! 3 file_tif  ===================== ', file_tif
        
        # *****************************************************************************

        # for coord_line in all_coord:
        # kml = simplekml.Kml()
        # # kml.newpoint(name=kml_name, coords=outer_coord[0])  # lon, lat, optional height
        # kml.newpoint(name=kml_name, coords=coord_line)  # lon, lat, optional height
        # kml.save(file_path_in_new_calculations_coord)

        # *****************************************************************************

        # list_file_tif, list_data_db = getUploadListTifFiles(customer, data_set, *args)
        # list_file_tif = getUploadListTifFiles(customer, data_set, *args)
        
        # count_data = 0
        # list_val = []
        # attr_name = []
        # attr_name = ''
        # values = []


    # for file_tif in list_file_tif:
        # print '!!! FILE TIF =========================== ', file_tif

        # shd_id = list_data_db[count_data].split('$$$')[0]
        # scale = ShelfData.objects.get(id=shd_id).scale
        # command_line_ts = ''


        # print '!!!!!!!!!!!!! file_tif  =========================== ', file_tif
        # print '!!!!!!!!!!!!! line_list  =========================== ', line_list

        line_list = file_tif.split('$$$')
        select_shd = ShelfData.objects.get(id=line_list[0])
        attr_name = line_list[1]
        shd_attr_name = attr_name

        # print '!!!!!!!!!!!!! line_list  =========================== ', line_list[2]
        # print '!!!!!!!!!!!!! select_shd  =========================== ', select_shd
        # print '!!!!!!!!!!!!! attr_name  =========================== ', attr_name
        # print '!!!!!!!!!!!!! shd_attr_name  =========================== ', shd_attr_name

        if is_ts:
            shd_attr_name = attr_name.split(' ')[:-1]
            shd_attr_name = (' ').join(shd_attr_name)

        
        # print '!!!!!!!!!!!!! attr_name  =========================== ', attr_name

        # units = ShelfData.objects.get(attribute_name=shd_attr_name).units
        scale = select_shd.scale
        units = select_shd.units

        
        # print '!!! FILE TIF  =========================== ', line_list
        # print '!!! FILE TIF 0  =========================== ', line_list[0]
        # print '!!! FILE TIF 1 =========================== ', line_list[1]

        # out_new_calculations_tif = str(customer) + '_out_new_calculations_tif_tmp'
        new_attr_name = attr_name.replace(' ', '-')
        ds_name = str(data_set.name)
        ds_name = ds_name.replace(' ', '-')
        out_new_calculations_tif = '{0}_{1}_{2}'.format(customer, ds_name, new_attr_name)

        # print '!!! REMAP FILE  =========================== ', out_new_calculations_tif

        file_path_out_new_calculations_tif = os.path.join(REMAP_PATH, str(customer), out_new_calculations_tif)

        # print '!!! REMAP PATH  =========================== ', file_path_out_new_calculations_tif

        path_remap_tif = os.path.join(REMAP_PATH, str(customer))

        if not os.path.exists(path_remap_tif):
            os.makedirs(path_remap_tif)

        command_line = '{0} {1} {2} {3}'.format(
                            SCRIPT_GETPOLYINFO,
                            # file_tif,
                            line_list[2],
                            file_path_in_new_calculations_coord,
                            file_path_out_new_calculations_coord
                        )

        command_line_remap = '{0} {1} {2} {3} {4}'.format(
                            SCRIPT_REMAP,
                            # SCRIPT_GETPOLYINFO,
                            # file_tif,
                            line_list[2],
                            file_path_in_new_calculations_coord,
                            file_path_out_new_calculations_tif,
                            10
                        )

        # print '!!! COMMAND LINE =========================== ', command_line
        # print '!!! FILE =========================== ', f_tif
        proc_script = Popen(command_line, shell=True)
        proc_script.wait()

        proc_script_remap = Popen(command_line_remap, shell=True, stdout=PIPE, stderr=PIPE)
        proc_script_remap.wait()

        output, err = proc_script_remap.communicate()

        ####################### write log file
        log_file = '/home/gsi/LOGS/REMAP.log'
        remap_script = open(log_file, 'w+')
        now = datetime.now()
        remap_script.write('DATE: {0}\n'.format(str(now)))
        remap_script.write('USER: {0}\n'.format(customer))
        remap_script.write('=== COMMAND LINE ====================\n')
        remap_script.write('COMMAND LINE: {0}\n'.format(command_line_remap))
        remap_script.write('=== ERR ====================\n')
        remap_script.write('ERR: {0}\n'.format(err))
        remap_script.write('=== OUT ====================\n')
        remap_script.write('OUT: {0}\n'.format(output))
        remap_script.write('=============================\n')
        remap_script.close()
        #######################

        # count_tif += 1

        # print '!!! COMMAND LINE =========================== ', command_line

        if os.path.exists(file_path_out_new_calculations_coord):
            file_out_coord_open = open(file_path_out_new_calculations_coord)
            new_line_list = []
            

            for line in file_out_coord_open.readlines():
                new_line = line.replace(' ', '')
                new_line = new_line.replace('\n', '')
                # new_line = new_line.replace(',', '$$$')
                new_line_list.append(new_line)
                # print '!!! 1 NEW LINE LIST =========================== ', new_line_list
                # count_data += 1

            new_line_list = new_line_list[:-1]
            count_new_line_list = len(new_line_list)
            # count_line = 0
            list_val = []
            # n_val = []
            # print '!!! 2 NEW LINE LIST =========================== ', new_line_list

            
            for n in new_line_list:
                nl = n.split(',')

                # print '!!! 2 N LIST =========================== ', nl

                per_ha_scale = float(nl[2])
                
                if scale:
                    per_ha_scale = float(nl[2]) / scale

                if len(new_line_list) > 1:
                    # nl = n.split(',')
                    # attr_name.append(nl[0])
                    # new_line[2] = '{0:,}'.format(total_aoi).replace(',', ',')
                    
                    # list_val.append(nl[1])
                    # list_val.append(nl[2])
                    # list_val.append(nl[3])
                    
                    # print '!!!!!!!!!!!!!!!!! TOTAL ======================== ', nl[1]
                    # print '!!!!!!!!!!!!!!!!! TOTAL TYPE ======================== ', type(nl[1])

                    # tot_ar = '{0:,}'.format(float(nl[1])).replace(',', ',')
                    per_ha = '{0:,}'.format(per_ha_scale).replace(',', ',')
                    tot = '{0:,}'.format(float(nl[3])).replace(',', ',')
                    
                    list_val.append(nl[1])
                    list_val.append(per_ha)
                    list_val.append(tot)
                else:
                    # total_area = nl[1]
                    # units_per_ha = nl[2]
                    # total = nl[3]
                    
                    # total_area = '{0:,}'.format(float(nl[1])).replace(',', ',')
                    total_area = nl[1]
                    units_per_ha = '{0:,}'.format(per_ha_scale).replace(',', ',')
                    total = '{0:,}'.format(float(nl[3])).replace(',', ',')

            if list_val:
                # print '!!!!!!!!!!!!!!!!! LIST VAL ======================== ', list_val

                total_area_tmp = float(list_val[0])
                units_per_ha = list_val[1]
                total = list_val[2]
                len_list_val = len(list_val)

                for n in xrange(3, len_list_val, 3):
                    # print '!!!!!!!!!!!!!!! list_val[n] =========================== ', list_val[n]

                    # if (n+3) < len_list_val:
                    total_area_tmp -= float(list_val[n])

                    # print '!!!!!!!!!!!!!!! list_val[n+3] =========================== ', list_val[n]

                # total_area = str(total_area_tmp)
                total_area = '{0:,}'.format(total_area_tmp).replace(',', ',')
                total_area_tmp = 0

            # print '!!!!!!!!!!!!!!! attr_name =========================== ', attr_name
            # print '!!!!!!!!!!!!!!! total_area =========================== ', total_area
            # print '!!!!!!!!!!!!!!! units_per_ha =========================== ', units_per_ha
            # print '!!!!!!!!!!!!!!! total =========================== ', total
            # print '!!!!!!!!!!!!! LIST VAL =========================== ', list_val
            # print '!!!!!!!!!!!!! ATTR NAME =========================== ', attr_name
            
            list_attr.append(attr_name)
            list_units.append(units)
            list_value.append(units_per_ha)
            list_total.append(total)
            list_total_area.append(total_area)

        tmp_info_window = '<tr>';
        tmp_info_window += '<td align="left" style="padding:10px">{0}</td>\n'.format(attr_name)
        tmp_info_window += '<td style="padding:10px">{0}</td>\n'.format(units_per_ha)
        tmp_info_window += '<td style="padding:10px">{0}</td>\n'.format(units)
        tmp_info_window += '<td style="padding:10px">{0}</td>\n'.format(total)
        tmp_info_window += '</tr>\n'
        list_data_kml.append(tmp_info_window)

        # print '!!! total_area =========================== ', total_area
        # print '!!! units_per_ha =========================== ', units_per_ha
        # print '!!! total =========================== ', total
    # print '!!!!!!!!!!!!!!!!!!! list_data_kml =========================== ', list_data_kml


    # try:
    #     try:
    #         name_kml = doc_kml.Document.Placemark.description
    #     except Exception, e:
    #         name_kml = doc_kml.Document.Placemark.name
    # except Exception:
    #     name_kml = ''

    info_window = '<h4 align="center" style="color:{0};"><b>Attribute report: {1}</b></h4>\n'.format(
                                                COLOR_HEX_NAME[count_color], upload_file)
    info_window += '<p align="center"><span><b>Total Area:</b></span> {0} ha</p>'.format(total_area)
    info_window += '<p align="center"><span><b>Values:</b></span> {0}</p>'.format(SUB_DIRECTORIES_REVERCE[statistic])
    info_window += '<div style="overflow:auto;" class="ui-widget-content">'

    info_window += '<table border="1" cellspacing="5" cellpadding="5" style="border-collapse:collapse;border:1px solid black;width:100%;">\n'
    info_window += '<thead>\n'
    info_window += '<tr bgcolor="#CFCFCF">\n'
    info_window += '<th align="left" style="padding:10px">Attribute</th>\n'
    info_window += '<th style="padding:10px">Units per Hectare</th>\n'
    info_window += '<th style="padding:10px">Units</th>\n'
    info_window += '<th style="padding:10px">Total</th>\n'
    info_window += '</tr>\n'
    info_window += '</thead>\n'
    info_window += '<tbody>\n'

    # print '!!!!!!!!!!!!!!!!!!!!!!!! list_data_kml ================================= ', list_data_kml

    for n in xrange(len(list_data_kml)):
        if n % 2 == 0:
            info_window += '<tr bgcolor="#F5F5F5">\n'
        else:
            info_window += '<tr>';

        info_window += list_data_kml[n]
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(list_value[n])



        # info_window += '<td align="left" style="padding:10px">{0}</td>\n'.format(attribute[n])
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(value[n])
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(units[n])
        # info_window += '<td style="padding:10px">{0}</td>\n'.format(total[n])

        # info_window += '</tr>\n'

    info_window += '</tbody>\n'
    info_window += '</table>\n'
    info_window += '</div>'

    # print '!!!!!!!!!!!! info_window =========================== ', info_window

    return info_window, list_attr, list_units, list_value, list_total, list_total_area


def createUploadTimeSeriesResults(customer, aoi, attributes, data_set):
    # list_files_tif = []
    # list_data_db = []

    # print '!!!!!!!!!!!!!!!!!!!! USER =============================== ', customer
    # print '!!!!!!!!!!!!!!!!!!!! AOI =============================== ', aoi
    # print '!!!!!!!!!!!!!!!!!!!! ATTR =============================== ', attributes

    project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory)
    # attributes_reports = AttributesReport.objects.filter(
    #                         user=aoi.user, data_set=aoi.data_set
    #                     ).order_by('attribute')

    in_new_calculations_coord = str(customer) + '_in_new_calculations_coord_tmp.kml'
    out_new_calculations_coord = str(customer) + '_out_new_calculations_coord_tmp.txt'
    
    file_path_in_new_calculations_coord = os.path.join(TMP_PATH, in_new_calculations_coord)
    file_path_out_new_calculations_coord = os.path.join(TMP_PATH, out_new_calculations_coord)

    # attributes_reports = AttributesReport.objects.filter(
    #                         user=aoi.user, data_set=aoi.data_set
    #                     ).order_by('shelfdata__attribute_name')

    # print '!!!!!!!!!!!!!!!!!! ATTRIBUTES REPORTS ================================ ', attributes_reports

    for attr in attributes:
        cur_attr = (attr).split('_')[0]
        result_year = (cur_attr).split(' ')[-1]

        # result_year = attr.shelfdata.root_filename
        # sub_dir_name = SUB_DIRECTORIES[attr.statistic]
        # sub_dir = result_year + '/' + sub_dir_name
        
        project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory, result_year)

        # project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory, result_year)
        # project_directory = os.path.join(PROJECTS_PATH, aoi.data_set.results_directory, sub_dir)

        # print '!!!!!!! YEAR ========================== ', result_year
        # print '!!!!!!! DIR YEAR ========================== ', project_directory
        # print '!!!!!!! YES DIR YEAR ========================== ', os.path.exists(project_directory)

        # project_directory = os.path.join(sub_dir_path)

        if os.path.exists(project_directory):
            root_year, dirs_year, files_year = os.walk(project_directory).next()
            dirs_year.sort()
            # files.sort()

            for d in dirs_year:
                sub_dir_name = d
                project_directory_year = os.path.join(project_directory, d)
                sub_root, sub_dirs, sub_files = os.walk(project_directory_year).next()
                sub_dirs.sort()
                sub_files.sort()

                for f in sub_files:
                    fl, ext = os.path.splitext(f)

                    # print '!!!!!!! FILE ========================== ', f

                    if ext == '.tif':
                        file_ts_tif = os.path.join(project_directory_year, f)
                        
                        try:
                            ts_day = f.split(result_year+'_')[1]

                            # print '!!!!!!! 1 DAY  ========================== ', ts_day

                            ts_day = ts_day.split('_')[0]

                            # print '!!!!!!! 2 DAY  ========================== ', ts_day

                            ts_date = date(int(result_year), 1, 1)
                            ts_delta = timedelta(days=int(ts_day)-1)
                            result_date = ts_date + ts_delta
                            ts_name = '{0}_{1}_{2}_{3}'.format(aoi.name, result_year, sub_dir_name, ts_day)
                            ts_value = '0'

                            command_line_ts = '{0} {1} {2} {3}'.format(
                                                    SCRIPT_GETPOLYINFO,
                                                    file_ts_tif,
                                                    file_path_in_new_calculations_coord,
                                                    file_path_out_new_calculations_coord
                                                )

                            proc_script = Popen(command_line_ts, shell=True)
                            proc_script.wait()

                            file_out_coord_open = open(file_path_out_new_calculations_coord)

                            for line in file_out_coord_open.readlines():
                                new_line = line.replace(' ', '')
                                new_line = new_line.replace('\n', '')
                            
                                # print '!!!!!!! 1 NEW LINE ========================== ', new_line

                                if new_line:
                                    ts_value = new_line.split(',')[2]
                                    scale = data_set.shelf_data.scale

                                    # print '!!!!!!! 1 NEW LINE ========================== ', new_line

                                    if scale:
                                        ts_value = str(float(ts_value) / scale)

                                    # print '!!!!!!! 2 NEW LINE ========================== ', new_line
                                    
                            addUploadTsToDB(ts_name, aoi.user, aoi.data_set, aoi, result_year,
                                        sub_dir_name, result_date, ts_value, cur_attr)

                            # list_files_tif.append(fl_tif)
                            # list_data_db.append(str_data_db)

                            # print '!!!!!!!!!! DAY ========================= ', ts_day
                            # print '!!!!!!!!!! DATE ========================= ', result_date
                        except Exception, e:
                            print '!!!!!!!!!!!!!!! ERROR INDEX ==================== ', e
                            pass


def addUploadTsToDB(name, customer, data_set, customer_polygons, result_year,
                stat_code, result_date, value_of_time_series, attribute):
    if TimeSeriesResults.objects.filter(name=name, user=customer, data_set=data_set).exists():
        ts_obj = TimeSeriesResults.objects.filter(name=name, user=customer, data_set=data_set).delete()

    ts_obj = TimeSeriesResults.objects.create(
        name=name, user=customer, data_set=data_set,
        customer_polygons=customer_polygons,
        result_year=result_year, stat_code=stat_code,
        result_date=result_date,
        value_of_time_series=value_of_time_series,
        attribute=attribute
    )
    ts_obj.save()
