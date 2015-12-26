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
    return {'run': run, 'step': step}
