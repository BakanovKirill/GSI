from datetime import datetime
import os

from django.test import TestCase
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.core.files import File

from gsi.models import (HomeVariables, VariablesGroup, Tile, Area, Year, YearGroup, Satellite, InputDataDirectory,
                        ListTestFiles, Resolution, TileType, OrderedCardItem, ConfigFile, CardSequence, Log)
from cards.models import CardItem, QRF


class ModelsTestCase(TestCase):
    """The test the GSI models"""

    def setUp(self):
        """We set the initial data."""

        home_variables = HomeVariables.objects.create(
            SAT_TIF_DIR_ROOT='/lustre/w23/mattgsi/satdata/sat_tif/250m',
            RF_DIR_ROOT='/lustre/w23/mattgsi/satdata/sat_tif/250m',
            USER_DATA_DIR_ROOT='/lustre/w23/mattgsi/satdata/sat_tif/250m',
            MODIS_DIR_ROOT='/lustre/w23/mattgsi/satdata/sat_tif/250m',
            RF_AUXDATA_DIR='/lustre/w23/mattgsi/satdata/sat_tif/250m',
            SAT_DIF_DIR_ROOT='/lustre/w23/mattgsi/satdata/sat_tif/250m',
        )

        variables_group = VariablesGroup.objects.create(
            name='1km_override',
            environment_variables='RF_DIR_ROOT=/lustre/w23/mattgsi/satdata/RF/1km\n'\
                                    'export  RF_DIR=/lustre/w23/mattgsi/satdata/RF/1km\n'\
                                    'export MODIS_DIR=/home/w23/Satellite/Biomass-PreProcessing/Modis/New1km\n'\
                                    'export SAT_TIF_DIR=/lustre/w23/mattgsi/satdata/sat_tif/1km\n'\
                                    'export USER_DATA_DIR=/lustre/w23/mattgsi/satdata/RF/1km\n'\
        )

        # When you create the object Tile model to create the new object Area model
        tile = Tile.objects.create(name='h06v03')

        # Create a new object of the Area model
        # and add the created object of the Tile model in the M2M the "tiles" field
        area = Area.objects.create(name='ALASKA')
        area.tiles.add(tile)

        year = Year.objects.create(name='2016')

        # Create a new object of the YearGroup model
        # and add the created object of the Year model in the M2M the "years" field
        year_group = YearGroup.objects.create(name='2016_only')
        year_group.years.add(year)

        satellite = Satellite.objects.create(name='100m PROBA-V')

        inputdatadirectory = InputDataDirectory.objects.create(name='Crop_HarvestedArea')

        listtestfiles = ListTestFiles.objects.create(name='clover_Production_0.1.tif')

        resolution = Resolution.objects.create(name='1KM', value='1000')

        tiletype = TileType.objects.create(name='UserDataset')

        configfile = ConfigFile.objects.create(pathname='AUZ_SOC_2.cfg')

        # Create an object of the CardSequence model
        cardsequence = CardSequence.objects.create(name='CS155')
        # For the testing the CardSequence model to create the QRF card
        qrf_card = QRF.objects.create(name='QRF')

        log = Log.objects.create(
                name='1255_670.log',
                log_file_path='/lustre/w23/mattgsi/scripts/runs/R_1255/LOGS')

    def test_homevariable_model(self):
        """Testing start HomeVariables model.

        Checking with the creation of the test object initialization.
        Since the model is SingletonModel, then check to create another object model.
        """

        home_variables_all = HomeVariables.objects.all()
        home_variables = HomeVariables.objects.get(SAT_TIF_DIR_ROOT='/lustre/w23/mattgsi/satdata/sat_tif/250m')

        self.assertEqual(1, home_variables_all.count())
        self.assertEqual('/lustre/w23/mattgsi/satdata/sat_tif/250m', home_variables.SAT_TIF_DIR_ROOT)

        home_variables.SAT_TIF_DIR_ROOT = 'Satelite Data Top Level'
        home_variables.save()

        self.assertEqual(1, home_variables_all.count())
        self.assertEqual('Satelite Data Top Level', home_variables.SAT_TIF_DIR_ROOT)

        # You can not create another object
        # You will getting the error in the console what the object already exists
        with self.assertRaises(IntegrityError):
            home_variables_2 =  HomeVariables.objects.create(SAT_TIF_DIR_ROOT='/lustre')

    def test_variablesgroup_model(self):
        """Testing start of the VariablesGroup model."""

        variables_group_all = VariablesGroup.objects.all()
        variables_group = VariablesGroup.objects.get(name='1km_override')
        environment = 'RF_DIR_ROOT=/lustre/w23/mattgsi/satdata/RF/1km\n'\
                        'export  RF_DIR=/lustre/w23/mattgsi/satdata/RF/1km\n'\
                        'export MODIS_DIR=/home/w23/Satellite/Biomass-PreProcessing/Modis/New1km\n'\
                        'export SAT_TIF_DIR=/lustre/w23/mattgsi/satdata/sat_tif/1km\n'\
                        'export USER_DATA_DIR=/lustre/w23/mattgsi/satdata/RF/1km\n'

        self.assertEqual(1, variables_group_all.count())
        self.assertEqual(environment, variables_group.environment_variables)

    def test_tile_model(self):
        """Testing start of the Tile model."""

        tile_all = Tile.objects.all()

        self.assertEqual(1, tile_all.count())
        self.assertTrue(Tile.objects.get(name='h06v03'))

        # Check what created the model object Area when we created the model object Tile in initialisation
        self.assertTrue(Area.objects.get(name='h06v03'))

    def test_area_model(self):
        """Testing start of the Area model."""

        area_all = Area.objects.all()
        area_alaska = Area.objects.filter(name='ALASKA')
        area_tile = Area.objects.filter(tiles__name='h06v03')

        self.assertEqual(1, area_alaska.count())

        # There should be teh two object Area model
        self.assertEqual(2, area_all.count())
        self.assertEqual(2, area_tile.count())

    def test_year_model(self):
        """Testing start of the Year model."""

        year_all = Year.objects.all()
        year = Year.objects.get(name='2016')

        self.assertEqual(1, year_all.count())
        self.assertEqual('2016', year.name)

    def test_yeargroup_model(self):
        """Testing start of the YearGroup model."""

        yeargroup_all = YearGroup.objects.all()
        yeargroup_year = YearGroup.objects.filter(years__name='2016')

        self.assertEqual(1, yeargroup_all.count())
        self.assertEqual(1, yeargroup_year.count())

    def test_satellite_model(self):
        """Testing start of the Satellite model."""

        satellite_all = Satellite.objects.all()
        satellite = Satellite.objects.get(name='100m PROBA-V')

        self.assertEqual(1, satellite_all.count())
        self.assertEqual('100m PROBA-V', satellite.name)

    def test_input_data_directory_model(self):
        """Testing start of the InputDataDirectory model.

        When created model object InputDataDirectory create automatically the m2m field "full_path".

        The variable for the "full_path" field geting from the variable SAT_TIF_DIR_ROOT of the object
        of the HomeVariables model and the variable "name" of the object of the InputDataDirectory model
        """

        inputdatadirectory_all = InputDataDirectory.objects.all()
        inputdatadirectory = InputDataDirectory.objects.get(name='Crop_HarvestedArea')

        self.assertEqual(1, inputdatadirectory_all.count())
        self.assertEqual('Crop_HarvestedArea', inputdatadirectory.name)
        self.assertEqual('/lustre/w23/mattgsi/satdata/sat_tif/250m/Crop_HarvestedArea', inputdatadirectory.full_path)

        inputdatadirectory_all_2 = InputDataDirectory.objects.all()
        inputdatadirectory.full_path = '/home/w23'
        inputdatadirectory.save()

        self.assertEqual(1, inputdatadirectory_all_2.count())
        self.assertEqual('Crop_HarvestedArea', inputdatadirectory.name)
        self.assertEqual('/lustre/w23/mattgsi/satdata/sat_tif/250m/Crop_HarvestedArea', inputdatadirectory.full_path)

    def test_list_test_files_model(self):
        """Testing start of the ListTestFiles model."""

        listtestfiles_all = ListTestFiles.objects.all()
        datetime_now = datetime.now()

        self.assertEqual(1, listtestfiles_all.count())
        self.assertTrue(ListTestFiles.objects.get(name='clover_Production_0.1.tif'))

        listtestfiles = ListTestFiles.objects.get(name='clover_Production_0.1.tif')
        inputdatadirectory = InputDataDirectory.objects.get(name='Crop_HarvestedArea')

        listtestfiles.input_data_directory = inputdatadirectory
        listtestfiles.size = '645.55 KB'
        listtestfiles.date_modified = datetime_now
        listtestfiles.save()

        self.assertEqual(1, listtestfiles_all.count())
        self.assertEqual(inputdatadirectory, listtestfiles.input_data_directory)
        self.assertEqual('645.55 KB', listtestfiles.size)
        self.assertEqual(datetime_now, listtestfiles.date_modified)

    def test_resolution_model(self):
        """Testing start of the Resolution model."""

        resolution_all = Resolution.objects.all()

        self.assertEqual(1, resolution_all.count())
        self.assertTrue(Resolution.objects.get(name='1KM'))

    def test_tiletype_model(self):
        """Testing start of the TileType model."""

        tiletype_all = TileType.objects.all()

        self.assertEqual(1, tiletype_all.count())
        self.assertTrue(TileType.objects.get(name='UserDataset'))

    def test_configfile_model(self):
        """Testing start of the ConfigFile model."""

        configfile_all = ConfigFile.objects.all()

        self.assertEqual(1, configfile_all.count())
        self.assertTrue(ConfigFile.objects.get(pathname='AUZ_SOC_2.cfg'))

        configfile = ConfigFile.objects.get(pathname='AUZ_SOC_2.cfg')
        configfile.description = 'Test configfile'
        configfile.configuration_file = '/lustre/w23/mattgsi/scripts/runs'
        configfile.save()

        configfile_all = ConfigFile.objects.all()

        self.assertEqual(1, configfile_all.count())
        self.assertTrue(ConfigFile.objects.get(pathname='AUZ_SOC_2.cfg'))
        self.assertEqual('Test configfile', configfile.description)
        self.assertEqual('/lustre/w23/mattgsi/scripts/runs', configfile.configuration_file)

    def test_cardsequence_model(self):
        """Testing start of the CardSequence model."""

        cardsequence_all = CardSequence.objects.all()
        card_item_all = CardItem.objects.all()

        # Check what created an object of the CardItem model
        self.assertEqual(1, card_item_all.count())
        self.assertEqual(1, cardsequence_all.count())
        self.assertTrue(CardSequence.objects.get(name='CS155'))

        cardsequence = CardSequence.objects.get(name='CS155')
        variables_group = VariablesGroup.objects.get(name='1km_override')
        # Get an object of the CardItem model
        card_item = CardItem.objects.get(name='QRF')
        configfile = ConfigFile.objects.get(pathname='AUZ_SOC_2.cfg')

        # Across an intermediary model added an object of the CardItem model in an object of the CardSequence model
        ordered_card_item = OrderedCardItem.objects.create(card_item=card_item, sequence=cardsequence)
        cardsequence.environment_base = variables_group
        cardsequence.environment_override = 'This text field'
        cardsequence.configfile = configfile
        cardsequence.save()

        cardsequence_all = CardSequence.objects.all()

        self.assertEqual(1, cardsequence_all.count())
        self.assertTrue(OrderedCardItem.objects.get(card_item=card_item, sequence=cardsequence))

    def test_log_model(self):
        """Testing start of the Log model."""

        log_all = Log.objects.all()

        self.assertEqual(1, log_all.count())
        self.assertTrue(Log.objects.get(name='1255_670.log'))

        file_dir = os.path.abspath(os.curdir)
        full_file_path = os.path.join(file_dir, 'src/gsi/tests/1255_670.log')

        log = Log.objects.get(name='1255_670.log')

        self.assertFalse(log.log_file)

        log_file = open(full_file_path, 'rb')
        log_file = File(log_file)
        log.log_file = log_file
        log.save()

        self.assertTrue(log.log_file)
