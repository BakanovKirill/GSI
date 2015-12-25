from django.utils.translation import ugettext_lazy as _


class UnicodeNameMixin(object):
    def __unicode__(self):
        return _(u"%s") % self.name


def validate_status(status):
    if not status:
        return {
            'status': False,
            'message': 'An error in the name of a parameter or is missing'}

    return {'status': status}
