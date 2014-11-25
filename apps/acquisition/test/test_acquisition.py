
import unittest
import os, time
from config import es_constants
from apps.acquisition import acquisition
from lib.python import es_logging as log
logger = log.my_logger(__name__)


class TestDaemon(unittest.TestCase):

    #   ---------------------------------------------------------------------------
    #   Test IngestDaemon()
    #   TODO-M.C.: does the exit(0) in daemon code make the test fail ?
    #   TODO-M.C.: add a status() method to daemon ?
    #   ---------------------------------------------------------------------------
    def TestIngestDaemon(self):

        pid_file = es_constants.ingest_pid_filename
        daemon = acquisition.IngestDaemon(pid_file, dry_run=True)

        # If the daemon is running, stop it and check file does not exist
        if os.path.isfile(pid_file):
            logger.info('Ingest pid file exist: stop daemon')
            try:
                daemon.stop()
                self.assertEqual(daemon.status(), 0)
            except:
                pass
            self.assertEqual(os.path.isfile(pid_file), 0)
        else:
            logger.info('Ingest pid file does NOT exist: start daemon')
            try:
                daemon.start()
                self.assertEqual(daemon.status(), 1)
            except:
                pass
            time.sleep(1)
            self.assertEqual(os.path.isfile(pid_file), 1)

    def TestGetInternetDaemon(self):

        logger.info('Test GetInternet daemon')

        pid_file = es_constants.get_internet_pid_filename
        daemon = acquisition.GetInternetDaemon(pid_file, dry_run=True)

        # If the daemon is running, stop it and check file does not exist
        if os.path.isfile(pid_file):
            logger.info('GetInternet pid file exist: stop daemon')
            try:
                daemon.stop()
            except:
                pass
            self.assertEqual(os.path.isfile(pid_file), 0)
        else:
            logger.info('GetInternet pid file des NOT exist: start daemon')
            try:
                daemon.start()
            except:
                pass
            time.sleep(1)
            self.assertEqual(os.path.isfile(pid_file), 1)

    def TestGetEumetcastDaemon(self):

        logger.info('Test GetEumetcast daemon')

        pid_file = es_constants.get_eumetcast_pid_filename
        daemon = acquisition.GetEumetcastDaemon(pid_file, dry_run=True)

        # If the daemon is running, stop it and check file does not exist
        if os.path.isfile(pid_file):
            logger.info('GetEumetcast pid file exist: stop daemon')
            try:
                daemon.stop()
            except:
                pass
            self.assertEqual(os.path.isfile(pid_file), 0)
        else:
            logger.info('GetEumetcast pid file des NOT exist: start daemon')
            try:
                daemon.start()
            except:
                pass
            time.sleep(1)
            self.assertEqual(os.path.isfile(pid_file), 1)
