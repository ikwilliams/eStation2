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
        WrongFrequencyType, WrongFrequencyDateFormat )


class TestDatasets(unittest.TestCase):
    def test_class(self):
        self.assertIsNotNone(Dataset(product="Product", subproduct="SubProduct"))
