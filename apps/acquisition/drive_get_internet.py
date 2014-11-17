_author__ = "Marco Clerici"

import locals
import os, time
from config import es_constants
from apps.acquisition import get_internet
from apps.acquisition import acquisition
from lib.python import es_logging as log
logger = log.my_logger(__name__)


#get_internet.drive_get_internet()

# Manual Switch for START/STOP
do_start = False
dry_run  = True

pid_file = es_constants.get_internet_pid_filename
daemon = acquisition.GetInternetDaemon(pid_file, dry_run=dry_run)


if do_start:
    if daemon.status():
        logger.info('GetInternet process is running: Exit')
    else:
        logger.info('GetInternet process is NOT running: Start it.')
        daemon.start()
else:
    if not daemon.status():
        logger.info('GetInternet process is NOT running: Exit')
    else:
        logger.info('GetInternet process is running: Stop it.')
        daemon.stop()


