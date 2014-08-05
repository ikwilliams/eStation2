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
        self.assertIsInstance(Dataset(productcode="Product", subproductcode="SubProduct"), Dataset)

    def test_class_no_product(self):
        kwargs = {'productcode':"---prod---", 'subproductcode': "---subprod---"}
        self.assertRaisesRegexp(NoProductFound,
                ".*%s.*" % (",".join("%s='%s'" % (key, value) for key, value in kwargs.items())),
                Dataset, **kwargs)
