#
#	purpose: Define the processing service (by using ruffus)
#	author:  M.Clerici & Jurriaan van't Klooster
#	date:	 11.06.2014
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

# Import third-party modules
from osgeo.gdalconst import *
from osgeo import gdal
from osgeo import osr
import pygrib
import numpy as N
from ruffus import *

logger = log.my_logger(__name__)

input_dir = locals.es2globals['test_data_in']+'/FEWSNET_RFE/tif/RFE/'
# interm_dir = locals.es2globals['test_data_inter']

#   Still to be done
#   TODO-M.C.test: upsert to DB
#   TODO-M.C.ok: Add metadata to the output
#   TODO-M.C.: functions to avoid repetitions
#   TODO-M.C.: more checks on the IN/OUT
#   TODO-M.C.ok: NODATA management -> not for RFE !!
#   TODO-M.C.ok: Check and create output dir
#   TODO-M.C.test: Activate/deactivate according to DB settings
#   TODO-M.C.test: Add a mechanism to extract/visualize the 'status' -> pipeline_printout(verbose=3)+grep-like function ?
#   TODO-M.C.: create unittest-like functions for validating the chain
#   TODO-M.C.: multiprocessing does not work -> VM issue ?
#   TODO-M.C.test: add the Np anomalies
#   TODO-M.C.test: find a robust method to solve the tuple/string issue in filename (fttb: return_as_element_of_list() ?)

# Delete a file for re-creating

#   General definitions for this processing chain
prod="FEWSNET_RFE"
mapset='FEWSNET_Africa_8km'
ext='.tif'

#   general switch
activate_fewsnet_rfe_comput=1

#   switch wrt temporal resolution
activate_10d_comput=1
activate_1month_comput=1

#   specific switch for each subproduct
activate_10davg_comput=1
activate_10dmin_comput=1
activate_10dmax_comput=1
activate_10ddiff_comput=1
activate_10dperc_comput=1
activate_10dnp_comput=1

activate_1moncum_comput=0
activate_1monavg_comput=0
activate_1monmin_comput=0
activate_1monmax_comput=0
activate_1mondiff_comput=0
activate_1monperc_comput=0
activate_1monnp_comput=0

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

@active_if(activate_fewsnet_rfe_comput, activate_10d_comput, activate_10davg_comput)
@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10davg(input_file, output_file):

    check_output_dir(os.path.dirname(output_file[0]))
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_avg_image(**args)
    upsert_processed_ruffus(output_file[0])


#   ---------------------------------------------------------------------
#   Minimum
output_sprod="10dmin"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@active_if(activate_fewsnet_rfe_comput, activate_10d_comput, activate_10dmin_comput)
@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10dmin(input_file, output_file):

    check_output_dir(os.path.dirname(output_file[0]))
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_min_image(**args)
    upsert_processed_ruffus(output_file[0])

#   ---------------------------------------------------------------------
#   Maximum
output_sprod="10dmax"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

# Take all RFE of the same dekad, along yearly timeseries ...
formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
# ... and merge into a single file
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@active_if(activate_fewsnet_rfe_comput, activate_10d_comput, activate_10dmax_comput)
@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10dmax(input_file, output_file):

    check_output_dir(os.path.dirname(output_file[0]))
    args = {"input_file": input_file, "output_file": output_file[0], "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_max_image(**args)
    upsert_processed_ruffus(output_file[0])

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
@active_if(activate_fewsnet_rfe_comput, activate_10d_comput, activate_10ddiff_comput)
@transform(starting_files, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_10ddiff(input_file, output_file):

    check_output_dir(os.path.dirname(output_file))
    args = {"input_file": input_file, "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_oper_subtraction(**args)
    upsert_processed_ruffus(output_file)

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
@active_if(activate_fewsnet_rfe_comput, activate_10d_comput, activate_10dperc_comput)
@transform(starting_files, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_10dperc(input_file, output_file):

    check_output_dir(os.path.dirname(output_file))
    args = {"input_file": input_file[0], "avg_file": input_file[1], "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_compute_perc_diff_vs_avg(**args)
    upsert_processed_ruffus(output_file)

#   ---------------------------------------------------------------------
#   10dnp
output_sprod="10dnp"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

#   Starting files + min + max
formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}{MMDD[0]}"+out_prod_ident

ancillary_sprod_1 = "10dmin"
ancillary_subdir_1 = "derived"+os.path.sep+ancillary_sprod_1+os.path.sep
ancillary_sprod_ident_1 = '_'+prod+'_'+ancillary_sprod_1+'_'+mapset+ext
ancillary_input_1="{subpath[0][2]}"+os.path.sep+ancillary_subdir_1+"{MMDD[0]}"+ancillary_sprod_ident_1

ancillary_sprod_2 = "10dmax"
ancillary_subdir_2 = "derived"+os.path.sep+ancillary_sprod_2+os.path.sep
ancillary_sprod_ident_2 = '_'+prod+'_'+ancillary_sprod_2+'_'+mapset+ext
ancillary_input_2="{subpath[0][2]}"+os.path.sep+ancillary_subdir_2+"{MMDD[0]}"+ancillary_sprod_ident_2

@follows(fewsnet_10davg)
@active_if(activate_fewsnet_rfe_comput, activate_10d_comput, activate_10dnp_comput)
@transform(starting_files, formatter(formatter_in), add_inputs(ancillary_input_1, ancillary_input_2), formatter_out)
def fewsnet_10dnp(input_file, output_file):

    check_output_dir(os.path.dirname(output_file))
    args = {"input_file": input_file[0], "min_file": input_file[1],"max_file": input_file[2], "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_make_vci(**args)
    upsert_processed_ruffus(output_file)

#   ---------------------------------------------------------------------
#   1moncum
output_sprod="1moncum"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

# inputs: files from same months
formatter_in="(?P<YYYYMM>[0-9]{6})(?P<DD>[0-9]{2})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYYMM[0]}"+'01'+out_prod_ident

# @follows(fewsnet_10davg)
@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1moncum_comput)
@collate(starting_files, formatter(formatter_in), formatter_out)
def fewsnet_1moncum(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file,"output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_cumulate(**args)
    upsert_processed_ruffus(output_file_1)

#   ---------------------------------------------------------------------
#   Monthly Average
in_prod_ident='_'+prod+'_1moncum_'+mapset+ext
output_sprod="1monavg"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1monavg_comput)
@collate(fewsnet_1moncum, formatter(formatter_in),formatter_out)
def fewsnet_1monavg(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file, "output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_avg_image(**args)
    upsert_processed_ruffus(output_file_1)

#   ---------------------------------------------------------------------
#   Monthly Minimum
output_sprod="1monmin"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][2]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1monmin_comput)
@collate(fewsnet_1moncum, formatter(formatter_in),formatter_out)
def fewsnet_1monmin(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file, "output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_min_image(**args)
    upsert_processed_ruffus(output_file_1)

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

@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1monmax_comput)
@collate(fewsnet_1moncum, formatter(formatter_in),formatter_out)
def fewsnet_1monmax(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file, "output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_max_image(**args)
    upsert_processed_ruffus(output_file_1)

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
@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1mondiff_comput)
@transform(fewsnet_1moncum, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_1mondiff(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file, "output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_oper_subtraction(**args)
    upsert_processed_ruffus(output_file_1)

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
@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1monperc_comput)
@transform(fewsnet_1moncum, formatter(formatter_in), add_inputs(ancillary_input), formatter_out)
def fewsnet_1monperc(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file[0], "avg_file": input_file[1], "output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_compute_perc_diff_vs_avg(**args)
    upsert_processed_ruffus(output_file_1)

#   ---------------------------------------------------------------------
#   1monnp
output_sprod="1monnp"
output_subdir="derived"+os.path.sep+output_sprod+os.path.sep
out_prod_ident='_'+prod+'_'+output_sprod+'_'+mapset+ext

#   Starting files + min + max
formatter_in="(?P<YYYY>[0-9]{4})(?P<MMDD>[0-9]{4})"+in_prod_ident

formatter_out="{subpath[0][2]}"+os.path.sep+output_subdir+"{YYYY[0]}{MMDD[0]}"+out_prod_ident

ancillary_sprod_1 = "1monmin"
ancillary_subdir_1 = "derived"+os.path.sep+ancillary_sprod_1+os.path.sep
ancillary_sprod_ident_1 = '_'+prod+'_'+ancillary_sprod_1+'_'+mapset+ext
ancillary_input_1="{subpath[0][2]}"+os.path.sep+ancillary_subdir_1+"{MMDD[0]}"+ancillary_sprod_ident_1

ancillary_sprod_2 = "1monmax"
ancillary_subdir_2 = "derived"+os.path.sep+ancillary_sprod_2+os.path.sep
ancillary_sprod_ident_2 = '_'+prod+'_'+ancillary_sprod_2+'_'+mapset+ext
ancillary_input_2="{subpath[0][2]}"+os.path.sep+ancillary_subdir_2+"{MMDD[0]}"+ancillary_sprod_ident_2

@follows(fewsnet_1monavg)
@active_if(activate_fewsnet_rfe_comput, activate_1month_comput, activate_1monnp_comput)
@transform(fewsnet_1moncum, formatter(formatter_in), add_inputs(ancillary_input_1, ancillary_input_2), formatter_out)
def fewsnet_1monnp(input_file, output_file):

    output_file_1 = return_as_element_of_list(output_file)
    check_output_dir(os.path.dirname(output_file_1))
    args = {"input_file": input_file[0], "min_file": input_file[1],"max_file": input_file[2], "output_file": output_file_1, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_make_vci(**args)
    upsert_processed_ruffus(output_file_1)

#   ---------------------------------------------------------------------
#   Upsert in the DB table a product generated by ruffus

def upsert_processed_ruffus(file_fullpath):

        # -------------------------------------------------------------------------
        # Upsert into DB table 'products_data'
        # -------------------------------------------------------------------------

        filename = os.path.basename(file_fullpath)
        dirname = os.path.dirname(file_fullpath)

        # TODO-M.C.: add tests, try/except
        [productcode, subproductcode, version] = get_from_path_dir(dirname)
        [str_date, mapsetcode] = get_from_path_filename(filename, productcode, subproductcode)
        [str_year, str_month, str_day, str_hour] = extract_from_date(str_date)

        if str_year == '':
            str_year='0'
        cruddb = crud.CrudDB()
        recordkey = {'productcode': productcode.lower(),
                     'subproductcode': subproductcode.lower(),
                     'version': 'undefined',
                     'mapsetcode': mapsetcode,
                     'product_datetime': str_date}

        record = {'productcode': productcode.lower(),
                  'subproductcode': subproductcode.lower(),
                  'version': 'undefined',
                  'mapsetcode': mapsetcode,
                  'product_datetime': str_date,
                  'directory': dirname,
                  'filename': filename,
                  'year': int(str_year),
                  'month': int(str_month),
                  'day': int(str_day),
                  'hour': int(str_hour),
                  'file_role': 'active',
                  'file_type': 'GTiff'}

        if len(cruddb.read('products.products_data', **recordkey)) > 0:
            logger.debug('Updating products_data record: ' + str(recordkey))
            cruddb.update('products.products_data', record)
        else:
            logger.debug('Creating products_data record: ' + str(recordkey))
            cruddb.create('products.products_data', record)

#   ---------------------------------------------------------------------
#   Run the pipeline

def processing_fewsnet_rfe():

    logger.info("Entering routine %s" % 'processing_fewsnet_rfe')
    #pipeline_printout(verbose=3)
    #sleep 1
    pipeline_run(verbose=2)
    #pipeline_run(multiprocess=6)
    #pipeline_printout()
    #pipeline_printout_graph('flowchart.jpg')