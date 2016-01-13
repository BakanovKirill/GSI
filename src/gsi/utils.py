# -*- coding: utf-8 -*-
import os, stat

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

    run = Run.objects.create(run_base=run_base, user=user)
    log = Log.objects.create(name="run_%s" % run.id)
    run.log = log
    run.save()
    first_card = OrderedCardItem.objects.filter(sequence__runbase=run_base).first()
    step = RunStep.objects.create(parent_run=run, card_item=first_card)

    #TODO: make scripts for each step
    create_scripts(run, step)

    return {'run': run, 'step': step}


def create_scripts(run, step):
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
    LOCAL_VAR_GROUPS = run.run_base.card_sequence.environment_base.environment_variables

    # <EXECUTABLE>
    card_item = step.card_item.card_item
    EXECUTABLE = get_exrcutable(run, step, card_item)

    # path to scripts for runs and steps
    path_runs = GSI_HOME + 'scripts/runs/R_{0}/'.format(run.id)
    # path_steps = GSI_HOME + 'scripts/steps/'

    try:
        os.makedirs(path_runs)
    except OSError:
        print '*** FOLDER EXIST ***'
    finally:
        script_name = 'card_{0}.sh'.format(card_item.id)
        script_path = path_runs + script_name
        fd = open(script_path, 'w+')
        fd.writelines('. ' + RESOLUTION_ENV_SCRIPT + '\n\n')
        fd.writelines(export_home_var + '\n\n')
        fd.writelines(LOCAL_VAR_GROUPS + '\n\n')
        fd.writelines(EXECUTABLE)
        os.chmod(script_path, 0755)
        fd.close()


def get_years(name):
    from gsi.models import YearGroup

    year_group = YearGroup.objects.get(name=name)
    return year_group.years.through.objects.filter(yeargroup=year_group)


def get_area_tiles(name):
    from gsi.models import Area

    card_area = Area.objects.get(name=name)
    return card_area.tiles.through.objects.filter(area=card_area)


def get_exrcutable(run, step, card_item):
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
    name_card = step.card_item.card_item.content_object
    EXECUTABLE = ''
    pid = 1

    if card_model == 'rfscore':
        #  u'RFscore <Tile> [[MyDir]] [<BiasCorrn>] [<QRFopts>] [<RefTarget>] [<CleanName>]'
        # data_card = RFScore.objects.get(name='AUZ_SOC3_RFSCORE')
        data_card = RFScore.objects.get(name=name_card)
        years = get_years(data_card.year_group.name)
        area_tiles = get_area_tiles(data_card.area)

        for year in years:
            year_card = Year.objects.get(id=year.year_id)
            for tile in area_tiles:
                tile_card = Tile.objects.get(id=tile.tile_id)
                EXECUTABLE += '$RF_EXEC_DIR/RFscore {0} {1}_{2} {3} {4} {5} {6} -r {7} -c {8} -s {9}\n'.format(
                        tile_card,
                        data_card.name,
                        step.parent_run.run_base.directory_path,
                        data_card.bias_corrn,
                        year_card,
                        data_card.number_of_threads,
                        data_card.QRFopts,
                        run.id,
                        card_item.id,
                        pid,
                )
                pid += 1

    if card_model == 'rftrain':
        # u'RFtrain <Tile> [<Ntrees>] [<training>] [<Nvar>] [<Nthread>]'
        data_card = RFTrain.objects.get(name=name_card)
        training = 10
        n_thread = 1
        EXECUTABLE += '$RF_EXEC_DIR/RFtrain {0} {1} {2} {3} {4} -r {5} -c {6} -s {7}\n'.format(
            data_card.tile_type.name,
            data_card.number_of_trees,
            training,
            data_card.value,
            n_thread,
            run.id,
            card_item.id,
            pid,
        )
        pid += 1

    if card_model == 'qrf':
        # u'QRF [<QRFinterval>] [<ntrees>] [<nthreads>] [<MyDir>]'
        data_card = QRF.objects.get(name=name_card)
        EXECUTABLE += '$RF_EXEC_DIR/QRF {0} {1} {2} {3} -r {4} -c {5} -s {6}\n'.format(
            data_card.interval,
            data_card.number_of_trees,
            data_card.number_of_threads,
            data_card.directory,
            run.id,
            card_item.id,
            pid,
        )
        pid += 1

    if card_model == 'remap':
        # u'Remap <FileSpec> <RoI> <OutRoot>[,<OutSuffix>] [<ColourTable>] [<RefStatsFile>] [<RefStatsScale>]'
        data_card = Remap.objects.get(name=name_card)
        EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} -r {7} -c {8} -s {9}\n'.format(
            data_card.file_spec,
            data_card.roi,
            data_card.output_root,
            data_card.output_suffix,
            data_card.color_table,
            data_card.refstats_file,
            data_card.refstats_scale,
            run.id,
            card_item.id,
            pid,
        )
        pid += 1

    if card_model == 'yearfilter':
        # u'YearFilter <Tile> <FileType> [<Filter>] [<FiltOut>] [<ExtendStart>] [<InpFourier>] [<OutDir>] [<InpDir>]'
        # data_card = YearFilter.objects.get(name='YearFilter_1')
        data_card = YearFilter.objects.get(name=name_card)
        area_tiles = get_area_tiles(data_card.area)

        for tile in area_tiles:
            tile_card = Tile.objects.get(id=tile.tile_id)
            EXECUTABLE += '$RF_EXEC_DIR/YearFilter {0} {1} {2} {3} {4} {5} {6} {7} -r {8} -c {9} -s {10}\n'.format(
                tile_card,
                data_card.filetype,
                data_card.filter,
                data_card.filter_output,
                data_card.extend_start,
                data_card.input_fourier,
                data_card.output_directory,
                data_card.input_directory,
                run.id,
                card_item.id,
                pid,
            )
            pid += 1

    if card_model == 'preproc':
        # u'PreProc [<Tile>|<file.hdf>] [<Year>] [<Mode>]'
        # data_card = PreProc.objects.get(name='PreProc_1')
        data_card = PreProc.objects.get(name=name_card)
        years = get_years(data_card.year_group.name)
        area_tiles = get_area_tiles(data_card.area)

        for year in years:
            year_card = Year.objects.get(id=year.year_id)
            for tile in area_tiles:
                tile_card = Tile.objects.get(id=tile.tile_id)
                EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} {1} {2} -r {3} -c {4} -s {5}\n'.format(
                    tile_card,
                    year_card,
                    data_card.mode,
                    run.id,
                    card_item.id,
                    pid,
                )
                pid += 1

    if card_model == 'collate':
        # u'Collate <Tile> [<Mode>] [<InpFile>] [<OutDirFile>] [<InpScale>]'
        # data_card = Collate.objects.get(name='Collate_1')
        data_card = Collate.objects.get(name=name_card)
        area_tiles = get_area_tiles(data_card.area)

        for tile in area_tiles:
            tile_card = Tile.objects.get(id=tile.tile_id)
            EXECUTABLE += '$RF_EXEC_DIR/Collate {0} {1} {2} {3} {4} -r {5} -c {6} -s {7}\n'.format(
                tile_card,
                data_card.mode,
                data_card.input_file,
                data_card.output_tile_subdir,
                data_card.input_scale_factor,
                run.id,
                card_item.id,
                pid,
            )
            pid += 1

    # if card_model == 'mergecsv':
    #     # MergeCSV <PathSpec>/<FileSpec> [<OutFile>] [<Scale>]
    #     data_card = MergeCSV.objects.get(name=name_card)
    #     EXECUTABLE += '$RF_EXEC_DIR/MergeCSV {0} {1} {2} -r {3} -c {4} -s {5}\n'.format(
    #         run.id,
    #         card_item.id,
    #         pid,
    #     )

    return EXECUTABLE
