# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from lib.python import es_logging as log
# Trivial change
logger = log.my_logger(__name__)

__author__ = "Jurriaan van 't Klooster"

from database import querydb


class TestQuerydb(TestCase):

    def Test_get_active_internet_sources(self):

        internet_sources = querydb.get_active_internet_sources()
        logger.info("Internet sources are: %s", internet_sources)
        for internet_source in internet_sources:
            print internet_source.url

        self.assertEqual(1,1)
