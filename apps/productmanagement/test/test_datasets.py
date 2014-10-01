# -*- coding: utf-8 -*-

#
#	purpose: Test dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import

import unittest
import datetime
import sys
from ..helpers import INTERVAL_TYPE
from ..datasets import Dataset
from ..exceptions import (WrongDateType, NoProductFound)

from lib.python import functions
from database import querydb
import json

class TestDatasets(unittest.TestCase):
    def setUp(self):
        self.kwargs = {'product_code':"fewsnet_rfe", 'sub_product_code': "rfe", 'mapset': 'FEWSNET_Africa_8km'}
        self.files_dekad = [
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
                "20140601_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.missing",
                "20140611_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.missing",
                "20140621_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.missing",
                "20140701_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140711_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140721_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                # Here 3 holes
                "20140901_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140911_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140921_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141001_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141011_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141021_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141111_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141121_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141201_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141211_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20141221_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                ]

    def test_class(self):
        self.assertIsInstance(Dataset(**self.kwargs), Dataset)

    def test_class_no_product(self):
        kwargs = {'product_code':"---prod---", 'sub_product_code': "---subprod---", 'mapset': '---mapset---'}
        self.assertRaisesRegexp(NoProductFound, "(?i).*found.*product.*", Dataset, **kwargs)

    def test_wrong_date(self):
        kwargs = self.kwargs.copy()
        kwargs.update({'from_date': '2014-10-01'})
        self.assertRaisesRegexp(WrongDateType, "(?i).*wrong.*date.*type.*",
                Dataset, **kwargs)

    def test_intervals(self):
        kwargs = self.kwargs.copy()
        kwargs.update({'to_date': datetime.date(2014, 12, 31)})
        dataset = Dataset(**kwargs)
        dataset.get_filenames = lambda: self.files_dekad
        intervals = dataset.intervals
        self.assertEquals(len(intervals), 5)
        self.assertEquals(intervals[0].interval_type, INTERVAL_TYPE.PRESENT)
        self.assertEquals(intervals[1].interval_type, INTERVAL_TYPE.PERMANENT_MISSING)
        self.assertEquals(intervals[2].interval_type, INTERVAL_TYPE.PRESENT)
        self.assertEquals(intervals[3].interval_type, INTERVAL_TYPE.MISSING)
        self.assertEquals(intervals[4].interval_type, INTERVAL_TYPE.PRESENT)


    def test_number_files(self):
        kwargs = self.kwargs.copy()
        kwargs.update({'to_date': datetime.date(2014, 12, 31)})
        dataset = Dataset(**kwargs)
        dataset.get_filenames = lambda: self.files_dekad
        number = dataset.get_number_files()
        self.assertEquals(number, number)

    def test_normalized_info(self):
        kwargs = self.kwargs.copy()
        kwargs.update({'to_date': datetime.date(2014, 2, 1)})
        files_dekad = [
                "20140101_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                "20140111_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif",
                # Here 1 hole
                "20140201_FEWSNET_RFE_RFE_FEWSNET_Africa_8km.tif"
                ]
        dataset = Dataset(**kwargs)
        dataset.get_filenames = lambda: files_dekad
        segments = dataset.get_dataset_normalized_info()

        total = 0
        for segment in segments:
            total += segment['intervalpercentage']
        self.assertEquals(int(total), 100)
        self.assertEquals(segments[0]['intervalpercentage'], 50.0)
        self.assertEquals(segments[1]['intervalpercentage'], 25.0)
        self.assertEquals(segments[2]['intervalpercentage'], 25.0)

    def test_normalized_info2(self):
        ingestions = querydb.get_ingestions(echo=False)

        completeness2 = {
            'completeness': {
                'firstdate': '2010-01-01',
                'lastdate': '2014-12-21',
                'totfiles': 312,
                'missingfiles': 4,
                'intervals': [{
                    'fromdate': '2010-01-01',
                    'todate': '2013-05-21',
                    'intervaltype': 'present',
                    'intervalpercentage': 20
                }, {
                    'fromdate': '2013-06-01',
                    'todate': '2013-06-21',
                    'intervaltype': 'missing',
                    'intervalpercentage': 1
                }, {
                    'fromdate': '2014-07-01',
                    'todate': '2014-07-21',
                    'intervaltype': 'present',
                    'intervalpercentage': 35
                }, {
                    'fromdate': '2014-08-01',
                    'todate': '2014-08-21',
                    'intervaltype': 'permanent-missing',
                    'intervalpercentage': 2
                }, {
                    'fromdate': '2014-09-01',
                    'todate': '2014-12-21',
                    'intervaltype': 'present',
                    'intervalpercentage': 32
                }, {
                    'fromdate': '2014-09-01',
                    'todate': '2014-12-21',
                    'intervaltype': 'missing',
                    'intervalpercentage': 1
                }, {
                    'fromdate': '2014-09-01',
                    'todate': '2014-12-21',
                    'intervaltype': 'present',
                    'intervalpercentage': 9
                }]
            }
        }

        if ingestions.__len__() > 0:
            ingest_dict_all = []
            for row in ingestions:
                kwargs = {'product_code': row.productcode,
                          'sub_product_code': row.subproductcode,
                          'version': row.version,
                          'mapset': row.mapsetcode}
                print kwargs
                #kwargs.update({'to_date': datetime.date(2013, 12, 31)})
                dataset = Dataset(**kwargs)
                completeness = dataset.get_dataset_normalized_info()
                print completeness
                ingest_dict = functions.row2dict(row)
                ingest_dict['completeness'] = completeness
                ingest_dict_all.append(ingest_dict)

            #print ingest_dict_all

            #ingestions_json = tojson(ingestions)
            ingestions_json = json.dumps(ingest_dict_all,
                                         ensure_ascii=False,
                                         sort_keys=True,
                                         indent=4,
                                         separators=(', ', ': '))
            ingestions_json = '{"success":true, "total":'+str(ingestions.__len__())+',"ingestions":'+ingestions_json+'}'
        else:
            ingestions_json = '{"success":false, "error":"No ingestions defined!"}'

        print ingestions_json
