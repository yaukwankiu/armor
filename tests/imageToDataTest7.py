#   attempting the classify the charts, after armor/tests/imageToDataTest3.py
#   this is the loop version of imageToTest5.py
#   Plan:   1. compute features and store them
#          *2. classify
#                   - basically, put all of the feature vectors in an array and perform k-means or others such as DBSCAN (once i know how to do it)
#           3. display
#
sleepTime = 1800
import time
time.sleep(sleepTime)
import os
import time
import pickle
import numpy as np
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
imageFolder  = dp.defaultImageDataFolder + 'charts2-allinone-/'
inputFolder  = dp.root  + 'labLogs2/charts2_features0/'
outputFolder = dp.root + 'labLogs2/charts2_classification_local/'
timeStamp   = str(int(time.time()))
logFilePath = outputFolder + 'log_' + timeStamp + '.log.txt'
resultFilePath  = outputFolder + 'result_' + timeStamp + '.pydump'
try:
    os.makedirs(outputFolder)
except:
    print outputFolder, 'exists'
    
L = os.listdir(inputFolder)
L.sort()
len(L)
L[:10]
L[0][9:22]
#L = [v[9:22] for v in L]

timeString = str(int(time.time()))
k =  60 # k for k-means
N =  1000 # number of images to be tested
stepSize = len(L)//N  # N is supposed to be smaller than len(L) or else we will have overflow
open(logFilePath,'a').write('k=' + str(k) + '\nN='+str(N) + '\n\nData:\n')
block= False
display=False
throttle=0.01
featureMatrix=0         # initialisation
featureRowToShapeLabel = {}
#featureMatrix = np.array([])

for i in range(0, len(L),stepSize):
    print "\n============================================================="
    print 'sample:', i
    a           = dbz(dataTime=L[i][9:22])
    print a.dataTime
    open(logFilePath,'a').write(a.dataTime+'\n')
    a.loadImage(rawImage=True)
    if display:
        a.show()
    time.sleep(throttle)
    a.loadImage()
    a.show()
    time.sleep(throttle)
    a1          = a.connectedComponents()

    features    = pickle.load(open(inputFolder+L[i],'r'))
    lf          = features['localFeatures']
    #
    #   constructing the feature matrix
    #
    for j in range(len(lf)):
        # key line below:
        #fmRow = np.array([np.log10(lf[j]['volume'])] + (lf[j]['centroid']/10).tolist() + [np.log(v) for v in lf[j]['HuMoments']] + [lf[j]['numberOfComponents']])
        fmRow = np.array([(lf[j]['volume'])**.5] + (lf[j]['centroid']/10).tolist() + [np.log(v) for v in lf[j]['HuMoments']] + [lf[j]['numberOfComponents']])
        inds          = np.where(np.isnan(fmRow))
        #fmRow[inds]      = -99
        fmRow[inds]      = 0.
        inds          = np.where(np.isinf(fmRow))
        #fmRow[inds]      = -999
        fmRow[inds]      = 0.
        print fmRow
        try:
            featureMatrix = np.vstack([featureMatrix, fmRow])
            featureRowToShapeLabel[len(featureMatrix)-1] = (a.dataTime, j)
            print "feature level", len(featureMatrix)-1, ":", a.dataTime, 'shape label', j
        except:
            featureMatrix = fmRow
            featureRowToShapeLabel[0] = (a.dataTime, j)
            print "feature level 0:", a.dataTime, 'shape label', j
open(logFilePath,'a').write('\n===========================\nFeature matrix:\n'+str(featureMatrix))
#
#   classification
#
from scipy import cluster
print "\n======================================================"
print 'feature matrix size: ', featureMatrix.shape
time.sleep(throttle)
print 'clustering....'
res = cluster.vq.kmeans2(cluster.vq.whiten(featureMatrix), k=k)
pickle.dump(res, open(resultFilePath,'a'))
#
#   display
#
print '\n======================================================='
print 'Results:'
time.sleep(throttle)
os.makedirs(outputFolder+timeString+"__k%d__N%d" %(k, N))
for j in range(k):
    print "\n-----------------------------------------------------------------\n"
    print "Cluster:", j
    open(logFilePath,'a').write('\n-------------\n')
    open(logFilePath,'a').write('Cluster:' + str(j) + '\n')
    ind = np.where(res[1]==j)
    for jj in ind[0]:
        dataTime, j1 = featureRowToShapeLabel[jj]
        print 'chart:', dataTime, ' / region index:', j1, 
        open(logFilePath,'a').write('chart:' + dataTime + ' / region index:' + str(j1) + '\n')
        if block:
            print "  ... waiting"
        else:
            print ''
        if a.dataTime != dataTime:
            a   = dbz(dataTime=dataTime, name="chart2_"+dataTime).load()
            a1  = a.connectedComponents()
        if display:
            a1.levelSet(j1).show(block=block)
        a1.levelSet(j1).saveImage(outputFolder + timeString + "__k%d__N%d/cluster%d_%s_region%d.png"% (k, N, j, dataTime, j1)) 
        if not block:
            time.sleep(throttle)    

    
    
        
