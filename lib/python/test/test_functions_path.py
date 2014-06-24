from unittest import TestCase

__author__ = 'clerima'

import os
from lib.python.functions import *
sep=os.path.sep

class TestFunctionsPath(TestCase):

    def test_get_from_path(self):

        dirname=sep+'base'+sep+'dir'+sep+'some'+sep+'where' + sep +\
                'my_prod_code'+sep+'dir_type'+sep+'my_subprod_code'+sep

        [prodcode,subprodcode] = get_from_path_dir(dirname)

        self.assertEqual(prodcode,'my_prod_code')
        self.assertEqual(subprodcode,'my_subprod_code')


    def test_get_from_path_filename(self):

        str_date = '201401011200'
        str_version = 'my_version'
        str_prod = 'my_prod_code_'+str_version
        str_sprod = 'my_subprod_code'
        str_mapset= 'my_mapset'

        filename=str_date+'_'+str_prod+'_'+str_sprod+'_'+str_mapset+'.tif'

        [my_date, my_mapset] = get_from_path_filename(filename, str_prod, str_sprod)

        self.assertEqual(my_date,str_date)
        self.assertEqual(my_mapset,str_mapset)


