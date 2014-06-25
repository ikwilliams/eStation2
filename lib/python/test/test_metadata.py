#
#   Test metadata reading/writing
#

from unittest import TestCase

__author__ = 'clerima'

import locals
from osgeo import gdal
from lib.python.metadata import *

# input_dir = locals.es2globals['data_dir']+'FEWSNET_RFE/derived/10davg/'
# file=input_dir+'0101_FEWSNET_RFE_10davg_FEWSNET_Africa_8km.tif'

input_dir = locals.es2globals['data_dir']+'FEWSNET_RFE/tif/RFE/'
file=input_dir+'20100101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif'

class TestMapSet(TestCase):
    # def test_reading_meta_item(self):
    #
    #     fid = gdal.Open(file)
    #     sds_meta = SdsMetadata()
    #     sds_meta.read_from_ds(fid)
    #     sds_meta.print_out()

    def test_write_meta_into_domain(self):

        item='new_item'
        domain='my_own_domain'
        value='new_value'

        fid = gdal.Open(file)
        #sds_meta = SdsMetadata()
        fid.SetMetadataItem(item,value,domain)

    def test_read_meta_from_domain(self):

        my_domain='my_own_domain'

        fid = gdal.Open(file)
        # Get from default domain
        list = fid.GetMetadata_List()
        print ' Metadata from default domain'
        print list
        list = fid.GetMetadata_List(my_domain)
        print ' Metadata from my_domain '
        print list