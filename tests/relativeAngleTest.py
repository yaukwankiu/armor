from armor import pattern
from armor.geometry import frames
import numpy as np
import time
reload(pattern)

dbz=pattern.DBZ
a = pattern.a.load()
thres=0
print 'a, b,\t angle,\t aspect ratios'

L = [v for v in range(200, 950, 10) if v%100<60]
N = len(L)

for i in range(20):
    v1,v2  = (np.random.random(2)*N).astype(int)
    #print v1, v2,
    a = dbz('20120612.0'+str(L[v1])).load(verbose=False)
    b = dbz('20120612.0'+str(L[v2])).load(verbose=False)

    theta = round(a.getRelativeAngle(b, threshold=thres),3)
    r0, r1 = a.getAspectRatios(b, threshold=thres).round(3)
    print a.dataTime, b.dataTime, '\t', theta, '\t', r0, r1
    c=a.copy()
    c.matrix = np.ma.hstack([a.matrix, b.matrix])
    c.imagePath = 'testing/' + str(time.time())+a.dataTime + "_" + b.dataTime + '.png'
    c.name = '0'+str(L[v1]) + '/' + '0'+str(L[v2]) + '\ntheta, r0, r1: ' + str(theta) + ', ' + str(r0) + ', ' + str(r1)
    c.saveImage()
    #c.show()
    #time.sleep(1)