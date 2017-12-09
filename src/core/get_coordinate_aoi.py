# -*- coding: utf-8 -*-
import os
from lxml import html

from gsi.settings import FTP_PATH


# get_coord_document_placemark_polygon_outerboundaryIs(doc)
# get_coord_document_placemark_multigeometry_polygon_outerboundaryIs(doc)
# get_coord_placemark_polygon_outerboundaryIs(doc)
# get_coord_placemark_multigeometry_polygon_outerboundaryIs(doc)
# 
# get_coord_document_placemark_polygon_innerboundaryIs(doc)
# get_coord_placemark_polygon_innerboundaryIs(doc)

# xml = html.parse(two_folder)
# xml_outerboundaryis = xml.xpath("//outerboundaryis")

# path_kml_user = os.path.join(KML_PATH, customer.username)


def get_coord_aoi(doc):
    outer_coord = []
    inner_coord = []
    # count_outer = get_count_outerboundaryis(customer, file_name)

    # UOTER COORD
    outer_coord, error = get_coord_document_placemark_polygon_outerboundaryIs(doc)

    if error:
        outer_coord, error = get_coord_document_placemark_multigeometry_polygon_outerboundaryIs(doc)

        if error:
            outer_coord, error = get_coord_document_folder_placemark_multigeometry_polygon_outerboundaryIs(doc)

            if error:
                outer_coord, error = get_coord_placemark_polygon_outerboundaryIs(doc)

                if error:
                    outer_coord, error = get_coord_placemark_multigeometry_polygon_outerboundaryIs(doc)

    # INNER COORD
    inner_coord, error = get_coord_document_placemark_polygon_innerboundaryIs(doc)

    if error:
        inner_coord, error = get_coord_placemark_polygon_innerboundaryIs(doc)

    print '!!!!!!!!!!!!!!!! TMP outer_coord ======================== ', outer_coord
    print '!!!!!!!!!!!!!!!! TMP inner_coord ======================== ', inner_coord

    return outer_coord, inner_coord


# UOTER COORD
def get_coord_document_placemark_polygon_outerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_document_placemark_polygon_outerboundaryIs =============================='
    
    outer_coord = []
    error = ''

    try:
        outer_boundary_is = doc_kml.Document.Placemark.Polygon.outerBoundaryIs
        # inner_boundary_is = doc_kml.Document.Placemark.Polygon.innerBoundaryIs

        for n in xrange(len(outer_boundary_is)):
            tmp_tuples = []
            tmp = []
            doc_tmp_list = str(doc_kml.Document.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)
            # print '!!!!!!!!!!!!!!!! DOC TMP LIST ======================== ', doc_tmp_list
            
            for n in doc_tmp_list:
                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n
                n = n.replace(',0.0', '')
                n = n.replace('\t', '')

                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                if n:
                    tmp.append(n)

            # print '!!!!!!!!!!!!!!!! TMP  ======================== ', tmp

            if len(tmp) == 1:
                tmp_copy = []
                tmp_list = tmp[0].split(' ')

                # print '!!!!!!!!!!!!!!!! TMP LIST Document ======================== ', tmp_list

                for m in tmp_list:
                    m = m.replace('\t', '')

                    if m:
                        m_split = m.split(',')

                        # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                        if m_split[-1] == '0.0' or m_split[-1] == '0':
                            tmp_copy.append(tuple(m_split[:-1]))
                        else:
                            tmp_copy.append(tuple(m_split))

                # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                outer_coord.append(tmp_copy)

                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            else:
                if not tmp[0]:
                    tmp = tmp[1:]

                if not tmp[-1]:
                    tmp = tmp[:-1]

                for m in tmp:
                    if m:
                        # print '!!!!!!!!!!!!!!!! LINE M ======================== ', m
                        line = m.split(',')
                        tmp_tuples.append(tuple(line))

                        # print '!!!!!!!!!!!!!!!! LINE ======================== ', line

                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                
                outer_coord.append(tmp_tuples)
                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR outer_coord Document ========================== ', e
        error = e

    return outer_coord, error


def get_coord_document_placemark_multigeometry_polygon_outerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_document_placemark_multigeometry_polygon_outerboundaryIs =============================='

    outer_coord = []
    error = ''

    try:
        outer_boundary_is = doc_kml.Document.Placemark.MultiGeometry.Polygon.outerBoundaryIs

        # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(outer_boundary_is)

        for n in xrange(len(outer_boundary_is)):
            tmp_tuples = []
            tmp = []
            doc_tmp_list = str(doc_kml.Document.Placemark.MultiGeometry.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)
            # print '!!!!!!!!!!!!!!!! DOC TMP LIST ======================== ', doc_tmp_list
            
            for n in doc_tmp_list:
                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n
                n = n.replace(',0.0', '')
                n = n.replace('\t', '')

                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                if n:
                    tmp.append(n)

            # print '!!!!!!!!!!!!!!!! TMP  ======================== ', tmp

            if len(tmp) == 1:
                tmp_copy = []
                tmp_list = tmp[0].split(' ')

                # print '!!!!!!!!!!!!!!!! TMP LIST Document ======================== ', tmp_list

                for m in tmp_list:
                    m = m.replace('\t', '')

                    if m:
                        m_split = m.split(',')

                        # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                        if m_split[-1] == '0.0' or m_split[-1] == '0':
                            tmp_copy.append(tuple(m_split[:-1]))
                        else:
                            tmp_copy.append(tuple(m_split))

                # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                outer_coord.append(tmp_copy)

                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            else:
                if not tmp[0]:
                    tmp = tmp[1:]

                if not tmp[-1]:
                    tmp = tmp[:-1]

                for m in tmp:
                    if m:
                        # print '!!!!!!!!!!!!!!!! LINE M ======================== ', m
                        line = m.split(',')
                        tmp_tuples.append(tuple(line))

                        # print '!!!!!!!!!!!!!!!! LINE ======================== ', line

                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                
                outer_coord.append(tmp_tuples)
                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR outer_coord Document.MultiGeometry ========================== ', e
        error = e

    return outer_coord, error


def get_coord_document_folder_placemark_multigeometry_polygon_outerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_document_folder_placemark_multigeometry_polygon_outerboundaryIs =============================='

    coord = {}
    outer_coord = []
    inner_coord = []
    error = ''

    try:
        placemark = doc_kml.Document.Folder.Placemark
        count_area = len(placemark)

        # print '!!!!!!!!!!!!!!!! COUNT AREA ======================== ', count_area

        for m in xrange(count_area):
            outer_boundary_is = doc_kml.Document.Folder.Placemark[m].MultiGeometry.Polygon.outerBoundaryIs

            try:
                inner_boundary_is = doc_kml.Document.Folder.Placemark[m].MultiGeometry.Polygon.innerBoundaryIs
            except Exception:
                pass

            for n in xrange(len(outer_boundary_is)):
                tmp_tuples = []
                tmp = []
                doc_tmp_list = str(doc_kml.Document.Folder.Placemark[m].MultiGeometry.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

                # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! DOC TMP LIST ======================== ', doc_tmp_list
                
                for n in doc_tmp_list:
                    # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n
                    n = n.replace(',0.0', '')
                    n = n.replace('\t', '')

                    # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                    if n:
                        tmp.append(n)

                # print '!!!!!!!!!!!!!!!! TMP  ======================== ', tmp

                if len(tmp) == 1:
                    tmp_copy = []
                    tmp_list = tmp[0].split(' ')

                    # print '!!!!!!!!!!!!!!!! TMP LIST Document ======================== ', tmp_list

                    for m in tmp_list:
                        m = m.replace('\t', '')

                        if m:
                            m_split = m.split(',')

                            # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                            if m_split[-1] == '0.0' or m_split[-1] == '0':
                                tmp_copy.append(tuple(m_split[:-1]))
                            else:
                                tmp_copy.append(tuple(m_split))

                    # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                    outer_coord.append(tmp_copy)

                    # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
                else:
                    if not tmp[0]:
                        tmp = tmp[1:]

                    if not tmp[-1]:
                        tmp = tmp[:-1]

                    for m in tmp:
                        if m:
                            # print '!!!!!!!!!!!!!!!! LINE M ======================== ', m
                            line = m.split(',')
                            tmp_tuples.append(tuple(line))

                            # print '!!!!!!!!!!!!!!!! LINE ======================== ', line

                    # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                    # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                    
                    outer_coord.append(tmp_tuples)
                    # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            # print '!!!!!!!!!!!!!!!!!!!! TMP OUTER ============================== ', tmp_outer_coord
            # outer_coord.append(tmp_outer_coord)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR get_coord_document_folder_placemark_multigeometry_polygon_outerboundaryIs ========================== ', e
        error = e

    return outer_coord, error


def get_coord_placemark_polygon_outerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_placemark_polygon_outerboundaryIs =============================='

    outer_coord = []
    error = ''

    try:
        outer_boundary_is = doc_kml.Placemark.Polygon.outerBoundaryIs

        # print '!!!!!!!!!!!!!!!! TMP outer_boundary_is ======================== ', len(outer_boundary_is)

        for n in xrange(len(outer_boundary_is)):
            tmp_tuples = []
            tmp = []
            doc_tmp_list = str(doc_kml.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

            for n in doc_tmp_list:
                n = n.replace(',0.0', '')
                n = n.replace('\t', '')

                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                if n:
                    tmp.append(n)

            # print '!!!!!!!!!!!!!!!! TMP ======================== ', tmp
            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)

            if len(tmp) == 1:
                tmp_copy = []
                tmp_list = tmp[0].split(' ')

                # print '!!!!!!!!!!!!!!!! TMP LIST Placemark ======================== ', tmp_list

                for m in tmp_list:
                    m = m.replace('\t', '')

                    if m:
                        m_split = m.split(',')

                        # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                        if m_split[-1] == '0.0' or m_split[-1] == '0':
                            tmp_copy.append(tuple(m_split[:-1]))
                        else:
                            tmp_copy.append(tuple(m_split))

                # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                outer_coord.append(tmp_copy)

                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            else:
                if not tmp[0]:
                    tmp = tmp[1:]

                if not tmp[-1]:
                    tmp = tmp[:-1]

                for m in tmp:
                    if m:
                        line = m.split(',')
                        tmp_tuples.append(tuple(line))

                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                
                outer_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR outer_coord Placemark ========================== ', e
        error = e

    return outer_coord, error


def get_coord_placemark_multigeometry_polygon_outerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_placemark_multigeometry_polygon_outerboundaryIs =============================='

    outer_coord = []
    error = ''

    try:
        outer_boundary_is = doc_kml.Placemark.MultiGeometry.Polygon.outerBoundaryIs

        # print '!!!!!!!!!!!!!!!! TMP outer_boundary_is ======================== ', len(outer_boundary_is)

        for n in xrange(len(outer_boundary_is)):
            tmp_tuples = []
            tmp = []
            doc_tmp_list = str(doc_kml.Placemark.Polygon.outerBoundaryIs[n].LinearRing.coordinates).split('\n')

            for n in doc_tmp_list:
                n = n.replace(',0.0', '')
                n = n.replace('\t', '')

                # print '!!!!!!!!!!!!!!!! TMP N ======================== ', n

                if n:
                    tmp.append(n)

            # print '!!!!!!!!!!!!!!!! TMP ======================== ', tmp
            # print '!!!!!!!!!!!!!!!! TMP LEN ======================== ', len(tmp)

            if len(tmp) == 1:
                tmp_copy = []
                tmp_list = tmp[0].split(' ')

                # print '!!!!!!!!!!!!!!!! TMP LIST Placemark ======================== ', tmp_list

                for m in tmp_list:
                    m = m.replace('\t', '')

                    if m:
                        m_split = m.split(',')

                        # print '!!!!!!!!!!!!!!!! M SPLIT ======================== ', m_split

                        if m_split[-1] == '0.0' or m_split[-1] == '0':
                            tmp_copy.append(tuple(m_split[:-1]))
                        else:
                            tmp_copy.append(tuple(m_split))

                # print '!!!!!!!!!!!!!!!! TMP COPY ======================== ', tmp_copy

                outer_coord.append(tmp_copy)

                # print '!!!!!!!!!!!!!!!! outer_coord ======================== ', outer_coord
            else:
                if not tmp[0]:
                    tmp = tmp[1:]

                if not tmp[-1]:
                    tmp = tmp[:-1]

                for m in tmp:
                    if m:
                        line = m.split(',')
                        tmp_tuples.append(tuple(line))

                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', len(tmp)
                # print '!!!!!!!!!!!!!!!! outer_boundary_is ======================== ', tmp_tuples
                
                outer_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR outer_coord Placemark.MultiGeometry ========================== ', e
        error = e

    return outer_coord, error


# INNER COORD
def get_coord_document_placemark_polygon_innerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_document_placemark_polygon_innerboundaryIs =============================='

    inner_coord = []
    error = ''

    try:
        inner_boundary_is = doc_kml.Document.Placemark.Polygon.innerBoundaryIs

        for n in xrange(len(inner_boundary_is)):
            tmp_tuples = []
            tmp = str(inner_boundary_is[n].LinearRing.coordinates).split('\n')

            # print '!!!!!!!!!!!!!!!!! TMP -1 ========================== ', tmp[-1]

            if not tmp[0]:
                tmp = tmp[1:]

            if not tmp[-1]:
                tmp = tmp[:-1]

            for m in tmp:
                m = m.replace('\t', '')

                # print '!!!!!!!!!!!!!!!!! M ========================== ', m

                if m:
                    line = m.split(',')
                    tmp_tuples.append(tuple(line))

            inner_coord.append(tmp_tuples)

            # print '!!!!!!!!!!!!!!!!! M tmp_tuples ========================== ', tmp_tuples
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR inner_coord Document ========================== ', e
        error = e

    return inner_coord, error


def get_coord_placemark_polygon_innerboundaryIs(doc_kml):
    # print '!!!!!!!!!!!!!!!!!!!! get_coord_placemark_polygon_innerboundaryIs =============================='

    inner_coord = []
    error = ''

    try:
        inner_boundary_is = doc_kml.Placemark.Polygon.innerBoundaryIs

        for n in xrange(len(inner_boundary_is)):
            tmp_tuples = []
            tmp = str(inner_boundary_is[n].LinearRing.coordinates).split('\n')

            if not tmp[0]:
                tmp = tmp[1:]

            if not tmp[-1]:
                tmp = tmp[:-1]

            for m in tmp:
                m = m.replace('\t', '')

                if m:
                    line = m.split(',')
                    tmp_tuples.append(tuple(line))

            inner_coord.append(tmp_tuples)
    except Exception, e:
        print '!!!!!!!!!!!!!!!!! ERROR inner_coord Placemark ========================== ', e
        error = e

    return inner_coord, error
