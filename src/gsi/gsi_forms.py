# -*- coding: utf-8 -*-
from django import forms

from core.validator_gsi import *
from cards.models import CardItem
from gsi.models import (RunBase, Resolution, CardSequence, VariablesGroup,
                        HomeVariables, Tile, YearGroup, Year, Satellite,
                        InputDataDirectory, ConfigFile)


class RunForm(forms.ModelForm):
    """ form for editing RunBase """

    def __init__(self, *args, **kwargs):
        super(RunForm, self).__init__(*args, **kwargs)
        self.fields['card_sequence'].widget.attrs['disabled'] = 'disabled'
        self.fields['card_sequence'].initial = self.instance.card_sequence

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            # 'class': 'form-control border-bottom',
            'class': 'form-control',
            'placeholder': 'Name',
            # 'onChange': 'reloadPage(this)',
            # 'onChange': 'changeColorTyping(this)',
        }),
        label=u'Name', )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '5',
            'class': 'form-control border-bottom',
            'placeholder': 'Description',
            # 'onChange': 'changeColorTyping()',
        }),
        required=False,
        label=u'Description')
    purpose = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '5',
            'class': 'form-control border-bottom',
            'placeholder': 'Purpose of Run',
            # 'onChange': 'changeColorTyping()',
        }),
        required=False,
        label=u'Purpose of Run')
    directory_path = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-bottom form-control input-form',
            'placeholder': 'Directory path',
            # 'onChange': 'changeColorTyping()',
        }),
        # required=False,
        label=u'Directory path',
        help_text=u'Directory path is the name of the directory \
            that result will be stored')
    resolution = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control disabled',
            # 'onChange': "document.getElementById('new-run').submit()",
            # 'onChange': 'changeColorTyping()',
        }),
        queryset=Resolution.objects.all(),
        empty_label='Select',
        label=u'Resolution', )
    card_sequence = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Card sequence',
            # 'onChange': 'changeColorTyping()',
        }),
        required=False,
        label=u'Card sequence', )

    class Meta:
        model = RunBase
        fields = [
            'name',
            'author',
            'description',
            'purpose',
            'directory_path',
            'resolution',
        ]


class CardSequenceForm(forms.ModelForm):
    """ form for editing CardSecuence """

    def __init__(self, *args, **kwargs):
        super(CardSequenceForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )
    environment_override = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '5',
                                     'class': 'form-control'}),
        label=u'Environment override', )
    environment_base = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=VariablesGroup.objects.all(),
        # empty_label=None,
        required=False,
        label=u'Environment base', )

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
        widget=forms.Select(
            attrs={'class': 'form-control disabled',
                   'type': "hidden"}),
        # queryset=CardSequence.cards.through.objects.all(),
        queryset=CardItem.objects.all(),
        # empty_label=None,
        label=u'Environment base', )
    order = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'number',
        }),
        validators=[validate_order],
        label=u'Order', )

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

        if 'instance' in kwargs:
            self.fields['card_item'].queryset = CardItem.objects.filter(
                id__in=kwargs['instance'].cards.values_list(
                    'id', flat=True))

    # name = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     label=u'Name',
    # )
    environment_override = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '5',
                                     'class': 'form-control'}),
        required=False,
        label=u'Environment override', )
    environment_base = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=VariablesGroup.objects.all(),
        required=False,
        empty_label='Select',
        label=u'Environment base', )
    card_item = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        # queryset=CardSequence.cards.through.objects.all(),
        # queryset=CardSequence.objects.filter(),
        queryset=None,
        # queryset=CardItem.objects.all(),
        empty_label='Select',
        required=False,
        label=u'Card items', )
    order = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0,
        validators=[validate_order],
        error_messages={'required': 'Order must be a positive number'},
        # empty_label=None,
        required=False,
        label=u'Ordered card items', )

    class Meta:
        model = CardSequence.cards.through
        fields = [
            # 'name',
            'environment_base',
            'environment_override',
            'card_item',
            'order',
        ]


class HomeVariablesForm(forms.ModelForm):
    """ form for editing Home Variables """

    SAT_TIF_DIR_ROOT = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='SAT_TIF_DIR_ROOT',
        label=u'Satelite Data Top Level', )
    RF_DIR_ROOT = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='RF_DIR_ROOT',
        label=u'Top directory for Random Forest Files', )
    USER_DATA_DIR_ROOT = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='USER_DATA_DIR_ROOT',
        label=u'Top Level for user data dir', )
    MODIS_DIR_ROOT = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='MODIS_DIR_ROOT',
        label=u'Top Level for raw Modis data', )
    RF_AUXDATA_DIR = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='RF_AUXDATA_DIR',
        label=u'Top Level for Auxilliary data (SOIL, DEM etc.)', )
    SAT_DIF_DIR_ROOT = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='SAT_DIF_DIR_ROOT',
        label=u'Top Level for Satelite TF files', )

    def __init__(self, *args, **kwargs):
        super(HomeVariablesForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeVariables
        fields = [
            'SAT_TIF_DIR_ROOT',
            'RF_DIR_ROOT',
            'USER_DATA_DIR_ROOT',
            'MODIS_DIR_ROOT',
            'RF_AUXDATA_DIR',
            'SAT_DIF_DIR_ROOT',
        ]


class EnvironmentGroupsForm(forms.ModelForm):
    """ form for editing Environment Groups """

    def __init__(self, *args, **kwargs):
        super(EnvironmentGroupsForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )
    environment_variables = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '5',
                                     'class': 'form-control'}),
        label=u'Environment variables')

    class Meta:
        model = VariablesGroup
        fields = [
            'name',
            'environment_variables',
        ]


class AreasForm(forms.ModelForm):
    """ form for editing Areas """

    def __init__(self, *args, **kwargs):
        super(AreasForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )
    tiles = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'size': '10',
                   'class': 'form-control'}),
        queryset=Tile.objects.all(),
        # empty_label=None,
        required=False,
        label=u'Tiles', )

    class Meta:
        model = VariablesGroup
        fields = [
            'name',
            'tiles',
        ]


class YearGroupForm(forms.ModelForm):
    """ form for editing YearGroup """

    def __init__(self, *args, **kwargs):
        super(YearGroupForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )
    years = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'size': '10',
                   'class': 'form-control'}),
        queryset=Year.objects.all(),
        required=False,
        label=u'Years', )

    class Meta:
        model = YearGroup
        fields = [
            'name',
            'years',
        ]


class SatelliteForm(forms.ModelForm):
    """ form for editing Satellite """

    def __init__(self, *args, **kwargs):
        super(SatelliteForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )

    class Meta:
        model = Satellite
        fields = ['name', ]


class UploadFileForm(forms.Form):
    test_data = forms.FileField(label='Load Test Data')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['test_data'].widget.attrs.update({
            'class': 'form-control upload-file'
        })


class InputDataDirectoryForm(forms.ModelForm):
    """form for editing InputDataDirectory"""

    def __init__(self, *args, **kwargs):
        super(InputDataDirectoryForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )

    class Meta:
        model = InputDataDirectory
        fields = ['name', ]


class ConfigFileForm(forms.ModelForm):
    """form for editing ConfigFile"""

    def __init__(self, *args, **kwargs):
        super(ConfigFileForm, self).__init__(*args, **kwargs)


class ResolutionForm(forms.ModelForm):
    """form for editing Resolution"""

    def __init__(self, *args, **kwargs):
        super(ResolutionForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name',
        help_text='This will be a short display of the value, i.e. 1KM, 250M',)

    value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Value',
        help_text='Value in meters, e.g 1000 for 1KM display name',)

    class Meta:
        model = Resolution
        fields = ['name', 'value',]


class TileForm(forms.ModelForm):
    """form for editing Tile"""

    def __init__(self, *args, **kwargs):
        super(TileForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )

    class Meta:
        model = Tile
        fields = ['name', ]


class YearForm(forms.ModelForm):
    """form for editing Year"""

    def __init__(self, *args, **kwargs):
        super(YearForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=u'Name', )

    class Meta:
        model = Year
        fields = ['name', ]
