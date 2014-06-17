"""
mark1a.py
USE:
    cd [.. FILL IN YOUR ROOT DIRECTORY HERE ..]/ARMOR/python/
    from armor.patternMatching import mark1
    x=mark1.main(inputFolder="")
"""
#   0.  imports
#   1.  defining the parameters
#   2.  reading the data
#   3.  processing
#   4.  output

#   0.  imports
import time, datetime, os
import numpy as np
import matplotlib.pyplot as plt
from armor import defaultParameters as dp
from armor import pattern


#   1.  defining the parameters
root        = dp.defaultRootFolder
radarFolder = root + 'data/1may2014/RADARCV/'
radarPath   = root + "data/1may2014/RADARCV/COMPREF.20140501.1200.0p03.bin"
wrfFolder   = root + "data/1may2014/WEPS/201405010000/"
numberOfFramesPerModel  = 25
wrfHeight   = 201
wrfWidth    = 183
lowerLeft = (20.5, 118.0)
upperRight= (26.5, 123.46)

#   1a. setting up
wrfPathList = os.listdir(wrfFolder)
wrfPathList = [v for v in wrfPathList if ".dat" in v and "wrf" in v]   #trimming
dbz         = pattern.DBZ

#   1a1.do this once only
"""
from armor.taiwanReliefData import convertToGrid as cg
y=cg.main(files=['100','1000','2000','3000', 'Coast'], width=wrfWidth-1, height=wrfHeight-1, 
                lowerLeft=(lowerLeft[1], lowerLeft[0]),     # some peculiarities in early codes
                upperRight=(upperRight[1], upperRight[0]),
                folder=root+"python/armor/taiwanReliefData/", 
                suffix=".DAT", 
                #suffix=".txt", 
                outputFolder=radarFolder, dilation=0)

y2=cg.main(files=['100','1000','2000','3000', 'Coast'], width=wrfWidth-1, height=wrfHeight-1, 
                lowerLeft=(lowerLeft[1], lowerLeft[0]),     # some peculiarities in early codes
                upperRight=(upperRight[1], upperRight[0]),
                folder=root+"python/armor/taiwanReliefData/", 
                suffix=".DAT", 
                #suffix=".txt", 
                outputFolder=wrfFolder, dilation=0)

"""
#   1b. test
a       = dbz(dataPath=radarPath, 
             lowerLeftCornerLatitudeLongitude =lowerLeft,
              upperRightCornerLatitudeLongitude =upperRight,
               coastDataPath=radarFolder+"taiwanCoast.dat", )
a.load()
a.showWithCoast()

wrfs    = dbz(dataPath=wrfFolder+wrfPathList[0])  # adjust it here
wrfs.load(height=wrfHeight*numberOfFramesPerModel*2, width=wrfWidth)
modelLabel  = wrfs.dataPath[-6:-4]
#wrfFrames = [0]*26    # model count starts from 1
wrfFrames  = [0]
for i in range(numberOfFramesPerModel):
#for i in range(numberOfFramesPerModel*2):
    w = dbz(name="WRF"+ modelLabel + "_T" + str(i+1),           # model count starts from 1
             dataTime="NoneGiven",
             outputPath ="",imagePath="",
             coordinateOrigin="default",
              coastDataPath=wrfFolder+"taiwanCoast.dat", 
              lowerLeftCornerLatitudeLongitude =lowerLeft,
              upperRightCornerLatitudeLongitude =upperRight,
              )
    w.matrix   = wrfs.matrix[i*2*wrfHeight:(i*2+1)*wrfHeight, :]
    #w.matrix   = wrfs.matrix[i*wrfHeight:(i+1)*wrfHeight, :]
    w.showWithCoast()
    wrfFrames.append(w)
#   2.  reading the data
#   3.  processing
#       a.  read the data one-by-one
#       b.  split the data files and compare
#       c.  compare the matching and record
#   4.  output the final result


