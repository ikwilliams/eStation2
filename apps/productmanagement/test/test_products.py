# -*- coding: utf-8 -*-

#
#	purpose: Test products functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 27.10.2014
#

from __future__ import absolute_import

import unittest
import os
from ..products import Product
from ..datasets import Dataset
from ..exceptions import (NoProductFound, MissingMapset)

import locals
from lib.python import functions
from database import querydb


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.kwargs = {'product_code':"vgt_ndvi"}
        self.mapsets = ('WGS84_Africa_1km', 'WGS84_Sahel_1km')
        self.subproducts = ('sm', 'ndv')
        self.files_mapsets = [os.path.join(locals.es2globals['data_dir'],
                              self.kwargs['product_code'], mapset) for mapset in self.mapsets]
        self.files_subproducts = [os.path.join(file_mapset, subproduct_type, subproduct)
                for file_mapset in self.files_mapsets
                for subproduct_type in functions.dict_subprod_type_2_dir.values()
                for subproduct in self.subproducts]

    def get_product(self):
        product = Product(**self.kwargs)
        product._get_full_mapsets = lambda: self.files_mapsets
        product._get_full_subproducts = lambda mapset='*': self.files_subproducts
        return product

    def test_class(self):
        self.assertIsInstance(Product(**self.kwargs), Product)

    def test_class_no_product(self):
        kwargs = {'product_code':"---prod---"}
        self.assertRaisesRegexp(NoProductFound, "(?i).*found.*product.*", Product, **kwargs)

    def test_class_mapsets(self):
        product = self.get_product()
        self.assertEqual(len(product.mapsets), len(self.mapsets))
        self.assertEqual(set(product.mapsets), set(self.mapsets))

    def test_class_subproduct(self):
        product = self.get_product()
        self.assertEqual(len(product.subproducts), len(self.subproducts))
        self.assertEqual(set(product.subproducts), set(self.subproducts))

    def test_class_get_subproduct(self):
        product = self.get_product()
        subproducts = product.get_subproducts(mapset=product.mapsets[0])
        self.assertEqual(len(subproducts), len(self.subproducts))
        self.assertEqual(set(subproducts), set(self.subproducts))

    def test_class_dataset(self):
        product = self.get_product()
        self.assertIsInstance(product.get_dataset(sub_product_code=product.subproducts[-1],
                                                  mapset=self.mapsets[0]), Dataset)

    def test_all_products_to_json(self):
        def row2dict(row):
            d = {}
            for column_name in row.c.keys():  # all_cols:
                d[column_name] = str(getattr(row, column_name))
            return d

        # get full distinct list of products (native only)
        db_products = querydb.get_product_native(allrecs=True, echo=False)
        self.assertTrue(db_products.__len__() > 0)
        products_dict_all = []
        # loop the products list
        for product in db_products:
            prod_dict = row2dict(product)
            productcode = prod_dict['productcode']
            version = prod_dict['version']
            p = Product(product_code=prod_dict['productcode'], version=version)

            # does the product have mapsets AND subproducts?
            all_prod_mapsets = p.mapsets
            all_prod_subproducts = p.subproducts
            if all_prod_mapsets.__len__() > 0 and all_prod_subproducts.__len__() > 0:
                prod_dict['productmapsets'] = []
                for mapset in all_prod_mapsets:
                    mapset_info = querydb.get_mapset(mapsetcode=mapset, allrecs=False, echo=False)
                    mapset_dict = row2dict(mapset_info)
                    mapset_dict['mapsetdatasets'] = []
                    all_mapset_datasets = p.get_subproducts(mapset=mapset)
                    for subproductcode in all_mapset_datasets:
                        dataset_info = querydb.get_subproduct(productcode=productcode,
                                                              version=version,
                                                              subproductcode=subproductcode,
                                                              echo=False)
                        dataset_dict = row2dict(dataset_info)
                        dataset = p.get_dataset(mapset=mapset, sub_product_code=subproductcode)
                        completeness = dataset.get_dataset_normalized_info()
                        dataset_dict['datasetcompleteness'] = completeness

                        mapset_dict['mapsetdatasets'].append(dataset_dict)
                    prod_dict['productmapsets'].append(mapset_dict)
                products_dict_all.append(prod_dict)
        self.assertEquals(len(db_products), 31)

    def test_get_missing(self):
        product = self.get_product()
        mapsets = product.mapsets
        subproducts = product.subproducts
        self.assertEqual(len(product.get_missing_datasets(mapset=mapsets[0], sub_product_code=subproducts[0])), 1)
        self.assertEqual(len(product.get_missing_datasets(mapset=mapsets[0])), 2)
        self.assertEqual(len(product.get_missing_datasets()), 4)
        self.assertRaisesRegexp(MissingMapset, "(?i).*mapset.*%s*" % subproducts[0], product.get_missing_datasets,
                **{'sub_product_code': subproducts[0]})
