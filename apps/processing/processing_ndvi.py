#
#	purpose: Define the processing chain for ndvi
#	author:  M.Clerici & Jurriaan van't Klooster
#	date:	 25.06.2014
#   descr:	 Generate additional derived products / implements processing chains
#	history: 1.0
#

# source my definitions
# import locals
#

# import standard modules
# import glob
# import os

# Import eStation2 modules
from lib.python import es_logging as log
from config.es_constants import *
import database.querydb as querydb
from lib.python.mapset import *
from lib.python.functions import *
from lib.python.metadata import *
from lib.python.image_proc import raster_image_math
from lib.python.image_proc.recode import *
import database.crud as crud
#from apps.processing.processing import *

# Import third-party modules

from ruffus import *

logger = log.my_logger(__name__)

input_dir = locals.es2globals['test_data_in']+'/VGT_NDVI/tif/NDV/'   # ????????


#   Still to be done

#   General definitions for this processing chain
prod="VGT_NDVI"
mapset='WGS84_Africa_1km'
ext='.tif'

#   general switch
activate_vgt_ndvi_comput=0

#   switch wrt to group
activate_nvi_no_filter_stats=1
activate_nvi_no_filter_anomalies=1

activate_filtered_prods=1
activate_filtered_stats=1
activate_filtered_anomalies=1

activate_monthly_prods=1

#   specific switch for each subproduct or small group
# activate_ndv_comput=1
# activate_10dmin_comput=1
# activate_10dmax_comput=1
# activate_10ddiff_comput=1
# activate_10dperc_comput=1
# activate_10dnp_comput=1
#
# activate_1moncum_comput=1
# activate_1monavg_comput=1
# activate_1monmin_comput=1
# activate_1monmax_comput=1
# activate_1mondiff_comput=1
# activate_1monperc_comput=1
# activate_1monnp_comput=1

#   ---------------------------------------------------------------------
#   Define input files
starting_sprod='NDV'
in_prod_ident='_'+prod+'_'+starting_sprod+'_'+mapset+ext
starting_files = input_dir+"*"+in_prod_ident


#   ---------------------------------------------------------------------
#   NDV avg x dekad (i.e. avg_dekad)
output_sprod="10davg"
#   ---------------------------------------------------------------------
#   NDV min x dekad (i.e. min_dekad)
output_sprod="10dmin"
#   ---------------------------------------------------------------------
#   NDV max x dekad (i.e. max_dekad)
output_sprod="10dmax"
#   ---------------------------------------------------------------------
#   NDV std x dekad (i.e. std_dekad)
output_sprod="10dstd"
#   ---------------------------------------------------------------------
#   NDV med x dekad (i.e. med_dekad)
output_sprod="10dmed"

#   ---------------------------------------------------------------------
#   NDV stats per year -> TBDone
#   ---------------------------------------------------------------------
#   NDV stats per absolute -> TBDone


#   ---------------------------------------------------------------------
#   NDV linearx1/x2
#   Note: here the difficulty is to manage the +1/-1 dekad across the year

output_sprod="ndvi_linearx1"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

def generate_parameters_on_the_fly():

        parameters = [
                        ['20130511_VGT_NDVI_NDV_WGS84_Africa_1km.tif','20130521_VGT_NDVI_NDV_WGS84_Africa_1km.tif','20130601_VGT_NDVI_NDV_WGS84_Africa_1km.tif'],
                        ['20130521_VGT_NDVI_NDV_WGS84_Africa_1km.tif','20130601_VGT_NDVI_NDV_WGS84_Africa_1km.tif','20130611_VGT_NDVI_NDV_WGS84_Africa_1km.tif'],
                        ['20130601_VGT_NDVI_NDV_WGS84_Africa_1km.tif','20130611_VGT_NDVI_NDV_WGS84_Africa_1km.tif','20130621_VGT_NDVI_NDV_WGS84_Africa_1km.tif']
        ]
        for job_pars in parameters:
                yield [input_dir+job_pars[0],input_dir+job_pars[1],input_dir+job_pars[2]]


#   Starting files + avg
#formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident
#formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}-1{MMDD[0]}"+out_prod_ident

# ancillary_sprod = "10davg"
# ancillary_subdir = "derived"+os.path.sep+ancillary_sprod+os.path.sep
# ancillary_sprod_ident = '_'+prod+'_'+ancillary_sprod+'_'+mapset+ext
# ancillary_input="{subpath[0][2]}"+os.path.sep+ancillary_subdir+"{MMDD[0]}"+ancillary_sprod_ident

#@transform(starting_files, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
#@transform(starting_files, formatter(formatter_in), formatter_out)
@active_if(activate_vgt_ndvi_comput)
@files(generate_parameters_on_the_fly)
def ndvi_linearx1(input_file, input_file1, input_file2):

    print "input_file: ", input_file
    print "input_file1:", input_file1
    print "input_file2:", input_file2








#   ---------------------------------------------------------------------
#   Run the pipeline

def processing_ndvi():

    logger.info("Entering routine %s" % 'processing_ndvi')
    #pipeline_printout(verbose=3)
    #sleep 1
    pipeline_run(verbose=2)
    #pipeline_run(multiprocess=6)
    #pipeline_printout()
    #pipeline_printout_graph('flowchart.jpg')