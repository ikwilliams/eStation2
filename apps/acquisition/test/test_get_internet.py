


from apps.acquisition.get_internet import *
import unittest


class TestGetInternet(unittest.TestCase):

    
    #   ---------------------------------------------------------------------------
    #   Test iteration on remote ftp (e.g. MODIS)
    #   ---------------------------------------------------------------------------
    def TestIterRemoteFtp(self):

        #check if the base_dir full_regex and remote_url starts with '/' and finish with '/' except full_regex
        base_dir='/Collection51/TIFF/'
        if base_dir.startswith("/"):
            base_dir=base_dir
            if base_dir.endswith("/"):
                base_dir=base_dir
            else:
                base_dir=base_dir+'/'                            
        else:
            base_dir='/'+base_dir
            if base_dir.endswith("/"):
                base_dir=base_dir
            else:
                base_dir=base_dir+'/'                            
        #full_regex='/Collection51/TIFF/Win[0-2][0-9]/20.*/MCD45monthly.A20.*burndate.tif.gz'        
        full_regex='/Collection51/TIFF/Win1[0-1]/201[1-2]/MCD45monthly.A20.*burndate.tif.gz'
        if full_regex.startswith("/"):
            full_regex=full_regex
        else:
            full_regex='/'+full_regex

        remote_url='ftp://ba1.geog.umd.edu/'
        if remote_url.endswith("/"):
            remote_url=remote_url
        else:
            remote_url=remote_url+'/'
        usr_pwd='user:burnt_data'
        list = get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex)
        logger.info('Returned list is: '+list[0])
        self.assertEqual(1,1)

    #   ---------------------------------------------------------------------------
    #   Test iteration on the filesystem
    #   ---------------------------------------------------------------------------
    def TestIterFilesystem(self):
        base_dir='/data/tmp/get_internet_tree/'
        full_regex='201./win02/file01'
        #remote_url='http://oceandata.sci.gsfc.nasa.gov/'
        #UserPwd='anonymous:anonymous'
        list = get_list_matching_files_dir_local(base_dir, full_regex)
        print 1
        #logger.info('Returned list is: '+list[0])
        self.assertEqual(1,1)

    #   ---------------------------------------------------------------------------
    #   Get contents of a directory (HTTP)  -> MODIS_SST_8D
    #   An html document is returned
    #   ---------------------------------------------------------------------------
    def TestHttpDir(self):
        filename='modis_sst_8d.txt'
        remote_url='http://oceandata.sci.gsfc.nasa.gov/'
        UserPwd='anonymous:anonymous'
        filepath = get_dir_contents_from_url(remote_url, target_file=filename, userpwd=UserPwd)

        logger.info('File downloaded to: '+filepath)
        self.assertEqual(1,1)

    #   ---------------------------------------------------------------------------
    #   Get contents of a directory (FTP)  -> MCD45A1_TIF_C51
    #   A list of the dir is returned (as form ls -l)
    #   ---------------------------------------------------------------------------
    def TestFtpDir(self):
        filename='mcd45a1.txt'
        remote_url='ftp://ba1.geog.umd.edu/'
        UserPwd='user:burnt_data'
        filepath = get_dir_contents_from_url(remote_url, target_file=filename, userpwd=UserPwd)

        logger.info('File downloaded to: '+filepath)
        self.assertEqual(1,1)

    #   ---------------------------------------------------------------------------
    #   Get a file from HTTP (list_from_template=TRUE, No User/psw) -> FEWSNET
    #   ---------------------------------------------------------------------------
    def TestFewsnetFile(self):
        filename='a14081rb.zip'
        remote_url='http://earlywarning.usgs.gov/ftp2/raster/rf/a/2014/'
        # filepath = get_file_from_url(remote_url+filename, target_file=filename)
        filepath = get_dir_contents_from_url(remote_url, target_file=filename)
        logger.info('File downloaded to: '+filepath)
        self.assertEqual(1,1)

    #   ---------------------------------------------------------------------------
    #   Get a file from FTP (list_from_template=FALSE, User/psw) -> FIRMS_NASA
    #   ---------------------------------------------------------------------------
    def TestFirmsFile(test):
        filename='Global_MCD14DL_2014237.txt'
        remote_url='ftp://nrt1.modaps.eosdis.nasa.gov/FIRMS/Global/'
        Username='jrcMondeFires'
        Password='FIRE@data1'
        UserPwd=Username+':'+Password
        get_file_from_url(remote_url, target_file=filename, userpwd=UserPwd)
