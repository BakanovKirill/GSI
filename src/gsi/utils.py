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
    from gsi.models import CardSequence, YearGroup, \
        Year, Tile, Area, HomeVariables as Home
    from cards.models import RFScore

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
    card_model = card_item.content_type.model
    data_card = ''
    EXECUTABLE = ''

    # AUZ_SOC3_RFSCORE

    # CARD_MODEL = (
    #     'qrf',
    #     'rfscore',
    #     'remap',
    #     'yearfilter',
    #     'preproc',
    #     'mergecsv',
    #     'rftrain',
    # )

    # choice card for create script
    # if card_model == 'rfscore':
    pid = 1
    script_name = 'RFscore'
    data_card = RFScore.objects.get(name='AUZ_SOC3_RFSCORE')
    year_group = YearGroup.objects.get(name=data_card.year_group.name)
    card_area = Area.objects.get(name=data_card.area)
    years = year_group.years.through.objects.filter(yeargroup=year_group)
    area_tiles = card_area.tiles.through.objects.filter(area=card_area)

    for year in years:
        year_card = Year.objects.get(id=year.year_id)
        for tile in area_tiles:
            tile_card = Tile.objects.get(id=tile.tile_id )
            EXECUTABLE += '$RF_EXEC_DIR/{0} {1} {2}_{3} {4} {5} {6} {7} -r {8} -c {9} -s {10}\n'.format(
                    script_name,
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

    # u'$RF_EXEC_DIR/RFscore h28v11 AUZ_TEST_1_MYDIR 0 2001 1  1 –r <run_id>  -c 1 –s   1'
    # u'$RF_EXEC_DIR/RFscore h28v12 AUZ_TEST_1_MYDIR 0 2001 1  1 –r <run_id>  -c 1 –s   2'
    # u'$RF_EXEC_DIR/RFscore h29v10 AUZ_TEST_1_MYDIR 0 2001 1  1 –r <run_id>  -c 1 –s   3'


    # EXECUTABLE = '$RF_EXEC_DIR/RFscore {0}  -r {1} -c {2}'.format(card_item, run.id, card_item.id)

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

