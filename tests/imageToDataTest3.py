import os
import time
import numpy as np
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
folder  = dp.defaultImageDataFolder + 'charts2-allinone-/'
outputFolder = dp.root + 'labLogs2/charts2_extracted/'
try:
    os.makedirs(outputFolder)
except:
    print outputFolder, 'exists'

N   = 1033
###
L   = os.listdir(folder)
print "number of files:", len(L)
R   = np.random.random(N)
R   = (R*len(L)).astype(int)
R   = list(set(R))
print "len(R):", len(R)
#
R   = [L[v] for v in R]
R[:10]
R   = [l[:4] + l[5:7] + l[8:10] + '.' + l[11:15] for l in R]
R[:10]
R   = [dbz(dataTime=v, imageTopDown=True, name=v) for v in R]
R[:10]
a = R[0]
if a.imageTopDown:  # set it once and for all
    origin="upper"
else:
    origin="lower"
print "imageOrigin:",origin
print "----------------------------"
time.sleep(1)
#
for a in R:
    a.imagePath = outputFolder+a.dataTime+'.png'
    if os.path.exists(a.imagePath):
        continue
    a.loadImage()
    #a.show(block=True) #debug
    b = a.copy()
    b.loadImage(rawImage=True)
    #b.show(block=True) #debug
    #
    plt.subplot(121)
    plt.imshow(b.matrix, origin=origin)
    plt.title(a.dataTime)
    #
    plt.subplot(122)
    plt.imshow(a.matrix, origin=origin)
    plt.title("35+ features")
    #
    plt.savefig(a.imagePath)
    plt.show(block=False)
    print 'sleeping 2 seconds'
    time.sleep(2)
    if N>=100:
        a.matrix=np.array([0])  #free up some memory
