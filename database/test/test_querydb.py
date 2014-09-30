# -*- coding: utf-8 -*-
__author__ = "Jurriaan van 't Klooster"

from __future__ import absolute_import
from unittest import TestCase
from lib.python import es_logging as log
logger = log.my_logger(__name__)

from database import querydb


class TestQuerydb(TestCase):

    def Test_get_active_internet_sources(self):

        internet_sources = querydb.get_active_internet_sources()
        logger.info("Internet sources are: %s", internet_sources)
        for internet_source in internet_sources:
            print internet_source.url

        self.assertEqual(1, 1)

    def Test_get_eumetcast_sources(self):

        eumetcast_sources = querydb.get_eumetcast_sources()
        logger.info("Eumetcast sources are: %s", eumetcast_sources)
        for row in eumetcast_sources:
            print row

        self.assertEqual(1, 1)

    def Test_get_datasource_descr(self):

        datasource_descr = querydb.get_datasource_descr(source_type='EUMETCAST',
                                                        source_id='EO:EUM:DAT:SPOT:S10NDVI')
        logger.info("Eumetcast source description is: %s", datasource_descr)
        for row in datasource_descr:
            print row

        datasource_descr = querydb.get_datasource_descr(source_type='INTERNET',
                                                        source_id='USGS:EARLWRN:FEWSNET')
        logger.info("Internet source description is: %s", datasource_descr)
        for row in datasource_descr:
            print row

        self.assertEqual(1, 1)

    def Test_get_product_sources(self):

        product_sources = querydb.get_product_sources(productcode='fewsnet_rfe',
                                                      subproductcode='fewsnet_rfe_native',
                                                      version='undefined')
        logger.info("Product sources are: %s", product_sources)
        for row in product_sources:
            print row

        self.assertEqual(1, 1)

    def Test_get_ingestion_subproduct(self):

        ingestion_subproduct = querydb.get_ingestion_subproduct(productcode='vgt_ndvi',
                                                                version='undefined')
        logger.info("All ingestions of product are: %s", ingestion_subproduct)
        for row in ingestion_subproduct:
            print row

        self.assertEqual(1, 1)

    def Test_get_ingestion_product(self):

        ingestion_product = querydb.get_ingestion_product(productcode='vgt_ndvi',
                                                          version='undefined')
        logger.info("Active ingestions of product are: %s", ingestion_product)
        for row in ingestion_product:
            print row

        self.assertEqual(1, 1)

    def Test_get_mapset(self):

        mapset = querydb.get_mapset(mapsetcode='WGS84_Africa_1km')
        logger.info("Mapset: %s", mapset)
        for row in mapset:
            print row

        self.assertEqual(1, 1)

    def Test_get_internet(self):

        internet = querydb.get_internet(internet_id='USGS:EARLWRN:FEWSNET')
        logger.info("Internet source info: %s", internet)
        for row in internet:
            print row

        self.assertEqual(1, 1)

    def Test_get_eumetcast(self):

        eumetcast = querydb.get_eumetcast(source_id='EO:EUM:DAT:SPOT:S10NDVI')
        logger.info("Eumetcast source info: %s", eumetcast)
        for row in eumetcast:
            print row

        self.assertEqual(1, 1)

    def Test_get_product_native(self):

        product = querydb.get_product_native(productcode='fewsnet_rfe')
        logger.info("Native product info: %s", product)
        for row in product:
            print row

        self.assertEqual(1, 1)

    def Test_get_product_in_info(self):

        product_in = querydb.get_product_in_info(productcode='fewsnet_rfe',
                                                 subproductcode='rfe',
                                                 version='undefined',
                                                 datasource_descr_id='USGS:EARLWRN:FEWSNET')
        logger.info("Product IN info: %s", product_in)
        for row in product_in:
            print row

        self.assertEqual(1, 1)

    def Test_get_product_out_info(self):

        product_out = querydb.get_product_out_info(productcode='fewsnet_rfe',
                                                   subproductcode='rfe',
                                                   version='undefined')
        logger.info("Product OUT info: %s", product_out)
        for row in product_out:
            print row

        self.assertEqual(1, 1)

    def Test_get_products(self):

        product = querydb.get_products(activated=True)
        logger.info("Active products: %s", product)
        for row in product:
            print row

        product = querydb.get_products(activated=False)
        logger.info("Non active products: %s", product)
        for row in product:
            print row

        self.assertEqual(1, 1)

    def Test_get_dataacquisitions(self):

        dataacquisitions = querydb.get_dataacquisitions()
        logger.info("All Data Acquisitions: %s", dataacquisitions)
        for row in dataacquisitions:
            print row

        self.assertEqual(1, 1)

    def Test_get_ingestions(self):

        ingestions = querydb.get_ingestions()
        logger.info("All Ingestions: %s", ingestions)
        for row in ingestions:
            print row

        self.assertEqual(1, 1)


