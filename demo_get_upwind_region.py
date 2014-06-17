#============================================================================
#
# today:  separation of the map into upwind, taiwan and downwind regions
#		continued:
#           5.  define functions: shiiba regress->splitting->segmentation
30-4-2013

"""method:
1. global shiiba regression, noncfl
2. get flow direction and split the regions
"""
# 0. get the data
# 1. shiiba regress
# 2. compute the upwind region

from armor import pattern
dbz=pattern.DBZ
import numpy as np

a = pattern.a.copy()
b = pattern.b.copy()

a_shiiba_b = a.shiiba(b)


taiwan = dbz(   name    = 'taiwan 1000m contour, extended by 50km',
                dataPath= '../data_temp/relief1000Extended.mat',
                matrix  = np.zeros((881,921)) )

taiwan.load()
taiwan.show()
taiwan.backupMatrix()

taiwan.dataPath= '../data_temp/relief1000Extended.mat'
taiwan.load()
taiwan.show()

taiwan = dbz(   name    = 'taiwan 1000m contour, extended by 50km',
                dataPath= '../data_temp/relief1000Extended2.mat',
                matrix  = np.zeros((881,921)) )

taiwan.load()
taiwan.show()
taiwan.backupMatrix()

x=a_shiiba_b
x.keys()

m,n = x['mn']
U   = x['vect'].U
V   = x['vect'].V
U   += n
V   += m

#############################
# finding the upwind region
# method: use a "dotted ray" and seek the taiwan region for every pixel.  return 1
#            if found, 0 if not found.

taiwanRegion = taiwan
height, width = a.matrix.shape
upwindRegion = np.zeros((height, width))

from time import time
t0=time()
for i in range(height):
    for j in range(width):
        if a.matrix.mask[i,j]==True:
            continue
        else:
            #i_new = [i + n*V[i,j] for n in range(20) if (i + n*V[i,j]<height and i + n*V[i,j]>0)]
            #j_new = [j + n*U[i,j] for n in range(20) if (j + n*U[i,j]<width  and j + n*U[i,j]>0)]
            hit_or_miss = sum([(1-taiwanRegion.matrix.mask[i+n*V[i,j], j+n*U[i,j]]) for n in range(100) \
                                    if (i + n*V[i,j]<height and i + n*V[i,j]>0 and
                                        j + n*U[i,j]<width  and j + n*U[i,j]>0 ) ],0 )
            upwindRegion[i,j] = hit_or_miss   

timeUsed = time()-t0
print "time used:", timeUsed

UW = dbz(matrix=upwindRegion, name= a.name+"upwind region")
UW.copy().show2()

