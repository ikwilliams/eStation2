_author__ = "Marco Clerici"
#
#	purpose: Define the processing service
#	author:  M.Clerici & Jurriaan van't Klooster
#	date:	 17.12.2014
#   descr:	 Process files into the specified 'mapset'
#	history: 1.0
#

# source eStation2 base definitions
import locals

# import standard modules
import time

# import eStation2 modules
from database import querydb
from lib.python import functions
from lib.python import es_logging as log
from config import es_constants

logger = log.my_logger(__name__)
data_dir= locals.es2globals['data_dir']

#   Main module in processing, driving a specific pipeline

from apps.processing import processing_fewsnet
from apps.processing import processing_ndvi
from lib.python.daemon import DaemonDryRunnable

def loop_processing(dry_run=False):

#    Driver of the process service
#    Reads configuration from the database
#    Creates the pipelines for the active processing
#    Calls the active pipelines with the relevant argument
#    Arguments: dry_run -> if > 0, it triggers pipeline_printout() rather than pipeline_run()
#                       -> if < 0, it triggers pipeline_printout_graph() rather than pipeline_run()


    logger.info("Entering routine %s" % 'loop_processing')
    echo_query = False

    while True:

        # Get all active processing chains from the database.
        active_processing_chains = querydb.get_processing_chains(allrecs=True, echo=echo_query)

        for active_chain in active_processing_chains:

            logger.info("Processing active for product: [%s] subproduct N. %s" % (active_processing_chain[0],
                                                                                  active_processing_chain[2]))
            productcode = active_product_ingest[0]
            productversion = active_product_ingest[1]



class ProcessingDaemon(DaemonDryRunnable):
    def run(self):
        loop_processing(dry_run=self.dry_run)

