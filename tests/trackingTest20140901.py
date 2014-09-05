#from armor import pattern
import numpy as np
from . import objects4 as ob
from . import defaultParameters as dp

may = ob.may2014
a = may('20140519.1830')[0]
a.load().show()

#a1 = a.above(35)
a1 = a.above(40)

x = a1.connectedComponents()
x.show()

print x.matrix.max()

N = x.matrix.max()
for i in range(N):
    size= x.levelSet(i).matrix.sum()
    if size>10 and size<100000:
        print i, ":", size, "||",

S = [v for v in range(N) if x.levelSet(v).matrix.sum()>10 and x.levelSet(v).matrix.sum()<100000]
print S

centroids = [x.levelSet(v).getCentroid().astype(int) for v in S]    

a.load()
for i, j in centroids:
    a.drawRectangle(max(0, i-30), max(0,j-30), min(880-30-i, 60), min(920-30-j, 60), newObject=False)

a.show()

a.load()
y = a.getKmeans(threshold=20, k=np.vstack(centroids), minit='matrix')
a2 = y['pattern']

N2 = a2.matrix.max()

for i in range(int(N2)):
    print i, a2.getRegionForValue(i)
    a.drawRectangle(*a2.getRegionForValue(i), newObject=False)
    
a.show()

import time

a.load()
a.show()
for i in range(int(N2)):
    print i, a2.getRegionForValue(i)
    a3 = a.getWindow(*a2.getRegionForValue(i))
    a3.matrix.mask = (a3.matrix<-dp.defaultMissingDataThreshold) #hack
    #print a3.matrix.mask.sum()
    #print a3.matrix.sum(), a3.matrix.shape
    #a3.show()
    #time.sleep(2)
    print a3.matrix.sum()
    print a3.matrix.shape[0]*a3.matrix.shape[1]*20 
    #if a3.matrix.sum()< 10000 or (a3.matrix.shape[0]*a3.matrix.shape[1]*10 > a3.matrix.sum()):
    if a3.matrix.sum()< 30000 or (a3.matrix.shape[0]*a3.matrix.shape[1]* > a3.matrix.sum()):
 
    #if (a3.matrix.shape[0]*a3.matrix.shape[1]*20 < a3.matrix.sum()):
        pass
    else:
        a.drawRectangle(*a2.getRegionForValue(i), newObject=False)

a.show()

