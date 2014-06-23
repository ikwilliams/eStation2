__author__ = "Marco Clerici"


import time
from apps.processing.processing import *
start = time.clock()

processing_fewsnet_rfe()

elapsed = time.clock()-start
print elapsed


exit()

