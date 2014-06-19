#
#   File defining 'local' variables, i.e. variables referring to the local machine (quigon, vm19, aniston)
#   Indeed, this is not to be synchronized through machines
#



import os, sys
this_dir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_dir)

es2globals = {
    'host': 'localhost',
    'port': '5432',
    'dbUser': 'estation',
    'dbPass': 'mesadmin',
    'dbName': 'estationdb',
    'schema': 'products',
    'base_dir': '/srv/www/eStation2/',
    'data_dir': this_dir+'/TestFiles/',
    'ingest_dir': this_dir+'/TestFiles/',
    'static_data_path': '',
    'temp_dir': '/tmp/eStation2/'
}

try:
    from my_locals import *
except ImportError:
    pass
