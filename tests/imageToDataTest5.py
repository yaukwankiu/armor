#   attempting the classify the charts, after armor/tests/imageToDataTest3.py
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
block=True
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

###############
#   test case
k =  4  # k for k-means
#featureMatrix = np.array([])
i=0
a           = dbz(dataTime=L[i][9:22])
print a.dataTime
a.loadImage(rawImage=True).show()
time.sleep(1)
a.loadImage().show()
a1          = a.connectedComponents()

features    = pickle.load(open(inputFolder+L[i],'r'))
lf          = features['localFeatures']
#
#   constructing the feature matrix
#
featureMatrix=0
for j in range(len(lf)):
    #fmRow = np.array([np.log10(lf[j]['volume'])] + (lf[j]['centroid']/10).tolist() + [np.log(v) for v in lf[j]['HuMoments']] + [lf[j]['numberOfComponents']])
    fmRow = np.array([(lf[j]['volume'])**.5] + (lf[j]['centroid']/10).tolist() + [np.log(v) for v in lf[j]['HuMoments']] + [lf[j]['numberOfComponents']])
    inds          = np.where(np.isnan(fmRow))
    fmRow[inds]      = -99
    inds          = np.where(np.isinf(fmRow))
    fmRow[inds]      = -999
    print fmRow
    try:
        featureMatrix = np.vstack([featureMatrix, fmRow])
    except:
        featureMatrix = fmRow
#
#   classification
#
from scipy import cluster
res = cluster.vq.kmeans2(cluster.vq.whiten(featureMatrix), k=k)
#
#   display
#
for j in range(k):
    print "cluster:", j
    ind = np.where(res[1]==j)
    for jj in ind[0]:
        print 'region index:', jj, 
        if block:
            print "  ... waiting"
        else:
            print ''
        a1.levelSet(jj).show(block=block)
        if not block:
            time.sleep(1)    

    
    
    
