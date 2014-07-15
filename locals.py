#
#   File defining 'local' variables, i.e. variables referring to the local machine (quigon, vm19, aniston)
#   Indeed, this is not to be synchronized through machines
#



import os
import sys

#this_dir=os.path.abspath(os.path.dirname(__file__))

my_dir = '/srv/www/MarcoDev/eStation2/'
oth_dir = '/srv/www/JurDev/eStation2/'

list = sys.path

if my_dir not in list:
    sys.path.append(my_dir)

if oth_dir in list:
    sys.path.remove(oth_dir)

es2globals = {
    'host': 'localhost',
    'port': '5432',
    'dbUser': 'estation',
    'dbPass': 'mesadmin',
    'dbName': 'estationdb',
    'schema': 'products',
    'base_dir': '/srv/www/eStation2/',
    'data_dir': my_dir+'/TestFiles/',
    'ingest_dir': my_dir+'/TestFiles/',
    'static_data_path': '',
    'temp_dir': '/tmp/eStation2/'
}

try:
    from my_locals import *
except ImportError:
    pass
