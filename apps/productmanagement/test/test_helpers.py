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
        WrongFrequencyType, WrongFrequencyDateFormat, WrongDateParameter)


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
        self.files_dekad = [
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
        self.files_day_gap = self.files_dekad[:3]
        self.date_from = datetime.date(2013, 12, 24)
        self.date_to = datetime.date(2014, 1, 5)
        self.files_day = [
                "20131227_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131228_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131229_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131230_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131231_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140102_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                ]
        self.files_15minutes = [
                "201310212200_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212215_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212230_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212245_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212300_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212315_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212330_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310212345_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310220000_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310220015_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "201310220030_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                ]
        self.files_months = [
                "20131001_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20131201_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140201_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140301_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                ]

    def test_find_gap_dekad_intervals_no_gap(self):
        self.assertEqual([], find_gaps(self.files_dekad, 
            frequency=Frequency(dateformat='YYYYMMDD', value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY),
            only_intervals=True))

    def test_find_gap_dekad_no_gap(self):
        self.assertEqual([], find_gaps(self.files_dekad, 
            frequency=Frequency(dateformat='YYYYMMDD', value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY)))

    def test_find_gap_dekad_no_gap_per(self):
        self.assertEqual([], find_gaps(self.files_dekad, 
            frequency=Frequency(dateformat='YYYYMMDD', value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.PER)))

    def test_find_gap_dekad_with_gap(self):
        gap = find_gaps(self.files_dekad[:10] + self.files_dekad[12:], 
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY))
        self.assertEqual(len(gap), 2)
        self.assertEqual(gap[0], self.files_dekad[10])
        self.assertEqual(gap[1], self.files_dekad[11])

    def test_find_gap_dekad_intervals_with_gap(self):
        intervals = find_gaps(self.files_dekad[:10] + self.files_dekad[14:], 
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.EVERY),
            only_intervals=True)
        self.assertEqual(len(intervals), 1)
        self.assertEqual(intervals[0], [self.files_dekad[10], self.files_dekad[13]])

    def test_find_gap_dekad_with_gap_per(self):
        gap = find_gaps(self.files_dekad[:10] + self.files_dekad[12:], 
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DEKAD, type_=Frequency.TYPE.PER))
        self.assertEqual(len(gap), 2)
        self.assertEqual(gap[0], self.files_dekad[10])
        self.assertEqual(gap[1], self.files_dekad[11])

    def test_find_gap_day(self):
        gap = find_gaps(self.files_day_gap,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.EVERY))
        self.assertEqual(len(gap), 19)

    def test_find_gap_intervals_day(self):
        intervals = find_gaps(self.files_day_gap,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.EVERY),
            only_intervals=True)
        self.assertEqual(len(intervals), 2)

    def test_find_gap_day_per(self):
        gap = find_gaps(self.files_day_gap,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.PER))
        self.assertEqual(len(gap), 19)

    def test_find_gap_minutes(self):
        self.assertEqual([], find_gaps(self.files_15minutes, 
            frequency=Frequency(value=4,
                unit=Frequency.UNIT.HOUR, type_=Frequency.TYPE.PER)))

    def test_find_gap_minutes_with_gap(self):
        gap = find_gaps(self.files_15minutes[:3] + self.files_15minutes[5:], 
            frequency=Frequency(value=4,
                unit=Frequency.UNIT.HOUR, type_=Frequency.TYPE.PER))
        self.assertEqual(len(gap), 2)
        self.assertEqual(gap[0], self.files_15minutes[3])
        self.assertEqual(gap[1], self.files_15minutes[4])

    def test_find_gap_months(self):
        self.assertEqual([], find_gaps(self.files_months, 
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.MONTH, type_=Frequency.TYPE.EVERY)))

    def test_find_gap_months_per(self):
        self.assertEqual([], find_gaps(self.files_months, 
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.MONTH, type_=Frequency.TYPE.PER)))

    def test_find_gap_day_no_gap(self):
        self.assertEqual([], find_gaps(self.files_day,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.EVERY)))

    def test_find_gap_day_from(self):
        gap = find_gaps(self.files_day,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.EVERY),
            from_date=self.date_from)
        self.assertEqual(len(gap), 3)

    def test_find_gap_day_to(self):
        gap = find_gaps(self.files_day,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.EVERY),
            to_date=self.date_to)
        self.assertEqual(len(gap), 3)

    def test_find_gap_day_from_to(self):
        gap = find_gaps(self.files_day,
            frequency=Frequency(value=1,
                unit=Frequency.UNIT.DAY, type_=Frequency.TYPE.EVERY),
            to_date=self.date_to,
            from_date=self.date_from)
        self.assertEqual(len(gap), 6)

    def test_find_gap_wrong_parameters(self):
        self.assertRaises(WrongDateParameter, find_gaps,
            *([], Frequency(value=1, unit=Frequency.UNIT.HOUR, type_=Frequency.TYPE.EVERY),),
            **{'to_date': datetime.date(2014, 10, 10)})
