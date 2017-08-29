# -*- coding: utf-8 -*-
from itertools import chain

from django import forms
from django.contrib.auth.models import User

from core.validator_gsi import validate_order, validate_lutfile
from core.utils import get_list_lutfiles
from customers.models import (Category, ShelfData, DataSet, LutFiles,
                            CustomerAccess, CustomerPolygons, LUTFILES,
                            SCALE)


class CategoryForm(forms.ModelForm):
    """**Form for editing Category.**"""

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name')

    class Meta:
        model = Category
        fields = ['name',]


class ShelfDataForm(forms.ModelForm):
    """**Form for editing ShelfData.**"""

    def __init__(self, *args, **kwargs):
        super(ShelfDataForm, self).__init__(*args, **kwargs)

    category = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=Category.objects.all(),
        empty_label='Select',
        label=u'Category', )
    attribute_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=u'Attribute Name')
    root_filename = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=u'Root Filename')
    units = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=u'Units')
    scale = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
        initial=0.0,
        min_value=0.0,
        validators=[validate_order],
        error_messages={'required': 'Must be a positive number'},
        required=False,
        label=u'Scale',
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '5',
            'class': 'form-control border-bottom',
            'placeholder': 'Description',
        }),
        required=False,
        label=u'Description')
    show_totals = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Show Totals',
    )
    lutfiles = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        required=False,
        queryset=LutFiles.objects.all(),
        empty_label='Select',
        label=u'LUT File', )

    class Meta:
        model = ShelfData
        fields = ['category', 'attribute_name', 'root_filename', 'units',
                'description', 'show_totals', 'scale', 'lutfiles']


class DataSetForm(forms.ModelForm):
    """**Form for editing DataSet.**"""

    def __init__(self, *args, **kwargs):
        super(DataSetForm, self).__init__(*args, **kwargs)

        if self.instance.shelf_data:
            self.fields['root_filename'].initial = self.instance.shelf_data.root_filename
            self.fields['attribute_name'].initial = self.instance.shelf_data.attribute_name
        else:
            self.fields['root_filename'].initial = ''
            self.fields['attribute_name'].initial = ''

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name')
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=u'Description')
    results_directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Enter only the project folder. For example: "WagnerB1/Scores_All"',
        label=u'Results Directory')
    is_ts = forms.BooleanField(
        initial=False,
        required=False,
        label=u'Time Series',
    )
    # shelf_data = forms.ModelChoiceField(
    #     widget=forms.Select(attrs={
    #         'class': 'form-control',
    #         'disabled': 'disabled',
    #     }),
    #     required=False,
    #     queryset=ShelfData.objects.all(),
    #     empty_label='Select',
    #     label=u'Shelf Data', )
    root_filename = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=False,
        label=u'Root Filename', )
    attribute_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=False,
        label=u'Attribute Name', )

    class Meta:
        model = DataSet
        fields = ['name', 'description', 'results_directory', 'is_ts']


class CustomerAccessForm(forms.ModelForm):
    """**Form for editing CustomerAccess.**"""

    def __init__(self, *args, **kwargs):
        super(CustomerAccessForm, self).__init__(*args, **kwargs)

    user = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=User.objects.all(),
        empty_label='Select',
        label=u'Customer Name', )
    data_set = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'size': '10',
                   'class': 'form-control'}),
        queryset=DataSet.objects.all(),
        required=False,
        label=u'DataSets', )

    class Meta:
        model = CustomerAccess
        fields = [
            'user',
            'data_set',
        ]


class CustomerPolygonsForm(forms.ModelForm):
    """**Form for editing Polygons.**"""

    def __init__(self, *args, **kwargs):
        super(CustomerPolygonsForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter area name'}),
        required=False,
        label=u'Name')

    class Meta:
        model = CustomerPolygons
        fields = ['name',]


class LutFilesForm(forms.ModelForm):
    """**Form for editing LutFiles.**"""

    def __init__(self, *args, **kwargs):
        super(LutFilesForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        # required=False,
        label=u'Name'
    )
    lut_file = forms.CharField(
        widget=forms.Select(
                attrs={'class': 'form-control'},
                choices=LUTFILES),
        # required=False,
        validators=[validate_lutfile],
        label=u'LUT File'
    )
    max_val = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=100,
        min_value=0,
        validators=[validate_order],
        error_messages={'required': 'Must be a positive number'},
        required=False,
        label=u'Max value',
        help_text=u'Maximum Value for colour scaling'
    )
    legend = forms.CharField(
        widget=forms.Select(
                attrs={'class': 'form-control'},
                choices=SCALE),
        required=False,
        label=u'Legend'
    )
    units = forms.CharField(
        widget=forms.TextInput(
                attrs={'class': 'form-control'}),
        required=False,
        label=u'Units'
    )
    val_scale = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
        initial=1.0,
        min_value=0.0,
        validators=[validate_order],
        error_messages={'required': 'Must be a positive number'},
        required=False,
        label=u'Value Scale',
        help_text=u'Pixel Scale Factor for units'
    )


    class Meta:
        model = LutFiles
        fields = ['name', 'lut_file', 'max_val', 'legend', 'units', 'val_scale']


