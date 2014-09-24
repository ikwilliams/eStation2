# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest

__author__ = "Jurriaan van 't Klooster"

from database import crud

crud_db = crud.CrudDB()
schema = ("%s." % crud_db.schema) if crud_db.schema else ""


class TestCrud(unittest.TestCase):
    def test_crud(self):
        records = len(crud_db.read(schema + 'date_format'))
        self.assertTrue(records > 0)
        
        record = {'date_format': 'TESTING123', 'definition': 'We are testing crud!'}
        crud_db.create(schema + 'date_format', record)
        
        self.assertEquals(len(crud_db.read(schema + 'date_format', date_format='TESTING123')), 1)
        
        record = {'date_format': 'TESTING123', 'definition': 'Updating this record!'}
        crud_db.update(schema + 'date_format', record)
        
        self.assertEquals(len(crud_db.read(schema + 'date_format')), records + 1)

        crud_db.delete(schema + 'date_format', date_format='TESTING123')

        self.assertEquals(len(crud_db.read(schema + 'date_format')), records)
