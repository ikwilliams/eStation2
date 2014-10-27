_author__ = "Marco Clerici"


import locals
from apps.acquisition import ingestion

import unittest

# Overwrite Dirs
locals.es2globals['ingest_dir']=locals.es2globals['test_data_in_dir']
locals.es2globals['data_dir']=locals.es2globals['test_data_out']

class TestIngestion(unittest.TestCase):

    def TestDriveAll(self):
        ingestion.drive_ingestion()
        self.assertEqual(1, 1)


    def test_ingest_vgt_ndvi(self):
        self.assertEqual(1, 1)

