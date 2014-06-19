#	Test SRS and dataset python classes

import os, sys, re, signal, commands, datetime, tempfile, re, zipfile
import time, string
from osgeo import osr, gdal

sys.path.append('/srv/www/eStation2/config/')

inNotGeorefFile='/srv/www/eStation2/apps/acquisition/tmp/0001_NDV.HDF'
inGeorefFile='/srv/www/eStation2/TestFiles/Inputs/20121021_NDWI.tif'

geoRef=1

if geoRef==1:
	inputfile=inGeorefFile
	outputfile='/srv/www/eStation2/apps/acquisition/tmp/NDV_ECOWAS_G.tif'
else:
	inputfile=inNotGeorefFile
	outputfile='/srv/www/eStation2/apps/acquisition/tmp/NDV_ECOWAS_NotG.tif'

# eStation2 base definitions
import es2

# Native mapset (file not geo-referenced)
native_mapset=es2.mapset()
native_mapset.assignVGT4Africa()
native_mapset.printOut()

# Open input file
origDs=gdal.Open(inputfile)
# Assign Proj/Transform
if geoRef==1:
	origCs=osr.SpatialReference()
	origCs.ImportFromWkt(origDs.GetProjectionRef())
else:
	origDs.SetProjection(native_mapset.SpatialRef.ExportToWkt())
	origDs.SetGeoTransform(native_mapset.GeoTransform)
	origCs=native_mapset.SpatialRef

# Output mapset 
output_mapset=es2.mapset()
output_mapset.assignECOWAS()
output_mapset.printOut()

outSizeX = output_mapset.sizeX
outSizeY = output_mapset.sizeY

# Create target in memory
memDriver = gdal.GetDriverByName('MEM')

# Define output dataset Proj/Transform
outCs=output_mapset.SpatialRef
outDs = memDriver.Create('',outSizeX, outSizeY, 1, gdal.GDT_Byte)
outDs.SetGeoTransform(output_mapset.GeoTransform)
outDs.SetProjection(outCs.ExportToWkt())

# Apply Reproject-Image (in memory)
res = gdal.ReprojectImage(origDs, outDs, origCs.ExportToWkt(), outCs.ExportToWkt(), gdal.GRA_Bilinear)
outData = outDs.ReadAsArray()

# Create and write outputfile
outDriver = gdal.GetDriverByName("GTiff")
trgDs = outDriver.CreateCopy(outputfile, outDs, 0)
trgDs = None

