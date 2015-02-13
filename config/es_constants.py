#
#	purpose: Define all variables for es2
#	author:  M.Clerici & Jurriaan van 't Klooster
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
import ConfigParser
from osgeo import gdalconst

thisfiledir = os.path.dirname(os.path.abspath(__file__))
config_factorysettings = ConfigParser.ConfigParser()
config_factorysettings.read(['factory_settings.ini', thisfiledir+'/factory_settings.ini'])

config_usersettings = ConfigParser.ConfigParser()
config_usersettings.read(['user_settings.ini', '/eStation2/settings/user_settings.ini'])

usersettings = config_usersettings.items('USER_SETTINGS')
for setting, value in usersettings:
    if not value is None and value != "":
        config_factorysettings.set('FACTORY_SETTINGS', setting, value)
    else:
        config_factorysettings.set('FACTORY_SETTINGS',
                                   setting,
                                   config_factorysettings.get('FACTORY_SETTINGS', setting, 0))

es2globals = {}
factorysettings = config_factorysettings.items('FACTORY_SETTINGS')
for setting, value in factorysettings:
    es2globals[setting] = value
    locals()[setting] = value

# ---------------------------------------------------------------
# Various definitions
# ---------------------------------------------------------------
ES2_OUTFILE_FORMAT = 'GTiff'
ES2_OUTFILE_EXTENSION = '.tif'
ES2_OUTFILE_OPTIONS = 'COMPRESS=LZW'
ES2_OUTFILE_INTERP_METHOD = gdalconst.GRA_NearestNeighbour
