# -*- coding: utf-8 -*-
#
#	purpose: Product functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 27.10.2014

from __future__ import absolute_import

import datetime
import os
import glob

import locals
from lib.python import es_logging as log
from lib.python import functions
from database import querydb

from .exceptions import (WrongFrequencyValue, WrongFrequencyUnit,
                         WrongFrequencyType, WrongFrequencyDateFormat,
                         NoProductFound, NoFrequencyFound,
                         WrongDateType)
from .datasets import Dataset

logger = log.my_logger(__name__)

class Product(object):
    def __init__(self, product_code, version=None):
        self.product_code = product_code
        kwargs = {'productcode': self.product_code}
        self.version=version
        if not version is None:
            kwargs['version'] = version
        self._db_product = querydb.get_product_native(**kwargs)
        if self._db_product is None:
            raise NoProductFound(kwargs)
        self._fullpath = os.path.join(locals.es2globals['data_dir'], product_code)

    @property
    def mapsets(self):
        _mapsets = getattr(self, "_mapsets", None)
        if _mapsets is None:
            _mapsets = [os.path.basename(mapset) for mapset in self._get_full_mapsets()]
            setattr(self, "_mapsets", _mapsets)
        return _mapsets

    def _get_full_mapsets(self):
        return glob.glob(os.path.join(self._fullpath, "*"))

    @property
    def subproducts(self):
        _subproducts = getattr(self, "_subproducts", None)
        if _subproducts is None:
            _subproducts = [subproduct for subproduct in 
                    set(os.path.basename(subproduct) for subproduct in self._get_full_subproducts())]
        return _subproducts

    def _get_full_subproducts(self, mapset="*"):
        return tuple(subproduct for subproduct_type in functions.dict_subprod_type_2_dir.values()
                                for subproduct in glob.glob(os.path.join(self._fullpath, mapset, subproduct_type)))

    def get_dataset(self, mapset, sub_product_code):
        return Dataset(self.product_code, sub_product_code=sub_product_code, mapset=mapset, version=self.version)

    def get_subproducts(self, mapset):
        return [subproduct for subproduct in 
                    set(os.path.basename(subproduct) for subproduct in self._get_full_subproducts(mapset=mapset))]
