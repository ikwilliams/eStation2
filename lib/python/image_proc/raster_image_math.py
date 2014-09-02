__author__ = 'clerima'
#
#	purpose: Define a set of simple mathematical functions for processing images
#	author:  M.Clerici
#	date:	 17.06.2014
#   descr:	 Define a set of simple mathematical functions for processing images, mainly derived for the
#            dedicated functions implemented in eStation 1.0 (e.g. avg.py).
#            Images are simply treated as arrays (no any geo-processing)
#	history: 1.0
#   common args:    input_files     -> one or more inputs
#                   output_files    -> one (or more?) outputs
#
#   common options: input_nodata    -> value to be considered as nodata in input_files
#                   output_nodata   -> value to be considered as nodata in output_files
#                   format          -> file format (default: GTIFF)
#                   output_type     -> data type in output (as input, if missing)
#
#   contents:       do_avg_image()  -> compute avg over list of images
#                   do_min_image()  -> compute min over list of images
#                   do_max_image()  -> compute max over list of images
#
#   General Notes on 'nodata':  they might be different in input and output files, at least for functions that
#                               create the output file(s) every time (no upgrade).
#                               E.g. -9999 in the input file might be recoded to -10000 in the output
#
#                               Nevertheless if input_nodata id <def> and output_nodata is <undef> the latter is assigned
#                               to the value of inputs.
#
#                               In functions like <min>, <max> in the loop over files we update an output if we find
#                               a <valid> data to replace a <nodata>
#

# source my definitions
#import locals

#import glob
#import os

# Import eStation lib modules
from lib.python import es_logging as log
from config.es_constants import *

# Import third-party modules
from osgeo.gdalconst import *
from osgeo import gdal
from osgeo import osr
import numpy as N

logger = log.my_logger(__name__)

# _____________________________
def do_avg_image(input_file='', output_file='', input_nodata=None, output_nodata=None, output_format=None,
           output_type=None, options='', output_stddev=None):

    # Note: no 'update' functionality is foreseen -> creates output EVERY TIME

    # Force input to be a list
    input_list = return_as_list(input_file)

    # Manage options
    options_list = []
    options_list.append(options)

    # Force output_nodata=input_nodata it the latter is DEF and former UNDEF
    if output_nodata is None and input_nodata is not None:
        output_nodata = input_nodata

    # Get infos from first file
    fidT=gdal.Open(input_list[0], GA_ReadOnly)
    nb=fidT.RasterCount
    ns=fidT.RasterXSize
    nl=fidT.RasterYSize
    dataType=fidT.GetRasterBand(1).DataType
    geotransform=fidT.GetGeoTransform()
    projection=fidT.GetProjection()
    driver_type=fidT.GetDriver().ShortName

    # manage out_type (take the input one as default)
    if output_type is None:
        outType=dataType
    else:
        outType=ParseType(output_type)

    # manage out_format (take the input one as default)
    if output_format is None:
        outFormat=driver_type
    else:
        outFormat=output_format

    # instantiate output/s
    outDrv=gdal.GetDriverByName(outFormat)
    outDS=outDrv.Create(output_file, ns, nl, nb, outType, options_list)
    outDS.SetProjection(projection)
    outDS.SetGeoTransform(geotransform)

    if output_stddev != None:
        outStd = gdal.GetDriverByName(output_format)
        stdDs = outStd.Create(output_stddev, ns, nl, nb, outType, options_list)
        stdDs.SetProjection(projection)
        stdDs.SetGeoTransform(geotransform)

    # pre-open input files
    rangenl = range(nl)
    rangeFile = range(len(input_list))
    fid = []
    for ifid in rangeFile:
        fid.append(gdal.Open(input_list[ifid], GA_ReadOnly))

    # Loop over bands
    for ib in range(nb):
        outband = outDS.GetRasterBand(ib+1)

        # parse image by line
        for il in rangenl:
            counter = N.zeros(ns)
            accum = N.zeros(ns)
            # for all files:
            for ifile in rangeFile:
                data = N.ravel(fid[ifile].GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1).astype(float))

                # variable initialization
                if (ifile==0):
                    if input_nodata is None:
                        avgData = data
                        stdData = N.multiply(data , data)
                        counter[:] = 1.0
                    else:
                        wts = (data != input_nodata)
                        avgData = N.zeros(data.shape)
                        stdData = N.zeros(data.shape)
                        if wts.any():
                            counter[wts] = 1.0
                            avgData[wts] = data[wts]
                            stdData[wts] = N.multiply(data[wts], data[wts])

                else:
                    if input_nodata is None:
                        avgData = avgData + data
                        counter = counter + 1.0
                        stdData = stdData + N.multiply(data, data)
                    else:
                        wts = (data != input_nodata)
                        if wts.any():
                            avgData[wts] = avgData[wts] + data[wts]
                            counter[wts] = counter[wts] + 1.0
                            stdData[wts] = stdData[wts] + N.multiply(data[wts], data[wts])

            wnz = (counter != 0)
            outData = N.zeros(ns)
            if wnz.any():
                outData[wnz] = avgData[wnz]/(counter[wnz])

            if output_nodata != None:
                wzz = (counter == 0)
                if wzz.any():
                    outData[wzz] = output_nodata

            # Check if stddev also required
            if output_stddev != None:
                outDataStd = N.zeros(ns)
                if wnz.any():
                    outDataStd[wnz] = N.sqrt( stdData[wnz]/(counter[wnz]) - N.multiply(outData[wnz],outData[wnz]) )
                if output_nodata != None:
                    wzz = (counter == 0)
                    if wzz.any():
                        outDataStd[wzz] = output_nodata

                outDataStd.shape = (1, -1)
                stdDs.GetRasterBand(ib+1).WriteArray(N.array(outDataStd), 0, il)

            # reshape before writing
            outData.shape = (1, -1)
            outband.WriteArray(N.array(outData), 0, il)

            gdal.TermProgress((ns * il + ib*(ns*nl))/float(nl*ns*nb))


    gdal.TermProgress(1)
    print ''

# _____________________________

def do_min_image(input_file='', output_file='', input_nodata=None, output_nodata=None, output_format=None,
           output_type=None, options='', index_file=None):
    #
    # Notes:'The command expects a list of at least 2 files in input.'
    #       'The optional index file will store the file index (position in input-list) used for the minimum.'
    # TODO-M.C.: : can be used in 'update' functionality ??? -> reuse output file ??

    # Force input to be a list
    input_list = return_as_list(input_file)

    # Manage options
    options_list = []
    options_list.append(options)

    # get infos from the last file (to manage case of 'upgraded' DataType - e.g. FEWSNET).
    nFiles=len(input_list)
    f1Fid = gdal.Open(input_list[nFiles-1], GA_ReadOnly)
    nb = f1Fid.RasterCount
    ns = f1Fid.RasterXSize
    nl = f1Fid.RasterYSize
    dataType = f1Fid.GetRasterBand(1).DataType
    geoTransform = f1Fid.GetGeoTransform()
    projection = f1Fid.GetProjection()
    driver_type=f1Fid.GetDriver().ShortName

    # Force output_nodata=input_nodata it the latter is DEF and former UNDEF
    if output_nodata is None and input_nodata is not None:
        output_nodata = input_nodata

    # manage out_type (take the input one as default)
    if output_type is None:
        outType=dataType
    else:
        outType=ParseType(output_type)

    # manage out_format (take the input one as default)
    if output_format is None:
        outFormat=driver_type
    else:
        outFormat=output_format

    # instantiate output(s)
    outDrv = gdal.GetDriverByName(outFormat)
    outDS = outDrv.Create(output_file, ns, nl, nb, outType,options_list)
    outDS.SetGeoTransform(geoTransform)
    outDS.SetProjection(projection)
    if (index_file is None):
        indexDS = None
    else:
        indexDrv = gdal.GetDriverByName(outFormat)
        indexDS = outDrv.Create(index_file, ns, nl, nb, GDT_Int16, options_list)
        indexDS.SetGeoTransform(geoTransform)
        indexDS.SetProjection(projection)

    # pre-open files, to speed up processing
    fidList=[]
    for ii in range(len(input_file)):
        fidList.append(gdal.Open(input_file[ii], GA_ReadOnly))

    for ib in range(nb):
        outband = outDS.GetRasterBand(ib+1)
        if index_file is not None:
            indexBand = indexDS.GetRasterBand(ib+1)

        for il in range(nl):

            for ifile in range(len(input_file)):
                fid = fidList[ifile]
                data = N.ravel(fid.GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1).astype(float))

                if (ifile == 0):
                    # initial value set on first file
                    minData = data
                    if (input_nodata is None):
                        indexData = N.zeros(ns)
                    else:
                        indexData = N.zeros(ns)-1
                        wtp = (minData != input_nodata)
                        if wtp.any():
                            indexData[wtp] = ifile

                else:
                    if (input_nodata is None):
                        wtp = (data < minData)
                        if wtp.any():
                            minData[wtp] = data[wtp]
                            indexData[wtp] = ifile

                    else:
                        wtp = (data < minData) * (data != input_nodata)
                        # can we find a value to replace a no data?
                        wtf = (minData == output_nodata ) * (data != input_nodata)

                        if wtp.any():
                            minData[wtp] = data[wtp]
                            indexData[wtp] = ifile

                        if wtf.any():
                            minData[wtf] = data[wtf]
                            indexData[wtf] = ifile

            minData.shape = (1,-1)
            indexData.shape = (1,-1)

            outband.WriteArray(N.array(minData),0,il)
            if indexDS is not None:
                #indexBand.WriteArray(gdalnumeric.array(indexData), 0, il)
                indexBand.WriteArray(N.array(indexData), 0, il)
            gdal.TermProgress( (ns*il + ib*(ns*nl))/float(nl*ns*nb) )
    gdal.TermProgress(1)
    print

# _____________________________

def do_max_image(input_file='', output_file='', input_nodata=None, output_nodata=None, output_format=None,
           output_type=None, options='', index_file=None, min_num_valid=None):
    #
    # Notes:'The command expects a list of at least 2 files in input.'
    #       'The optional index file will store the file index (position in input-list) used for the minimum.'
    # TODO-M.C.: : can be used in 'update' functionality ??? -> reuse output file ??

    # Force input to be a list
    input_list = return_as_list(input_file)

    # Manage options
    options_list = []
    options_list.append(options)

    # get infos from the last file (to manage case of 'upgraded' DataType - e.g. FEWSNET).
    nFiles=len(input_list)
    f1Fid = gdal.Open(input_list[nFiles-1], GA_ReadOnly)
    nb = f1Fid.RasterCount
    ns = f1Fid.RasterXSize
    nl = f1Fid.RasterYSize
    dataType = f1Fid.GetRasterBand(1).DataType
    geoTransform = f1Fid.GetGeoTransform()
    projection = f1Fid.GetProjection()
    driver_type=f1Fid.GetDriver().ShortName

    # Force output_nodata=input_nodata it the latter is DEF and former UNDEF
    if output_nodata is None and input_nodata is not None:
        output_nodata = input_nodata

    # manage out_type (take the input one as default)
    if output_type is None:
        outType=dataType
    else:
        outType=ParseType(output_type)

    # manage out_format (take the input one as default)
    if output_format is None:
        outFormat=driver_type
    else:
        outFormat=output_format

    # instantiate output(s)
    outDrv = gdal.GetDriverByName(outFormat)
    outDS = outDrv.Create(output_file, ns, nl, nb, outType,options_list)
    outDS.SetGeoTransform(geoTransform)
    outDS.SetProjection(projection)
    if (index_file is None):
        indexDS = None
    else:
        indexDrv = gdal.GetDriverByName(outFormat)
        indexDS = outDrv.Create(index_file, ns, nl, nb, GDT_Int16, options_list)
        indexDS.SetGeoTransform(geoTransform)
        indexDS.SetProjection(projection)

    # pre-open files, to speed up processing
    fidList=[]
    for ii in range(len(input_file)):
        fidList.append(gdal.Open(input_file[ii], GA_ReadOnly))

    for ib in range(nb):
        outband = outDS.GetRasterBand(ib+1)
        if index_file is not None:
            indexBand = indexDS.GetRasterBand(ib+1)

        for il in range(nl):
            counter = N.zeros(ns)
            for ifile in range(len(input_file)):
                fid = fidList[ifile]
                data = N.ravel(fid.GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1).astype(float))

                if (ifile == 0):
                    maxData = data
                    if (input_nodata is None):
                        indexData = N.zeros(ns)
                        counter[:] = 1.0
                    else:
                        indexData = N.zeros(ns)-1
                        wtp = (maxData != input_nodata)
                        if wtp.any():
                            indexData[wtp] = ifile
                            counter[wtp] = 1.0
                else:
                    if (input_nodata is None):
                        wtp = (data > maxData)
                        counter[:] = counter[:] + 1.0

                        if wtp.any():
                            maxData[wtp] = data[wtp]
                            indexData[wtp] = ifile

                    else:
                        wtp = (data > maxData) * (data != input_nodata)
                        # replace nodata with data
                        wtf = (maxData == input_nodata)*(data!=input_nodata)
                        if wtp.any():
                            maxData[wtp] = data[wtp]
                            indexData[wtp] = ifile
                        if wtf.any():
                            maxData[wtf] = data[wtf]
                            indexData[wtf] = ifile
                        # add valid pixels to count
                        wts = (data != input_nodata)
                        if wts.any():
                            counter[wts] = counter[wts] + 1.0

            # manage 'minvalid' option
            if min_num_valid is not None:
                wtb = (counter < min_num_valid)
                if wtb.any():
                    maxData[wtb] = output_nodata

            maxData.shape = (1,-1)
            indexData.shape = (1,-1)
            outband.WriteArray(N.array(maxData),0,il)
            if indexDS is not None:
                indexBand.WriteArray(N.array(indexData), 0, il)
            gdal.TermProgress( (ns*il + ib*(ns*nl))/float(nl*ns*nb) )
    gdal.TermProgress(1)
    print

def do_oper_subtraction(input_file='', output_file='', input_nodata=None, output_nodata=None, output_format=None,
           output_type=None, options=''):
    #
    # Notes:'The command expects exactly 2 files in input.'

    # Manage options
    options_list = []
    options_list.append(options)

    # Open input files
    fid0 = gdal.Open(input_file[0], GA_ReadOnly)
    fid1 = gdal.Open(input_file[1], GA_ReadOnly)

    # Read info from file1
    nb = fid0.RasterCount
    ns = fid0.RasterXSize
    nl = fid0.RasterYSize
    dataType = fid0.GetRasterBand(1).DataType
    geoTransform = fid0.GetGeoTransform()
    projection = fid0.GetProjection()
    driver_type=fid0.GetDriver().ShortName

    # Force output_nodata=input_nodata it the latter is DEF and former UNDEF
    if output_nodata is None and input_nodata is not None:
        output_nodata = input_nodata

    # manage out_type (take the input one as default)
    if output_type is None:
        outType=dataType
    else:
        outType=ParseType(output_type)

    # manage out_format (take the input one as default)
    if output_format is None:
        outFormat=driver_type
    else:
        outFormat=output_format

    # instantiate output
    outDrv = gdal.GetDriverByName(outFormat)
    outDS = outDrv.Create(output_file, ns, nl, nb, outType,options_list)
    outDS.SetGeoTransform(geoTransform)
    outDS.SetProjection(projection)

    for ib in range(nb):
        for il in range(nl):
            data0 = N.ravel(fid0.GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1)).astype(float)
            data1 = N.ravel(fid1.GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1)).astype(float)

            if input_nodata is None:
                dataout = data0 - data1
            else:
                if input_nodata is None:
                    dataout = N.zeros(ns)
                else:
                    dataout = N.zeros(ns) + output_nodata

                wtc = (data0 != input_nodata) * (data1 != input_nodata)
                if wtc.any():
                    dataout[wtc] = data0[wtc] - data1[wtc]

            dataout.shape=(1,-1)
            outDS.GetRasterBand(ib+1).WriteArray(N.array(dataout), 0, il)

            gdal.TermProgress( (ib*(ns*nl)+il*ns) / float(ns*nl) )

    gdal.TermProgress(1)


def do_oper_division(input_file='', output_file='', input_nodata=None, output_nodata=None, output_format=None,
           output_type=None, options=''):
    #
    # Notes:'The command expects exactly 2 files in input.'
    epsilon = 1e-10

    # Manage options
    options_list = []
    options_list.append(options)

    # Open input files
    fid0 = gdal.Open(input_file[0], GA_ReadOnly)
    fid1 = gdal.Open(input_file[1], GA_ReadOnly)

    # Read info from file1
    nb = fid0.RasterCount
    ns = fid0.RasterXSize
    nl = fid0.RasterYSize
    dataType = fid0.GetRasterBand(1).DataType
    geoTransform = fid0.GetGeoTransform()
    projection = fid0.GetProjection()
    driver_type=fid0.GetDriver().ShortName

    # Force output_nodata=input_nodata it the latter is DEF and former UNDEF
    if output_nodata is None and input_nodata is not None:
        output_nodata = input_nodata

    # manage out_type (take the input one as default)
    if output_type is None:
        outType=dataType
    else:
        outType=ParseType(output_type)

    # manage out_format (take the input one as default)
    if output_format is None:
        outFormat=driver_type
    else:
        outFormat=output_format

    # instantiate output
    outDrv = gdal.GetDriverByName(outFormat)
    outDS = outDrv.Create(output_file, ns, nl, nb, outType,options_list)
    outDS.SetGeoTransform(geoTransform)
    outDS.SetProjection(projection)

    for ib in range(nb):
        for il in range(nl):
            data0 = N.ravel(fid0.GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1)).astype(float)
            data1 = N.ravel(fid1.GetRasterBand(ib+1).ReadAsArray(0, il, ns, 1)).astype(float)

            if input_nodata is None:
                wtc = (N.abs(data1) > epsilon)
            else:
                wtc = (data0 != input_nodata) * (data1 != input_nodata) * (N.abs(data1) > epsilon)

            # TODO-M.C.: check this assignment is done for the other functions as well
            dataout=N.zeros(ns)
            if input_nodata is None:
                dataout=N.zeros(ns) + output_nodata

            if wtc.any():
                dataout[wtc] = data0[wtc] / data1[wtc]

            dataout.shape=(1,-1)
            outDS.GetRasterBand(ib+1).WriteArray(N.array(dataout), 0, il)

            gdal.TermProgress( (ib*(ns*nl)+il*ns) / float(ns*nl) )

    gdal.TermProgress(1)
# _____________________________
#   Merge/move wrt processing.py functions
def ParseType(type):
    if type == 'Byte':
	return GDT_Byte
    elif type == 'Int16':
	return GDT_Int16
    elif type == 'UInt16':
	return GDT_UInt16
    elif type == 'Int32':
	return GDT_Int32
    elif type == 'UInt32':
	return GDT_UInt32
    elif type == 'Float32':
	return GDT_Float32
    elif type == 'Float64':
	return GDT_Float64
    elif type == 'CInt16':
	return GDT_CInt16
    elif type == 'CInt32':
	return GDT_CInt32
    elif type == 'CFloat32':
	return GDT_CFloat32
    elif type == 'CFloat64':
	return GDT_CFloat64
    else:
	return GDT_Byte

def return_as_list(input_args):

    my_list = []
    if isinstance(input_args, list):
        my_list = input_args
    else:
        for item in input_args:
            my_list.append(item)
    return my_list