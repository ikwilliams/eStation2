_author__ = "Marco Clerici"

#
#   Main module in acquisition, driving the services
#

from apps.acquisition import get_eumetcast
from apps.acquisition import get_internet
from apps.acquisition import ingestion
from lib.python.daemon import Daemon


class DaemonDryRunnable(Daemon):
    def __init__(self, *args, **kwargs):
        self.dry_run = kwargs.pop('dry_run', True)
        Daemon.__init__(self, *args, **kwargs)


class IngestDaemon(DaemonDryRunnable):
    def run(self):
        ingestion.drive_ingestion(dry_run=self.dry_run)


class GetEumetcastDaemon(DaemonDryRunnable):
    def run(self):
        get_eumetcast.drive_eumetcast(dry_run=self.dry_run)


class GetInternetDaemon(DaemonDryRunnable):
    def run(self):
        get_internet.drive_get_internet(dry_run=self.dry_run)
