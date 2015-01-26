__author__ = "Marco Clerici"


import time

# General definitions/switches
args = {'pipeline_run_level':1, \
        'pipeline_run_touch_only':0, \
        'pipeline_printout_level':0, \
        'pipeline_printout_graph_level':0}

from apps.processing.processing_ndvi import *
from apps.processing.processing_fewsnet import *

start = time.clock()

#   ---------------------------------------------------------------------
#   Run the pipeline

#processing_fewsnet_rfe(**args)
processing_ndvi(**args)