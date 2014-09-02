#from armor import pattern
import numpy as np
from armor import objects4 as ob

may = ob.may2014
a = may('20140519.1830')[0]
a.load().show()

a1 = a.above(35)
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

