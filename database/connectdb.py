__author__ = "Jurriaan van 't Klooster"

import sys
from lib.python import es_logging as log

# Import eStation lib modules
# import locals
from config import es_constants

import sqlalchemy
import sqlsoup
from sqlalchemy.orm import *

logger = log.my_logger(__name__)


######################################################################################
#   connect_db()
#   Purpose: Create a connection to the database
#   Author: Marco Clerici and Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: schema='products', usesqlsoup=True
#   Output: Return connection handler to the database
class ConnectDB(object):

    @staticmethod
    def is_testing():
        # Define _testing from a global variable
        # if _testing == True -> connect to sqlite
        #                else -> connect to postgresql

        if getattr(ConnectDB, "_testing", None) is None:
            setattr(ConnectDB, "_testing", es_constants.es2globals.get('db_test_mode' == 1)
                    or "nosetests" in sys.argv[0].lower())
        # Force through a global variable
        #if es_constants.es2globals.get('db_test_mode'):
        #    setattr(ConnectDB, "_testing", 1)
        return ConnectDB._testing

    @staticmethod
    def get_db_url():
        if ConnectDB.is_testing():
            if getattr(ConnectDB, '_db_url', None) is None:
                import sqlite3, os
                # SQL Alchemy cound not execute full sql scripts
                # so we use a regular file to import fixtures
                #CrudDB._db_url = "sqlite://"
                #con = sqlite3.connect(":memory:")
                import tempfile
                tf = tempfile.NamedTemporaryFile()
                tmp_name = tf.name
                tf.close()
                ConnectDB._db_url = "sqlite:///%s" % tmp_name
                con = sqlite3.connect(tmp_name)
                con.executescript(file(os.path.join(os.path.dirname(__file__), "fixtures", "sqlite.sql")).read())
                con.close()
                # Used in querydb
                es_constants.es2globals['schema_products'] = None
            db_url = ConnectDB._db_url
        else:
            db_url = "postgresql://%s:%s@%s/%s" % (es_constants.es2globals['dbuser'],
                                                   es_constants.es2globals['dbpass'],
                                                   es_constants.es2globals['host'],
                                                   es_constants.es2globals['dbname'])
            logger.debug("Connect string: %s " % db_url)

        return db_url

    @staticmethod
    def get_db_engine():
        return sqlalchemy.create_engine(ConnectDB.get_db_url())

    # Initialize the DB
    def __init__(self, schema='products', usesqlsoup=True):

        try:
            self.schema = schema or es_constants.es2globals['schema_products']
            # logger.debug("Usesqlsoup is: %s " % usesqlsoup)
            if usesqlsoup:
                dburl = ConnectDB.get_db_url()
                self.db = sqlsoup.SQLSoup(dburl)
                self.session = self.db.session
            else:
                self.db = self.get_db_engine()
                Mysession = sessionmaker(bind=self.db, autoflush=True)
                self.session = Mysession()

            # logger.debug("is_testing is: %s " % self.is_testing())
            if self.is_testing():
                self.schema = None
            else:
                self.db.schema = self.schema
        except:
            exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
            #print traceback.format_exc()
            # Exit the script and print an error telling what happened.
            logger.error("Database connection failed!\n -> {}".format(exceptionvalue))
            #raise Exception("Database connection failed!\n ->%s" % exceptionvalue)

