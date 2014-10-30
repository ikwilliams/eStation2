# -*- coding: utf-8 -*-

#
#	purpose: Test products functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 27.10.2014
#

from __future__ import absolute_import

import unittest
import os
import datetime
import sys
from ..helpers import INTERVAL_TYPE
from ..products import Product
from ..datasets import Dataset
from ..exceptions import (WrongDateType, NoProductFound)

import locals
from lib.python import functions
from database import querydb
import json

class TestProducts(unittest.TestCase):
    def setUp(self):
        self.kwargs = {'product_code':"fewsnet_rfe"}
        self.mapsets = ('FEWSNET_Africa_8km', 'WGS84_Africa_1km')
        self.subproducts = ('10DAVG', 'rfe')
        self.files_mapsets = [os.path.join(locals.es2globals['data_dir'],
            self.kwargs['product_code'], mapset) for mapset in self.mapsets]
        self.files_subproducts = [os.path.join(file_mapset, subproduct_type, subproduct)
                for file_mapset in self.files_mapsets
                for subproduct_type in functions.dict_subprod_type_2_dir.values()
                for subproduct in self.subproducts]

    def test_class(self):
        self.assertIsInstance(Product(**self.kwargs), Product)

    def test_class_no_product(self):
        kwargs = {'product_code':"---prod---"}
        self.assertRaisesRegexp(NoProductFound, "(?i).*found.*product.*", Product, **kwargs)

    def test_class_mapsets(self):
        product = Product(**self.kwargs)
        product._get_full_mapsets = lambda: self.files_mapsets
        self.assertEqual(len(product.mapsets), len(self.mapsets))
        self.assertEqual(set(product.mapsets), set(self.mapsets))

    def test_class_subproduct(self):
        product = Product(**self.kwargs)
        product._get_full_subproducts = lambda: self.files_subproducts
        self.assertEqual(len(product.subproducts), len(self.subproducts))
        self.assertEqual(set(product.subproducts), set(self.subproducts))

    def test_class_get_subproduct(self):
        product = Product(**self.kwargs)
        product._get_full_mapsets = lambda: self.files_mapsets
        product._get_full_subproducts = lambda mapset: self.files_subproducts
        subproducts = product.get_subproducts(mapset=product.mapsets[0])
        self.assertEqual(len(subproducts), len(self.subproducts))
        self.assertEqual(set(subproducts), set(self.subproducts))

    def test_class_dataset(self):
        product = Product(**self.kwargs)
        product._get_full_subproducts = lambda: self.files_subproducts
        self.assertIsInstance(product.get_dataset(sub_product_code=product.subproducts[-1], mapset=self.mapsets[0]),
            Dataset)
