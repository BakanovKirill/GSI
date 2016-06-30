# -*- coding: utf-8 -*-
from django import forms

from core.validator_gsi import *
from cards.models import (QRF, RFScore, Remap,
                          YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain, RandomForest, CalcStats,
                          FILTER_OUT, PERIOD)
from gsi.models import (Area, YearGroup, TileType,
                        Satellite, InputDataDirectory, ListTestFiles,)


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
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=Area.objects.all(),
        empty_label='Select',
        label=u'Area',
    )
    year_group = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=YearGroup.objects.all(),
        empty_label='Select',
        label=u'Year group',
    )
    bias_corrn = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Bias corrn',
    )
    number_of_threads = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1,
        validators=[validate_order],
        required=False,
        label=u'Number of threads',
    )
    QRFopts = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        required=False,
        label=u'QRFopts',
    )
    ref_target = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        label=u'Ref target',
    )
    clean_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
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
    year_group = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=YearGroup.objects.all(),
        empty_label='Select',
        label=u'Year group',
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
        required=False,
        label=u'Output suffix',
    )
    scale = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Scale',
    )
    output = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Output',
    )
    color_table = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Color table',
    )
    refstats_file = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Refstats file',
    )
    refstats_scale = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0,
        validators=[validate_order],
        required=False,
        label=u'Refstats scale',
    )
    conditional_mean = forms.BooleanField(
        initial=False,
        required=False,
        label=u'ConditionalMean',
    )
    conditional_min = forms.BooleanField(
        initial=False,
        required=False,
        label=u'ConditionalMin',
    )
    conditional_median = forms.BooleanField(
        initial=False,
        required=False,
        label=u'ConditionalMedian',
    )
    conditional_max = forms.BooleanField(
        initial=False,
        required=False,
        label=u'ConditionalMax',
    )
    lower_quartile = forms.BooleanField(
        initial=False,
        required=False,
        label=u'LowerQuartile',
    )
    upper_quartile = forms.BooleanField(
        initial=False,
        required=False,
        label=u'UpperQuartile',
    )

    class Meta:
        model = Remap
        fields = [
            'name',
            'file_spec',
            'roi',
            'year_group',
            'output_root',
            'output_suffix',
            'scale',
            'output',
            'color_table',
            'refstats_file',
            'refstats_scale',
            'run_parallel',
            'conditional_mean',
            'conditional_min',
            'conditional_median',
            'conditional_max',
            'lower_quartile',
            'upper_quartile',
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
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=Area.objects.all(),
        empty_label='Select',
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
        required=False,
        label=u'Filter',
    )
    filter_output = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        label=u'Filter output',
    )
    extend_start = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        label=u'Extend start',
    )
    input_fourier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        label=u'Input fourier',
    )
    output_directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        label=u'Output directory',
    )
    input_directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
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
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=Area.objects.all(),
        empty_label='Select',
        label=u'Area',
    )
    mode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label=u'Mode',
    )
    output_tile_subdir = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Output tile subdir',
    )
    input_scale_factor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Input scale factor',
    )
    input_data_directory = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control disabled',
                                   "onchange": 'this.form.submit()'}),
        queryset=InputDataDirectory.objects.all(),
        empty_label='Select',
        required=False,
        label=u'Input Data Directory',
    )
    input_files = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'size': '10',
                   'class': 'form-control disabled'}
        ),
        queryset=ListTestFiles.objects.all(),
        required=False,
        label=u'Input Files',
    )

    class Meta:
        model = Collate
        fields = [
            'name',
            'area',
            'mode',
            'output_tile_subdir',
            'input_scale_factor',
            'run_parallel',
            'input_data_directory',
            'input_files',
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
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=Area.objects.all(),
        required=False,
        empty_label='Select',
        label=u'Area',
    )
    mode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False,
        label=u'Mode',
    )
    year_group = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=YearGroup.objects.all(),
        required=False,
        empty_label='Select',
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
        required=False,
        label=u'Csv1',
    )
    csv2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
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
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=TileType.objects.all(),
        empty_label='Select',
        label=u'Tile type',
    )
    value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        # required=False,
        label=u'Value',
    )
    config_file = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Config file',
    )
    output_tile_subdir = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Output tile subdir',
    )
    input_scale_factor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Input scale factor',
    )
    number_of_trees = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=50,
        validators=[validate_order],
        required=False,
        label=u'Number of trees',
    )
    training = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        # initial=0,
        # validators=[validate_order],
        required=False,
        label=u'Training',
    )
    number_of_variable = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        # initial=0,
        # validators=[validate_order],
        required=False,
        label=u'Number of Variable',
    )
    number_of_thread = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1,
        validators=[validate_order],
        required=False,
        label=u'Number of Thread',
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
            'training',
            'number_of_variable',
            'number_of_thread',
        ]


class RandomForestForm(forms.ModelForm):
    """ form for editing RandomForest Card """
    def __init__(self, *args, **kwargs):
        super(RandomForestForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    aoi_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'AoI Name',
    )
    satellite = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=Satellite.objects.all(),
        empty_label='Select',
        label=u'Satellite',
    )
    param_set = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
        label=u'Parameter Set'
    )
    run_set = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Run Set',
    )
    model = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Model',
    )
    mvrf = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'MVRF',
    )

    class Meta:
        model = RandomForest
        fields = [
            'name',
            'aoi_name',
            'satellite',
            'param_set',
            'run_set',
            'model',
            'mvrf',
        ]


class CalcStatsForm(forms.ModelForm):
    """ form for editing CalcStats Card """

    def __init__(self, *args, **kwargs):
        super(CalcStatsForm, self).__init__(*args, **kwargs)

        filter_out = forms.ModelChoiceField(
            widget=forms.Select(attrs={'class': 'form-control  disabled'}),
            queryset=FILTER_OUT,
            empty_label='Select',
            required=False,
            label=u'Filter Out',
        )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'Name',
    )
    output_tile_subdir = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        label=u'Output Tile Subdir',
    )
    year_group = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control disabled'}),
        queryset=YearGroup.objects.all(),
        empty_label='Select',
        required=False,
        label=u'Year group',
    )
    period = forms.CharField(
        widget=forms.Select(
                attrs={
                    "class": 'form-control disabled',
                    "onchange": 'visibleDoy()'
                },
                choices=PERIOD
        ),
        required=False,
        label=u'Period',
    )
    filter = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        initial=0,
        validators=[validate_order],
        error_messages={'required': 'Order must be a positive number'},
        required=False,
        label=u'Filter',
    )
    filter_out = forms.CharField(
        widget=forms.Select(
                attrs={'class': 'form-control  disabled'},
                choices=FILTER_OUT
        ),
        required=False,
        label=u'Filter Out',
    )
    input_fourier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Input Fourier',
    )
    out_dir = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        label=u'Out Dir',
    )
    doy_variable = forms.CharField(
        widget=forms.TextInput(
                attrs={'class': 'form-control doy disabled'}
        ),
        max_length=200,
        required=False,
        label=u'Input a variable',
    )

    class Meta:
        model = CalcStats
        fields = [
            'name',
            'output_tile_subdir',
            'year_group',
            'period',
            'filter',
            'filter_out',
            'input_fourier',
            'out_dir',
            'doy_variable',
        ]
