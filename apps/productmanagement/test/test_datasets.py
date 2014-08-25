# -*- coding: utf-8 -*-

#
#	purpose: Test dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import

import unittest
import datetime

from ..datasets import Dataset, Frequency
from ..helpers import find_gaps, add_years, add_months, add_dekads
from ..exceptions import (WrongFrequencyValue, WrongFrequencyUnit,
        WrongFrequencyType, WrongFrequencyDateFormat, NoProductFound )


class TestDatasets(unittest.TestCase):
    def test_class(self):
        kwargs = {'product_code':"fewsnet_rfe", 'sub_product_code': "rfe", 'mapset': 'FEWSNET_Africa_8km'}
        self.assertIsInstance(Dataset(**kwargs), Dataset)

    def test_class_no_product(self):
        kwargs = {'product_code':"---prod---", 'sub_product_code': "---subprod---", 'mapset': '---mapset---'}
        self.assertRaisesRegexp(NoProductFound, "(?i).*found.*product.*",
                Dataset, **kwargs)
