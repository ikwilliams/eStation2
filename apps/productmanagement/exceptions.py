# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import


class WrongFrequencyValue(Exception):
    def __init__(self, value):
        super(WrongFrequencyValue, self).__init__(u"Wrong frequency value: %s" % value)


class WrongFrequencyUnit(Exception):
    def __init__(self, unit):
        super(WrongFrequencyUnit, self).__init__(u"Wrong frequency unit: %s" % unit)


class WrongFrequencyType(Exception):
    def __init__(self, type_):
        super(WrongFrequencyType, self).__init__(u"Wrong frequency type: %s" % type_)
