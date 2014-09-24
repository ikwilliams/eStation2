__author__ = "Jurriaan van 't Klooster"

import sys

# Import eStation lib modules
import locals
from lib.python import es_logging as log
from config import es_constants

import sqlalchemy
from sqlalchemy.orm import *

logger = log.my_logger(__name__)

class ConnectDB(object):

    @staticmethod
    def is_testing():
        # Force connecting to sqlite db
        if getattr(ConnectDB, "_testing", None) is None:
            setattr(ConnectDB, "_testing", sys.argv[0].lower().endswith('nosetests'))
        # Force through a global variable
        if locals.es2globals['db_test_mode'] is not None:
            if locals.es2globals['db_test_mode'] is True:
                setattr(ConnectDB, "_testing", 1)

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
                es_constants.dbglobals['schema_products'] = None
            db_url = ConnectDB._db_url
        else:
            db_url = "postgresql://%s:%s@%s/%s" % (es_constants.dbglobals['dbUser'],
                                             es_constants.dbglobals['dbPass'],
                                             es_constants.dbglobals['host'],
                                             es_constants.dbglobals['dbName'])
        return db_url

    @staticmethod
    def get_db_engine():
        return sqlalchemy.create_engine(ConnectDB.get_db_url())

    # Initialize the DB
    def __init__(self, schema='products', echo=False):
        self.schema = schema or es_constants.dbglobals['schema_products']
        self.db = self.get_db_engine()

        if self.is_testing():
            self.schema = None

#        db.echo = echo
#        self.table_map = {}
        self.session = None

        #Initialize DB and create a hashmap of table name and associated ORM mapper class
#        metadata = MetaData(db, schema=self.schema)
        #retrieve database table information dynamically
#        metadata.reflect()
#        metadata.schema = None
#         for table_name in metadata.tables:
#             #create a class that inherits basetable class and maps the class to table
#             table_class = type(str(table_name), (BaseTable,), {})
#             try:
#                 mapper(table_class, Table(table_name, metadata, autoload=True))
#                 self.table_map[table_name] = table_class
#             except:
#                 #exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
#                 #print "could not map table ", table_name
#                 # Exit the script and print an error telling what happened.
#                 logger.error("CrudDB: could not map table %s!" % table_name)
#
#         #create a Session template that requires commit to be called explicit
        self.session = sessionmaker(bind=self.db, autoflush=True)
        # metadata.schema = self.schema

