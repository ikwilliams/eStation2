_author__ = "Marco Clerici"

import locals
import os, time
from config import es_constants
from apps.acquisition import get_eumetcast
from apps.acquisition import acquisition
from lib.python import es_logging as log
logger = log.my_logger(__name__)

# Manual Switch for START/STOP
do_start = False
dry_run = True

pid_file = es_constants.get_eumetcast_pid_filename
daemon = acquisition.GetEumetcastDaemon(pid_file, dry_run=dry_run)


if do_start:
    if daemon.status():
        logger.info('GetEumetcast process is running: Exit')
    else:
        logger.info('GetEumetcast process is NOT running: Start it.')
        daemon.start()
else:
    if not daemon.status():
        logger.info('GetEumetcast process is NOT running: Exit')
    else:
        logger.info('GetEumetcast process is running: Stop it.')
        daemon.stop()



