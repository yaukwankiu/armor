#   attempting the classify the charts, after armor/tests/imageToDataTest3.py
#   this is the loop version of imageToTest5.py
#   Plan:   1. compute features and store them
#          *2. classify
#                   - basically, put all of the feature vectors in an array and perform k-means or others such as DBSCAN (once i know how to do it)
#           3. display

#
import os
import time
import pickle
import numpy as np
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
imageFolder  = dp.defaultImageDataFolder + 'charts2-allinone-/'
inputFolder  = dp.root  + 'labLogs2/charts2_features/'
outputFolder = dp.root + 'labLogs2/charts2_classification_local/'
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

k =  8  # k for k-means
N = 6   # number of images to be tested
block= False
featureMatrix=0         # initialisation
featureRowToShapeLabel = {}
#featureMatrix = np.array([])

for i in range(N):
    print "\n============================================================="
    print 'sample:', i
    a           = dbz(dataTime=L[i][9:22])
    print a.dataTime
    a.loadImage(rawImage=True).show()
    time.sleep(1)
    a.loadImage().show()
    time.sleep(1)
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
#
#   classification
#
from scipy import cluster
print "\n======================================================"
print 'feature matrix size: ', featureMatrix.shape
time.sleep(1)
print 'clustering....'
res = cluster.vq.kmeans2(cluster.vq.whiten(featureMatrix), k=k)
#
#   display
#
print '\n======================================================='
print 'Results:'
time.sleep(1)
for j in range(k):
    print "\n-----------------------------------------------------------------\n"
    print "Cluster:", j
    ind = np.where(res[1]==j)
    for jj in ind[0]:
        dataTime, j1 = featureRowToShapeLabel[jj]
        print 'chart:', dataTime, ' / region index:', jj, 
        if block:
            print "  ... waiting"
        else:
            print ''
        if a.dataTime != dataTime:
            a   = dbz(dataTime=dataTime, name="chart2_"+dataTime).load()
            a1  = a.connectedComponents()
        a1.levelSet(jj).show(block=block)
        if not block:
            time.sleep(1)    

    
    
        
