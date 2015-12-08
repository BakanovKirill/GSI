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
        verbose_name_plural = 'QRF cards'


class RFScore(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    year_group = models.ForeignKey('gsi.YearGroup')
    bias_corrn = models.CharField(max_length=200)
    number_of_threads = models.IntegerField(default=1)
    QRFopts = models.CharField(max_length=300)
    ref_target = models.CharField(max_length=100)
    clean_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'RFScore cards'


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
        verbose_name_plural = 'Remap cards'


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
        verbose_name_plural = 'YearFilter cards'


class Collate(NamedModel, ParallelModel):
    area = models.ForeignKey('gsi.Area')
    mode = models.CharField(max_length=50)
    input_file = models.CharField(max_length=200)
    output_tile_subdir = models.CharField(max_length=200)
    input_scale_factor = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Collate cards'


