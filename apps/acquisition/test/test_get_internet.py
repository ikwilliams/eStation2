
from apps.acquisition.get_internet import *
from apps.acquisition.get_eumetcast import *

import unittest

class TestGetInternet(unittest.TestCase):

    def TestGetInfo(self):

        eum_id = 'EO:EUM:DAT:MSG:LST-SEVIRI'
        info = get_eumetcast_info(eum_id)

    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (e.g. MODIS)
    #   ---------------------------------------------------------------------------
    def TestRemoteFtp_MODIS_BA_monthly(self):

        # Retrieve a list of MODIS burndate file .. check only one present
        remote_url='ftp://ba1.geog.umd.edu'
        usr_pwd='user:burnt_data'
        full_regex   ='Collection51/TIFF/Win11/201./MCD45monthly.A20.*burndate.tif.gz'
        file_to_check='Collection51/TIFF/Win11/2011/MCD45monthly.A2011001.Win11.051.burndate.tif.gz'

        list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)

        self.assertTrue(file_to_check in list)

    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (e.g. NASA_FIRMS)
    #   ---------------------------------------------------------------------------
    def TestRemoteFtp_FIRMS_NASA(self):

        # Retrieve a list of MODIS burndate file .. check only one present
        remote_url='ftp://nrt1.modaps.eosdis.nasa.gov/FIRMS/Global'
        usr_pwd='jrcMondeFires:FIRE@data1'
        full_regex   ='Global_MCD14DL_201435..txt'
        file_to_check='Global_MCD14DL_2014350.txt'

        list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)

        self.assertTrue(file_to_check in list)

    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (e.g. ARC2)
    #   ---------------------------------------------------------------------------
    def TestRemoteFtp_ARC2(self):

        # Retrieve a list of MODIS burndate file .. check only one present
        remote_url='ftp://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/geotiff/'
        usr_pwd='anonymous:@'
        full_regex   ='africa_arc.2015.....tif.zip'
        file_to_check='africa_arc.20150121.tif.zip'

        list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)

        self.assertTrue(file_to_check in list)
    
    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (e.g. CAMS_OPI)
    #   ---------------------------------------------------------------------------
    def TestRemoteFtp_CAMS_OPI(self):

        # Retrieve a list of CQMS-OPI .. check only one present
        remote_url='ftp://ftp.cpc.ncep.noaa.gov/precip/data-req/cams_opi_v0208/'
        usr_pwd='anonymous:@'
        full_regex   ='africa_arc.2015.....tif.zip'
        file_to_check='africa_arc.20150121.tif.zip'

        list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)

        self.assertTrue(file_to_check in list)


    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (e.g. VITO GL-GIO products): Obsolete ?
    #   ---------------------------------------------------------------------------
    # def TestRemoteFtp_FTP_VITO(self):
    #
    #     # Retrieve a list of MODIS burndate file .. check only one present
    #     remote_url='ftp://catftp.vgt.vito.be/'
    #     usr_pwd='estationJRC:eStation14'
    #     full_regex   ='/^[A-Za-z0-9].*/^g2_BIOPAR_.*zip$'
    #     file_to_check=''
    #
    #     list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)
    #
    #     self.assertTrue(file_to_check in list)

    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (CHIRP/CHIRPS)
    #   ---------------------------------------------------------------------------
    def TestRemoteFtp_CHIRP(self):
        # Retrieve a list of CHIRP
        remote_url='ftp://chg-ftpout.geog.ucsb.edu/pub/org/chg/products/CHIRPS-latest/africa_dekad/tifs/'
        usr_pwd='anonymous:anonymous'
        full_regex   ='chirps-v1.8.2014.12.[1-3].tif'
        file_to_check='chirps-v1.8.2014.12.1.tif'
        
        list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)
        self.assertTrue(file_to_check in list)

    #   ---------------------------------------------------------------------------
    #   Get contents of a directory (FTP)  -> MCD45A1_TIF_C51
    #   A list of the dir is returned (as form ls -l)
    #   ---------------------------------------------------------------------------
    def TestRemoteFtp_MCD45A1(self):
        filename='mcd45a1.txt'
        remote_url='ftp://ba1.geog.umd.edu/Collection5/'
        UserPwd='user:burnt_data'
        filepath = get_dir_contents_from_url(remote_url, target_file=filename, userpwd=UserPwd)
        logger.info('File downloaded to: '+filepath)
        self.assertEqual(1,1)

    #   ---------------------------------------------------------------------------
    #   Get contents of a directory (HTTP)  -> MODIS_SST_8D
    #   An html document is returned
    #   ---------------------------------------------------------------------------
    def TestRemoteHttp_MODIS_SST_8D(self):
        filename='A20100012010008.L3m_8D_SST_4.bz2'
        remote_url='http://oceandata.sci.gsfc.nasa.gov/'
        UserPwd='anonymous:anonymous'
        filepath = get_file_from_url(remote_url, target_file=filename, userpwd=UserPwd)
        logger.info('File downloaded to: '+filepath)
        self.assertEqual(1,1)


    #   ---------------------------------------------------------------------------
    #   Get a file from HTTP (list_from_template=TRUE, No User/psw) -> FEWSNET
    #   ---------------------------------------------------------------------------

    def TestHttpDir_FEWSNET(self):
        #filename=''
        remote_url='http://earlywarning.usgs.gov/ftp2/raster/rf/a/2014/'
        #UserPwd='anonymous:anonymous'
        filepath = get_dir_contents_from_url(remote_url)
        print(filepath)

        #logger.info('File downloaded to: '+filepath)
        #self.assertEqual(1,1)

    def TestRemoteHttp_FEWSNET(self):
        filename='a14081rb.zip'
        remote_url='http://earlywarning.usgs.gov/ftp2/raster/rf/a/2014/'
        # filepath = get_file_from_url(remote_url+filename, target_file=filename)
        filepath = get_file_from_url(remote_url, target_file=filename)
        print(filepath)
        logger.info('File downloaded to: '+filepath)
        self.assertEqual(1,1)

 