# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import
import datetime

import locals

from .exceptions import (WrongFrequencyValue, WrongFrequencyUnit,
        WrongFrequencyType, WrongFrequencyDateFormat)

from .helpers import add_years, add_months, add_dekads

class Frequency(object):
    class UNIT:
        YEAR = 'year'
        MONTH = 'month'
        DEKAD = 'dekad'
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
        if unit in (class_.UNIT.DEKAD, class_.UNIT.MONTH, class_.UNIT.DAY):
            return class_.DATEFORMAT.DATE
        return class_.DATEFORMAT.DATETIME

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
        elif unit == self.UNIT.DEKAD:
            return add_dekads(date, value)
        elif unit == self.UNIT.DAY:
            return date + datetime.timedelta(days=value)
        elif unit == self.UNIT.HOUR:
            return date + datetime.timedelta(hours=value)
        else:
            raise Exception("Unit not managed: %s" % unit)

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
        return self.format_date(date) + filename[len(self.dateformat):]

    def __init__(self, value, unit, type_, dateformat=None):
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
    def __init__(self, product, subproduct):
        self.product = product
        self.subproduct = subproduct
        self._path = None


