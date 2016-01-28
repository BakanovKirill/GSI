# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from cards.models import CardItem
from gsi.models import (RunBase, Resolution,
                        CardSequence, VariablesGroup)


def validate_order(value):
    if value < 0:
        raise ValidationError('{0} invalid value. Order must be a positive number'.format(value))
    return value


class RunForm(forms.ModelForm):
    """ form for editing RunBase """
    def __init__(self, *args, **kwargs):
        super(RunForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label=u'Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
        required=False,
        label=u'Description'
    )
    purpose = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
        required=False,
        label=u'Purpose of Run'
    )
    directory_path = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=u'Directory path',
        help_text=u'Directory path is the name of the directory \
            that result will be stored'
    )
    resolution = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": 'form-control'}),
        queryset=Resolution.objects.all(),
        # empty_label=None,
        label=u'Resolution',
    )
    card_sequence = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=CardSequence.objects.all(),
        # empty_label=None,
        label=u'Card sequence',
    )

    class Meta:
        model = RunBase
        fields = [
            'name',
            'author',
            'description',
            'purpose',
            'directory_path',
            'resolution',
            'card_sequence',
        ]


class CardSequenceForm(forms.ModelForm):
    """ form for editing CardSecuence """
    def __init__(self, *args, **kwargs):
        super(CardSequenceForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label=u'Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    environment_override = forms.CharField(
        label=u'Environment override',
        widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'})
    )
    environment_base = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=VariablesGroup.objects.all(),
        # empty_label=None,
        label=u'Environment base',
    )

    class Meta:
        model = CardSequence
        fields = [
            'name',
            'environment_base',
            'environment_override',
        ]


class CardSequenceCardForm(forms.ModelForm):
    """ form for editing CardSecuence """
    def __init__(self, *args, **kwargs):
        super(CardSequenceCardForm, self).__init__(*args, **kwargs)

    card_item = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        # queryset=CardSequence.cards.through.objects.all(),
        queryset=CardItem.objects.all(),
        # empty_label=None,
        label=u'Environment base',
    )
    order = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'number',
        }),
        validators=[validate_order],
        label=u'Order',
    )

    class Meta:
        model = CardSequence.cards.through
        fields = [
            'card_item',
            'order',
        ]


class CardSequenceCreateForm(forms.ModelForm):
    """ form for editing CardSecuence """
    def __init__(self, *args, **kwargs):
        super(CardSequenceCreateForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name',
    )
    environment_override = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
        required=False,
        label=u'Environment override',
    )
    environment_base = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=VariablesGroup.objects.all(),
        required=False,
        label=u'Environment base',
    )
    card_item = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        # queryset=CardSequence.cards.through.objects.all(),
        queryset=CardItem.objects.all(),
        required=False,
        label=u'Card items',
    )
    order = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        initial=0,
        validators=[validate_order],
        error_messages={'required': 'Order must be a positive number'},
        # empty_label=None,
        label=u'Ordered card items',
    )

    class Meta:
        model = CardSequence.cards.through
        fields = [
            'name',
            'environment_base',
            'environment_override',
            'card_item',
            'order',
        ]