#   powerSpec2.py
#   2014-06-16
"""

LOOK into:
       CONTRAST:
       1 wrf v. 1 radar
       wrf time series average v. radar time series average

REPORT on:
list: datasource, time, etc. 
       method of data handling
       show relevant RADAR/WRF images versus spectra
       cut into the same area/box
"""
###########################################################################
###########################################################################
###########################################################################
#   imports

import shutil, os, re, time, datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

from armor import pattern
from armor import objects4 as ob
from armor import defaultParameters as dp

from armor.tests import powerSpec1 as ps1
sampling = ps1.averaging

root = dp.root
DBZ = pattern.DBZ

reload(ob)
kongrey = ob.kongrey
kongreywrf  = ob.kongreywrf
march2014   = ob.march2014
march2014wrf= ob.march2014wrf
kongreywrf.fix()
march2014wrf.fix()


###########################################################################
###########################################################################
#   parameters
thisScript   = 'powerSpec2.py'
scriptFolder = root+'python/armor/tests/' 

i1  = (20.-18.)/0.0125  #160
i2  = (29.-28.)/0.0125  #80
j1  = (117.5-115.)/0.0125   #200
j2  = (126.5-124.5)/0.0125  #160

###########################################################################
###########################################################################
#   functions

def getTimeString():
    return str(int(time.time()))
    
'''
def sampling(a, starting=(0,0)):
    # from powerSpecs1.py
    """4x4 to 1x1 averaging
    oversampling 4x4 to 1x1 avaraging with various starting points"""

    starting = (wrfLL - radarLL)/radarGridSize + starting
    ending   = starting + wrfGrid * radar_wrf_grid_ratio
    mask      = 1./16 * np.ones((4,4))
    a1  = a.copy()
    a1.matrix = signal.convolve2d(a1.matrix, mask, mode='same')  #http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html

    a1.matrix = a1.matrix[starting[0]:ending[0]:radar_wrf_grid_ratio,
                            starting[1]:ending[1]:radar_wrf_grid_ratio,
                          ]

    print 'starting, ending:',starting, ending  #debug
    return a1
'''
###########################################################################
#   test 1
#   1. load the data
#   2. cut out the data, interpolate if necessary
#   3. write the cut out data to outputFolder
#   4. perform the analysis
#   5. output the analysis results

timeString   = getTimeString()
outputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs2/powerSpec2/' + timeString + '/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
shutil.copyfile(scriptFolder+thisScript, outputFolder+thisScript)

w0   = kongreywrf[15]   #   <-- change here
dataTime    = w0.dataTime
k   = kongrey(dataTime)[0]
ws  = kongreywrf(dataTime)

#w   = ws[1]
for w in ws:
    k.load()
    w.load()
    k1  = k.getWindow(i1,j1, 880-i1-i2, 920-j1-j2)
    k1.setThreshold(-10)
    #k1.show()
    k1.saveImage(imagePath=outputFolder+ k.name+ 'k1.png')
    w.setThreshold(-10)
    #w.show()
    w.saveImage(imagePath=outputFolder+w.name+'.png')
    w_spec = ps1.getLaplacianOfGaussianSpectrum(w, thres=0, outputFolder=outputFolder)

    k2 = sampling(k)
    k2.setThreshold(-10)
    #k2.show()
    k2.saveImage(imagePath=outputFolder+ k2.name+'.png')

    k2_spec= ps1.getLaplacianOfGaussianSpectrum(k2, thres=0, outputFolder=outputFolder, toReload=False)



