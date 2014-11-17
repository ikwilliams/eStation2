_author__ = "Jurriaan van 't Klooster"

import locals
import os, time
from config import es_constants
from apps.acquisition import ingestion
from apps.acquisition import acquisition
from lib.python import es_logging as log
logger = log.my_logger(__name__)

# Manual Switch for START/STOP
do_start = False
dry_run  = True

pid_file = es_constants.ingest_pid_filename
daemon = acquisition.IngestDaemon(pid_file, dry_run=dry_run)

# locals.es2globals['ingest_dir']=locals.es2globals['test_data_in_dir']


if do_start:
    if daemon.status():
        logger.info('Ingest process is running: Exit')
    else:
        logger.info('Ingest process is NOT running: Start it.')
        daemon.start()
else:
    if not daemon.status():
        logger.info('Ingest process is NOT running: Exit')
    else:
        logger.info('Ingest process is running: Stop it.')
        daemon.stop()



