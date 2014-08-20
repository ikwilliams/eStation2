#
#   Test metadata reading/writing
#

from unittest import TestCase

__author__ = 'clerima'

import locals
from osgeo import gdal
from osgeo.gdalconst import *
from lib.python.metadata import *
import tempfile
import shutil

input_dir = locals.es2globals['test_data_refs_dir']+'Metadata/'
file=input_dir+'20140601_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif'

class TestMapSet(TestCase):

    def test_writing_reading_an_item(self):

        my_item='Test_Metadata_Item'
        my_value='Test_Metadata_Value'

        # Create a tmp Tiff file
        try:
            tmpdir = tempfile.mkdtemp(prefix=__name__, suffix='_test_writing_an_item', dir=locals.es2globals['temp_dir'])
        except IOError:
            logger.error('Cannot create temporary dir ' + locals.es2globals['temp_dir'] + '. Exit')
            return 1

        filename = tmpdir+'/temp_target.tif'

        gtiff_driver = gdal.GetDriverByName('GTiff')
        out_ds = gtiff_driver.Create(filename, 1, 1, 1, 1)

        out_ds.SetMetadataItem(my_item, my_value)

        # Close the file and remove temp dir
        out_ds = None

        # Open the file for reading
        in_ds = gdal.Open(filename, GA_ReadOnly)
        read_value=in_ds.GetMetadataItem(my_item)

        self.assertEqual(my_value, read_value)

        # Remove the tmp dir
        shutil.rmtree(tmpdir)

    def test_writing_meta_to_new_file(self):

        sds_meta = SdsMetadata()

        # Create a dummy output File
        try:
            tmpdir = tempfile.mkdtemp(prefix=__name__, suffix='_writing_meta_to_new_file', dir=locals.es2globals['temp_dir'])
        except IOError:
            logger.error('Cannot create temporary dir ' + locals.es2globals['temp_dir'] + '. Exit')
            return 1

        # Dummy output File
        filename = tmpdir+'/temp_target.tif'
        gtiff_driver = gdal.GetDriverByName('GTiff')
        out_ds = gtiff_driver.Create(filename, 1, 1, 1, 1)

        sds_meta.write_to_ds(out_ds)

        # Close the file
        out_ds = None
        gtiff_driver = None

        self.assertTrue(os.path.isfile(filename))

    def test_writing_meta_to_existing_file(self):

        sds_meta = SdsMetadata()

        # Create a dummy output File
        try:
            tmpdir = tempfile.mkdtemp(prefix=__name__, suffix='_writing_meta_to_new_file', dir=locals.es2globals['temp_dir'])
        except IOError:
            logger.error('Cannot create temporary dir ' + locals.es2globals['temp_dir'] + '. Exit')
            return 1

        # Dummy output File
        filename = tmpdir+'/temp_target.tif'
        gtiff_driver = gdal.GetDriverByName('GTiff')
        out_ds = gtiff_driver.Create(filename, 1, 1, 1, 1)

        # Close the file
        out_ds = None
        gtiff_driver = None

        sds_meta.write_to_file(filename)

        self.assertTrue(os.path.isfile(filename))


    def test_reading_meta_items_from_ds(self):

        # Read from a reference file
         fid = gdal.Open(file)
         sds_meta = SdsMetadata()
         sds_meta.read_from_ds(fid)
         sds_meta.print_out()

         value = sds_meta.get_item('eStation2_mapset')
         self.assertEqual(value, 'FEWSNET_Africa_8km')

         value = sds_meta.get_item('eStation2_nodata')
         self.assertEqual(value, '-32768')

         value = sds_meta.get_item('eStation2_es2_version')
         self.assertEqual(value, 'my_eStation2_sw_release')

         value = sds_meta.get_item('eStation2_conversion')
         self.assertEqual(value, 'Phys = DN * scaling_factor + scaling_offset')

         value = sds_meta.get_item('eStation2_input_files')
         self.assertEqual(value, '/data/Archives/FewsNET/a14061rb.zip;')

         value = sds_meta.get_item('eStation2_subProduct')
         self.assertEqual(value, 'rfe')

         value = sds_meta.get_item('eStation2_product')
         self.assertEqual(value, 'fewsnet_rfe')

         value = sds_meta.get_item('eStation2_scaling_factor')
         self.assertEqual(value, '1.0')

         value = sds_meta.get_item('eStation2_unit')
         self.assertEqual(value, None)

    def test_reading_meta_items_from_file(self):

         sds_meta = SdsMetadata()
        # Read from a reference file
         sds_meta.read_from_file(file)
         sds_meta.print_out()

         value = sds_meta.get_item('eStation2_mapset')
         self.assertEqual(value, 'FEWSNET_Africa_8km')

         value = sds_meta.get_item('eStation2_nodata')
         self.assertEqual(value, '-32768')

         value = sds_meta.get_item('eStation2_es2_version')
         self.assertEqual(value, 'my_eStation2_sw_release')

         value = sds_meta.get_item('eStation2_conversion')
         self.assertEqual(value, 'Phys = DN * scaling_factor + scaling_offset')

         value = sds_meta.get_item('eStation2_input_files')
         self.assertEqual(value, '/data/Archives/FewsNET/a14061rb.zip;')

         value = sds_meta.get_item('eStation2_subProduct')
         self.assertEqual(value, 'rfe')

         value = sds_meta.get_item('eStation2_product')
         self.assertEqual(value, 'fewsnet_rfe')

         value = sds_meta.get_item('eStation2_scaling_factor')
         self.assertEqual(value, '1.0')

         value = sds_meta.get_item('eStation2_unit')
         self.assertEqual(value, None)

