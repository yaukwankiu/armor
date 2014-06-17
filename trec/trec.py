# TREC - Tracking Radar Echo by Correlation

# consider also using optical flow in opencv:  http://docs.opencv.org/2.4.3/modules/video/doc/motion_analysis_and_object_tracking.html


###########
#imports

import numpy as np
import numpy.ma as ma
from .. import pattern
#from armor.shiiba import regression2 as regression
#from ..advection import semiLagrangian
#sl = semiLagrangian
from imp import reload
import time
#lsq = np.linalg.lstsq

time0= time.time()

###########
# setup
def tic():
    global timeStart
    timeStart = time.time()

def toc():
    print "time spent:", time.time()-timeStart

###########
# defining the functions

def getVectorField(a, b, scope=(5,5), window=(5,5)):
    """
    input:  armor.pattern.DBZ objects a, b
    output: armor.pattern.VectorField object vect
    """
    pass
    
    
#####################
# using opencv
# reference: http://docs.opencv.org/2.4.3/modules/video/doc/motion_analysis_and_object_tracking.html
# see also: http://opencv.willowgarage.com/documentation/python/imgproc_motion_analysis_and_object_tracking.html


import cv

lk = cv.CalcOpticalFlowPyrLK



