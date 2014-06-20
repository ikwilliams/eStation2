#
#	purpose: Define the processing service (by using ruffus)
#	author:  M.Clerici & Jurriaan van't Klooster
#	date:	 11.06.2014
#   descr:	 Generate additional derived products / implements processing chains
#	history: 1.0
#

# source my definitions
import locals

import glob
import os

# Import eStation lib modules
from lib.python import es_logging as log
from config.es_constants import *
import database.querydb as querydb
from lib.python.mapset import *
from lib.python.functions import *
from lib.python.metadata import *
from lib.python.image_proc import raster_image_math
from lib.python.image_proc.recode import *


# Import third-party modules
from osgeo.gdalconst import *
from osgeo import gdal
from osgeo import osr
import pygrib
import numpy as N
from ruffus import *

logger = log.my_logger(__name__)

input_dir = locals.es2globals['test_data_in']
interm_dir = locals.es2globals['test_data_inter']

#   Still to be done
#   TODO-M.C.: upsert to DB
#   TODO-M.C.: functions to avoid repetitions
#   TODO-M.C.: more checks on the IN/OUT
#   TODO-M.C.: NODATA management ?? not for RFE ??
#   TODO-M.C.: Check and create output dir
#   TODO-M.C.: Activate/deactivate according to DB settings
#   TODO-M.C.: Add a mechanism to extract/visualize the 'status' -> printout+grep ??
#   TODO-M.C.: Add metadata to the output
#   TODO-M.C.: create unittest-like functions for validating the chain
#   TODO-M.C.: multiprocessing ?!?!


#   General definitions for this processing chain
prod="FEWSNET_RFE"
mapset='FEWSNET_Africa_8km'
ext='.tif'

#   ---------------------------------------------------------------------
#   Define input files
starting_sprod='RFE'
in_prod_ident='_'+prod+'_'+starting_sprod+'_'+mapset+ext
starting_files = input_dir+"*"+in_prod_ident

#   ---------------------------------------------------------------------
#   Average
output_sprod="10davg"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10davg(input_file, output_file):

    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_avg_image(**args)

#   ---------------------------------------------------------------------
#   Minimum
output_sprod="10dmin"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10dmin(input_file, output_file):

    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_min_image(**args)

#   ---------------------------------------------------------------------
#   Maximum
output_sprod="10dmax"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

# Take all RFE of the same dekad, along yearly timeseries ...
formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
# ... and merge into a single file
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10dmax(input_file, output_file):

    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_max_image(**args)

#   ---------------------------------------------------------------------
#   10dDiff
output_sprod="10ddiff"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

#   Starting files + avg
formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}{MMDD[0]}"+out_prod_ident
ancillary_sprod = "10davg"

ancillary_subdir = "derived"+os.path.sep+ancillary_sprod+os.path.sep
ancillary_sprod_ident = '_'+prod+'_'+ancillary_sprod+'_'+mapset+ext
ancillary_input="{subpath[0][2]}"+os.path.sep+ancillary_subdir+"{MMDD[0]}"+ancillary_sprod_ident

@follows(fewsnet_10davg)
@transform(starting_files, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_10ddiff(input_file, output_file):

    args = {"input_file": input_file, "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_oper_subtraction(**args)

#   ---------------------------------------------------------------------
#   10dperc
output_sprod="10dperc"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

#   Starting files + avg
formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}{MMDD[0]}"+out_prod_ident
ancillary_sprod = "10davg"

ancillary_subdir = "derived"+os.path.sep+ancillary_sprod+os.path.sep
ancillary_sprod_ident = '_'+prod+'_'+ancillary_sprod+'_'+mapset+ext
ancillary_input="{subpath[0][2]}"+os.path.sep+ancillary_subdir+"{MMDD[0]}"+ancillary_sprod_ident

@follows(fewsnet_10davg)
@transform(starting_files, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_10dperc(input_file, output_file):

    args = {"input_file": input_file[0], "avg_file": input_file[1], "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_compute_perc_diff_vs_avg(**args)

#   ---------------------------------------------------------------------
#   1moncum
output_sprod="1moncum"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

# inputs: files from same months
formatter_in="(?P<YYYYMM>[0-9]{6})(?P<DD>[0-9]{2})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYYMM[0]}"+'01'+out_prod_ident

# @follows(fewsnet_10davg)
@collate(starting_files, formatter(formatter_in), formatter_out)
def fewsnet_1moncum(input_file, output_file):

    args = {"input_file": input_file,"output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_cumulate(**args)

#   ---------------------------------------------------------------------
#   Monthly Average
in_prod_ident='_'+prod+'_1moncum_'+mapset+ext
output_sprod="1monavg"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(fewsnet_1moncum, formatter(formatter_in),formatter_out)
def fewsnet_1monavg(input_file, output_file):

    # TODO-M.C.: add nodata management
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_avg_image(**args)
    # TODO-M.C.: upsert to DB

#   ---------------------------------------------------------------------
#   Monthly Minimum
output_sprod="1monmin"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(fewsnet_1moncum, formatter(formatter_in),formatter_out)
def fewsnet_1monmin(input_file, output_file):

    # TODO-M.C.: add nodata management
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_min_image(**args)

#   ---------------------------------------------------------------------
#   Monthly Maximum
output_sprod="1monmax"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

reg_ex_in="[0-9]{4}([0-9]{4})"+in_prod_ident

# Take all RFE of the same dekad, along yearly timeseries ...
formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
# ... and merge into a single file
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(fewsnet_1moncum, formatter(formatter_in),formatter_out)
def fewsnet_1monmax(input_file, output_file):

    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_max_image(**args)

#   ---------------------------------------------------------------------
#   1monDiff
output_sprod="1mondiff"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

# inputs
#   Starting files + avg
formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}{MMDD[0]}"+out_prod_ident
ancillary_sprod = "1monavg"

ancillary_subdir = "derived"+os.path.sep+ancillary_sprod+os.path.sep
ancillary_sprod_ident = '_'+prod+'_'+ancillary_sprod+'_'+mapset+ext
ancillary_input="{subpath[0][2]}"+os.path.sep+ancillary_subdir+"{MMDD[0]}"+ancillary_sprod_ident

@follows(fewsnet_1monavg)
@transform(fewsnet_1moncum, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_1mondiff(input_file, output_file):

    args = {"input_file": input_file, "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_oper_subtraction(**args)

#   ---------------------------------------------------------------------
#   1monperc
output_sprod="1monperc"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

# inputs
#   Starting files + avg
formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}{MMDD[0]}"+out_prod_ident
ancillary_sprod = "1monavg"

ancillary_subdir = "derived"+os.path.sep+ancillary_sprod+os.path.sep
ancillary_sprod_ident = '_'+prod+'_'+ancillary_sprod+'_'+mapset+ext
ancillary_input="{subpath[0][2]}"+os.path.sep+ancillary_subdir+"{MMDD[0]}"+ancillary_sprod_ident

@follows(fewsnet_1monavg)
@transform(fewsnet_1moncum, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_1monperc(input_file, output_file):

    args = {"input_file": input_file[0], "avg_file": input_file[1], "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_compute_perc_diff_vs_avg(**args)

#   ---------------------------------------------------------------------
#   Run the pipeline

pipeline_run()
#pipeline_run(multiprocess=6)
#pipeline_printout()
#pipeline_printout()
#pipeline_printout_graph('flowchart.jpg')