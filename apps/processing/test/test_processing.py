__author__ = "Marco Clerici"


import time

# General definitions/switches
starting_sprod='rfe'
prod="fewsnet_rfe"
mapset='FEWSNET_Africa_8km'
version='undefined'

# General definitions/switches
args = {'pipeline_run_level':0, \
        'pipeline_run_touch_only':0, \
        'pipeline_printout_level':0, \
        'pipeline_printout_graph_level':0}

from apps.processing.processing_std_precip import *

start = time.clock()

#list_prods = processing_std_precip(**args)
list_sprods = get_subprods_std_precip()

#   ---------------------------------------------------------------------
#   Run the pipeline

#processing_fewsnet_rfe(**args)
# processing_vgt_ndvi(**args)