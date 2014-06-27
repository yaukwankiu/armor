# -*- coding: utf-8  -*-

"""
tests:
    
1.  原始資料，雷達(881x921)與模式(150x140)的網格不同
        a. 2014年3月12日雨帶
        b. 2014年5月20日雨帶
        c. 2013年8月28-29日 Kong-Rey 颱風
2.  經過陳新淦先生以 Grace 重畫的資料 (201x183)，網格相同
        2014年5月20日雨帶
分析原始資料前，因為雷達COMPREF的網格比模式WRF的網格細，（雷達4x4 格等於模式 1x1格），故我們在計算之前先將網格歸一。具體方法有三：
1.  每4x4格點抽樣取1格點 (sampling)
2.  每4x4格點平均成1格點 (averaging)
3.  每4x4格點，由 4x4=16 個起點平均成1格點 ，再對比其差異 (over-sampling)。
以下我們先選幾個時間點上，同一時間之雷達回波圖與WRF模式輸出對比。之後再算時間序列 (times series) 的平均
因為結果的數值範圍大，所以我們以 log-log scale 來顯示。
[normalisation problems/ or not]
"""








#################################################################################
#   powerSpec3.py
#   adapted from powerSpec2.py
#   2014-06-22


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
thisScript   = 'powerSpec3.py'
scriptFolder = root+'python/armor/spectral/' 

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

#   end all setups
################################################################################

################################################################################
################################################################################
#   #   #   #   TESTS   #   #   #   #
#
#   1a.
##################################
#   restart test
if "ps1" in locals():
    reload(ps1)
if "pattern" in locals():
    reload(pattern)
################################################################################
#

timeString   = getTimeString()
reload(ps1)
outputFolder0 = '/media/TOSHIBA EXT/ARMOR/labLogs2/powerSpec3/'
outputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs2/powerSpec3/' + timeString + '/'

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
shutil.copyfile(scriptFolder+thisScript, outputFolder+thisScript)

#############################

dataTimes    = ["20140312.0900", "20140312.1200", "20140312.1500"]
wrf         = ob.march2014wrf
for dataTime in dataTimes:
    wrf.load(dataTime)

wrf.cutUnloaded()


monsoon     = ob.march2014

a   = monsoon("20140312.1140")[0]
b   = monsoon("20140312.1150")[0]

#ms  = monsoon("20140312.11") + monsoon("20140312.12") + monsoon("20140312.13")
#ms  = monsoon("20140312.12")
ms = wrf

print '\n'.join([v.name for v in ms])
print "sleeping 3 seconds"
time.sleep(3)

print "outputFolder:", outputFolder

for k in ms:
    k.load()
    res = k.powerSpec(thres=0, outputFolder=outputFolder, 
                #spectrumType = "numerical",
                responseThreshold=0.1, scaleSpacePower=0, 
                #useLogScale=True,
                useLogScale=True,
                useOnlyPointsWithSignals=False,
                )
    #k.powerSpec(thres=0, outputFolder=outputFolder, 
    #            #spectrumType = "total",
    #            responseThreshold=0.01,scaleSpacePower=0, useLogScale=True)

    #try:
    #    k.drawCoast()
    #except: 
    #    pass
    #k.saveImage(imagePath=outputFolder0+k.name+'.png')
    

print "outputFolder:", outputFolder

#########################################################




