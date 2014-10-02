__author__ = "Marco Clerici"


import time
from apps.processing.processing_switches import *

#from apps.processing.processing_fewsnet import *
#from apps.processing.processing_ndvi import *

from apps.processing.processing_generic import *
start = time.clock()

#   ---------------------------------------------------------------------
#   Run the pipeline

# General definitions/switches
starting_sprod='rfe'
prod="fewsnet_rfe"
mapset='FEWSNET_Africa_8km'
version='undefined'

args = {'pipeline_run_level':pipeline_run_level, \
        'pipeline_run_touch_only':pipeline_run_touch_only, \
        'pipeline_printout_level':pipeline_printout_level, \
        'pipeline_printout_graph_level':pipeline_printout_graph_level, \
        'starting_sprod': starting_sprod, \
        'prod':prod, \
        'mapset':mapset,\
        'version':version}


# do second fork
import os, sys
pid = os.fork()
if pid == 0:
    # Qui sono il figlio
    processing_generic(**args)
    sys.exit(0)
else:
    # Qui sono il padre
    os.wait()

pid = os.fork()
if pid == 0:
    args['mapset']='WGS84_Africa_1km'
    processing_generic(**args)
    sys.exit(0)

#processing_vgt_ndvi(**args)