####################################################################################################################
#	purpose: Define functions to access and query the postgresql db
#	author:  Jurriaan van 't Klooster
#	date:	 20.03.2014
#   descr:	 Functions to access and query the DB using SQLSoup and SQLAlchemy as Database Abstraction Layer and ORM.
####################################################################################################################

import locals
import sys
import traceback
import sqlsoup
#from sqlsoup import Session
from sqlalchemy.sql import or_, and_, desc, asc
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from lib.python import es_logging as log
from config.es_constants import *
from crud import CrudDB

logger = log.my_logger(__name__)

# TODO: Working with SQLAlchemy Sessions?


######################################################################################
#   connect_db()
#   Purpose: Create a connection to the database
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: None
#   Output: Return connection handler to the database
def connect_db():

    try:
        sqlsoup_dns = CrudDB.get_db_url()

        dbconn = sqlsoup.SQLSoup(sqlsoup_dns)
        dbconn.schema = dbglobals['schema_products']
        return dbconn
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        #print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("Database connection failed!\n -> {}".format(exceptionvalue))
        #raise Exception("Database connection failed!\n ->%s" % exceptionvalue)

db = connect_db()


######################################################################################
#   get_product_out_info(allrecs=False, echo=False, productcode='', subproductcode='', version='undefined')
#   Purpose: Query the database to get the records of all or a specific product from the table product
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#          productcode      - The productcode of the specific product info requested.
#                             If given also subproductcode and version have to be given. Default=''
#          subproductcode   - The subproductcode of the specific product info requested. Default=''
#          version          - The version of the specific product info requested. Default='undefined'
#   Output: Return the fields of all or a specific product record from the table product.
def get_product_out_info(allrecs=False, echo=False, productcode='', subproductcode='', version='undefined'):
    try:
        if allrecs:
            product_out_info = db.product.order_by(asc(db.product.productcode)).all()
            if echo:
                for row in product_out_info:
                    print row
        else:
            where = and_(db.product.productcode == productcode,
                         db.product.subproductcode == subproductcode,
                         db.product.version == version)
            product_out_info = db.product.filter(where).one()
            if echo:
                print product_out_info
        return product_out_info
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_product_out_info: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_product_out_info: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_product_in_info(allrecs=False, echo=False, productcode='', subproductcode='',
#                       version='undefined', datasource_descr_id='')
#   Purpose: Query the database to get the fields scale_factor, scale_offset, no_data, mask_min,
#            mask_max and data_type_id of all or a specific product datasource from the table sub_datasource_description
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: allrecs              - If True return all products. Default=False
#          echo                 - If True echo the query result in the console for debugging purposes. Default=False
#          productcode          - The productcode of the specific product datasource info requested.
#                                 If given also subproductcode, version and datasource_descr_id have to be given.
#                                 Default=''
#          subproductcode       - The subproductcode of the specific product info requested. Default=''
#          version              - The version of the specific product info requested. Default='undefined'
#          datasource_descr_id  - The version of the specific product info requested. Default='undefined'
#   Output: Return the fields of all [or a specific product record} from the sub_datasource_description table.
def get_product_in_info(allrecs=False, echo=False,
                        productcode='', subproductcode='',
                        version='undefined', datasource_descr_id=''):
    try:
        if allrecs:
            product_in_info = db.sub_datasource_description.order_by(asc(db.sub_datasource_description.productcode)).all()
            if echo:
                for row in product_in_info:
                    print row
        else:
            where = and_(db.sub_datasource_description.productcode == productcode,
                         db.sub_datasource_description.subproductcode == subproductcode,
                         db.sub_datasource_description.version == version,
                         db.sub_datasource_description.datasource_descr_id == datasource_descr_id)
            product_in_info = db.sub_datasource_description.filter(where).one()
            if echo:
                print product_in_info
        return product_in_info
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_product_out_info: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_product_in_info: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_product_native(pkid='', allrecs=False, echo=False)
#   Purpose: Query the database to get the records of all products or one specific product
#            with product_type='Native' from the table product.
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: productcode      - The productcode of the specific product info requested. Default=''
#          allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#   Output: Return the fields of all or a specific product record with product_type='Native' from the table product.
def get_product_native(productcode='', allrecs=False, echo=False):
    try:
        if allrecs:
            where = db.product.product_type == 'Native'
            product = db.product.filter(where).order_by(asc(db.product.productcode)).all()
            if echo:
                for row in product:
                    print row
        else:
            where = and_(db.product.productcode == productcode, db.product.product_type == 'Native')
            product = db.product.filter(where).one()
            if echo:
                print product
        return product
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_product_native: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_product_native: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_eumetcast(source_id='', allrecs=False, echo=False)
#   Purpose: Query the database to get the records of all eumetcast sources or one specific eumetcast source
#            from the table eumetcast_source.
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: source_id        - The eumetcast_id of the specific eumetcast source requested. Default=''
#          allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#   Output: Return the fields of all or a specific eumetcast source record from the table eumetcast_source.
def get_eumetcast(source_id='', allrecs=False, echo=False):
    try:
        if allrecs:
            eumetcasts = db.eumetcast_source.order_by(asc(db.eumetcast_source.eumetcast_id)).all()
            #eumetcasts.sort()
            if echo:
                for row in eumetcasts:
                    print row
        else:
            where = db.eumetcast_source.eumetcast_id == source_id
            eumetcasts = db.eumetcast_source.filter(where).one()
            if echo:
                print eumetcasts
        return eumetcasts
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        raise logger.error("get_eumetcast: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_eumetcast: Database query error!\n ->%s" % exceptionvalue)
    #finally:
        #if session:
        #    session.close()


######################################################################################
#   get_internet(internet_id='', allrecs=False, echo=False)
#   Purpose: Query the database to get the records of all internet sources or one specific internet source
#            from the table internet_source.
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: internet_id      - The internet_id of the specific internet source requested. Default=''
#          allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#   Output: Return the fields of all or a specific internet source record from the table internet_source.
def get_internet(internet_id='', allrecs=False, echo=False):
    try:
        if allrecs:
            internet = db.internet_source.order_by(asc(db.internet_source.internet_id)).all()
            if echo:
                for row in internet:
                    print row
        else:
            where = db.internet_source.internet_id == internet_id
            internet = db.internet_source.filter(where).one()
            if echo:
                print internet
        return internet
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_internet: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_internet: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_mapset(mapsetcode='', allrecs=False, echo=False)
#   Purpose: Query the database to get the records of all mapsets or one specific mapset
#            from the table mapset.
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: mapsetcode       - The mapsetcode of the specific mapset requested. Default=''
#          allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#   Output: Return the fields of all or a specific mapset record from the table mapset.
def get_mapset(mapsetcode='', allrecs=False, echo=False):
    try:
        mapset = []
        if allrecs:
            if db.mapset.order_by(asc(db.mapset.mapsetcode)).count() >= 1:
                mapset = db.mapset.order_by(asc(db.mapset.mapsetcode)).all()
                if echo:
                    for row in mapset:
                        print row
        else:
            where = db.mapset.mapsetcode == mapsetcode
            if db.mapset.filter(where).count() == 1:
                mapset = db.mapset.filter(where).one()
                if echo:
                    print mapset
        return mapset
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        raise logger.error("get_mapset: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_mapset: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_ingestion_product(allrecs=False, echo=False, productcode_in='', version_in='')
#   Purpose: Query the database to get the COUNT of all product ingestion definitions or one specific
#            product ingestion definition at product level from the table ingestion.
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#          productcode      - The productcode of the specific product ingestion definition requested. Default=''
#          version          - The version of the specific product ingestion definition requested. Default='undefined'
#   Output: Return the productcode, version and count() of subproducts of all [or a specific product ingestion definition] from the table
#           ingestion.
def get_ingestion_product(allrecs=False, echo=False, productcode='', version='undefined'):
    try:
        session = db.session
        ingest = aliased(db.ingestion)

        # Get all defined ingestion definitions with the amount of subproducts per product/version (count).
        ingestion_product = session.query(ingest.productcode,
                                          ingest.version,
                                          func.count(ingest.subproductcode), ). \
            group_by(ingest.productcode, ingest.version)

        active_ingestions = []
        if allrecs:
            ingestion_product = ingestion_product.filter(ingest.activated == True)

            if ingestion_product.count() >= 1:      # At least 1 product ingestion definition has to exist.
                active_ingestions = ingestion_product.all()
                if echo:
                    for row in active_ingestions:
                        print row
        else:
            where = and_(ingest.productcode == productcode,
                         ingest.activated == True,
                         ingest.version == version)
            if ingestion_product.filter(where).count() == 1:    # Exactly 1 product ingestion definition has to exist.
                active_ingestions = ingestion_product.filter(where).one()
                if echo:
                    print active_ingestions
        return active_ingestions
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_ingestion_product: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_ingestion_product: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_ingestion_subproduct(allrecs=False, echo=False, productcode='', version='')
#   Purpose: Query the database to get the records of all product ingestion definitions or one specific
#            product ingestion definition  at subproduct level (not product level) from the table ingestion.
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#          productcode      - The productcode of the specific product ingestion definition requested. Default=''
#          version          - The version of the specific product ingestion definition requested. Default='undefined'
#   Output: Return all relevant fields of all [or a specific ingestion definition record] from the table ingestion.
def get_ingestion_subproduct(allrecs=False, echo=False, productcode='', version=''):
    try:
        ingestion = []
        if allrecs:
            if db.ingestion.filter(db.ingestion.activated == True).count() >= 1:
                ingestion = db.ingestion.filter(db.ingestion.activated == True).\
                    order_by(asc(db.ingestion.productcode)).all()
                if echo:
                    for row in ingestion:
                        print row
        else:
            where = and_(db.ingestion.productcode == productcode,
                         db.ingestion.activated,
                         #db.ingestion.subproductcode == subproductcode,
                         db.ingestion.version == version)
            if db.ingestion.filter(where).count() >= 1:
                ingestion = db.ingestion.filter(where).all()
                if echo:
                    print ingestion
        return ingestion
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_ingestion_subproduct: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_ingestion_subproduct: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_product_sources(echo=False, productcode='', subproductcode='', version='')
#   Purpose: Query the database to get all the activated data sources defined for a specific product (INTERNET
#            and EUMETCAST), from the table product_acquisition_data_source
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: echo                 - If True echo the query result in the console for debugging purposes. Default=False
#          productcode          - The productcode of the specific product datasource info requested.
#                                 If given also subproductcode, version have to be given. Default=''
#          subproductcode       - The subproductcode of the specific product info requested. Default=''
#          version              - The version of the specific product info requested. Default='undefined'
#
#   Output: Return all the activated data sources defined for a specific product
#           from the table product_acquisition_data_source.
def get_product_sources(echo=False, productcode='', subproductcode='', version=''):
    try:
        sources = []
        where = and_(db.product_acquisition_data_source.productcode == productcode,
                     db.product_acquisition_data_source.subproductcode == subproductcode,
                     db.product_acquisition_data_source.version == version)

        if db.product_acquisition_data_source.filter(where).count() >= 1:
            sources = db.product_acquisition_data_source.filter(where). \
                order_by(asc(db.product_acquisition_data_source.type)).all()
            if echo:
                for row in sources:
                    print row
        return sources
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_product_sources: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_product_sources: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_datasource_descr(echo=False, source_type='', source_id='')
#   Purpose: Query the database to get the datasource description and filter expression of a specific datasource
#            (INTERNET or EUMETCAST).
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: echo             - If True echo the query result in the console for debugging purposes. Default=False
#          source_type      - The data source type. Values: INTERNET or EUMETCAST   Default=''
#          source_id        - The eumetcast_id or internet_id of the specific data source description requested.
#                             Default=''
#
#   Output: Return the datasource description and filter expression of the requested data source.
def get_datasource_descr(echo=False, source_type='', source_id=''):
    try:
        session = db.session
        if source_type == 'EUMETCAST':
            #q = "select e.filter_expression_jrc, dd.* \
            #     from products.datasource_description dd \
            #     inner join products.eumetcast_source e \
            #     on e.datasource_descr_id = dd.datasource_descr_id \
            #     where e.eumetcast_id = '%s' " % source_id
            es = aliased(db.eumetcast_source)
            dsd = aliased(db.datasource_description)
            datasource_descr = session.query(es.filter_expression_jrc, dsd).join(dsd). \
                filter(es.eumetcast_id == source_id).all()

        else:   # source_type == 'INTERNET'
            datasource_descr = session.query(db.internet_source, db.datasource_description). \
                join(db.datasource_description). \
                filter(db.internet_source.internet_id == source_id).all()

        if echo:
            for row in datasource_descr:
                print row
        return datasource_descr
    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_datasource_descr: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_ingestion: Database query error!\n ->%s" % exceptionvalue)


######################################################################################
#   get_eumetcast_sources(echo=False)
#   Purpose: Query the database to get the filter_expression of all the active product EUMETCAST data sources.
#            Mainly used in get_eumetcast.py
#   Author: Jurriaan van 't Klooster
#   Date: 2014/05/16
#   Input: echo             - If True echo the query result in the console for debugging purposes. Default=False
#
#   Output: Return the filter_expression of all the active product EUMETCAST data sources.
def get_eumetcast_sources(echo=False):
    try:
        session = db.session

        es = session.query(db.eumetcast_source.eumetcast_id, db.eumetcast_source.filter_expression_jrc).subquery()
        pads = aliased(db.product_acquisition_data_source)

        # The columns on the subquery "es" are accessible through an attribute called "c"
        # e.g. es.c.filter_expression_jrc
        eumetcast_sources = session.query(pads, es.c.eumetcast_id, es.c.filter_expression_jrc).\
            outerjoin(es, pads.data_source_id == es.c.eumetcast_id).\
            filter(and_(pads.type == 'EUMETCAST', pads.activated == True)).all()

        if echo:
            for row in eumetcast_sources:
                print row

        return eumetcast_sources

    except:
        exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
        if echo:
            print traceback.format_exc()
        # Exit the script and print an error telling what happened.
        logger.error("get_eumetcast_sources: Database query error!\n -> {}".format(exceptionvalue))
        #raise Exception("get_ingestion: Database query error!\n ->%s" % exceptionvalue)

######################################################################################
#   get_processing_product(allrecs=False, echo=False, productcode_in='', version_in='')
#   Purpose: Query the database to get the list of all product processing definitions or one specific
#            product ingestion definition at product level from the table processing.
#   Author: Marco Clerici and Jurriaan van 't Klooster
#   Date: 2014/06/04
#   Input: allrecs          - If True return all products. Default=False
#          echo             - If True echo the query result in the console for debugging purposes. Default=False
#          productcode      - The productcode of the specific product ingestion definition requested. Default=''
#          version          - The version of the specific product ingestion definition requested. Default='undefined'
#   Output: Return the productcode, version and the list of dependency products of all [or a specific product ingestion definition]
#           from the table processing.
#   TODO-M.C.: complete the functions (Jur)
def get_processing_product(allrecs=False, echo=False, productcode='', version='undefined'):
    # try:
    #     session = db.session
    #     ingest = aliased(db.ingestion)
    #
    #     # Get all defined ingestion definitions with the amount of subproducts per product/version (count).
    #     ingestion_product = session.query(ingest.productcode,
    #                                       ingest.version,
    #                                       func.count(ingest.subproductcode), ). \
    #         group_by(ingest.productcode, ingest.version)
    #
        active_processing = []
        active_1 = {"productcode": "fewsnet_rfe",
                    "version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_product_version_1": "undefined"
                    }
        active_processing.append(active_1)
        active_2 = {"productcode": "vgt_ndvi",
                    "version": "undefined",
                    "dep_product_code_1": "vgt_ndvi",
                    "dep_product_version_1": "undefined"
                    }
        active_processing.append(active_2)
        active_3 = {"productcode": "vgt_vhi",
                    "version": "undefined",
                    "dep_product_code_1": "vgt_ndvi",
                    "dep_product_version_1": "undefined",
                    "dep_product_code_2": "fewsnet_rfe",
                    "dep_product_version_2": "undefined"
                    }
        active_processing.append(active_3)


    #     if allrecs:
    #         ingestion_product = ingestion_product.filter(ingest.activated == True)
    #
    #         if ingestion_product.count() >= 1:      # At least 1 product ingestion definition has to exist.
    #             active_ingestions = ingestion_product.all()
    #             if echo:
    #                 for row in active_ingestions:
    #                     print row
    #     else:
    #         where = and_(ingest.productcode == productcode,
    #                      ingest.activated == True,
    #                      ingest.version == version)
    #         if ingestion_product.filter(where).count() == 1:    # Exactly 1 product ingestion definition has to exist.
    #             active_ingestions = ingestion_product.filter(where).one()
    #             if echo:
    #                 print active_ingestions

        return active_processing
    # except:
    #     exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
    #     if echo:
    #         print traceback.format_exc()
    #     # Exit the script and print an error telling what happened.
    #     logger.error("get_processing_product: Database query error!\n -> {}".format(exceptionvalue))

######################################################################################
#   get_processing_product_subproducts(allrecs=False, echo=False, productcode_in='', version_in='')
#   Purpose: Query the database to get the list of all sub-product derived for a specific product.
#   Author: Marco Clerici and Jurriaan van 't Klooster
#   Date: 2014/06/04
#   Input: echo             - If True echo the query result in the console for debugging purposes. Default=False
#          productcode      - The productcode of the specific product ingestion definition requested. Default=''
#          version          - The version of the specific product ingestion definition requested. Default='undefined'
#   Output: Return the list of productcode, subproductcode, version and the list of dependency products of all subproducts
#   TODO-M.C.: complete the functions (Jur)

def get_processing_product_subproducts(False, echo=False, productcode='', version='undefined'):
    # try:
    #     session = db.session
    #     ingest = aliased(db.ingestion)
    #
    #     # Get all defined ingestion definitions with the amount of subproducts per product/version (count).
    #     ingestion_product = session.query(ingest.productcode,
    #                                       ingest.version,
    #                                       func.count(ingest.subproductcode), ). \
    #         group_by(ingest.productcode, ingest.version)
    #
        active_processing_subproducts = []

        # 10d statistics
        active_1 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10dmax",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_1)
        active_2 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10dmin",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_2)
        active_3 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10dstd",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_3)
        active_4 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10davg",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_4)
        active_5 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10dmed",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_5)

        # 10d anomalies
        active_6 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10ddiff",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe",
                    "dep_product_code_2": "fewsnet_rfe",
                    "dep_subproduct_code_2": "10davg"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_6)
        active_7 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10dperc",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe",
                    "dep_product_code_2": "fewsnet_rfe",
                    "dep_subproduct_code_2": "10davg"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_7)
        active_8 = {"product_code": "fewsnet_rfe",
                    "subproduct_code": "10dnpcum",
                    #"version": "undefined",
                    "dep_product_code_1": "fewsnet_rfe",
                    "dep_subproduct_code_1": "rfe",
                    "dep_product_code_2": "fewsnet_rfe",
                    "dep_subproduct_code_2": "10dmax",
                    "dep_product_code_3": "fewsnet_rfe",
                    "dep_subproduct_code_3": "10dmin"
                    #"dep_product_version_1": "undefined"
                    }
        active_processing_subproducts.append(active_8)


    #     if allrecs:
    #         ingestion_product = ingestion_product.filter(ingest.activated == True)
    #
    #         if ingestion_product.count() >= 1:      # At least 1 product ingestion definition has to exist.
    #             active_ingestions = ingestion_product.all()
    #             if echo:
    #                 for row in active_ingestions:
    #                     print row
    #     else:
    #         where = and_(ingest.productcode == productcode,
    #                      ingest.activated == True,
    #                      ingest.version == version)
    #         if ingestion_product.filter(where).count() == 1:    # Exactly 1 product ingestion definition has to exist.
    #             active_ingestions = ingestion_product.filter(where).one()
    #             if echo:
    #                 print active_ingestions

        return active_processing
    # except:
    #     exceptiontype, exceptionvalue, exceptiontraceback = sys.exc_info()
    #     if echo:
    #         print traceback.format_exc()
    #     # Exit the script and print an error telling what happened.
    #     logger.error("get_processing_product: Database query error!\n -> {}".format(exceptionvalue))
