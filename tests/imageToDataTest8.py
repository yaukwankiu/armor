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

def makeImage(resultString, title1="", title2="", cmap2='jet',block=False, minBlockSize=1, display=True, outputFolder=""):
    """chart:20140525.0400 / region index:6"""
    #plt.close()
    rs = resultString
    dataTime = rs[6:19]
    regionNumber = int(rs.split(":")[-1])
    a = dbz(dataTime)
    b = a.copy()
    a.loadImage(rawImage=True)
    b.loadImage(rawimage=False)
    b.cmap=cmap2
    b1 = b.connectedComponents().levelSet(regionNumber)
    b.matrix += b1.matrix*600
    b.setMaxMin()
    region = b1.getRegionForValue(1)
    if region[2]*region[3] < minBlockSize:
        return "block too small!!"
    imagePath = outputFolder+title2+'_'+dataTime+"_"+ str(region)+'.jpg'
    if os.path.exists(imagePath):
        print 'image exists! - ', dataTime 
        return 0

    print '* '
    print '* Block dimensions:', region[2:4]
    print "*"
    b.drawRectangle(*region, newObject=False)
    #b.drawCross(*region[0:2], newObject=False, radius=30)
    #print 'b.imageTopDown:',b.imageTopDown #debug
    plt.close()
    if outputFolder!="":
        b.saveImage(imagePath=imagePath)
    if display:
        a.showWith(b, block=block, title1=title1, title2=title2)
    return b

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

def main(loops=10, samples=3, folder=folder, classificationResultsFileName=classificationResultsFileName, throttle=1., 
            block=False, minBlockSize=100, randomise=True, outputFolder="", display=True):
    filePath = folder+classificationResultsFileName
    clustersList = readFile(filePath)
    k = len(clustersList)
    if outputFolder=="auto":
        outputFolder=folder+classificationResultsFileName[4:-8]+'_k' +str(k) + '/'
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        
    if loops <=0:
        loops=k
    if randomise:
        R = (np.random.random(loops) * k).astype(int).tolist()
    else:
        R = range(k)
    for i in R:
        print "\n***************************************************\n"
        print 'Showing the %dth Cluster:' %i 
        print "cluster size: ", len(clustersList[i])
        time.sleep(throttle)
        if len(clustersList[i])==0:
            continue
        if samples>0:
            jList = enumerate((np.random.random(samples) * len(clustersList[i])).astype(int).tolist())
        else:
            jList = enumerate(range(len(clustersList[i])))
        for count,j in jList:
            print '\n=========================\n'
            print count, 'Showing the %dth sample from the %dth cluster:' %(j, i), '\t', clustersList[i][j]
            print 
            #display(clustersList[i][j], block=block, minBlockSize=minBlockSize, title2='%d, Cluster %d, Sample %d' %(count, i, j))
            makeImage(clustersList[i][j], block=block, minBlockSize=minBlockSize, title2='Cluster_%d' % i, outputFolder=outputFolder, display=display )
            if not block:
                time.sleep(throttle)

if __name__ =="__main__":
    main(block=False)
    main(block=False, display=False, classificationResultsFileName='log_1412738213.log.txt' ,outputFolder='auto', randomise=False, samples=-1 )