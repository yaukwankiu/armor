"""
cd /media/TOSHIBA\ EXT/ARMOR/python/
ipython -pylab

"""
import time, datetime, os
import numpy as np
import matplotlib.pyplot as plt
from armor import defaultParameters as dp
from armor import pattern

##################
#   regridding
#from armor.dataStreamTools import kongrey as kr
#WRFstreams  = kr.constructAllWRFstreams()
#WRFstreams2  = kr.constructAllWRFstreamsRegridded()
#   end regridding
##################

from armor import pattern2 as p2
from armor.filter import filters
from armor.patternMatching import algorithms
dss = p2.kongreyDSS
#print dss.name
#print dss.obs.name
#print dss.wrfs[0].name
#wrfs    = dss.wrfs
#obs     = dss.obs
#obs[0].load()
#obs[0].show()
#dss.backupMatrices()


def constructOutputString(dss, filt, matchingAlgorithm, timeString, results, **kwargs):
    x   = "ARMOR filter and matching algorithm testing"
    x   += "\nTime:  "        + time.asctime()
    x   += "\ntimeString:  "  + timeString
    x   += "\nFilter:  "      + str(filt)
    x   += "\nMatching Algorithm:  "    + str(matchingAlgorithm)
    x   += "\nOther Arguments:  "       + str(kwargs)
    x   += "\nTop Results:   "
    x   += "\n0:  "                     + str(results[0])
    x   += "\n1:  "                     + str(results[1])
    x   += "\n2:  "                     + str(results[2])
    x   += "\n..................................................\n"
    x   += "\nAll Results:  "           + str(results)
    return x


def pipeline(dss=dss,
            filterAlgorithm         = filters.gaussianFilter,
            filterArgs              = {'sigma':20},
            matchingAlgorithm       = algorithms.plainCorr,
            matchingAlgorithmArgs   = {'obsTime':"20130829.0300", 'maxHourDiff':6} ,
            outputFolder=dp.defaultOutputFolder + "/media/TOSHIBA EXT/ARMOR/labReports/2014-03-07-filter-matching-scoring-pipeline/",
            toLoad=False, 
            **kwargs):
    ##################################################
    """analysis loop
        input:  dss - an armor.pattern2.DataStreamSet object
                filter
                matchingAlgorithm
                parameters
        return:
            ranking results
        write to file:
            ranking and other analytic results;  relevant pics
            
    """
    #parameter setup
    time0 = time.time()
    #timeString      = str(int(time.time()))[-6:]    
    timeString      = str(int(time.time()))     # i don't want any technical debt whatsoever 
    outputFolder    =  outputFolder + timeString + "/"
    os.makedirs(outputFolder)     
    diagramCount    = 0
    if toLoad:
        dss.load()
    #   filtering
    dss.filtering(filteringAlgorithm, verbose=False, **filterArgs)
    #   matching
    results = dss.matching(matchingAlgorithm, verbose=False, **matchingAlgorithmArgs)
    #   printing to screen
    results1 = [v['wrf']+', ' + str(v['timeShift']) + 'H;  score: ' + str(v['score']) for v in results]
    print '\n'.join(results1)
    #   writing log file
    outputString    = constructOutputString(dss, 
                                            filt=filters.gaussianFilter, 
                                            matchingAlgorithm=algorithms.plainCorr, 
                                            timeString=timeString, 
                                            results=results, 
                                            matchingAlgorithmArgs=matchingAlgorithmArgs,        # other kwargs for constructOutputString
                                            filterArgs=filterArgs,
                                            )

    open(outputFolder+"log" + timeString +".txt", "w").write(outputString)

    #   saving relevant images
    obs         = dss.obs
    T   = results[0]['obsTime']
    a           = obs(T)[0]
    print '................................................................'    
    print obs.name
    print T
    print a.name
    a.saveImage(imagePath=outputFolder+str(diagramCount)+'.png')
    for R in results[:3]:
        wrfName     = R['wrf']
        timeShift   = R['timeShift']
        T           = R['obsTime']
        T2          = a.datetime(dh=timeShift)
        T2          = a.getDataTime(T2) # string format
        wrf         = [w for w in dss.wrfs if w.name == wrfName][0]
        b           = wrf(T2)[0]
        
        print '.............................'
        print wrf.name
        print T2
        print b.name
        diagramCount    +=1
        b.saveImage(imagePath=outputFolder+str(diagramCount)+'.png')
    #   end
    print "time spent:", time.time() - time0
    return results1    
    

if __name__=="__main__":
    results=pipeline()








