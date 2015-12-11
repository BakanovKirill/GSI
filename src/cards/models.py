from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import \
    ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()

from django.contrib.contenttypes.models import ContentType

from django.db import models
from gsi.utils import UnicodeNameMixin


class NamedModel(UnicodeNameMixin, models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class ParallelModel(models.Model):
    run_parallel = models.BooleanField(default=False)

    class Meta:
        abstract = True


class QRF(NamedModel):
    interval = models.CharField(max_length=100)
    number_of_trees = models.IntegerField(default=0)
    number_of_threads = models.IntegerField(default=1)
    directory = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = _('QRF cards')


class RFScore(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    year_group = models.ForeignKey('gsi.YearGroup')
    bias_corrn = models.CharField(max_length=200)
    number_of_threads = models.IntegerField(default=1)
    QRFopts = models.CharField(max_length=300)
    ref_target = models.CharField(max_length=100)
    clean_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _('RFScore cards')


class Remap(NamedModel, ParallelModel):
    file_spec = models.CharField(max_length=200)
    roi = models.CharField(max_length=200)
    output_root = models.CharField(max_length=200)
    output_suffix = models.CharField(max_length=200)
    scale = models.CharField(max_length=200)
    output = models.CharField(max_length=200)
    color_table = models.CharField(max_length=200)
    refstats_file = models.CharField(max_length=200)
    refstats_scale = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('Remap cards')


class YearFilter(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    filetype = models.CharField(max_length=50)
    filter = models.CharField(max_length=200)
    filter_output = models.CharField(max_length=300)
    extend_start = models.CharField(max_length=200)
    input_fourier = models.CharField(max_length=200)
    output_directory = models.CharField(max_length=300)
    input_directory = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('YearFilter cards')


class Collate(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    mode = models.CharField(max_length=50)
    input_file = models.CharField(max_length=200)
    output_tile_subdir = models.CharField(max_length=200)
    input_scale_factor = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('Collate cards')


class PreProc(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    mode = models.CharField(max_length=50)
    year_group = models.ForeignKey('gsi.YearGroup')

    class Meta:
        verbose_name_plural = _('PreProc cards')


class MergeCSV(NamedModel, models.Model):
    csv1 = models.CharField(max_length=200)
    csv2 = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('MergeCSV cards')


class RFTrain(NamedModel, ParallelModel):
    tile_type = models.ForeignKey('gsi.TileType')
    number_of_trees = models.IntegerField(default=0)
    value = models.CharField(max_length=300)
    config_file = models.CharField(max_length=200)
    output_tile_subdir = models.CharField(max_length=200)
    input_scale_factor = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('RFTRain cards')


class CardItem(NamedModel):
    CONTENT_LIMIT = (
        models.Q(app_label='cards', model='RFTrain') |
        models.Q(app_label='cards', model='MergeCSV') |
        models.Q(app_label='cards', model='PreProc') |
        models.Q(app_label='cards', model='Collate') |
        models.Q(app_label='cards', model='YearFilter') |
        models.Q(app_label='cards', model='Remap') |
        models.Q(app_label='cards', model='RFScore') |
        models.Q(app_label='cards', model='QRF')
    )

    content_type = models.ForeignKey(ContentType, limit_choices_to=CONTENT_LIMIT)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id')


def get_card_item(self):
    card_item, created = CardItem.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(self.__class__),
        object_id=self.pk,
        name=self.name
    )
    return card_item

def __unicode__(self):
    return self.name

ContentType.__unicode__=__unicode__