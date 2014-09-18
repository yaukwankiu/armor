#   attempting the classify the charts, after armor/tests/imageToDataTest3.py
#   Plan:   1. compute features and store them
#           2. classify
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
inputFolder  = dp.defaultImageDataFolder + 'charts2-allinone-/'
imageFolder  = dp.root  + 'labLogs2/charts2_extracted/'
outputFolder = dp.root + 'labLogs2/charts2_features/'
try:
    os.makedirs(outputFolder)
except:
    print outputFolder, 'exists'

N   = 500
#L   = os.listdir(inputFolder)
L   = os.listdir(imageFolder)
L.sort()
print len(L)
print L[:10]

R   = np.random.random(N)
R   = (R*len(L)).astype(int)
R   = [L[v] for v in R]
R[:10]
#R   = [l[:4] + l[5:7] + l[8:10] + '.' + l[11:15] for l in R]
R[:10]
R   = [dbz(v) for v in R]
R[:10]
##############
#   test case
a = R[0]
print a.dataTime
a.loadImage(rawImage=True)
a.show()
#
a.loadImage()
a.show()
#
a1  = a.connectedComponents()
a2  = a.above(51).connectedComponents()
a1.show(block=True)
a2.show(block=True)
#   get the components
M1  = a1.matrix.max()
M2  = a2.matrix.max()
components1 = [(a1.matrix==v).sum() for v in range(M1+1)]
components2 = [(a2.matrix==v).sum() for v in range(M2+1)]
#components1 = sorted([(a1.matrix==v).sum() for v in range(M1+1)][1:], reverse=True)
#components2 = sorted([(a2.matrix==v).sum() for v in range(M2+1)][1:], reverse=True)
#components1 = [v for v in components1 if v>=100]
#components2 = [v for v in components2 if v>=10]
print sorted(components1, reverse=True)[1:]
print sorted(components2, reverse=True)[1:]
#   get the moments
from armor.geometry import moments as mmt
HuPowers = np.array([2., 4., 6., 6., 12., 8., 12.])
HuPowers = (HuPowers)**-1
moments1 = np.array([mmt.HuMoments(a1.matrix==v)**HuPowers for v in range(len(components1))])
moments2 = np.array([mmt.HuMoments(a2.matrix==v)**HuPowers for v in range(len(components2))])
print moments1
print moments2

#   defining the features
numberOfComponents = len([v for v in components1[1:] if v>=100])    # region of at least 100 pixels
volume             = a1.matrix.sum() + a2.matrix.sum()

features  = {   'dataTime'              : a.dataTime,
                'globalFeatures'        : a1.globalShapeFeatures(lowerThreshold=1, upperThreshold=51,),
                'localFeatures'         : [a1.levelSet(v).globalShapeFeatures() for v in range(len(components1))], # this includes the "background"
            }


pickle.dump(features, open('features_' + a.dataTime +'.pydump','w'))
#
###########
#   later #
###########
count = 0
for imageName in L:
    count +=1
    dataTime = imageName[:-4]
    print dataTime
    a=dbz(dataTime)
    a.loadImage()
    a.show()
    a1  = a.connectedComponents()
    a2  = a.above(51).connectedComponents()
    if count < 1:
        print 'waiting for check'
        a1.show(block=True)
        print 'waiting for check'
        a2.show(block=True)
        
    elif count==3:
        print 'it runs from now on, no more a1.show(block=True)'
    #   get the components
    M1  = a1.matrix.max()
    M2  = a2.matrix.max()
    components1 = [(a1.matrix==v).sum() for v in range(M1+1)]
    components2 = [(a2.matrix==v).sum() for v in range(M2+1)]
    print sorted(components1, reverse=True)[1:]
    print sorted(components2, reverse=True)[1:]

    #   defining the features
    numberOfComponents = len([v for v in components1[1:] if v>=100])    # region of at least 100 pixels
    volume             = a1.matrix.sum() + a2.matrix.sum()
    synopsis =  "volume: " + str(volume) +'\n'
    synopsis +=  "major components: " + str(sorted(components1, reverse=True)[1:])
    print synopsis
    features  = {   'dataTime'              : a.dataTime,
                    'globalFeatures'        : a1.globalShapeFeatures(lowerThreshold=1, upperThreshold=51,),
                    'localFeatures'         : [a1.levelSet(v).globalShapeFeatures() for v in range(len(components1))],
                    'synopsis'              : synopsis    ,
                }


    pickle.dump(features, open(outputFolder+'features_' + a.dataTime +'.pydump','w'))





    
"""
for a in R:
    a.imagePath = outputFolder+a.dataTime+'.png'
    if os.path.exists(a.imagePath):
        continue
    a.loadImage()
    b = a.copy()
    b.loadImage(rawImage=True)
    plt.subplot(121)
    plt.imshow(b.matrix, origin='lower')
    plt.subplot(122)
    plt.imshow(a.matrix, origin='lower')
    plt.title(a.dataTime)
    plt.savefig(a.imagePath)
    plt.show(block=False)
    print 'sleeping 2 seconds'
    time.sleep(2)
    if N>=100:
        a.matrix=np.array([0])  #free up some memory
"""
