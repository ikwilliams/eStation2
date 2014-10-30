_author__ = "Marco Clerici"

#
#   Main module in acquisition, driving the services
#

from apps.acquisition import get_eumetcast
from apps.acquisition import get_internet
from apps.acquisition import ingestion
from lib.python.daemon import Daemon

class IngestDaemon(Daemon):
    def run(self):
        ingestion.drive_ingestion(dry_run=True)

class GetEumetcastDaemon(Daemon):
    def run(self):
        get_eumetcast.drive_eumetcast(dry_run=True)

class GetInternetDaemon(Daemon):
    def run(self):
        get_internet.drive_get_internet(dry_run=True)
