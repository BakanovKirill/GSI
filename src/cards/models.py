from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import \
    ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.utils import UnicodeNameMixin


class NamedModel(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True


class ParallelModel(models.Model):
    run_parallel = models.BooleanField(default=False)

    class Meta:
        abstract = True


class QRF(NamedModel):
    interval = models.CharField(max_length=100, blank=True)
    number_of_trees = models.IntegerField(default=0, blank=True)
    number_of_threads = models.IntegerField(default=1, blank=True)
    directory = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = _('QRF cards')


class RFScore(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    year_group = models.ForeignKey('gsi.YearGroup')
    bias_corrn = models.CharField(max_length=200, blank=True)
    number_of_threads = models.IntegerField(default=1, blank=True)
    QRFopts = models.CharField(max_length=300, blank=True)
    ref_target = models.CharField(max_length=100, blank=True)
    clean_name = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = _('RFScore cards')


class Remap(NamedModel, ParallelModel):
    file_spec = models.CharField(max_length=200)
    roi = models.CharField(max_length=200)
    output_root = models.CharField(max_length=200)
    output_suffix = models.CharField(max_length=200, blank=True)
    scale = models.CharField(max_length=200, blank=True)
    output = models.CharField(max_length=200, blank=True)
    color_table = models.CharField(max_length=200, blank=True)
    refstats_file = models.CharField(max_length=200, blank=True)
    refstats_scale = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('Remap cards')


class YearFilter(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    filetype = models.CharField(max_length=50)
    filter = models.CharField(max_length=200, blank=True)
    filter_output = models.CharField(max_length=300, blank=True)
    extend_start = models.CharField(max_length=200, blank=True)
    input_fourier = models.CharField(max_length=200, blank=True)
    output_directory = models.CharField(max_length=300, blank=True)
    input_directory = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('YearFilter cards')


class Collate(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    mode = models.CharField(max_length=50, blank=True)
    input_file = models.CharField(max_length=200, blank=True)
    output_tile_subdir = models.CharField(max_length=200, blank=True)
    input_scale_factor = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('Collate cards')


class PreProc(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area', null=True, blank=True)
    mode = models.CharField(max_length=50, blank=True)
    year_group = models.ForeignKey('gsi.YearGroup', null=True, blank=True)

    class Meta:
        verbose_name_plural = _('PreProc cards')


class MergeCSV(NamedModel, models.Model):
    csv1 = models.CharField(max_length=200, blank=True)
    csv2 = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('MergeCSV cards')


class RFTrain(NamedModel, ParallelModel):
    tile_type = models.ForeignKey('gsi.TileType')
    number_of_trees = models.IntegerField(default=50, blank=True)
    value = models.CharField(max_length=300)
    config_file = models.CharField(max_length=200, blank=True)
    output_tile_subdir = models.CharField(max_length=200, blank=True)
    input_scale_factor = models.CharField(max_length=200, blank=True)
    training = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_variable = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_thread = models.PositiveIntegerField(default=1, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('RFTRain cards')


class RandomForest(NamedModel):
    aoi_name = models.CharField(max_length=200)
    satellite = models.ForeignKey('gsi.Satellite')
    param_set = models.TextField()
    run_set = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    mvrf = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('Random Forest cards')

    def __unicode__(self):
        return u"{0}".format(self.name)


class CardItem(models.Model):
    CONTENT_LIMIT = (
        models.Q(app_label='cards', model='rftrain') |
        models.Q(app_label='cards', model='mergecsv') |
        models.Q(app_label='cards', model='preproc') |
        models.Q(app_label='cards', model='collate') |
        models.Q(app_label='cards', model='yearfilter') |
        models.Q(app_label='cards', model='remap') |
        models.Q(app_label='cards', model='rfscore') |
        models.Q(app_label='cards', model='qrf') |
        models.Q(app_label='cards', model='randomforest')
    )

    content_type = models.ForeignKey(ContentType, limit_choices_to=CONTENT_LIMIT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('content_type', 'object_id')

    def __unicode__(self):
        return u"{0}".format(self.content_object)


class OrderedCardItem(models.Model):
    card_item = models.ForeignKey(CardItem)
    order = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u"{0}".format(self.card_item)


def get_card_item(self):
    card_item, created = CardItem.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self.__class__),
            object_id=self.pk,
    )
    return card_item


def __unicode__(self):
    return self.name


ContentType.__unicode__ = __unicode__


@receiver(post_save)
def auto_add_card_item(sender, instance=None, created=False, **kwargs):
    list_of_models = (
        RFScore, RFTrain, QRF, YearFilter, MergeCSV,
        Collate, PreProc, Remap, RandomForest
    )
    if sender in list_of_models:
        if created:
            get_card_item(instance)
