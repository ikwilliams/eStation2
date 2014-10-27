_author__ = "Jurriaan van 't Klooster"

import locals
from apps.acquisition import ingestion

import time

start = time.clock()
locals.es2globals['ingest_dir']=locals.es2globals['test_data_in_dir']

print locals.es2globals['data_dir']
ingestion.drive_ingestion()

elapsed = time.clock()-start
print elapsed


