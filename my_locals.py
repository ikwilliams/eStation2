#
#   File defining 'local' variables, i.e. variables referring to the local machine (quigon, vm19, aniston)
#   Indeed, this is not to be synchronized through machines
#

import os, sys
from locals import *

oth_dir = '/srv/www/JurDev/eStation2/'
my_dir = '/srv/www/MarcoDev/eStation2/'

list_syspath = sys.path

if my_dir not in list_syspath:
    sys.path.append(my_dir)

if oth_dir in list_syspath:
    sys.path.remove(oth_dir)

# Overwrite definitions (for vm19)
es2globals['base_dir']=my_dir
es2globals['static_data_path']=''
#es2globals['ingest_dir']=my_dir+'/TestFiles/'
es2globals['ingest_dir'] = '/data/Archives/FewsNET/'

# Overwrite data_fir (for vm19)
#es2globals['data_dir']= my_dir+'/TestFiles/'
es2globals['data_dir'] = '/data/processing/'

# Add a test_data_dir (in/out/tmp)
es2globals['test_data_in'] = es2globals['data_dir']+'FEWSNET_RFE/tif/RFE/'
es2globals['test_data_out'] = es2globals['base_dir']+'TestFiles/Outputs/'
es2globals['test_data_inter'] = es2globals['base_dir']+'TestFiles/Interm/'
