__author__ = "Jurriaan van 't Klooster"

import sys
# Import eStation lib modules
from lib.python import es_logging as log
from config.es_constants import *


from sqlalchemy import *
from sqlalchemy.orm import *

logger = log.my_logger(__name__)

class CrudDB(object):
    @staticmethod
    def is_testing():
        if getattr(CrudDB, "_testing", None) is None:
            setattr(CrudDB, "_testing", sys.argv[0].endswith('nosetests'))
        return CrudDB._testing

    @staticmethod
    def get_db_url():
        if CrudDB.is_testing():
            if getattr(CrudDB, '_db_url', None) is None:
                import sqlite3, os
                # SQL Alchemy cound not execute full sql scripts
                # so we use a regular file to import fixtures
                #CrudDB._db_url = "sqlite://"
                #con = sqlite3.connect(":memory:")
                import tempfile
                tf = tempfile.NamedTemporaryFile()
                tmp_name = tf.name
                tf.close()
                CrudDB._db_url = "sqlite:///%s" % tmp_name
                con = sqlite3.connect(tmp_name)
                con.executescript(file(os.path.join(os.path.dirname(__file__), "fixtures", "sqlite.sql")).read())
                con.close()
                dbglobals['schema_products'] = None
            db_url = CrudDB._db_url
        else:
            db_url = "postgresql://%s:%s@%s/%s" % (dbglobals['dbUser'],
                                             dbglobals['dbPass'],
                                             dbglobals['host'],
                                             dbglobals['dbName'])
        return db_url

    @staticmethod
    def get_db_engine():
        return create_engine(CrudDB.get_db_url())

    # Initialize the DB
    def __init__(self, schema='products', echo=False):

        if schema == '':
            schema = dbglobals['schema_products']

        db = CrudDB.create_engine()
        self.schema = schema
        db.echo = echo
        self.table_map = {}
        self.session = None

        # new session
        #self.Session = Session()
        # set the search path
        #db.execute("SET search_path TO products")

        #Initialize DB and create a hashmap of table name and associated ORM mapper class
        metadata = MetaData(db, schema=self.schema)
        #retrieve database table information dynamically
        metadata.reflect()
        metadata.schema = None
        for table_name in metadata.tables:
            #create a class that inherits basetable class and maps the class to table
            table_class = type(str(table_name), (BaseTable,), {})
            try:
                mapper(table_class, Table(table_name, metadata, autoload=True))
                self.table_map[table_name] = table_class
            except:
                #exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
                #print "could not map table ", table_name
                # Exit the script and print an error telling what happened.
                logger.error("CrudDB: could not map table %s!" % table_name)

        #create a Session template that requires commit to be called explicit
        self.session = sessionmaker(bind=db, autoflush=True)
        metadata.schema = self.schema

    #create a record
    def create(self, table_name, record):
        session = None
        status = False
        try:
            #lookup the corresponding table class and create an instance
            table_instance = self.table_map[table_name]()
            table_instance.pack(record)
            session = self.session()
            session.add(table_instance)
            session.commit()
            status = True
            return status
        except:
            exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
            # Exit the script and print an error telling what happened.
            logger.error("CrudDB: create record error in table {}!\n {}".format(table_name, exceptionvalue))
        finally:
            if session:
                session.close()
            return status

    #fetch all the records from table that have conditions specified
    def read(self, table_name, **keywords):
        session = None
        records = []
        try:
            table_class = self.table_map[table_name]
            session = self.session()
            query = session.query(table_class)
            resultset = query.filter_by(**keywords).all()
            for record in resultset:
                records.append(record.unpack())

            return records
        except:
            exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
            # Exit the script and print an error telling what happened.
            logger.error("CrudDB: error read records of table {}!\n {}".format(table_name, exceptionvalue))
        finally:
            if session:
                session.close()
            return records

    #update a record
    def update(self, table_name, record):
        session = None
        status = False
        try:
            #lookup the corresponding table class and create an instance
            table_instance = self.table_map[table_name]()
            table_instance.pack(record)
            session = self.session()
            session.merge(table_instance)
            session.commit()
            status = True
            return status
        except:
            exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
            #print traceback.format_exc()
            # Exit the script and print an error telling what happened.
            logger.error("CrudDB: update record error in table {}!\n {}".format(table_name, exceptionvalue))
        finally:
            if session:
                session.close()
            return status

    #delete a record
    def delete(self, table_name, **keywords):
        session = None
        status = False
        try:
            #lookup the corresponding table class and create an instance
            table_class = self.table_map[table_name]
            session = self.session()
            session.query(table_class).filter_by(**keywords).delete()

            session.commit()
            status = True
            return status
        except:
            exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
            #print traceback.format_exc()
            # Exit the script and print an error telling what happened.
            logger.error("CrudDB: delete record error in table {}!\n {}".format(table_name, exceptionvalue))
        finally:
            if session:
                session.close()
            return status


class BaseTable(object):
    #map the record dictionary to table instance variables
    def pack(self, record):
        for column in record:
            self.__dict__[column] = record[column]

    #return the dictionary representation of the table instance
    def unpack(self):
        record = {}
        for name in self.__dict__:
            if name[0] == "_":
                continue  # exclude non column keys
            value = self.__dict__[name]
            #if value is None: continue #exclude null values
            try:
                record[name] = unicode(value)
            except:
                record[name] = repr(value)
        return record

    #string representation of the record
    def __str__(self):
        return self.unpack()

