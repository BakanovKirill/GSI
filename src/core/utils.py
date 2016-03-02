# -*- coding: utf-8 -*-
import os, stat
import subprocess
from subprocess import Popen, PIPE

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class UnicodeNameMixin(object):
    def __unicode__(self):
        return _(u"%s") % self.name


def validate_status(status):
    from gsi.models import STATES
    states = [st[0] for st in STATES]
    if not status or status not in states:
        return {
            'status': False,
            'message': 'Invalid or missing "status" GET parameter.'
        }

    return {'status': status}


def make_run(run_base, user):
    from gsi.models import Run, Log, RunStep, OrderedCardItem

    scripts = []
    run = Run.objects.create(run_base=run_base, user=user)
    # log = Log.objects.create(name="run_%s" % run.id)
    # run.log = log
    # run.save()
    # first_card = OrderedCardItem.objects.filter(sequence__runbase=run_base).first()
    all_card = OrderedCardItem.objects.filter(sequence__runbase=run_base).order_by('order')
    # step = RunStep.objects.create(parent_run=run, card_item=first_card)

    for card in all_card:
        step = RunStep.objects.create(parent_run=run, card_item=card)
        #TODO: make scripts for each step
        sequence = step.parent_run.run_base.card_sequence
        script = create_scripts(run, sequence, card, step)
        script['step'] = step
        scripts.append(script)
    execute = execute_script(run, scripts)

    return {'run': run, 'step': step}


def create_scripts(run, sequence, card, step):
    """ Create a script at startup run_base """
    from gsi.models import HomeVariables as Home

    home_var = Home.objects.all()
    export_home_var = ''

    # home dir scripts
    GSI_HOME = settings.SCRIPTS_HOME

    # <RESOLUTION_ENV_SCRIPT>
    resolution = run.run_base.resolution
    RESOLUTION_ENV_SCRIPT = GSI_HOME + 'bin/' + str(resolution)+'_config'

    # <HOME_ENV_OVERRIDES>
    for hv in home_var:
        export_home_var += 'export SAT_TIF_DIR=' + hv.SAT_DIF_DIR_ROOT + '\n'
        export_home_var += 'export RF_DIR=' + hv.RF_DIR_ROOT + '\n'
        export_home_var += 'export USER_DATA_DIR=' + hv.USER_DATA_DIR_ROOT + '\n'
        export_home_var += 'export MODIS_DIR=' + hv.MODIS_DIR_ROOT + '\n'
        export_home_var += 'export RF_AUXDATA_DIR=' + hv.RF_AUXDATA_DIR + '\n'
        export_home_var += 'export SAT_DIF_DIR=' + hv.SAT_DIF_DIR_ROOT

    # <LOCAL_ENV_OVERRIDES>
    LOCAL_VAR_GROUPS = u'export {0}'.format(
        run.run_base.card_sequence.environment_base.environment_variables
    )

    # <ENVIROMENT OVERRIDE>
    ENVIROMENT_OVERRIDE = u'export {0}'.format(run.run_base.card_sequence.environment_override)

    # <EXECUTABLE>
    card_item = step.card_item.card_item
    EXECUTABLE = get_executable(run, sequence, card, card_item)

    # path to scripts for runs and steps
    path_runs = GSI_HOME + 'scripts/runs/R_{0}/'.format(run.id)
    path_runs_logs = GSI_HOME + 'scripts/runs/R_{0}/LOGS'.format(run.id)
    # path_steps = GSI_HOME + 'scripts/steps/'

    try:
        os.makedirs(path_runs)
        os.makedirs(path_runs_logs)
    except OSError:
        print '*** FOLDER EXIST ***'
    finally:
        script_name = 'card_{0}.sh'.format(card_item.id)
        script_path = path_runs + script_name
        fd = open(script_path, 'w+')
        fd.write('# Sequence: {0}, card: {1} - Generated {2} \n\n'.\
                 format(sequence.name, card.card_item, step.start_date))
        fd.writelines('. ' + RESOLUTION_ENV_SCRIPT + '\n\n')
        fd.writelines(export_home_var + '\n\n')
        fd.writelines(LOCAL_VAR_GROUPS + '\n\n')
        fd.writelines(ENVIROMENT_OVERRIDE + '\n\n')
        fd.writelines(EXECUTABLE)
        os.chmod(script_path, 0777)
        fd.close()

    return {
        'path_runs': path_runs,
        'path_runs_logs': path_runs_logs,
        'script_name': script_name,
        'card': card_item.id
    }


def execute_script(run, scripts):
    from gsi.models import Log

    status = True
    fd = None

    for script in scripts:
        script['step'].state = 'running'
        script['step'].save()
        run.state = 'running'
        run.save()

        log_name = str(run.id) + '_' + str(script['card']) + '.log'
        path_log = script['path_runs_logs'] + '/' + log_name
        rs = subprocess.call('./{0}'.format(script['path_runs']), shell=True)
        log = Log.objects.create(name=log_name)
        log.log_file_path = path_log
        log.save()
        run.log = log
        run.save()
        proc = Popen(
            './{0}'.format(script['path_runs']),
            shell=True,
            stdout=PIPE,
            stderr=PIPE
        )
        proc.wait()    # дождаться выполнения
        res = proc.communicate()  # получить tuple('stdout', 'stderr')

        try:
            os.makedirs(script['path_runs_logs'])
        except OSError:
            print '*** FOLDER LOGS EXIST ***'
        finally:
            fd = open(path_log, 'w+')

        if proc.returncode and rs != 0:
            # fd = open(path_log, 'w+')
            if fd is not None:
                fd.writelines('ERROR: ' + res[1] + '\n')
                fd.writelines('Status error: ' + str(rs) + '\n')
                fd.close()
            script['step'].state = 'fail'
            script['step'].save()
            run.state = 'fail'
            run.save()
            return False
        fd.writelines(res[0] + '\n\n')
        fd.writelines('Status: ' + str(rs) + '\n\n')
        fd.close()
        script['step'].state = 'success'
        script['step'].save()

    return status


def get_years(name):
    from gsi.models import YearGroup

    year_group = YearGroup.objects.get(name=name)
    return year_group.years.through.objects.filter(yeargroup=year_group)


def get_area_tiles(name):
    from gsi.models import Area

    card_area = Area.objects.get(name=name)
    return card_area.tiles.through.objects.filter(area=card_area)


def get_executable(run, sequence, card, card_item):
    """ get the <EXECUTABLE> to script """
    from cards.models import RFScore, RFTrain, QRF, \
        Remap, YearFilter, PreProc, Collate, MergeCSV
    from gsi.models import Year, Tile

    # CARD_MODEL = (
    #     'qrf',        +
    #     'rfscore',    +
    #     'remap',      +
    #     'yearfilter', +
    #     'preproc',    +
    #     'collate',    +
    #     'rftrain',    ?
    #     'mergecsv',   -
    # )

    card_model = card_item.content_type.model
    # name_card = step.card_item.card_item.content_object
    EXECUTABLE = ''
    pid = 1

    if card_model == 'rfscore':
        #  u'RFscore <Tile> [[MyDir]] [<BiasCorrn>] [<QRFopts>] [<RefTarget>] [<CleanName>]'
        # data_card = RFScore.objects.sget(name='AUZ_SOC3_RFSCORE')
        data_card = RFScore.objects.get(name=card.card_item.content_object)
        years = get_years(data_card.year_group.name)
        area_tiles = get_area_tiles(data_card.area)

        for year in years:
            year_card = Year.objects.get(id=year.year_id)
            for tile in area_tiles:
                tile_card = Tile.objects.get(id=tile.tile_id)
                EXECUTABLE += '$RF_EXEC_DIR/RFscore {0} {1}_{2} {3} {4} {5} {6} -s {7}.{8}.{9}.{10}\n'.format(
                        tile_card,
                        data_card.name,
                        run.run_base.directory_path,
                        data_card.bias_corrn,
                        year_card,
                        data_card.number_of_threads,
                        data_card.QRFopts,
                        run.id,
                        sequence.id,
                        card.id,
                        pid,
                )
                pid += 1

    if card_model == 'rftrain':
        # u'RFtrain <Tile> [<Ntrees>] [<training>] [<Nvar>] [<Nthread>]'
        data_card = RFTrain.objects.get(name=card.card_item.content_object)
        training = 10
        n_thread = 1
        EXECUTABLE += '$RF_EXEC_DIR/RFtrain {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}\n'.format(
            data_card.tile_type.name,
            data_card.number_of_trees,
            training,
            data_card.value,
            n_thread,
            run.id,
            sequence.id,
            card.id,
            pid,
        )
        pid += 1

    if card_model == 'qrf':
        # u'QRF [<QRFinterval>] [<ntrees>] [<nthreads>] [<MyDir>]'
        data_card = QRF.objects.get(name=card.card_item.content_object)
        EXECUTABLE += '$RF_EXEC_DIR/QRF {0} {1} {2} {3} -s {4}.{5}.{6}.{7}\n'.format(
            data_card.interval,
            data_card.number_of_trees,
            data_card.number_of_threads,
            data_card.directory,
            run.id,
            sequence.id,
            card.id,
            pid,
        )
        pid += 1

    if card_model == 'remap':
        # u'Remap <FileSpec> <RoI> <OutRoot>[,<OutSuffix>] [<ColourTable>] [<RefStatsFile>] [<RefStatsScale>]'
        data_card = Remap.objects.get(name=card.card_item.content_object)
        EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} -s {7}.{8}.{9}.{10}\n'.format(
            data_card.file_spec,
            data_card.roi,
            data_card.output_root,
            data_card.output_suffix,
            data_card.color_table,
            data_card.refstats_file,
            data_card.refstats_scale,
            run.id,
            sequence.id,
            card.id,
            pid,
        )
        pid += 1

    if card_model == 'yearfilter':
        # u'YearFilter <Tile> <FileType> [<Filter>] [<FiltOut>] [<ExtendStart>] [<InpFourier>] [<OutDir>] [<InpDir>]'
        # data_card = YearFilter.objects.get(name='YearFilter_1')
        data_card = YearFilter.objects.get(name=card.card_item.content_object)
        area_tiles = get_area_tiles(data_card.area)

        for tile in area_tiles:
            tile_card = Tile.objects.get(id=tile.tile_id)
            EXECUTABLE += '$RF_EXEC_DIR/YearFilter {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}\n'.format(
                tile_card,
                data_card.filetype,
                data_card.filter,
                data_card.filter_output,
                data_card.extend_start,
                data_card.input_fourier,
                data_card.output_directory,
                data_card.input_directory,
                run.id,
                sequence.id,
                card.id,
                pid,
            )
            pid += 1

    if card_model == 'preproc':
        # u'PreProc [<Tile>|<file.hdf>] [<Year>] [<Mode>]'
        # data_card = PreProc.objects.get(name='PreProc_1')
        data_card = PreProc.objects.get(name=card.card_item.content_object)
        years = get_years(data_card.year_group.name)
        area_tiles = get_area_tiles(data_card.area)

        for year in years:
            year_card = Year.objects.get(id=year.year_id)
            for tile in area_tiles:
                tile_card = Tile.objects.get(id=tile.tile_id)
                EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} {1} {2} -s {3}.{4}.{5}.{6}\n'.format(
                    tile_card,
                    year_card,
                    data_card.mode,
                    run.id,
                    sequence.id,
                    card.id,
                    pid,
                )
                pid += 1

    if card_model == 'collate':
        # u'Collate <Tile> [<Mode>] [<InpFile>] [<OutDirFile>] [<InpScale>]'
        # data_card = Collate.objects.get(name='Collate_1')
        data_card = Collate.objects.get(name=card.card_item.content_object)
        area_tiles = get_area_tiles(data_card.area)

        for tile in area_tiles:
            tile_card = Tile.objects.get(id=tile.tile_id)
            EXECUTABLE += '$RF_EXEC_DIR/Collate {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}\n'.format(
                tile_card,
                data_card.mode,
                data_card.input_file,
                data_card.output_tile_subdir,
                data_card.input_scale_factor,
                run.id,
                sequence.id,
                card.id,
                pid,
            )
            pid += 1

    # if card_model == 'mergecsv':
    #     # MergeCSV <PathSpec>/<FileSpec> [<OutFile>] [<Scale>]
    #     data_card = MergeCSV.objects.get(name=card)
    #     EXECUTABLE += '$RF_EXEC_DIR/MergeCSV {0} {1} {2} -s {3}.{4}.{5}\n'.format(
    #         run.id,
    #         card_item.id,
    #         pid,
    #     )

    return EXECUTABLE
