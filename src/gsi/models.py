# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()
from solo.models import SingletonModel
from django.db import IntegrityError

from core.utils import (UnicodeNameMixin, create_new_folder, update_root_list_files, update_list_dirs,
                        slash_remove_from_path, create_symlink)
from gsi.settings import STATIC_ROOT, STATIC_DIR


class HomeVariables(SingletonModel):
    """**Model for the Home Variables.**

    :Fields:

        **SAT_TIF_DIR_ROOT**: Satelite Data Top Level

        **RF_DIR_ROOT**: Top directory of Random Forest Files

        **USER_DATA_DIR_ROOT**: Top Level for user data directory

        **MODIS_DIR_ROOT**: Top Level for raw Modis data

        **RF_AUXDATA_DIR**: Top Level for Auxilliary data(SOIL, DEM etc.

        **SAT_DIF_DIR_ROOT**: Top Level for Satelite TF files

    """

    SAT_TIF_DIR_ROOT = models.CharField(
        max_length=300,
        verbose_name=_('Satelite Data Top Level'),
        help_text=_('SAT_TIF_DIR_ROOT'))
    RF_DIR_ROOT = models.CharField(
        max_length=300,
        verbose_name=_('Top directory of Random Forest Files'),
        help_text=_('RF_DIR_ROOT'))
    USER_DATA_DIR_ROOT = models.CharField(
        max_length=300,
        verbose_name=_('Top Level for user data directory'),
        help_text=_('USER_DATA_DIR_ROOT'))
    MODIS_DIR_ROOT = models.CharField(
        max_length=300,
        verbose_name=_('Top Level for raw Modis data'),
        help_text=_('MODIS_DIR_ROOT'))
    RF_AUXDATA_DIR = models.CharField(
        max_length=300,
        verbose_name=_('Top Level for Auxilliary data(SOIL, DEM etc.)'),
        help_text=_('RF_AUXDATA_DIR'))
    SAT_DIF_DIR_ROOT = models.CharField(
        max_length=300,
        verbose_name=_('Top Level for Satelite TF files'),
        help_text=_('SAT_DIF_DIR_ROOT'))

    def save(self, *args, **kwargs):
        if self.USER_DATA_DIR_ROOT:
            path_dir_root = self.USER_DATA_DIR_ROOT
            static_dir_root = path_dir_root.split('/')[-1]

            if not static_dir_root:
                static_dir_root = path_dir_root.split('/')[-2:-1]

            path_static = STATIC_DIR + '/' + static_dir_root[0]
            path_collected_static = STATIC_ROOT + '/' + static_dir_root[0]
            path_static = slash_remove_from_path(path_static)
            path_collected_static = slash_remove_from_path(
                path_collected_static)
            create_symlink(STATIC_DIR, path_dir_root, path_static)
            create_symlink(STATIC_ROOT, path_dir_root, path_collected_static)

        return super(HomeVariables, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(_('Home variables'))

    class Meta:
        verbose_name = _(u"Home variables")


class VariablesGroup(UnicodeNameMixin, models.Model):
    """**Model for the Variables Groups.**

    :Fields:

        **name**: Name of a Variables Group

        **environment_variables**: List of the Variables

    """

    name = models.CharField(max_length=50)
    environment_variables = models.TextField()


class Tile(UnicodeNameMixin, models.Model):
    """**Model for the Tiles.**

    :Fields:

        **name**: Name of a Tile

    """

    name = models.CharField(max_length=6, unique=True)


class Area(UnicodeNameMixin, models.Model):
    """**Model for the Areas.**

    :Fields:

        **name**: Name of a Area

        **tiles**: Relation with the Tile model from the applications GSI

    """

    name = models.CharField(max_length=50, unique=True)
    tiles = models.ManyToManyField(Tile, related_name='areas')

    class Meta:
        ordering = ['name']


class Year(UnicodeNameMixin, models.Model):
    """**Model for the Years.**

    :Fields:

        **name**: Name of a Year

    """

    name = models.CharField(max_length=4)


class YearGroup(UnicodeNameMixin, models.Model):
    """**Model for the Year Groups.**

    :Fields:

        **name**: Name of a Tile

        **years**: Relation with the Year model from the applications GSI

    """

    name = models.CharField(max_length=50)
    years = models.ManyToManyField(Year, related_name='year_groups')


class Satellite(UnicodeNameMixin, models.Model):
    """**Model for the Satellites.**

    :Fields:

        **name**: Name of a Satellite

    """

    name = models.CharField(max_length=50)


class InputDataDirectory(UnicodeNameMixin, models.Model):
    """**Model for the Input Data Directorys.**

    :Fields:

        **name**: Name of a Input Data Directory

        **full_path**: Full path to the Input Data Directory

    """

    name = models.CharField(max_length=200, unique=True)
    full_path = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        """**The method "save" start when create a new object of the model**

        Create the new directory ('name' variable) at the specified path ('full_path' variable)

        """
        try:
            self.full_path = create_new_folder(self.name)
            super(InputDataDirectory, self).save(*args, **kwargs)
        except IntegrityError, e:
            pass
        update_root_list_files()
        update_list_dirs()


class ListTestFiles(UnicodeNameMixin, models.Model):
    """**Model for the Lists Test Files.**

    :Fields:

        **name**: Name of a List Test Files

        **input_data_directory**: Relation with the InputDataDirectory model from the applications GSI

        **size**: File size

        **date_modified**: Date modified of file

    """

    name = models.CharField(max_length=200)
    input_data_directory = models.ForeignKey(
        'InputDataDirectory',
        blank=True,
        null=True,
        related_name='data_directory')
    size = models.CharField(max_length=100, blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)


class Resolution(UnicodeNameMixin, models.Model):
    """**Model for the Resolutions.**

    :Fields:

        **name**: Name of a Resolution (this will be a short display of the value, i.e. 1KM, 250M)

        **value**: Value in meters, e.g 1000 for 1KM display name

    """

    name = models.CharField(
        max_length=50,
        help_text=_(
            'This will be a short display of the value, i.e. 1KM, 250M'))
    value = models.CharField(
        max_length=20,
        help_text=_('Value in meters, e.g 1000 for 1KM display name'))


class TileType(UnicodeNameMixin, models.Model):
    """**Model for the Tile Types.**

    :Fields:

        **name**: Name of a Tile Type

    """

    name = models.CharField(max_length=50)


class OrderedCardItem(models.Model):
    """**Model for the Ordered Card Items.**

    :Functions:
        The OrderedCardItem model is designed for relational communication the objects of models of cards with objects CardSequence model

    :Fields:

        **card_item**: Relation with the CardItem model from the applications Cards

        **sequence**: Relation with the CardSequence model from the applications GSI

        **order**: Priority object in its CardSequence

        **run_parallel**: Startup type parallel or not

        **number_sub_cards**: The number of sub-cards to the card when run

    """

    card_item = models.ForeignKey('cards.CardItem', related_name='ordered_cards')
    sequence = models.ForeignKey('CardSequence')
    order = models.PositiveIntegerField(default=0)
    run_parallel = models.BooleanField(default=False)
    number_sub_cards = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u"{0}".format(self.card_item)

    class Meta:
        ordering = ('order', )


class ConfigFile(models.Model):
    """**Model for the Config Files.**

    :Fields:

        **pathname**: Path to the config file

        **description**: The config file description

        **configuration_file**: Name the configuration file

    """

    pathname = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    configuration_file = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _(u"Configuration Files")
        ordering = ('pathname', )

    def __unicode__(self):
        return u"{0}".format(self.pathname)


class CardSequence(UnicodeNameMixin, models.Model):
    """**Model for the Card Sequences.**

    :Functions:
        The CardSequence model unites the selected cards in a sequence of cards

    :Fields:

        **name**: Name the Card Sequence

        **environment_base**: Relation with the VariablesGroup model from the applications GSI

        **environment_override**: The Environment override for the object of the Card Sequence model

        **cards**: Relation with the CardItem model from the applications cards

        **configfile**: Relation with the ConfigFile model from the applications GSI

    """

    name = models.CharField(max_length=100)
    environment_base = models.ForeignKey(VariablesGroup, null=True, blank=True)
    environment_override = models.TextField(null=True, blank=True)
    cards = models.ManyToManyField(
        'cards.CardItem',
        through=OrderedCardItem,
        related_name='card_sequences')
    configfile = models.ForeignKey(ConfigFile, null=True, blank=True)


class Log(UnicodeNameMixin, models.Model):
    """**Model for the Logs.**

    :Fields:

        **name**: Name the Log

        **log_file_path**: The path to the log file

        **log_file**: The log file name

    """

    name = models.CharField(max_length=200, null=True, blank=True)
    log_file_path = models.CharField(max_length=200, null=True, blank=True)
    log_file = models.FileField(blank=True, null=True)


class RunBase(UnicodeNameMixin, models.Model):
    """**Model for the Runs Base.**

    :Functions:
        The CardSequence model is designed to run the cards that are in the CardSequence model

    :Fields:

        **name**: Name the Run Bas

        **author**: Relation with the User model from the Django Auth model

        **description**: RunBase description

        **purpose**: Purpose of Run

        **directory_path**: Directory path

        **resolution**: Resolution

        **card_sequence**: Relation with the CardSequence model from the applications GSI

        **date_created**: The RunBase object date created

        **date_modified**: The RunBase object date modified

    """

    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    directory_path = models.CharField(max_length=200)

    resolution = models.ForeignKey(Resolution)
    card_sequence = models.ForeignKey(CardSequence, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """The method 'save' records the modified date when the object was changed"""
        self.date_modified = datetime.now()
        return super(RunBase, self).save(*args, **kwargs)


STATES = (
    ('created', 'Created'),
    ('pending', 'Pending'),
    ('running', 'Running'),
    ('success', 'Success'),
    ('fail', 'Fail'), )


class Run(models.Model):
    """**Model for the Runs.**

    :Functions:
        The Run model stores information about each startup RunBase model

    :Fields:

        **user**: Relation with the User model from the Django Auth model

        **run_base**: Relation with the RunBase model from the applications GSI

        **state**: Execution the RunBase model status

        **log**: Relation with the Log model from the applications GSI

        **run_date**: Execution the RunBase model date of creating

    """

    user = models.ForeignKey(User, null=True, blank=True)
    run_base = models.ForeignKey(RunBase)
    state = models.CharField(max_length=100, choices=STATES, default='running')
    log = models.ForeignKey(Log, null=True, blank=True)
    run_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0}".format(self.run_base)


class RunStep(UnicodeNameMixin, models.Model):
    """**Model for the Runs Steps.**

    :Functions:
        RunStep model stores information about the cards after execute RunBase model

    :Fields:

        **parent_run**: Relation with the Run model from the applications GSI

        **card_item**: Relation with the OrderedCardItem model from the applications GSI

        **state**: Status executed of the card work

        **start_date**: Date of the run of card


    """

    parent_run = models.ForeignKey(Run)
    card_item = models.ForeignKey(OrderedCardItem)
    state = models.CharField(max_length=100, choices=STATES, default='pending')
    start_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0}_{1}".format(self.card_item, self.parent_run)

    def get_next_step(self):
        """Gets the next card. If it is, then return the card object. If not - False"""

        next_card = OrderedCardItem.objects.filter(
            sequence__runbase=self.parent_run.run_base,
            order__gte=self.card_item.order).exclude(id=self.card_item.id)
        is_last_step = False

        if len(next_card) == 0:
            return False, True
        if next_card:
            next_card = next_card[0]
            step, created = RunStep.objects.get_or_create(
                parent_run=self.parent_run, card_item=next_card)
            return step, is_last_step
        else:
            return False, False


class SubCardItem(UnicodeNameMixin, models.Model):
    """**Model for the Sub-Card Items.**

    :Functions:
        The SubCardItem model unites the syb-cards with its main the card to the parallel start.

    :Fields:

        **name**: Name the Sub-Card Item

        **state**: Status executed of the card work

        **run_id**: RUN ID's

        **card_id**: CARD ID's

        **start_date**: Date of the run of syb-card

        **start_time**: Time of the run of syb-card

    """

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATES, default='pending')
    run_id = models.PositiveIntegerField()
    card_id = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    start_time = models.TimeField(auto_now_add=True, null=True, blank=True)
