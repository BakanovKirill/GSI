import os

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
    create_scripts(run)

    return {'run': run, 'step': step}


def create_scripts(run):
    print 'run_base ============ ', run_base
    print 'path ============ ', os.getcwd()

    OUTPUT_DIR = os.getcwd() + '/src/gsi/scripts/'
    first_line = '#!/bin/bash'
    GSI_HOME = '/home/w23/mattgsi'
    RESOLUTION_ENV_SCRIPT = GSI_HOME + '/bin/'
    resolution = run.run_base.resolution

    f = open(OUTPUT_DIR+str(run.run_base)+'.sh', 'w+')
    f.writelines(first_line+'\n')
    f.writelines('source $'+RESOLUTION_ENV_SCRIPT+str(resolution)+'_config'+'\n')
    f.close()
