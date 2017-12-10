import os

import simplekml
from simplekml import Kml

from gsi.settings import PROJECTS_PATH, TMP_PATH, KML_PATH, COLOR_HEX
from customers.models import CustomerPolygons


def getResultDirectory(dataset, shelfdata):
    dirs_list = []
    # is_ts = dataset.is_ts

    try:
        project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)
        root, dirs, files = os.walk(project_directory).next()
        dirs.sort()

        for sd in shelfdata:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)

        # if 'TS_' in dataset.results_directory:
        #     for dy in dirs:
        #         dirs_list.append(dy)
        #     is_ts = True
        # else:
        #     for sd in shelfdata:
        #         if str(sd.root_filename) in dirs:
        #             dirs_list.append(sd)
    except Exception, e:
        print '----->>>    Exception getResultDirectory ========================= ', e
        pass

    # print '!!!!!!!!!!!!!!!!!!!! DIRS LIST ========================= ', dirs_list
    # print '!!!!!!!!!!!!!!!!!!!! TS ========================= ', is_ts

    return dirs_list
    
def getTsResultDirectory(dataset):
    dirs_list = []
    shelf_data = dataset.shelf_data

    try:
        project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)
        root, dirs, files = os.walk(project_directory).next()
        dirs.sort()

        # print '!!!!!!!!!!!! project_directory ======================= ', project_directory
        # print '!!!!!!!!!!!! DIRS ======================= ', dirs

        for d in dirs:
            name = '{0} {1}'.format(shelf_data, d)
            dirs_list.append(name)

        # if 'TS_' in dataset.results_directory:
        #     for dy in dirs:
        #         dirs_list.append(dy)
        #     is_ts = True
        # else:
        #     for sd in shelfdata:
        #         if str(sd.root_filename) in dirs:
        #             dirs_list.append(sd)
    except Exception, e:
        print '----->>>    Exception getTsResultDirectory ========================= ', e
        pass

    # print '!!!!!!!!!!!!!!!!!!!! DIRS LIST ========================= ', dirs_list
    # print '!!!!!!!!!!!!!!!!!!!! TS ========================= ', is_ts

    return dirs_list


def getCountTs(dataset, shd):
    # print '!!!!!!!!!!!!!!!!! SHD ===================== ', shd

    is_ts = dataset.is_ts
    count_ts = 0

    path_cur_proj = dataset.results_directory
    path_to_proj = os.path.join(PROJECTS_PATH, path_cur_proj)

    # print '!!!!!!!!!!!!!!!!! path_to_proj ===================== ', path_to_proj

    try:
        if os.path.exists(path_to_proj):
            pr_root, pr_dirs, pr_files = os.walk(path_to_proj).next()
            pr_dirs.sort()

            # print '!!!!!!!!!!!!!!!!! pr_dirs ===================== ', pr_dirs


            for d in pr_dirs:
                # print '!!!!!!!!!!!!!!!!! d ===================== ', d
                # print '!!!!!!!!!!!!!!!!! IN SHD ===================== ', shd
                # print '!!!!!!!!!!!!!!!!! d in shd ===================== ', d in shd
                if d in shd:
                    path_to_subdir = os.path.join(path_to_proj, d)
                    sub_root, sub_dirs, sub_files = os.walk(path_to_subdir).next()
                    sub_dirs.sort()

                    # print '!!!!!!!!!!!!!!!!! path_to_subdir ===================== ', path_to_subdir

                    for sd in sub_dirs:
                        attr_dir = os.path.join(path_to_subdir, sd)
                        attr_root, attr_dirs, attr_files = os.walk(attr_dir).next()
                        attr_files.sort()

                        # print '!!!!!!!!!!!!!!!!! attr_dir ===================== ', attr_dir

                        for f in attr_files:
                            fl, ext = os.path.splitext(f)

                            if ext == '.tif':
                                count_ts += 1
    except Exception:
        pass

    # print '!!!!!!!!!!!!!!!!! getCountTs ===================== ', count_ts

    return count_ts


def createKml(user, filename, info_window, url, data_set, count_color, *args):
    # Create KML file for the draw polygon
    
    outer_coord = []
    inner_coord = []
    kml_filename = str(filename) + '.kml'
    kml_url = url + '/' + kml_filename

    if not args:
        tmp_file = str(user) + '_coord_kml.txt'
        tmp_path = os.path.join(TMP_PATH, tmp_file)
        coord = getGeoCoord(tmp_path)
    else:
        outer_coord = args[0]['outer_coord'][0]
        inner_coord = args[0]['inner_coord']

        # tmp_inner_coord = []
        # len_inner_coord = len(args[0]['inner_coord'])

        # if args[0]['inner_coord']:
        #     for n in xrange(len_inner_coord):
        #         tmp_inner_coord += args[0]['inner_coord'][n]

        # inner_coord.append(tmp_inner_coord)

    # print '!!!!!!!!!!! 2 info_window ======================== ', info_window
    # print '!!!!!!!!!!! 2 outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!! 2 inner_coord ======================== ', inner_coord
    # print '!!!!!!!!!!! 2 inner_coord LEN ======================== ', len(args[0]['inner_coord'])
    # print '!!!!!!!!!!! 2 args ======================== ', args
    # print '!!!!!!!!!!! 2 outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!! 2 inner_coord ======================== ', inner_coord
    # print '!!!!!!!!!!! 2 info_window ======================== ', info_window
    # print '!!!!!!!!!!! COLOR ======================== ', COLOR_KML[count_color]
    # print '!!!!!!!!!!! LAST ID COUNT AOI ======================== ', cip_last_id.id
    # print '!!!!!!!!!!! %%%%%%%% ======================== ', count_color
    # print '!!!!!!!!!!! filename ======================== ', filename
    # print '!!!!!!!!!!! COORD ======================== ', coord
    # print '!!!!!!!!!!! COORD outer_coord ======================== ', outer_coord
    # print '!!!!!!!!!!! COORD inner_coord ======================== ', inner_coord
    # var = 'x'
    # for i in range(10):
    #     exec(var+str(i)+' = ' + str(i))

    # len_inner_coord = len(inner_coord)
    # pol_dict = {}

    kml = simplekml.Kml()
    pol = kml.newpolygon(name=filename)

    if not args:
        pol.outerboundaryis.coords = coord
    else:
        pol.outerboundaryis = outer_coord

        if inner_coord:
            pol.innerboundaryis = inner_coord


    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # if len_inner_coord:
    #     for n in xrange(1, len_inner_coord):
    #         pol_dict['pol_'+str(n)] = kml.newpolygon(name=filename)
    # **************************************************************************
    
    # print '!!!!!!!!!!!!!!!!!! len_inner_coord =========================== ', len_inner_coord

    # if not args:
    #     pol.outerboundaryis.coords = coord
    # else:
    #     pol.outerboundaryis = outer_coord
    #     # pol_2.outerboundaryis = outer_coord
    #     # pol.innerboundaryis = inner_coord[1]

    #     if len_inner_coord:
    #         pol.innerboundaryis = inner_coord[0]

    #         for n in xrange(1, len_inner_coord):
    #             pol_dict['pol_'+str(n)].innerboundaryis = inner_coord[n]

    # **************************************************************************
    # # **************************************************************************
    # # **************************************************************************

        # inner_list.append(inner_coord[0])
        # inner_list.append(inner_coord[1])
        # pol.innerboundaryis = inner_coord
        # pol_2.innerboundaryis = inner_coord[1]

        # for n in xrange(len(inner_coord)):
        #     pol.innerboundaryis = inner_coord[n]
            
    # pol.style.linestyle.color = simplekml.Color.hex('#ffffff')
    
    # print '!!!!!!!!!!!!!!!!!! pol_dict =========================== ', pol_dict
    
    pol.style.linestyle.color = 'ffffffff'
    pol.style.linestyle.width = 2

    # pol_2.style.linestyle.color = 'ffffffff'
    # pol_2.style.linestyle.width = 2


    pol.style.polystyle.color = simplekml.Color.changealphaint(100, COLOR_HEX[count_color])
    # pol_2.style.polystyle.color = simplekml.Color.changealphaint(100, COLOR_HEX[count_color])
    # pol.style.polystyle.color = simplekml.Color.changealphaint(100, 'ff3c14dc')
    # pol.style.polystyle.color = 'ff3c14dc'

    pol.style.balloonstyle.text = info_window
    # pol_2.style.balloonstyle.text = info_window
    # pol.style.balloonstyle.bgcolor = simplekml.Color.lightgreen
    # pol.style.balloonstyle.bgcolor = simplekml.Color.red
    pol.style.balloonstyle.bgcolor = COLOR_HEX[count_color]
    pol.style.balloonstyle.textcolor = COLOR_HEX[count_color]

    # pol_2.style.balloonstyle.bgcolor = COLOR_HEX[count_color]
    # pol_2.style.balloonstyle.textcolor = COLOR_HEX[count_color]
    # pol.style.balloonstyle.textcolor = simplekml.Color.hex('#283890')

    kml_path = os.path.join(KML_PATH, user.username, kml_filename)

    # print '!!!!!!!!!!!!!!!!!! kml_path =========================== ', kml_path
    
    kml.save(kml_path)

    if inner_coord:
        testkml = ''

        with open(kml_path) as f:
            testkml = f.readlines()

        testkml = "".join(map(lambda x: x.strip(), testkml))
        tmp_line = re.sub(r"Ring><Linear", "Ring></innerBoundaryIs><innerBoundaryIs><Linear", testkml)
        list_lines = tmp_line.split('>')[0:]
        new_tmp_line = '>\n'.join(list_lines)
        my_file = open(kml_path, 'w')
        my_file.write(new_tmp_line)
        my_file.close()

        # print '!!!!!!!!!!!!!!!!! kml_path 33 ============================= ', kml_path


    polygon = addPolygonToDB(filename, kml_filename, user, kml_path, kml_url, data_set, info_window)

    return polygon


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
