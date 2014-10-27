
import unittest
import os
from apps.acquisition import acquisition

#
class TestDaemon(unittest.TestCase):

    #   ---------------------------------------------------------------------------
    #   Test get_eumetcast_info()
    #   ---------------------------------------------------------------------------
    def TestIngestDaemon(self):

        daemon = acquisition.IngestDaemon('/tmp/ingest-daemon.pid')
        daemon.start()
        self.assertEqual(os.path.isfile('/tmp/ingest-daemon.pid'), 1)
