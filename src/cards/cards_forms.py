# -*- coding: utf-8 -*-
from django import forms

from core.validator_gsi import *
from cards.models import (QRF, RFScore, Remap,
                          YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain)
from gsi.models import Area, YearGroup, TileType


class QRFForm(forms.ModelForm):
    """ form for editing QRF Card """
    def __init__(self, *args, **kwargs):
        super(QRFForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    interval = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        label=u'Interval',
    )
    number_of_trees = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0,
        validators=[validate_order],
        required=False,
        label=u'Number of trees',
    )
    number_of_threads = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1,
        validators=[validate_order],
        required=False,
        label=u'Number of threads',
    )
    directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        required=False,
        label=u'Directory',
    )

    class Meta:
        model = QRF
        fields = [
            'name',
            'interval',
            'number_of_trees',
            'number_of_threads',
            'directory',
        ]


class RFScoreForm(forms.ModelForm):
    """ form for editing RFScore Card """
    def __init__(self, *args, **kwargs):
        super(RFScoreForm, self).__init__(*args, **kwargs)

    run_parallel = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Run parallel',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    area = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=Area.objects.all(),
        # empty_label=None,
        label=u'Area',
    )
    year_group = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=YearGroup.objects.all(),
        # empty_label=None,
        label=u'Year group',
    )
    bias_corrn = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Bias corrn',
    )
    number_of_threads = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1,
        validators=[validate_order],
        label=u'Number of threads',
        # required=False,
    )
    QRFopts = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        label=u'QRFopts',
    )
    ref_target = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Ref target',
    )
    clean_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Clean name',
    )

    class Meta:
        model = RFScore
        fields = [
            'name',
            'area',
            'year_group',
            'bias_corrn',
            'number_of_threads',
            'QRFopts',
            'ref_target',
            'clean_name',
            'run_parallel',
        ]


class RemapForm(forms.ModelForm):
    """ form for editing Remap Card """
    def __init__(self, *args, **kwargs):
        super(RemapForm, self).__init__(*args, **kwargs)

    run_parallel = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Run parallel',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    file_spec = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'File spec',
    )
    roi = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Roi',
    )
    output_root = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Output root',
    )
    output_suffix = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Output suffix',
    )
    scale = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Scale',
    )
    output = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Output',
    )
    color_table = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Color table',
    )
    refstats_file = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Refstats file',
    )
    refstats_scale = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Refstats scale',
    )

    class Meta:
        model = Remap
        fields = [
            'name',
            'file_spec',
            'roi',
            'output_root',
            'output_suffix',
            'scale',
            'output',
            'color_table',
            'refstats_file',
            'refstats_scale',
            'run_parallel',
        ]


class YearFilterForm(forms.ModelForm):
    """ form for editing YearFilter Card """
    def __init__(self, *args, **kwargs):
        super(YearFilterForm, self).__init__(*args, **kwargs)

    run_parallel = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Run parallel',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    area = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=Area.objects.all(),
        # empty_label=None,
        label=u'Area',
    )
    filetype = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Filetype',
    )
    filter = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Filter',
    )
    filter_output = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Filter output',
    )
    extend_start = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Extend start',
    )
    input_fourier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Input fourier',
    )
    output_directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Output directory',
    )
    input_directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Input directory',
    )

    class Meta:
        model = YearFilter
        fields = [
            'name',
            'area',
            'filetype',
            'filter',
            'filter_output',
            'extend_start',
            'input_fourier',
            'output_directory',
            'input_directory',
            'run_parallel',
        ]


class CollateForm(forms.ModelForm):
    """ form for editing Collate Card """
    def __init__(self, *args, **kwargs):
        super(CollateForm, self).__init__(*args, **kwargs)

    run_parallel = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Run parallel',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    area = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=Area.objects.all(),
        # empty_label=None,
        label=u'Area',
    )
    mode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label=u'Mode',
    )
    input_file = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Input file',
    )
    output_tile_subdir = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Output tile subdir',
    )
    input_scale_factor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Input scale factor',
    )

    class Meta:
        model = Collate
        fields = [
            'name',
            'area',
            'mode',
            'input_file',
            'output_tile_subdir',
            'input_scale_factor',
            'run_parallel',
        ]


class PreProcForm(forms.ModelForm):
    """ form for editing PreProc Card """
    def __init__(self, *args, **kwargs):
        super(PreProcForm, self).__init__(*args, **kwargs)

    run_parallel = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Run parallel',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    area = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=Area.objects.all(),
        # empty_label=None,
        label=u'Area',
    )
    mode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label=u'Mode',
    )
    year_group = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=YearGroup.objects.all(),
        # empty_label=None,
        label=u'Year group',
    )

    class Meta:
        model = PreProc
        fields = [
            'name',
            'area',
            'mode',
            'year_group',
            'run_parallel',
        ]


class MergeCSVForm(forms.ModelForm):
    """ form for editing MergeCSV Card """
    def __init__(self, *args, **kwargs):
        super(MergeCSVForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    csv1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Csv1',
    )
    csv2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Csv2',
    )

    class Meta:
        model = MergeCSV
        fields = [
            'name',
            'csv1',
            'csv2',
        ]


class RFTrainForm(forms.ModelForm):
    """ form for editing RFTrain Card """
    def __init__(self, *args, **kwargs):
        super(RFTrainForm, self).__init__(*args, **kwargs)

    run_parallel = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Run parallel',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    tile_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=TileType.objects.all(),
        # empty_label=None,
        label=u'Tile type',
    )
    number_of_trees = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0,
        validators=[validate_order],
        required=False,
        label=u'Number of trees',
    )
    value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        label=u'Value',
    )
    config_file = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Config file',
    )
    output_tile_subdir = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Output tile subdir',
    )
    input_scale_factor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Input scale factor',
    )

    class Meta:
        model = RFTrain
        fields = [
            'name',
            'tile_type',
            'number_of_trees',
            'value',
            'config_file',
            'output_tile_subdir',
            'input_scale_factor',
            'run_parallel',
        ]
