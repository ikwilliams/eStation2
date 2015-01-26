_author__ = "Marco Clerici"


from config import es_constants
from apps.acquisition import ingestion

import unittest

# Overwrite Dirs
es_constants.ingest_dir = es_constants.test_data_in_dir
es_constants.data_dir = es_constants.test_data_out


class TestIngestion(unittest.TestCase):

    def TestDriveAll(self):
        ingestion.drive_ingestion()
        self.assertEqual(1, 1)


    def test_ingest_vgt_ndvi(self):
        
        productcode = 'vgt_ndvi'
        productversion = 'undefined'
        subproductcode = 'ndvi_native'
        mapsetcode = 'WGS84_Africa_1km'
        
        product = {"productcode": productcode,
                   "version": productversion}
        args = {"productcode": productcode,
                "subproductcode": subproductcode,
                "datasource_descr_id": '',
                "version": productversion}
        
        product_in_info = querydb.get_product_in_info(echo=echo_query, **args)

        re_process = product_in_info.re_process
        re_extract = product_in_info.re_extract

        sprod = {'subproduct': ingest.subproductcode,
                             'mapsetcode': ingest.mapsetcode,
                             're_extract': re_extract,
                             're_process': re_process}

        subproducts.append(sprod)
        
        ingestion(date_fileslist, in_date, product, subproducts, datasource_descr, echo_query=echo_query)

        self.assertEqual(1, 1)

