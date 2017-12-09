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
