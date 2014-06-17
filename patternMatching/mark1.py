"""
mark1.py
ALGORITHM:
    moment-normalised correlation
USE:
cd [.. FILL IN YOUR ROOT DIRECTORY HERE ..]/ARMOR/python/
python
from armor.patternMatching import mark1
x=mark1.main(verbose=True)

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
outputFolder    = root + "data/1may2014/"
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

a.name  = a.dataPath.split('/')[-1][8:21]
##   defining the functions
#   reading the data

def read1Wrf(wrfPath=wrfPathList[0], rawReturn=False):
    wrfData     = dbz(dataPath=wrfFolder+wrfPath)  
    wrfData.load(height=wrfHeight*numberOfFramesPerModel*2, width=wrfWidth)
    if rawReturn:
        return wrfData
    modelLabel  = wrfData.dataPath[-6:-4]

    wrfFrames   = []
    for i in range(numberOfFramesPerModel):
    #for i in range(numberOfFramesPerModel*2):
        w = dbz(name="WRF"+ modelLabel + "_T" + str(i),           # model count starts from 1
                 dataTime="NoneGiven",
                 outputPath ="",imagePath="",
                 coordinateOrigin="default",
                  coastDataPath=wrfFolder+"taiwanCoast.dat", 
                  lowerLeftCornerLatitudeLongitude =lowerLeft,
                  upperRightCornerLatitudeLongitude =upperRight,
                  )
        w.matrix   = wrfData.matrix[(i*2)*wrfHeight:(i*2+1)*wrfHeight, :]
        wrfFrames.append(w)
    return wrfFrames

#   scoring

def corr(a, b):
    #just a wrapper
    return a.corr(b)
    
#   3.  processing
#       c.  compare the matching and record
def matching(a=a, wrfFolder=wrfFolder, verbose=False):
    count   = 0
    a.load()
    wrfPathList=os.listdir(wrfFolder)
    wrfPathList = [v for v in wrfPathList if ".dat" in v and "wrf" in v]   #trimming
    scores  = []
    for wrfPath in wrfPathList:
        #   read the data one-by-one + split the data files
        wrfFrames   = read1Wrf(wrfPath=wrfPath)
        for w in wrfFrames:
            count +=1
            score = corr(a, w)   #   key line
            scores.append({'radar':a.name, 'wrf': w.name,
                           'score': score
                           })
            if verbose:
                print count, a.name, "v", w.name, ":",  score
    #ordering the results
    scores.sort(key=lambda v:v['score'], reverse=True)
    return scores

#   result checking

def get1frame(model="02",T=6, wrfFolder=wrfFolder):
    fileName = [v for v in os.listdir(wrfFolder) if 'e'+model in v][0]
    wrfFrames = read1Wrf(wrfPath=fileName)
    w   = wrfFrames[T]
    return w

#   4.  output the final result
#   test run

def main(**kwargs):
    scores = matching(a, wrfFolder, **kwargs)
    outputPath  = outputFolder + str(int(time.time())) + "matchingOutput_" + a.name + ".txt"
    print "\n========\nTop 10 matches"
    print "\n".join([str(v) for v in scores[:10]])
    print "writing to file: ", outputPath
    open(outputPath,'w').write(" ,\n".join([str(v) for v in scores]))
    return scores

