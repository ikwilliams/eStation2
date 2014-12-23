_author__ = "Marco Clerici"
#
#	purpose: Define the processing service
#	author:  M.Clerici & Jurriaan van't Klooster
#	date:	 17.12.2014
#   descr:	 Process files into the specified 'mapset'
#	history: 1.0
#

# source eStation2 base definitions
import locals, os, sys
import shutil

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

from apps.processing import processing_std_precip
from lib.python.daemon import DaemonDryRunnable

def loop_processing(dry_run=False):

#    Driver of the process service
#    Reads configuration from the database
#    Creates the pipelines for the active processing
#    Calls the active pipelines with the relevant argument
#    Arguments: dry_run -> if > 0, it triggers pipeline_printout() rather than pipeline_run()
#                       -> if < 0, it triggers pipeline_printout_graph() rather than pipeline_run()

    # Clean dir with locks
    shutil.rmtree(es_constants.processing_tasks_dir)
    logger.info("Entering routine %s" % 'loop_processing')
    echo_query = False
    functions.check_output_dir(es_constants.processing_tasks_dir)
    while True :

        logger.debug("Entering infinite loop")
        # Get all active processing chains from the database.
        processing_chains = querydb.get_processing_chains(allrecs=True)
        for chain in processing_chains:

            product_code = chain.product_code
            sub_product_code = chain.subproduct_code
            mapset = chain.output_mapsetcode
            algorithm

            # The following id comes either from the DB id, or a combination of fields
            processing_unique_id=functions.set_path_filename_no_date(product_code, sub_product_code, mapset, '.lock')
            processing_unique_lock=es_constants.processing_tasks_dir+processing_unique_id


            args = {'pipeline_run_level':1, \
                    'starting_sprod': product_code, \
                    'prod':sub_product_code, \
                    'mapset':mapset,\
                    'version':'undefined'}

            if not os.path.isfile(processing_unique_lock):
                logger.debug("Launching processing for ID: %s" % processing_unique_id)
                open(processing_unique_lock,'a').close()
                # fork and call the std_precip 'generic' processing
                pid = os.fork()
                if pid == 0:
                    # Call to the processing pipeline
                    [l1,l2] = processing_std_precip.processing_std_precip()
                    print l1
                    print l2
                    #processing_std_precip.processing_std_precip(**args)
                    # Simulate longer processing (TEMP)
                    time.sleep(1)
                    os.remove(processing_unique_lock)
                    sys.exit(0)
                else:
                    # Qui sono il padre
                    pass
                    #os.wait()
            else:
                logger.debug("Processing already running for ID: %s " % processing_unique_id)

        time.sleep(1)

class ProcessingDaemon(DaemonDryRunnable):
    def run(self):
        loop_processing(dry_run=self.dry_run)

