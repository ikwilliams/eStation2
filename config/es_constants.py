#
#	purpose: Define all variables for es2
#	author:  M.Clerici
#	date:	 13.03.2014
#   descr:	 Define all variables for es2
#	history: 1.0
#
#   NOTE: all the definitions are going to be in es_constants.ini, that will contain two sections
#         Factory Settings : some of them are going to be written at the .deb package generation from iniEnv
#         User Settings: User can overwrite a sub-set of the Factory settings (not the 'internal' ones)
#         This module will:     1. Read both Factory/User Settings from .ini
#                               2. Manage priorities (User -> Factory)
#                               3. Make available the settings, part in es2globals, part
#
#   This module will be be imported by any other (instead of locals.py -> to be discontinued)
#
import os
#import locals
from osgeo import gdalconst

# Get base dir
try:
    base_dir = locals.es2globals['base_dir']
except EnvironmentError:
    print 'Error - base_dir not defined in locals.  Exit'
    exit(1)

try:
    data_dir = locals.es2globals['data_dir']
except EnvironmentError:
    print 'Error - data_dir not defined in locals.  Exit'
    exit(1)

# ---------------------------------------------------------------
# Software version
# ---------------------------------------------------------------
ES2_SW_VERSION = '2.0.0'

# ---------------------------------------------------------------
# Application paths (depends on locals.py)
# ---------------------------------------------------------------
#install_path = base_dir
base_dir = '/srv/www/eStation2/'                                ## User Defined !
apps_dir = base_dir+'/apps/'
config_dir = base_dir+'/config/'
processing_dir = apps_dir+'/processing'

log_dir = base_dir+'/log/'
wrk_dir = base_dir+'/wrk_dir/'
base_tmp_dir = os.path.sep+'tmp'+os.path.sep+'eStation2'+os.path.sep    ## User Defined !

# Data paths (temp)
data_dir =  '/data/'                                            ## User Defined !

eumetcast_files_dir = data_dir+'my_eumetcast_dir/'              ## User Defined !
ingest_server_in_dir = data_dir+'my_data_ingest_dir/'           ## User Defined !

template_mapfile = apps_dir+'analysis/MAP_main.map'

# ---------------------------------------------------------------
# Services: GET/INGEST
# ---------------------------------------------------------------

processed_list_base_dir = base_tmp_dir + 'get_lists' +os.path.sep
processed_list_eum_dir = processed_list_base_dir+'get_eumetcast'+os.path.sep
processed_list_int_dir = processed_list_base_dir+'get_internet'+os.path.sep

get_eumetcast_processed_list_prefix = processed_list_eum_dir+'get_eum_processed_list_'
get_internet_processed_list_prefix = processed_list_int_dir + 'get_internet_processed_list_'

poll_frequency = 5

pid_file_dir=base_tmp_dir+'services'+os.path.sep
get_internet_pid_filename=pid_file_dir+'get-internet.pid'
get_eumetcast_pid_filename=pid_file_dir+'get-eumetcast.pid'
ingest_pid_filename=pid_file_dir+'ingest.pid'
processing_pid_filename=pid_file_dir+'processing.pid'
processing_tasks_dir=base_tmp_dir+'processing'+os.path.sep

#umask 0002
# Python libs paths
#export PYTHONPATH = /opt/extern/gdal/lib/python2.6/site-packages/:/opt/extern/gdal/lib/python2.6/site-packages/osgeo
#export LD_LIBRARY_PATH = /opt/extern/gdal/lib:/usr/share/szip-2.1/lib/usr/local/lib

# GDAL directory and commands
GDAL_dir='/usr/bin/'
GDAL_merge=GDAL_dir+'gdal_merge.py'

# Additional processing generic product _directories
#processing__dir = "archive tif xml derived"

# ---------------------------------------------------------------
# DATABASE: schemas/tables names
# ---------------------------------------------------------------

DB_SCHEMA_PRODUCTS = 'products'
DB_SCHEMA_ANALYSIS = 'analysis'
DB_SCHEMA_DATA = 'data'

dbglobals = {
    'host': locals.es2globals['host'],
    'port': locals.es2globals['port'],
    'dbUser': locals.es2globals['dbUser'],
    'dbPass': locals.es2globals['dbPass'],
    'dbName': locals.es2globals['dbName'],
    'schema_products': DB_SCHEMA_PRODUCTS,
    'schema_analysis': DB_SCHEMA_ANALYSIS,
    'schema_data': DB_SCHEMA_DATA
}

# ---------------------------------------------------------------
# Various definitions
# ---------------------------------------------------------------
ES2_OUTFILE_FORMAT = 'GTiff'
ES2_OUTFILE_EXTENSION = '.tif'
ES2_OUTFILE_OPTIONS = 'COMPRESS=LZW'
ES2_OUTFILE_INTERP_METHOD = gdalconst.GRA_NearestNeighbour

# ---------------------------------------------------------------
# Copy some of the definitions to es2globals (previously in locals.py)
# ---------------------------------------------------------------
es2globals = {
    'host': 'localhost',
    'port': '5432',
    'dbUser': 'estation',
    'dbPass': 'mesadmin',
    'dbName': 'estationdb',
    'schema': 'products',
    'base_dir': '/srv/www/eStation2/',              # eStation2 installation dir
    'data_dir': '',                                 # root dir for all eStation2 operational data
    'ingest_dir': '',                               # 'pool' dir for all retrieved files (GET service)
    'static_data_path': '',
    'temp_dir': '/tmp/eStation2/'
}

