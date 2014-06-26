__author__ = "Marco Clerici"


import time
from apps.processing.processing import *
from apps.processing.processing_ndvi import *

start = time.clock()

processing_fewsnet_rfe()
#processing_ndvi()

elapsed = time.clock()-start
print elapsed


exit()

