# -*- coding: utf-8 -*-
from __future__ import absolute_import
__author__ = "Jurriaan van 't Klooster"

import unittest
from config import es_constants
from database import crud

crud_db = crud.CrudDB(schema=es_constants.dbglobals['schema_products'])


class TestCrud(unittest.TestCase):

    def test_crud(self):
        #schema='products.'
        schema = ''
        records = len(crud_db.read('date_format'))
        self.assertTrue(records > 0)

        record = {'date_format': 'TESTING123', 'definition': 'We are testing crud!'}
        crud_db.create('date_format', record)

        self.assertEquals(len(crud_db.read('date_format', date_format='TESTING123')), 1)

        record = {'date_format': 'TESTING123', 'definition': 'Updating this record!'}
        crud_db.update('date_format', record)

        self.assertEquals(len(crud_db.read('date_format')), records + 1)

        crud_db.delete('date_format', date_format='TESTING123')

        self.assertEquals(len(crud_db.read('date_format')), records)

        productinfo = {'productcode': 'vgt_fapar', 'activated': False, 'version': 'V1.3', 'product_type': 'Native', 'subproductcode': 'vgt_fapar_native'}
        crud_db.update('product', productinfo)
        self.assertEquals(len(crud_db.read(schema + 'product')), records)



