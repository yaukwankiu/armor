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


def constructOutputString(dss, filteringAlgorithm, matchingAlgorithm, timeString, results, remarks="-", **kwargs):
    x   = "ARMOR filter and matching algorithm testing"
    x   += "\nTime start:  "            + time.asctime()
    x   += "\nReferencetimeString:  "   + timeString
    x   += "\nFilter:  "                + str(filteringAlgorithm)
    x   += "\nMatching Algorithm:  "    + str(matchingAlgorithm)
    x   += "\nOther Arguments:  "       + str(kwargs)
    x   += "\nRemarks:  "               + remarks
    x   += "\n"                         + "" 
    x   += "\nTop Results:   "
    x   += "\n1:  "                     + str(results[0])
    x   += "\n2:  "                     + str(results[1])
    x   += "\n3:  "                     + str(results[2])
    x   += "\n4:  "                     + str(results[3])
    x   += "\n5:  "                     + str(results[4])
    x   += "\n..................................................\n"
    x   += "\nAll Results:  "           + str(results)
    return x

def pipeline(dss=dss,
            filteringAlgorithm      = filters.gaussianFilter,
            filteringAlgorithmArgs   = {'sigma':20},
            matchingAlgorithm       = algorithms.plainCorr,
            matchingAlgorithmArgs   = {'obsTime':"20130829.0300", 'maxHourDiff':7} ,
            outputFolder=dp.defaultRootFolder + "labReports/2014-03-07-filter-matching-scoring-pipeline/",
            toBackupMatrices=False,
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
    #outputFolder    =  outputFolder + timeString + "-" + matchingAlgorithmArgs['obsTime'] + "_hl.4-kh.3-yl.3/"      # 2014-03-18
    outputFolder    =  outputFolder + timeString + "-" + matchingAlgorithmArgs['obsTime']  + "/"      # 2014-03-18
    os.makedirs(outputFolder)     
    diagramCount    = 0
    if toLoad:
        dss.load()
    if toBackupMatrices:
        dss.backupMatrices()
    #   filtering
    if filteringAlgorithm != "":
        dss.filtering(filteringAlgorithm, verbose=False, **filteringAlgorithmArgs)
    #   matching
    #try:        # try clause added 18-03-2014 to create nested outputFolders
    #    results = dss.matching(matchingAlgorithm, verbose=False, outputFolder=outputFolder, **matchingAlgorithmArgs)
    #except:
    results = dss.matching(matchingAlgorithm, verbose=False, **matchingAlgorithmArgs)
    #   printing to screen
    results1 = [v['wrf']+', ' + str(v['timeShift']) + 'H;  score: ' + str(v['score']) for v in results]
    print '\n'.join(results1)
    #   saving relevant images
    obs         = dss.obs
    T   = results[0]['obsTime']
    a           = obs(T)[0]
    print '................................................................'    
    print obs.name
    print T
    print a.name
    a.backupMatrix('good_copy')
    try:
        a.drawCoast()
    except:
        pass
    a.saveImage(imagePath=outputFolder+str(diagramCount)+'.png')
    a.restoreMatrix('good_copy')
    for R in results[:5]:
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
        b.backupMatrix('good_copy')
        try:
            b.coastDataPath = a.coastDataPath
            b.drawCoast()
        except:
            pass
        b.saveImage(imagePath=outputFolder+str(diagramCount)+'.png')
        b.restoreMatrix('good_copy')

    #   end
    #   writing log file
    outputString    = constructOutputString(dss, 
                                            filteringAlgorithm=filteringAlgorithm,
                                            matchingAlgorithm=matchingAlgorithm,
                                            timeString=timeString, 
                                            results=results, 
                                            matchingAlgorithmArgs=matchingAlgorithmArgs,        # other kwargs for constructOutputString
                                            filteringAlgorithmArgs=filteringAlgorithmArgs,
                                            **kwargs)

    outputString    += "\nTime spent:  " + str(int(time.time()-time0)) + " seconds\n"
    print "writing log to file:", outputFolder+"log"+timeString+".txt"
    open(outputFolder+"log" + timeString +".txt", "w").write(outputString)
    print "time spent:", time.time() - time0
    return results1    
    

if __name__=="__main__":
    results=pipeline()








