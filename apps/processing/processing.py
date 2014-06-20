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
from lib.python import myCumulate
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

#   General definitions for this processing chain
prod="FEWSNET_RFE"
mapset='FEWSNET_Africa_8km'
ext='.tif'


#   ---------------------------------------------------------------------
#   Define input files
starting_sprod='RFE'
in_prod_ident='_'+prod+'_'+starting_sprod+'_'+mapset+ext
starting_files = input_dir+"*"+in_prod_ident
print 'starting_files = ', starting_files

#   ---------------------------------------------------------------------
#   First step: from RFE to stats (min/max/avg/std)
#   input ->            YYYY       MMDD              _<prod>_<sprod>_<mapset>.tif
#   formatter_in -> "[0-9]{4} (?P<MMDD>[0-9]{4})"+in_prod_ident
#
#   output ->           MMDD_<prod>_<sprod_OUT>_<mapset>.tif
#   formatter_out ->dir+"{MMDD[0]}"+out_prod_ident
#   where dir     -> "{subpath[0][2]}"+os.path.sep+output_subdir


#   ---------------------------------------------------------------------
#   Average
output_sprod="10davg"
output_subdir="derived/10davg/"
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

reg_ex_in="[0-9]{4}([0-9]{4})"+in_prod_ident

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10davg(input_file, output_file):

    # TODO-M.C.: add nodata management
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_avg_image(**args)
    # TODO-M.C.: upsert to DB

#   ---------------------------------------------------------------------
#   Minimum
output_sprod="10dmin"
output_subdir="derived/10dmin/"
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

reg_ex_in="[0-9]{4}([0-9]{4})"+in_prod_ident

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10dmin(input_file, output_file):

    # TODO-M.C.: add nodata management
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_min_image(**args)
    # TODO-M.C.: upsert to DB

#   ---------------------------------------------------------------------
#   Maximum
output_sprod="10dmax"
output_subdir="derived/10dmax/"
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

reg_ex_in="[0-9]{4}([0-9]{4})"+in_prod_ident

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10dmax(input_file, output_file):

    # TODO-M.C.: add nodata management
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_max_image(**args)
    # TODO-M.C.: upsert to DB

#   ---------------------------------------------------------------------
#   Run the pipeline

pipeline_run()
#pipeline_printout()
#pipeline_printout()
#pipeline_printout_graph('flowchart.jpg')