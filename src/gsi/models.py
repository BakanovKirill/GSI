from django.contrib.auth.models import User
from django.db import models

# Always aware of translations to other languages in the future -> wrap all texts into _()
from django.utils.translation import ugettext_lazy as _


class UnicodeNameMixin(object):

    def __unicode__(self):
        return _(u"%s") % self.name


# class Currency(UnicodeNameMixin, models.Model):
#     """
#     Default currency will be USD. All rates are USD based.
#     """
#     pass



