import time
import os
import re
import pickle
import numpy as np
from armor import pattern
dbz = pattern.DBZ
plt = pattern.plt
classificationResultsFileName = 'log_1411289056.log.txt'
folder   = pattern.dp.root + 'labLogs2/charts2_classification_local/'

def display(resultString, title1="", title2="", block=True, minBlockSize=1):
    """chart:20140525.0400 / region index:6"""
    #plt.close()
    rs = resultString
    dataTime = rs[6:19]
    regionNumber = int(rs.split(":")[-1])
    a = dbz(dataTime)
    b = a.copy()
    a.loadImage(rawImage=True)
    b.loadImage(rawimage=False)
    b1 = b.connectedComponents().levelSet(regionNumber)
    region = b1.getRegionForValue(1)
    if region[2]*region[3] < minBlockSize:
        return "block too small!!"
    print '* '
    print '* Block dimensions:', region[2:4]
    print "*"
    b.drawRectangle(*region, newObject=False)
    #b.drawCross(*region[0:2], newObject=False, radius=30)
    #print 'b.imageTopDown:',b.imageTopDown #debug
    plt.close()
    a.showWith(b, block=block, title1=title1, title2=title2)


#display('chart:20140525.0400 / region index:6')

def readFile(filePath=folder+classificationResultsFileName):
    x = open(filePath,'r').read()
    y = x.split('\n')
    N = len(y)
    ind = [v for v in range(N) if "Cluster:" in y[v]]
    clustersList = []    
    for i in range(len(ind)):
        try:
            z = y[ind[i] : ind[i+1]]
        except IndexError:
            z = y[ind[i]:]
        z = [v for v in z if 'chart:' in v]
        clustersList.append(z)

    return clustersList

def main(loops=10, samples=3, filePath=folder+classificationResultsFileName, throttle=1., block=True, minBlockSize=100):
    clustersList = readFile(filePath)
    N = len(clustersList)
    R = (np.random.random(loops) * N).astype(int).tolist()
    for i in R:
        print "\n***************************************************\n"
        print 'Showing the %dth Cluster:' %i 
        print "cluster size: ", len(clustersList[i])
        time.sleep(throttle)
        if len(clustersList[i])==0:
            continue
        for count,j in  enumerate((np.random.random(samples) * len(clustersList[i])).astype(int).tolist()):
            print '\n=========================\n'
            print count, 'Showing the %dth sample from the %dth cluster:' %(j, i), '\t', clustersList[i][j]
            print 
            display(clustersList[i][j], block=block, minBlockSize=minBlockSize, title2='%d, Cluster %d, Sample %d' %(count, i, j))
            if not block:
                time.sleep(1)

if __name__ =="__main__":
    main(block=False)
