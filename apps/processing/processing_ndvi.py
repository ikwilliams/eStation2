#
#	purpose: Define the processing chain for ndvi
#	author:  M.Clerici & Jurriaan van't Klooster
#	date:	 25.06.2014
#   descr:	 Generate additional derived products / implements processing chains
#	history: 1.0
#

# source my definitions
import locals
#

# Import eStation2 modules
from config.es_constants import *
import database.querydb as querydb
from lib.python.functions import *
from lib.python.metadata import *
from lib.python.image_proc import raster_image_math
from lib.python.image_proc.recode import *
import database.crud as crud

# Import third-party modules
from ruffus import *

logger = log.my_logger(__name__)

#   Still to be done

#   General definitions for this processing chain
prod="VGT_NDVI"
mapset='WGS84_Guinea2Nig_1km'
ext='.tif'
version='undefined'

#   general switch
activate_vgt_ndvi_comput=1

#   switch wrt to group
activate_nvi_no_filter_stats=0
activate_nvi_no_filter_anomalies=0

activate_filtered_prods=1
activate_filtered_stats=0
activate_filtered_anomalies=0

activate_monthly_prods=0

#   and for each prod in: activate_nvi_no_filter_stats
activate_10davg_no_filter = 1

#   ---------------------------------------------------------------------
#   Define input files
starting_sprod='NDV'
in_prod_ident = set_path_filename_no_date(prod, starting_sprod, mapset, ext)

input_dir = locals.es2globals['data_dir']+ \
            set_path_sub_directory(prod, starting_sprod, 'tif', version)

starting_files = input_dir+"*"+in_prod_ident

#   ---------------------------------------------------------------------
#   NDV avg x dekad (i.e. avg_dekad)
output_sprod="10DAVG"

out_prod_ident = set_path_filename_no_date(prod, output_sprod, mapset, ext)
output_subdir  = set_path_sub_directory   (prod, output_sprod, 'derived', version)

formatter_in="[0-9]{4}(?P<MMDD>[0-9]{4})"+in_prod_ident
formatter_out=["{subpath[0][3]}"+os.path.sep+output_subdir+"{MMDD[0]}"+out_prod_ident]

@active_if(activate_vgt_ndvi_comput, activate_nvi_no_filter_stats, activate_10davg_no_filter)
@collate(starting_files, formatter(formatter_in),formatter_out)
def fewsnet_10davg(input_file, output_file):

    output_file = list_to_element(output_file)
    check_output_dir(os.path.dirname(output_file))
    args = {"input_file": input_file, "output_file": output_file, "output_format": 'GTIFF', "options": "compress=lzw"}
    raster_image_math.do_avg_image(**args)
    #upsert_processed_ruffus(output_file)

#   ---------------------------------------------------------------------
#   NDV min x dekad (i.e. min_dekad)
output_sprod="10DMIN"
#   ---------------------------------------------------------------------
#   NDV max x dekad (i.e. max_dekad)
output_sprod="10DMAX"
#   ---------------------------------------------------------------------
#   NDV std x dekad (i.e. std_dekad)
output_sprod="10DSTD"
#   ---------------------------------------------------------------------
#   NDV med x dekad (i.e. med_dekad)
output_sprod="10DMED"

#   ---------------------------------------------------------------------
#   NDV stats per year -> TBDone
#   ---------------------------------------------------------------------
#   NDV stats per absolute -> TBDone

#   ---------------------------------------------------------------------
#   NDV linearx1/x2
#   Note: here the difficulty is to manage the +1/-1 dekad across the year

output_sprod="NDVI_LINEARX1"
out_prod_ident = set_path_filename_no_date(prod, output_sprod, mapset, ext)
output_subdir  = set_path_sub_directory   (prod, output_sprod, 'derived', version)

def generate_parameters_on_the_fly():

        # TODO-M.C.: replace with functions that parse all 'tif/NDV' files and finds out two neighbors
        parameters = [
            [('20100101_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif','20100111_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif','20100121_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif'), 'my_out.tif'],
            [('20100101_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif','20100111_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif','20100121_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif'), 'my_out.tif'],
            [('20100101_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif','20100111_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif','20100121_VGT_NDVI_NDV_WGS84_Guinea2Nig_1km.tif'), 'my_out.tif']
        ]

        # TODO-M.C.: create function to append directory to list of parameters
        for job_pars in parameters:
            pars_list = []
            for element in job_pars:
                if isinstance(element,tuple):
                    new_element = ()
                    for component in element:
                        new_element = new_element + (input_dir+component,)
                else:
                    new_element = input_dir+element
                pars_list.append(new_element)
            yield pars_list

        # for job_pars in parameters:
        #     yield job_pars

@active_if(activate_vgt_ndvi_comput, activate_filtered_prods)
@files(generate_parameters_on_the_fly)
def ndvi_linearx1(input_files, output_file):

    print "input_file: ", input_files[0]
    print "input_file1:", input_files[1]
    print "input_file2:", input_files[2]

    print "output_file:", output_file


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