import os

from gsi.settings import PROJECTS_PATH


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
