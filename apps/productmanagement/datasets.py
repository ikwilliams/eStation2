# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import

import locals

from .exceptions import (WrongFrequencyValue, WrongFrequencyUnit, WrongFrequencyType)

class Frequency(object):
    class UNIT:
        MONTH = 'month'
        DEKAD = 'dekad'
        DAY = 'day'
        HOUR = 'hour'

    class TYPE:
        PER = 'p'
        EVERY = 'e'

    @classmethod
    def _check_constant(class_, constant_name, value):
        for k, v in getattr(getattr(class_, constant_name, None),
                '__dict__', {}).items():
            if k.isupper() and v == value:
                return True
        return False

    @classmethod
    def dateformat_default(class_, unit):
        if unit in (class_.UNIT.DEKAD, class_.UNIT.MONTH):
            return 'YYYYMMDD'

    def __init__(self, value, unit, type_, dateformat=None):
        if not isinstance(value, int):
            raise WrongFrequencyValue(value)
        if not self._check_constant('UNIT', unit):
            raise WrongFrequencyUnit(unit)
        if not self._check_constant('TYPE', type_):
            raise WrongFrequencyType(type_)
        self.value = value
        self.unit = unit
        self.type_ = type_
        self.dateformat = dateformat or self.dateformat_default(unit)


class Dataset(object):

    def __init__(self, product, subproduct):
        self.product = product
        self.subproduct = subproduct
        self._path = None


