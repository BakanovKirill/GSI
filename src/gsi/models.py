from datetime import datetime

from django.contrib.auth.models import User
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


class TileType(models.Model):
    name = models.CharField(max_length=50)


class OrderedCardItem(models.Model):
    card_item = models.ForeignKey('cards.CardItem', related_name='ordered_cards')
    sequence = models.ForeignKey('CardSequence')

    order = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u"{0}".format(self.card_item)


class CardSequence(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=100)
    environment_base = models.ForeignKey(VariablesGroup, null=True, blank=True)
    environment_override = models.TextField(null=True, blank=True)

    cards = models.ManyToManyField('cards.CardItem', through=OrderedCardItem, related_name='card_sequences')


class Log(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    log_file_path = models.CharField(max_length=300, null=True, blank=True)
    log_file = models.FileField(blank=True, null=True)


class RunBase(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    directory_path = models.CharField(max_length=200)

    resolution = models.ForeignKey(Resolution)
    card_sequence = models.ForeignKey(CardSequence)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.date_modified = datetime.now()
        return super(RunBase, self).save(*args, **kwargs)


STATES = (
    ('created', 'Created'),
    ('pending', 'Pending'),
    ('running', 'Running'),
    ('success', 'Success'),
    ('fail', 'Fail'),
)


class Run(models.Model):
    STATES = (
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('fail', 'Fail'),
    )

    user = models.ForeignKey(User, null=True, blank=True)
    run_base = models.ForeignKey(RunBase)

    state = models.CharField(max_length=100, choices=STATES, default='created')

    log = models.ForeignKey(Log, null=True, blank=True)

    run_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0}".format(self.run_base)


class RunStep(UnicodeNameMixin, models.Model):
    parent_run = models.ForeignKey(Run)
    card_item = models.ForeignKey('cards.CardItem')

    state = models.CharField(max_length=100, choices=STATES, default='pending')

    start_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0}_{1}".format(self.card_item.content_object.name, self.parent_run)
