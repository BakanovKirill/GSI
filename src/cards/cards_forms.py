# -*- coding: utf-8 -*-
from django import forms

from core.validator_gsi import *
from cards.models import (QRF)

# import pdb;pdb.set_trace()

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
        label=u'Interval',
        required=False,
    )
    number_of_trees = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0,
        validators=[validate_order],
        label=u'Number of trees',
        required=False,
    )
    number_of_threads = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1,
        validators=[validate_order],
        label=u'Number of threads',
        required=False,
    )
    directory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        label=u'Directory',
        required=False,
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