# -*- coding: utf-8 -*-
#
#	purpose: Test dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import
import unittest

import locals

from ..datasets import Dataset, Frequency
from ..helpers import find_gaps
from ..exceptions import (WrongFrequencyValue, WrongFrequencyUnit, WrongFrequencyType)

class TestFrequency(unittest.TestCase):
    def test_class(self):
        self.assertIsInstance(Frequency(1, Frequency.UNIT.DEKAD, Frequency.TYPE.PER), Frequency)

    def test_class_wrong_value_1(self):
        self.assertRaises(WrongFrequencyValue, Frequency, *('a', Frequency.UNIT.DEKAD, Frequency.TYPE.PER))

    def test_class_wrong_value_2(self):
        self.assertRaises(WrongFrequencyValue, Frequency, *(1.1, Frequency.UNIT.DEKAD, Frequency.TYPE.PER))

    def test_class_wrong_unit(self):
        self.assertRaises(WrongFrequencyUnit, Frequency, *(1, '-' + Frequency.UNIT.DEKAD, Frequency.TYPE.PER))

    def test_class_wrong_type(self):
        self.assertRaises(WrongFrequencyType, Frequency, *(1, Frequency.UNIT.DEKAD, '-' + Frequency.TYPE.PER))


class TestDatasets(unittest.TestCase):
    def test_class(self):
        self.assertIsNotNone(Dataset(product="Product", subproduct="SubProduct"))


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.files = [
                "20131021_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131111_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131121_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131201_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131211_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131221_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140111_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140121_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140201_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140211_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140221_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140301_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140311_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140321_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140401_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140411_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140421_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140501_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140511_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140521_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140601_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                ]

    def test_find_dekad_gap(self):
        self.assertEqual([], find_gaps(self.files, 
            frequency=Frequency(dateformat='YYYYMMDD', value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY)))
