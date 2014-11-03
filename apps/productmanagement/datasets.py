# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#
#   TODO-M.C.: improve the error handling

from __future__ import absolute_import

import datetime
import os
import glob

import locals
from lib.python import es_logging as log
from lib.python import functions
from database import querydb


logger = log.my_logger(__name__)


from .exceptions import (WrongFrequencyValue, WrongFrequencyUnit,
                         WrongFrequencyType, WrongFrequencyDateFormat,
                         NoProductFound, NoFrequencyFound,
                         WrongDateType)
from .helpers import add_years, add_months, add_dekads, add_pentads, add_days, find_gaps, cast_to_int, INTERVAL_TYPE


def _check_constant(class_, constant_name, value):
    for k, v in getattr(getattr(class_, constant_name, None),
            '__dict__', {}).items():
        if k.isupper() and v == value:
            return True
    return False

class Frequency(object):
    class UNIT:
        YEAR = 'year'
        MONTH = 'month'
        DEKAD = 'dekad'
        DAYS8 = '8days'
        DAYS16 = '16days'
        PENTAD = 'pentad'
        DAY = 'day'
        HOUR = 'hour'
        MINUTE = 'minute'

    class TYPE:
        PER = 'p'
        EVERY = 'e'

    class DATEFORMAT:
        DATETIME = 'YYYYMMDDHHMM'
        DATE = 'YYYYMMDD'
        MONTHDAY = 'MMDD'

    @classmethod
    def dateformat_default(class_, unit):
        if unit in (class_.UNIT.HOUR, class_.UNIT.MINUTE,):
            return class_.DATEFORMAT.DATETIME
        return class_.DATEFORMAT.DATE

    def today(self):
        if Frequency.dateformat_default(self.unit) == self.DATEFORMAT.DATETIME:
            return datetime.datetime.today()
        return datetime.date.today()

    def filename_mask_ok(self, filename):
        if len(filename) > len(self.dateformat) + 1:
            if filename[:len(self.dateformat)].isdigit():
                return filename[len(self.dateformat)] == "_"
        return False

    def format_date(self, date):
        if self.dateformat == self.DATEFORMAT.DATE:
            return date.strftime("%Y%m%d")
        elif self.dateformat == self.DATEFORMAT.MONTHDAY:
            return date.strftime("%m%d")
        elif self.dateformat == self.DATEFORMAT.DATETIME:
            return date.strftime("%Y%m%d%H%M")
        else:
            raise Exception("Dateformat not managed: %s" % self.dateformat)

    def get_next_date(self, date, unit, value):
        if unit == self.UNIT.YEAR:
            return add_years(date, value)
        elif unit == self.UNIT.MONTH:
            return add_months(date, value)
        elif unit == self.UNIT.DAYS8:
            return add_days(date, value, 8)
        elif unit == self.UNIT.DAYS16:
            return add_days(date, value, 16)
        elif unit == self.UNIT.DEKAD:
            return add_dekads(date, value)
        elif unit == self.UNIT.PENTAD:
            return add_pentads(date, value)
        elif unit == self.UNIT.DAY:
            return date + datetime.timedelta(days=value)
        elif unit == self.UNIT.HOUR:
            return date + datetime.timedelta(hours=value)
        elif unit == self.UNIT.MINUTE:
            return date + datetime.timedelta(minutes=value)
        else:
            logger.error("Unit not managed: %s" % unit)
            #raise Exception("Unit not managed: %s" % unit)

    def get_mapset(self, filename):
        return filename[len(self.dateformat):]

    def format_filename(self, date, mapset):
        return self.format_date(date) + mapset

    def check_date(self, date_datetime):
        if type(date_datetime) is datetime.datetime and (
                self.dateformat in (self.DATEFORMAT.DATE, self.DATEFORMAT.MONTHDAY)):
            return False
        if type(date_datetime) is datetime.date and self.dateformat == self.DATEFORMAT.DATETIME:
            return False
        return True

    def extract_date(self, filename):
        if self.dateformat == self.DATEFORMAT.MONTHDAY:
            date_parts = (datetime.date.today().year, int(filename[:2]), int(filename[2:4]))
            date = datetime.date(*date_parts)
            print date
        else:
            date_parts = (int(filename[:4]), int(filename[4:6]), int(filename[6:8]))
            if self.dateformat == self.DATEFORMAT.DATE:
                date = datetime.date(*date_parts)
            else:
                date_parts += (int(filename[8:10]), int(filename[10:12]))
                date = datetime.datetime(*date_parts)
        return date

    def next_date(self, date):
        if self.frequency_type == self.TYPE.EVERY or self.value == 1:
            date = self.get_next_date(date, self.unit, self.value)
        elif self.frequency_type == self.TYPE.PER:
            new_date = self.get_next_date(date, self.unit, 1)
            date = date + (new_date - date)/self.value
        else:
            raise Exception("Dateformat not managed: %s" % self.dateformat)
        return date

    def count_dates(self, fromdate, todate):
        date = self.next_date(fromdate)
        count = 1
        while date <= todate:
            date = self.next_date(date)
            count += 1
        return count

    def next_filename(self, filename):
        date = self.next_date(self.extract_date(filename))
        return self.format_filename(date, self.get_mapset(filename))

    def __init__(self, value, unit, frequency_type, dateformat=None):
        value = cast_to_int(value)
        unit = unit.lower()
        frequency_type = frequency_type.lower()
        if dateformat:
            dateformat = dateformat.upper()
        if not isinstance(value, int):
            raise WrongFrequencyValue(value)
        if not _check_constant(self, 'UNIT', unit):
            raise WrongFrequencyUnit(unit)
        if not _check_constant(self, 'TYPE', frequency_type):
            raise WrongFrequencyType(frequency_type)
        if dateformat and not _check_constant(self, 'DATEFORMAT', dateformat):
            raise WrongFrequencyDateFormat(dateformat)
        self.value = value
        self.unit = unit
        self.frequency_type = frequency_type
        self.dateformat = dateformat or self.dateformat_default(unit)


class Interval(object):
    def __init__(self, interval_type, from_date, to_date, length, percentage):
        self.interval_type = interval_type
        self.from_date = from_date
        self.to_date = to_date
        self.length = length
        self.percentage = percentage

    @property
    def missing(self):
        return self.interval_type == INTERVAL_TYPE.MISSING

class Dataset(object):
    def _check_date(self, date):
        if not isinstance(date, datetime.date):
            raise WrongDateType(date, datetime.date)

    def __init__(self, product_code, sub_product_code, mapset, version=None, from_date=None, to_date=None):
        kwargs = {'productcode': product_code, 'subproductcode': sub_product_code}
        if not version is None:
            kwargs['version'] = version
        if from_date:
            self._check_date(from_date)
        if to_date:
            self._check_date(to_date)
        self._db_product = querydb.get_product_out_info(**kwargs)
        if self._db_product is None or self._db_product == []:
            raise NoProductFound(kwargs)
        if isinstance(self._db_product, list):
            self._db_product = self._db_product[0]
        self._path = functions.set_path_sub_directory(product_code, sub_product_code,
                self._db_product.product_type, version, mapset)
        self._fullpath = os.path.join(locals.es2globals['data_dir'], self._path)
        self._fullpath = os.path.join(locals.es2globals['data_dir'], self._path)
        self._db_frequency = querydb.db.frequency.get(self._db_product.frequency_id)
        if self._db_frequency is None:
            raise NoFrequencyFound(self._db_product)
        self._frequency = Frequency(value=self._db_frequency.frequency,
                                    unit=self._db_frequency.time_unit,
                                    frequency_type=self._db_frequency.frequency_type,
                                    dateformat=self._db_product.date_format)
        self.from_date = from_date or None
        self.to_date = to_date or self._frequency.today()

    def get_filenames(self):
        return glob.glob(os.path.join(self._fullpath, "*"))

    def get_number_files(self):
        return len(self.get_filenames())

    def get_basenames(self):
        return list(os.path.basename(filename) for filename in self.get_filenames())

    def find_intervals(self, from_date=None, to_date=None, only_intervals=True):
        return find_gaps(self.get_basenames(), self._frequency, only_intervals, from_date=from_date or self.from_date, to_date=to_date or self.to_date)

    def find_gaps(self, from_date=None, to_date=None):
        return find_gaps(self.get_basenames(), self._frequency, only_intervals=False, from_date=from_date or self.from_date, to_date=to_date or self.to_date)

    def _extract_kwargs(self, interval):
        return {
            "from_date": interval[0],
            "to_date": interval[1],
            "interval_type": interval[2],
            "length": interval[3],
            "percentage": interval[4],
        }

    def get_dataset_normalized_info(self, from_date=None, to_date=None):
        interval_list = list({'totfiles': interval.length,
                     'fromdate': interval.from_date.strftime("%Y-%m-%d"),
                     'todate': interval.to_date.strftime("%Y-%m-%d"),
                     'intervaltype': interval.interval_type,
                     'missing': interval.missing,
                     'intervalpercentage': interval.percentage} for interval in self.intervals)

        return {
                'firstdate': interval_list[0]['fromdate'] if interval_list else '',
                'lastdate': interval_list[-1]['todate'] if interval_list else '',
                'totfiles': sum(i['totfiles'] for i in interval_list),
                'missingfiles': sum(i['totfiles'] for i in interval_list if i['missing']),
                'intervals': interval_list
        }

    @property
    def intervals(self):
        _intervals = getattr(self, "_intervals", None)
        if _intervals is None:
            _intervals = [Interval(**self._extract_kwargs(interval)) for interval in self.find_intervals()]
            setattr(self, "_intervals", _intervals)
        return _intervals
