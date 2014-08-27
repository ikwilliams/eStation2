# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import
import datetime
import os
import glob

from lib.python import functions
from database import querydb
import locals

from .exceptions import (WrongFrequencyValue, WrongFrequencyUnit,
        WrongFrequencyType, WrongFrequencyDateFormat,
        NoProductFound, NoFrequencyFound )
from .helpers import add_years, add_months, add_dekads, add_pentads, add_days, find_gaps, cast_to_int


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

    class TYPE:
        PER = 'p'
        EVERY = 'e'

    class DATEFORMAT:
        DATETIME = 'YYYYMMDDHHMM'
        DATE = 'YYYYMMDD'

    @classmethod
    def _check_constant(class_, constant_name, value):
        for k, v in getattr(getattr(class_, constant_name, None),
                '__dict__', {}).items():
            if k.isupper() and v == value:
                return True
        return False

    @classmethod
    def dateformat_default(class_, unit):
        if unit in (class_.UNIT.HOUR,):
            return class_.DATEFORMAT.DATETIME
        return class_.DATEFORMAT.DATE

    def filename_mask_ok(self, filename):
        if len(filename) > len(self.dateformat) + 1:
            if filename[:len(self.dateformat)].isdigit():
                return filename[len(self.dateformat)] == "_"
        return False

    def format_date(self, date):
        if self.dateformat == self.DATEFORMAT.DATE:
            return date.strftime("%Y%m%d")
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
        else:
            raise Exception("Unit not managed: %s" % unit)

    def get_mapset(self, filename):
        return filename[len(self.dateformat):]

    def format_filename(self, date, mapset):
        return self.format_date(date) + mapset

    def check_date(self, date_datetime):
        if type(date_datetime) is datetime.datetime and self.dateformat == self.DATEFORMAT.DATE:
            return False
        if type(date_datetime) is datetime.date and self.dateformat == self.DATEFORMAT.DATETIME:
            return False
        return True

    def next_filename(self, filename):
        date_parts = (int(filename[:4]), int(filename[4:6]), int(filename[6:8]))
        if self.dateformat == self.DATEFORMAT.DATE:
            date = datetime.date(*date_parts)
        else:
            date_parts += (int(filename[8:10]), int(filename[10:12]))
            date = datetime.datetime(*date_parts)
        if self.type_ == self.TYPE.EVERY or self.value == 1:
            date = self.get_next_date(date, self.unit, self.value)
        elif self.type_ == self.TYPE.PER:
            new_date = self.get_next_date(date, self.unit, 1)
            date = date + (new_date - date)/self.value
        else:
            raise Exception("Dateformat not managed: %s" % self.dateformat)
        return self.format_filename(date, self.get_mapset(filename))

    def __init__(self, value, unit, type_, dateformat=None):
        value = cast_to_int(value)
        unit = unit.lower()
        type_ = type_.lower()
        if dateformat:
            dateformat = dateformat.upper()
        if not isinstance(value, int):
            raise WrongFrequencyValue(value)
        if not self._check_constant('UNIT', unit):
            raise WrongFrequencyUnit(unit)
        if not self._check_constant('TYPE', type_):
            raise WrongFrequencyType(type_)
        if dateformat and not self._check_constant('DATEFORMAT', dateformat):
            raise WrongFrequencyDateFormat(dateformat)
        self.value = value
        self.unit = unit
        self.type_ = type_
        self.dateformat = dateformat or self.dateformat_default(unit)


class Dataset(object):
    def __init__(self, product_code, sub_product_code, mapset, version=None):
        kwargs = {'productcode':product_code, 'subproductcode':sub_product_code}
        if not version is None:
            kwargs['version'] = version
        self._db_product = querydb.get_product_out_info(**kwargs)
        if self._db_product is None:
            raise NoProductFound(kwargs)
        self._path = functions.set_path_sub_directory(product_code, sub_product_code,
                self._db_product.product_type, version, mapset)
        self._fullpath = os.path.join(locals.es2globals['data_dir'], self._path)
        self._db_frequency = querydb.db.frequency.get(self._db_product.frequency_id)
        if self._db_frequency is None:
            raise NoFrequencyFound(self._db_product)
        self._frequency = Frequency(value=self._db_frequency.frequency, 
                                    unit=self._db_frequency.time_unit, 
                                    type_=self._db_frequency.frequency_type)


    def get_filenames(self):
        return glob.glob(os.path.join(self._fullpath, "*"))

    def get_basenames(self):
        return list(os.path.basename(filename) for filename in self.get_filenames())

    def find_intervals(self, from_date=None, to_date=None):
       return find_gaps(self.get_basenames(), self._frequency, only_intervals=True, from_date=from_date, to_date=to_date)

    def find_gaps(self, from_date=None, to_date=None):
       return find_gaps(self.get_basenames(), self._frequency, only_intervals=False, from_date=from_date, to_date=to_date)
