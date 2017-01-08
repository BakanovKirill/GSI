# -*- coding: utf-8 -*-
from django import forms

from customers.models import (Category, ShelfData)


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
            'class': 'form-control disabled',
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
