#   localFeaturesValidationTest.py
#   to test the matching algorithm via local features
#   1.  load the COMPREF and WRF respectively
#   2.  construct local features after segmentation
#   3.  order local features according to volume, descending
#   4.  match the local features in COMPREF and WRF and compute the distances via the greedy algorithm
#   5.  compute the weighed distance between two images
#   6.  look for the closest WRF match to the COMPREF
#   7.  validation of the above algorithm

import time, os, pickle
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
from armor import objects4 as ob
compref    = ob.kongrey
wrf       = ob.kongreywrf2
wrf.fix()

a   = compref('20130829.1200')[0].load()
a.show()
a.localShapeFeatures(lowerThreshold=10, upperThreshold=35)

b1  = wrf('20130829.1200')
b2  = wrf('20130829.1500')
b3  = wrf('20130829.0900')
B   = b1 +b2 + b3

for b in B:
    b.localShapeFeatures(lowerThreshold=10, upperThreshold=35)
    print 
