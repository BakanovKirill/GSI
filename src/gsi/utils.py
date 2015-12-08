from django.utils.translation import ugettext_lazy as _

class UnicodeNameMixin(object):
    def __unicode__(self):
        return _(u"%s") % self.name