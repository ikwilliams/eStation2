#
#	purpose: Define the get_internet service
#	author:  M.Clerici
#	date:	 19.02.2014
#   descr:	 Reads the definition from eStation DB and execute the copy to local disk
#	history: 1.0


# Import local definitions
import locals

# Import standard modules
import pycurl
from StringIO import StringIO
import cStringIO
import tempfile
import os
import unittest
import glob
import re

# Import eStation2 modules
from lib.python import es_logging as log
from config.es_constants import *
import database.querydb as querydb
from lib.python.functions import *

logger = log.my_logger(__name__)

#   General definitions
c = pycurl.Curl()
buffer = StringIO()
tmpdir = tempfile.mkdtemp(prefix=__name__, dir=locals.es2globals['temp_dir'])

#   ---------------------------------------------------------------------------
#   Functions
#   ---------------------------------------------------------------------------

def get_list_current_subdirs_ftp(remote_url, usr_pwd):

    d = pycurl.Curl()
    response = cStringIO.StringIO()
    d.setopt(pycurl.URL, remote_url)
    d.setopt(pycurl.USERPWD, usr_pwd)
    d.setopt(pycurl.FOLLOWLOCATION, 1)
    d.setopt(pycurl.WRITEFUNCTION, response.write)
    d.perform()
    d.close()
    current_list = []
    content=response.getvalue()
    lines = content.split('\n')
    for line in lines:
        check_line = len(str(line))
        if check_line is not 0:
            line_dir=line.split()[-1]
            current_list.append(line_dir)
    
    return current_list

def get_list_matching_files_dir_ftp(remote_url, usr_pwd, full_regex):

    # Local implementation (filesystem, not http/ftp remote server)
    list_matches=[]
    level = 1
    maxlevel= len(re.findall("/",full_regex))
    toprint=''
    get_list_matching_files_subdir_ftp(list_matches, remote_url, usr_pwd, base_dir, full_regex, level, maxlevel,'')
    for elem in list_matches:
        toprint+=elem+','
    logger.info(toprint)
    return list_matches 

#   Returns the list of objects(files or dirs) located in a remote subdir and
#   matching 'regex' (single 'regex' - not tree structure). Can be called iteratively.
def get_list_matching_files_subdir_ftp(list, remote_url, usr_pwd, base_dir, regex, level, max_level, sub_dir):

    # split the regex
    tokens=regex.split('/')
    regex_my_level=''
    # regex for this level
    regex_my_level+=tokens[level]
    #my_list=[]
    my_list = get_list_current_subdirs_ftp(remote_url, usr_pwd)
    for element in my_list:
        if re.match(regex_my_level,element) is not None:
            # Is it already the file ?
            if max_level == level:
                print sub_dir
                print element
                #logger.info(element)
                list.append(sub_dir+element)
            else:
                # Enter the subdir
                print sub_dir
                new_level=level+1
                new_sub_dir=sub_dir+element+'/'
                new_remote_url=remote_url+'/'+element+'/'
                get_list_matching_files_subdir_ftp(list, new_remote_url, usr_pwd, base_dir, regex, new_level, max_level, new_sub_dir)   
    return 0
   
#   Target dir is created as 'tmpdir' if not passed
#   Full pathname is returned (or positive number for error)

#   Returns the list of files matching 'regex' (complex 'regex' - i.e. tree structure).
#   It applies to cases like 'dirs_ftp'

def get_list_matching_files_dir_local(remote_url_dir, full_regex):

    # Local implementation (filesystem, not http/ftp remote server)
    list_matches=[]
    level = 1
    maxlevel=len(full_regex.split('/'))
    toprint=''
    get_list_matching_files_subdir_local(list_matches, remote_url_dir, full_regex, level, maxlevel,'')
    for elem in list_matches:
        toprint+=elem+','
    logger.info(toprint)

#   Returns the list of objects(files or dirs) located in a remote subdir and
#   matching 'regex' (single 'regex' - not tree structure). Can be called iteratively.
def get_list_matching_files_subdir_local(list, remote_url_dir, regex, level, max_level, sub_dir):

    # split the regex
    tokens=regex.split('/')
    regex_my_level=''
    # regex for this level
    regex_my_level+=tokens[level-1]

    my_list = os.listdir(remote_url_dir)
    for element in my_list:
        if re.match(regex_my_level,element) is not None:
            # Is it already the file ?
            if max_level == level:
                #logger.info(element)
                list.append(sub_dir+element)
            else:
                # Enter the subdir
                new_level=level+1
                new_sub_dir=sub_dir+element+'/'
                get_list_matching_files_subdir_local(list, remote_url_dir+'/'+element, regex, new_level, max_level, new_sub_dir)

    return 0

#   Target dir is created as 'tmpdir' if not passed
#   Full pathname is returned (or positive number for error)
def get_file_from_url(remote_url_file, target_file=None, target_dir=None, userpwd=''):

    if target_dir is None:
        tmpdir = tempfile.mkdtemp(prefix=__name__, dir=locals.es2globals['temp_dir'])
    else:
        tmpdir = target_dir

    if target_file is None:
        target_file='test_output_file'

    target_fullpath=tmpdir+os.sep+target_file

    outputfile=open(target_fullpath, 'wb')
    logger.debug('Output File: '+target_fullpath)

    c.setopt(c.URL,remote_url_file)
    c.setopt(c.WRITEFUNCTION,outputfile.write)
    if userpwd is not '':
        c.setopt(c.USERPWD,userpwd)
    c.perform()
    outputfile.close()

    return target_fullpath

#   Target dir is created as 'tmpdir' if not passed
#   Full pathname is returned (or positive number for error)
#   TODO-M.C.: return in a python object rather than writing in a file

def get_dir_contents_from_url(remote_url_dir, target_file=None, target_dir=None, userpwd=''):

    if target_dir is None:
        tmpdir = tempfile.mkdtemp(prefix=__name__, dir=locals.es2globals['temp_dir'])
    else:
        tmpdir = target_dir

    if target_file is None:
        target_file='test_output_file'

    target_fullpath=tmpdir+os.sep+target_file

    outputfile=open(target_fullpath, 'wb')
    logger.debug('Output File: '+target_fullpath)

    c.setopt(c.URL,remote_url_dir)
    c.setopt(c.WRITEFUNCTION,outputfile.write)
    if userpwd is not '':
        c.setopt(c.USERPWD,userpwd)
    c.perform()
    outputfile.close()

    return target_fullpath
