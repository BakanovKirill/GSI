# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from customers.models import Category, ShelfData, DataSet, CustomerAccess


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
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '5',
            'class': 'form-control border-bottom',
            'placeholder': 'Description',
        }),
        required=False,
        label=u'Description')

    class Meta:
        model = ShelfData
        fields = ['category', 'attribute_name', 'root_filename', 'units', 'description']


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
        fields = ['name', 'description', 'results_directory']


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
