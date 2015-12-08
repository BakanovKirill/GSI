from django.db import models
from django.utils.translation import \
    ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()


from solo.models import SingletonModel

from .utils import UnicodeNameMixin


class HomeVariables(SingletonModel):
    SAT_TIF_DIR_ROOT = models.CharField(max_length=300, verbose_name=_('Satelite Data Top Level'),
                                        help_text=_('SAT_TIF_DIR_ROOT'))
    RF_DIR_ROOT = models.CharField(max_length=300, verbose_name=_('Top directory of Random Forest Files'),
                                   help_text=_('RF_DIR_ROOT'))
    USER_DATA_DIR_ROOT = models.CharField(max_length=300, verbose_name=_('Top Level for user data directory'),
                                          help_text=_('USER_DATA_DIR_ROOT'))
    MODIS_DIR_ROOT = models.CharField(max_length=300, verbose_name=_('Top Level for raw Modis data'),
                                      help_text=_('MODIS_DIR_ROOT'))
    RF_AUXDATA_DIR = models.CharField(max_length=300, verbose_name=_('Top Level for Auxilliary data(SOIL, DEM etc.)'),
                                      help_text=_('RF_AUXDATA_DIR'))
    SAT_DIF_DIR_ROOT = models.CharField(max_length=300, verbose_name=_('Top Level for Satelite TF files'),
                                        help_text=_('SAT_DIF_DIR_ROOT'))

    def __unicode__(self):
        return _(u"Home variables")

    class Meta:
        verbose_name = _(u"Home variables")


class VariablesGroup(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=50)
    environment_variables = models.TextField()


class Tile(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=6)


class Area(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=50)
    tiles = models.ManyToManyField(Tile, related_name='areas')


class Year(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=4)


class YearGroup(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=50)
    years = models.ManyToManyField(Year, related_name='year_groups')


class Resolution(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=50, help_text=_('This will be a short display of the value, i.e. 1KM, 250M'))
    value = models.CharField(max_length=20, help_text=_('Value in meters, e.g 1000 for 1KM display name'))
