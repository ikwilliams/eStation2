#
#   File defining 'local' variables, i.e. variables referring to the local machine (quigon, vm19, aniston)
#   Indeed, this is not to be synchronized through machines
#

import os, sys
from locals import *

dir()

# Overwrite Ingest_dir (for vm19)
es2globals['ingest_dir'] = '/data/Archives/FewsNET/'

# Overwrite data_fir (for vm19)
es2globals['data_dir'] = '/data/processing/'

# Add a test_data_dir (in/out/tmp)
es2globals['test_data_in'] = es2globals['data_dir']+'FEWSNET_RFE/tif/RFE/'
es2globals['test_data_out'] = es2globals['base_dir']+'TestFiles/Outputs/'
es2globals['test_data_inter'] = es2globals['base_dir']+'TestFiles/Interm/'
