#   attempting the classify the charts, after armor/tests/imageToDataTest3.py
#   Plan:   1. compute features and store them
#           2. classify
#           3. display

#
import os
import time
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
###
L   = os.listdir(inputFolder)
print len(L)
R   = np.random.random(N)
R   = (R*len(L)).astype(int)
R   = [L[v] for v in R]
R[:10]
R   = [l[:4] + l[5:7] + l[8:10] + '.' + l[11:15] for l in R]
R[:10]
R   = [dbz(v) for v in R]
R[:10]
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
