"""
mark3.py
    switched to wepsFolder - the folder containing all forecasts made at different startTimes
    fixed wrfPathList problem
    
ALGORITHM:
    moment-normalised correlation
USE:
cd [.. FILL IN YOUR ROOT DIRECTORY HERE ..]/ARMOR/python/
python
from armor.patternMatching import mark5
reload(mark5)
x=mark5.main(verbose=True, saveImage=True,  display=False)  #<-- change it to saveImage=False to save space

x=mark5.main(verbose=True, saveImage=False,  display=False)  #<-- change it to saveImage=False to save space


x=mark5.main(verbose=True, saveImage=False,  key2="e03", display=False)  #<-- change it to saveImage=False to save space


"""
#   0.  imports
#   1.  defining the parameters
#   2.  reading the data
#   3.  processing
#   4.  output

#   0.  imports
import time, datetime, os, re
import numpy as np
import matplotlib.pyplot as plt
from armor import defaultParameters as dp
from armor import pattern
from armor.geometry import transformedCorrelations as tr


#   1.  defining the parameters
root        = dp.defaultRootFolder
radarFolder = root + 'data/1may2014/RADARCV/'
radarPath   = root + "data/1may2014/RADARCV/COMPREF.20140501.1200.0p03.bin"
wepsFolder  = root + "data/1may2014/WEPS/"  # folder for all forecasts made at various times
wrfFolder   = root + "data/1may2014/WEPS/201405010000/"
#outputFolder    = root + "data/1may2014/"
outputFolder    = root+ "labLogs2/patternMatching/"
numberOfFramesPerModel  = 25
wrfHeight   = 201
wrfWidth    = 183
lowerLeft = (20.5, 118.0)
upperRight= (26.5, 123.46)


#   1a. setting up
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
wrfPathList = os.listdir(wrfFolder)
wrfPathList = [wrfFolder+v+"/" for v in wrfPathList if ".dat" in v and "wrf" in v]   #trimming

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
a0       = dbz(dataPath=radarPath, 
             lowerLeftCornerLatitudeLongitude =lowerLeft,
              upperRightCornerLatitudeLongitude =upperRight,
               coastDataPath=radarFolder+"taiwanCoast.dat", )

a0.name  = a0.dataPath.split('/')[-1][8:21]
dT = re.findall(r'\d\d\d\d', radarPath.split('/')[-1])
a0.dataTime = dT[0] + dT[1] + '.' + dT[2]

##   defining the functions

#   get all wrf folders

def getRadarDBZ(radarPath=radarPath):
    aName  = radarPath.split('/')[-1][8:21]
    dT  = re.findall(r'\d\d\d\d', radarPath.split('/')[-1])
    dT  = dT[0] + dT[1] + '.' + dT[2]
    a   = dbz(name=aName,
              dataPath=radarPath, 
              dataTime=dT,
              lowerLeftCornerLatitudeLongitude =lowerLeft,
              upperRightCornerLatitudeLongitude =upperRight,
              coastDataPath=radarFolder+"taiwanCoast.dat", )
    return a


def getWrfFolders(wepsFolder=wepsFolder, a="", key1="", maxTimeDiff=6., reportLength=72):
    wrfFolders  = os.listdir(wepsFolder)
    if a=="":
        maxDataTime="99999999.9999"
        minDataTime="00000000.0000"
    else:
        maxDataTime     = a.getDataTime(a.datetime()-datetime.timedelta(1.*maxTimeDiff/24))
        maxDataTime     = maxDataTime[:8] + maxDataTime[9:]
        minDataTime     = a.getDataTime(a.datetime()-datetime.timedelta(1.*reportLength/24))    #2014-06-04
        minDataTime     = minDataTime[:8] + minDataTime[9:]
    wrfFolders  = [wepsFolder+v+"/" for v in wrfFolders if v<maxDataTime and v>=minDataTime]
    wrfFolders  = [v for v in wrfFolders if key1 in v]
    return wrfFolders

def getWrfFrameIndices(a=a0, wrfFolder=wrfFolder, maxTimeDiff=6, timeInterval=3, verbose=False):
    #   2014-06-01
    #   to get the frame indices in a list from a.dataTime and startTime as recorded in the wrfFolder
    minDataTime = a.datetime(dh=-maxTimeDiff)
    maxDataTime = a.datetime(dh= maxTimeDiff)
    wrfStartTime = wrfFolder.split('/')[-2]
    wrfStartTime = wrfStartTime[:8] + '.' + wrfStartTime[8:]
    wrfStartTime = a.datetime(wrfStartTime)
    timeDiff    = a.datetime() - wrfStartTime
    hoursDiff   = (timeDiff.days * 86400 + timeDiff.seconds)/3600
    #return hoursDiff
    startIndex  = int(np.ceil (1.*(hoursDiff-maxTimeDiff)/timeInterval))
    endIndex    = int(np.floor(1.*(hoursDiff+maxTimeDiff)/timeInterval))
    if verbose:
        print "wrfStartTime, timeDiff, hoursDiff"#debug
        print wrfStartTime  #debug
        print timeDiff
        print hoursDiff#debug
        print "startIndex, endIndex"
        print startIndex, endIndex
    return startIndex, endIndex

#   reading the data
def read1Wrf(wrfPath=wrfPathList[0], rawReturn=False):
    wrfData     = dbz(dataPath=wrfPath)  
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

#   scoring key lines

def getScore(a, b, weights=[1.0, 0.2, 0.1, 0.1, ], thres=0):
    #just a wrapper
    corr= a.gaussianCorr(b, sigma=0, sigmaWRF=0, thres=0, showImage=False, saveImage=False, outputFolder='')
    angle = a.getRelativeAngle(b, threshold=thres, returnType='radian')
    r0, r1 = a.getAspectRatios(b, threshold=thres)

    score = weights[0]*corr - weights[1]*abs(angle) - weights[2]*abs(np.log(r0)) - weights[3]*abs(np.log(r1))
    print a.name, b.name, '\t', score
    return score
    
#   3.  processing
#       c.  compare the matching and record
def matching(a=a0, wepsFolder=wepsFolder, thres=0, maxTimeDiff=6, timeInterval=3, key1="", key2="",
            verbose=False, display=False, saveImage=False):
    count   = 0
    a.load()
    a.truncate(thres, newObject=False)
    if verbose:
        print "================================="
        print 'name, dataTime:'
        print a.name
        print a.dataTime
    #   debug   ################################################################
    if display:
        #a.show()
        #time.sleep(1)
        tr.showArrayWithAxes(a)
    if saveImage:
        plt.close()
        tr.showArrayWithAxes(a, display=False, outputPath=outputFolder+ str(int(time.time()))+a.name+ ".png")
    #   end debug   ############################################################
    scores  = []
    wrfFolders = getWrfFolders(wepsFolder, a=a, maxTimeDiff=maxTimeDiff, key1=key1)
    for wrfFolder in wrfFolders:
        wrfPathList=os.listdir(wrfFolder)
        wrfPathList = [wrfFolder+v for v in wrfPathList if ".dat" in v and "wrf" in v]   #trimming
        wrfPathList = [v for v in wrfPathList if key2 in v]   #trimming
        wrfPathList.sort()
        if verbose:
            print "key2:", key2
            print "wrfPathList:"
            print '\n'.join([str(v) for v in wrfPathList])
        if wrfPathList == []:
            continue

        for wrfPath in wrfPathList:
            #   read the data one-by-one + split the data files
            wrfFrames   = read1Wrf(wrfPath=wrfPath)
            startIndex, endIndex = getWrfFrameIndices(a=a, wrfFolder=wrfFolder, 
                                                      maxTimeDiff=maxTimeDiff, timeInterval=timeInterval,
                                                      verbose=verbose)
            startIndex  = max(0, startIndex)
            endIndex    = min(numberOfFramesPerModel-1, endIndex)   # fixed 2014-06-11
            if verbose:
                print "================================="
                print wrfPath, "start and end indices:", startIndex, endIndex
            for w in wrfFrames[startIndex: endIndex+1]:
                w.truncate(thres, newObject=False)

                #   debug   ################################################################
                if saveImage:
                    plt.close()
                    tr.showArrayWithAxes(w, display=False,outputPath=outputFolder+ str(int(time.time()))+w.name+ ".png")
                if display:
                    #w.show()
                    #time.sleep(1)
                    plt.close()
                    tr.showArrayWithAxes(w)
                #   end debug   ############################################################

                if verbose:
                    print count, a.name, "v", w.name, ":",
                count +=1
                score = getScore(a, w, thres=thres)   #   key line
                if verbose:
                    print score
                scores.append({'radar':a.name, 
                               'score': score, 
                               'wrfFolder': wrfFolder.split('/')[-2],
                               'wrf': w.name,
                               })

    #ordering the results
    scores.sort(key=lambda v:v['score'], reverse=True)
    return scores

#   result checking

def get1frame(model="02",T=6, wrfFolder=wrfFolder):
    T = int(T)
    if isinstance(model, int):
        model = ("0"+str(model))[-2:]
    fileName = [v for v in os.listdir(wrfFolder) if 'e'+model in v][0]
    wrfFrames = read1Wrf(wrfPath=fileName)
    w   = wrfFrames[T]
    return w

def getOutputStrings(scores, timeInterval=3, verbose=True):
    #   timeInterval = time interval between successive times of forecast within a WRF
    outputStrings    = ["# model no., time forecast made, time of forecast, delta time, score\n"]

    for scoreRecord in scores:
        # from 
        #       {'wrf': 'WRF02_T6', 'radar': '20140501.1200', 'score': 0.50716670859396218, 'wrfFolder': '201405010000'} ,
        # to
        #   # model no., time forecast made, time of forecast, delta time, score
        #'  22  20140312_1200  20140312_2100   9  0.9698248506'

        #   1. get the info
        modelNo, deltaTime = re.findall(r'\d+', scoreRecord['wrf'])
        timeForecastMade    = scoreRecord['wrfFolder']
        score               = scoreRecord['score']
        #   2. convert the format
        modelNo     = ("  "+modelNo)[-4:]
        deltaTime   = timeInterval * int(deltaTime)
        timeOfForecast  = a0.datetime(timeForecastMade) + datetime.timedelta(1./24*deltaTime)    # a0 = global object
        timeOfForecast  = "  " +str(timeOfForecast.year) +       ('0'+str(timeOfForecast.month))[-2:] +\
                           ('0'+str(timeOfForecast.day ))[-2:]  +\
                      "_" +('0'+str(timeOfForecast.hour))[-2:] + ('0'+str(timeOfForecast.minute))[-2:] 
        timeForecastMade= "  " + timeForecastMade.replace(".","_")
        deltaTime   = ("   "+str(deltaTime))[-4:]
        score       = "  " + str(score)
        outputLine  = modelNo   + timeForecastMade + timeOfForecast + deltaTime + score
        outputStrings.append(outputLine)
        if verbose:
            print '\n'.join(outputStrings[:10])
    return outputStrings
        
#   4.  output the final result
#   test run

def main(radarPath=radarPath, wepsFolder=wepsFolder, key1="", key2="", **kwargs):
    time0=time.time()
    a   = getRadarDBZ(radarPath)
    print "\n==============================================================="
    print "comparing", a.name, a.dataTime
    print "to", wepsFolder
    scores = matching(a, wepsFolder,key1=key1, key2=key2, **kwargs)
    outputPath  = outputFolder + str(int(time.time())) + "matchingOutput_" + a.name + ".txt"
    outputStrings = getOutputStrings(scores, timeInterval=3)
    print "\n========\nTop 10 matches"
    print "\n".join([str(v) for v in outputStrings[:10]])
    print "writing to file: ", outputPath
    open(outputPath,'w').write("\n".join([str(v) for v in outputStrings]))
    print '\nTime spent:', time.time()-time0, 'seconds'
    return scores

