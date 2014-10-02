# Import local definitions
import locals

outputfile='test.tif'
file='/tmp/eStation2/apps.acquisition.ingestionQOvo4N_A2002185.L3m_DAY_CHL_chlor_a_4km.bz2/A2002185.L3m_DAY_CHL_chlor_a_4km'

# Import third-party modules
from osgeo.gdalconst import *
from osgeo import gdal
from osgeo import osr


# By using GDAL -
ds=gdal.Open(file)
orig_cs=osr.SpatialReference()
orig_cs.ImportFromWkt(ds.GetProjectionRef())
orig_geo_transform = ds.GetGeoTransform()
orig_size_x = ds.RasterXSize
orig_size_y = ds.RasterYSize

print orig_geo_transform
print orig_size_x

