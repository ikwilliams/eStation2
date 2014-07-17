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


class TestFrequency(unittest.TestCase):
    def test_class(self):
        self.assertIsInstance(Frequency(1, Frequency.UNIT.DEKAD, Frequency.TYPE.PER), Frequency)

    def test_wrong_value_1(self):
        self.assertRaises(WrongFrequencyValue, Frequency, *('a', Frequency.UNIT.DEKAD, Frequency.TYPE.PER))

    def test_wrong_value_2(self):
        self.assertRaises(WrongFrequencyValue, Frequency, *(1.1, Frequency.UNIT.DEKAD, Frequency.TYPE.PER))

    def test_wrong_unit(self):
        self.assertRaises(WrongFrequencyUnit, Frequency, *(1, '-' + Frequency.UNIT.DEKAD, Frequency.TYPE.PER))

    def test_wrong_type(self):
        self.assertRaises(WrongFrequencyType, Frequency, *(1, Frequency.UNIT.DEKAD, '-' + Frequency.TYPE.PER))

    def test_dataformat_default_1(self):
        frequency =  Frequency(1, Frequency.UNIT.DEKAD, Frequency.TYPE.PER)
        self.assertEqual(frequency.dateformat, Frequency.DATEFORMAT.DATE)

    def test_dataformat_default_2(self):
        frequency =  Frequency(4, Frequency.UNIT.HOUR, Frequency.TYPE.PER)
        self.assertEqual(frequency.dateformat, Frequency.DATEFORMAT.DATETIME)

    def test_wrong_dataformat(self):
        self.assertRaises(WrongFrequencyDateFormat, Frequency, *(4, Frequency.UNIT.HOUR, Frequency.TYPE.PER, '-' + Frequency.DATEFORMAT.DATETIME))


class TestHelpersDate(unittest.TestCase):
    def test_add_years(self):
        self.assertEquals(add_years(datetime.date(2000, 3, 4), 4), datetime.date(2004, 3, 4))

    def test_add_years_to_leap_year_1(self):
        self.assertEquals(add_years(datetime.date(2000, 2, 29), 4), datetime.date(2004, 2, 29))

    def test_add_years_to_leap_year_2(self):
        self.assertEquals(add_years(datetime.date(2000, 2, 29), 3), datetime.date(2003, 2, 28))

    def test_add_months_1(self):
        self.assertEquals(add_months(datetime.date(2000, 3, 4), 4), datetime.date(2000, 7, 4))

    def test_add_months_2(self):
        self.assertEquals(add_months(datetime.date(2000, 3, 4), 26), datetime.date(2002, 5, 4))

    def test_add_months_3(self):
        self.assertEquals(add_months(datetime.date(2000, 3, 31), 13), datetime.date(2001, 4, 30))

    def test_add_months_4(self):
        self.assertEquals(add_months(datetime.date(2000, 1, 1), 11), datetime.date(2000, 12, 1))

    def test_add_dekad_1(self):
        self.assertEquals(add_dekads(datetime.date(2000, 1, 1), 2), datetime.date(2000, 1, 21))

    def test_add_dekad_2(self):
        self.assertEquals(add_dekads(datetime.date(2000, 1, 28), 1), datetime.date(2000, 2, 8))

    def test_add_dekad_3(self):
        self.assertEquals(add_dekads(datetime.date(2000, 1, 30), 3), datetime.date(2000, 3, 10))


class TestHelpersGap(unittest.TestCase):
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

    def test_find_gap_dekad_no_gap(self):
        self.assertEqual([], find_gaps(self.files, 
            frequency=Frequency(dateformat='YYYYMMDD', value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY)))

    def test_find_gap_dekad_with_gap(self):
        gap = find_gaps(self.files[:10] + self.files[12:], 
            frequency=Frequency(dateformat='YYYYMMDD', value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY))
        self.assertEqual(len(gap), 2)
        self.assertEqual(gap[0], self.files[10])
        self.assertEqual(gap[1], self.files[11])


class TestDatasets(unittest.TestCase):
    def test_class(self):
        self.assertIsNotNone(Dataset(product="Product", subproduct="SubProduct"))
