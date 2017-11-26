# -*- coding: utf-8 -*-
import os
from subprocess import check_call, Popen, PIPE

from pykml import parser
from lxml import html
from random import randint
import simplekml
from simplekml import Kml

from gsi.settings import COLOR_HEX_NAME, PROJECTS_PATH, TMP_PATH, SCRIPT_GETPOLYINFO
from core.get_coordinate_aoi import get_coord_aoi
from customers.models import ShelfData


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
        error = validation_kml(doc, old_path)

        # print '!!!!!!!!!!!!!!! COPY DOC ERROR =================== ', error

        if error:
            if os.path.exists(old_path):
                os.remove(old_path)
            return doc, error

        with open(old_path) as f:
            doc = parser.parse(f).getroot()

        command_line = 'cp {0} {1}'.format(old_path, new_path)
        proc = Popen(command_line, shell=True)
        proc.wait()
    except Exception, e:
        error = e
        print '!!!!!!!!!!!!!!! ERROR copy_file_kml =================== ', e
        # command_line = 'cp {0} {1}'.format(old_path, new_path)
        # proc = Popen(command_line, shell=True)
        # proc.wait()
        # error = str(e)

    return doc, error


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


def validation_kml(kml_name, kml_path):
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
        print '!!!!!!!!!!!!!!!!!! ERROR VALIDATION KML  =========================== ', e
        return e

    # print '!!!!!!!!!!!!!!!!!!!!!! ERR MESG validation_kml ===================== ', error_msg

    return error_msg


def is_calculation_aoi(doc_kml):
    is_calculation = False

    try:
        if doc_kml.Document.Placemark.Polygon.outerBoundaryIs:
            return True
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Document  ===================== ', e

    try:
        if doc_kml.Document.Placemark.MultiGeometry.Polygon.outerBoundaryIs:
            return True
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Document.MultiGeometry  ===================== ', e

    try:
        if doc_kml.Document.Folder.Placemark.MultiGeometry.Polygon.outerBoundaryIs:
            return True
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Document.MultiGeometry  ===================== ', e

    try:
        if doc_kml.Placemark.Polygon.outerBoundaryIs:
            return True
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Placemark  ===================== ', e

    try:
        if doc_kml.Placemark.MultiGeometry.Polygon.outerBoundaryIs:
            return True
    except Exception, e:
        print '!!!!!!!!!!!!!!! ERROR KML Placemark.MultiGeometry  ===================== ', e

    # print '!!!!!!!!!!!!!!! 2 is_calculation_aoi  ===================== ', is_calculation

    return is_calculation


def get_info_window(doc_kml, file_name, path_to_file):
    text = ''
    count_color = get_count_color()
    error = validation_kml(doc_kml, path_to_file)
    

    info_window = '<h4 align="center" style="color:{0};"><b>Attribute report: {1}</b></h4>\n'.format(
                        COLOR_HEX_NAME[count_color], file_name)

    if not error:
        try:
            text = doc_kml.Document.name
        except Exception, e:
            # print '!!!!!!!!!!!!!!! ERROR IW Document  ===================== ', e
            try:
                text = doc_kml.Folder.name
            except Exception, e:
                # print '!!!!!!!!!!!!!!! ERROR IW Folder  ===================== ', e
                try:
                    text = doc_kml.Placemark.name
                except Exception, e:
                    # print '!!!!!!!!!!!!!!! ERROR IW Placemark  ===================== ', e
                    pass

        if text:
            info_window += '<p align="center">{0}</p>'.format(text);

    print '!!!!!!!!!!!!!!! IW get_info_window  ===================== ', info_window

    return info_window


def getUploadListTifFiles(customer, dataset, *args):
    # print '!!!!!!!!!!!!!!!!!!! args ====================== ', args
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
                            
    # print '!!!!!!!!!!!!!!!!!!! attributes_tmp ====================== ', attributes_tmp

    # print '!!!!!!!!!!!!!!!!!!! statistic ====================== ', statistic
    # print '!!!!!!!!!!!!!!!!!!! attributes ====================== ', attributes
    # print '!!!!!!!!!!!!!!!!!!! attributes_reports ====================== ', attributes_reports
    # print '!!!!!!!!!!!!!!!!!!! upload_file ====================== ', upload_file

    if attributes:
        if dataset.is_ts:
            # attributes_reports = attributes_reports.order_by('attribute')
            # attributes = attributes.sort()
            # attributes_reports = sorted(attributes_reports.keys())

            # print '!!!!!!!!!!!!!!!!!!! 2 attributes_reports ====================== ', attributes_reports

            for attr in attributes:
                # sub_dir = attr.shelfdata.root_filename + '/' + SUB_DIRECTORIES[attr.statistic]
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory, sub_dir)
                # sub_dir_path = os.path.join(PROJECTS_PATH, dataset.results_directory)

                attr_list = attr.split('_')
                project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)

                # print '!!!!!!!!!! attr_list ========================= ', attr_list
                # print '!!!!!!!!!! sub_dir_path ========================= ', sub_dir_path
                # print '!!!!!!!!!! project_directory ========================= ', project_directory

                try:
                    if os.path.exists(project_directory):
                        pr_root, pr_dirs, pr_files = os.walk(project_directory).next()
                        pr_dirs.sort()

                        # print '!!!!!!!!!! project_directory ========================= ', project_directory
                        # print '!!!!!!!!!! attr.attribute ========================= ', attr.attribute

                        for pd in pr_dirs:
                            if pd in attr_list[0]:
                                # attribute_name = attr_list[0].split(' ')[:-1]
                                # attribute_name = str((' ').join(attribute_name))

                                # print '!!!!!!!!!! attr.attribute ========================= ', attribute_name
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
                                        new_fl_tif = '{0}$$${1}$$$'.format(attr_list[0], fl_tif)
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

            for attr in attributes:
                attr_list = attr.split('_')
                select_shd = ShelfData.objects.get(id=attr_list[1])
                name_1 = select_shd.root_filename
                name_2 = dataset.results_directory.split('/')[0]
                tif_path = os.path.join(PROJECTS_PATH, dataset.results_directory, name_1)

                # print '!!!!!!!!!!!!!!!!!!! TIF PATH ====================== ', tif_path

                fl_tif = '{0}/{1}_{2}.{3}.tif'.format(tif_path, SUB_DIRECTORIES_REVERCE[statistic], name_1, name_2)
                new_fl_tif = '{0}$$${1}$$$'.format(select_shd.attribute_name, fl_tif)
                # str_data_db = '{0}$$${1}$$$'.format(attr_list[1], fl_tif)

                # print '!!!!!!!!!!!!!!!!!!! TIF PATH NAME ====================== ', fl_tif

                list_files_tif.append(new_fl_tif)
                # list_data_db.append(str_data_db)

    # print '!!!!!!!!!! FILE ========================= ', list_files_tif
    # print '!!!!!!!!!! DATA DB ========================= ', list_data_db

    return list_files_tif


def create_new_calculations_aoi(customer, doc_kml, data_set, *args):
    # print '!!!!!!!!!! create_new_calculations_aoi ========================= '

    info_window = ''
    attr_name = ''
    total_area = ''
    units_per_ha = ''
    total = ''
    list_value = []
    list_attr = []
    list_units = []
    list_total = []
    list_total_area = []

    list_data_kml = []

    # print '!!!!!!!!!!!!!!! ARGS  ===================== ', args

    is_ts = data_set.is_ts
    statistic = args[0]['statistic']
    attributes = args[0]['attr']
    upload_file = args[0]['upload_file']
    upload_file = upload_file.split('.kml')[0]
    count_color = get_count_color()
    outer_coord, inner_coord = get_coord_aoi(doc_kml)
    list_file_tif = getUploadListTifFiles(customer, data_set, *args)

    # print '!!!!!!!!!!!!!!! CREATE Outer Coord  ===================== ', outer_coord

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

    print '!!!!!!!!!!!!!!! outer_coord  ===================== ', outer_coord
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
        attr_name = line_list[0]
        shd_attr_name = attr_name

        # print '!!!!!!!!!!!!! line_list  =========================== ', line_list

        if is_ts:
            shd_attr_name = attr_name.split(' ')[:-1]
            shd_attr_name = (' ').join(shd_attr_name)

        
        # print '!!!!!!!!!!!!! attr_name  =========================== ', attr_name

        units = ShelfData.objects.get(attribute_name=shd_attr_name).units

        
        # print '!!! FILE TIF  =========================== ', line_list
        # print '!!! FILE TIF 0  =========================== ', line_list[0]
        # print '!!! FILE TIF 1 =========================== ', line_list[1]

        command_line = '{0} {1} {2} {3}'.format(
                            SCRIPT_GETPOLYINFO,
                            # file_tif,
                            line_list[1],
                            file_path_in_new_calculations_coord,
                            file_path_out_new_calculations_coord
                        )

        # print '!!! COMMAND LINE =========================== ', command_line
        # print '!!! FILE =========================== ', f_tif
        proc_script = Popen(command_line, shell=True)
        proc_script.wait()

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
                    per_ha = '{0:,}'.format(float(nl[2])).replace(',', ',')
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
                    units_per_ha = '{0:,}'.format(float(nl[2])).replace(',', ',')
                    total = '{0:,}'.format(float(nl[3])).replace(',', ',')

            if list_val:
                # print '!!!!!!!!!!!!!!!!! LIST VAL ======================== ', list_val

                total_area_tmp = float(list_val[0])
                units_per_ha = list_val[1]
                total = list_val[2]
                len_list_val = len(list_val)

                for n in xrange(3, len_list_val, 3):
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
