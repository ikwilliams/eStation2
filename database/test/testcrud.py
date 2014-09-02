# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest

__author__ = "Jurriaan van 't Klooster"

import database.crud as crudDB

crud = crudDB.CrudDB()
schema = ("%s." % crud.schema) if crud.schema else ""


class TestCrud(unittest.TestCase):
    def test_crud(self):
        records = len(crud.read(schema + 'date_format'))
        self.assertTrue(records > 0)
        
        record = {'date_format': 'TESTING123', 'definition': 'We are testing crud!'}
        crud.create(schema + 'date_format', record)
        
        self.assertEquals(len(crud.read(schema + 'date_format', date_format='TESTING123')), 1)
        
        record = {'date_format': 'TESTING123', 'definition': 'Updating this record!'}
        crud.update(schema + 'date_format', record)
        
        self.assertEquals(len(crud.read(schema + 'date_format')), records + 1)

        crud.delete(schema + 'date_format', date_format='TESTING123')

        self.assertEquals(len(crud.read(schema + 'date_format')), records)
