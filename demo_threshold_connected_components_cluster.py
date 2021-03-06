# demo: threshold, find connected components, and cluster 
# date: 24-4-2013
# 
# cd /media/KINGSTON/ARMOR/python
# python
# from armor.demo_threshold_connected_components_cluster import *

import numpy as np
from matplotlib import pyplot as plt
from time import time
from armor import pattern
a=pattern.a
dbz=pattern.DBZ
from armor.geometry import components

a10 = a.threshold(10)
a10.copy().show2()

from armor.geometry import edges
m = edges.find(a10)
m2 = np.flipud(m)
plt.imshow(m2>0)
plt.show()

a10 = dbz(matrix=(m>0))
a10.vmax= a10.matrix.max()*2
a10.vmin= a10.matrix.min()*(-1.5)
a10.copy().show2()
#################################

###############################

a35 = a.threshold(35)
a35.copy().show2()

t=time(); reload(components); acomp35  = components.connected(a35.matrix.mask.astype(int)) ; t2=time()-t; print "time used: ", t2

acomp35=dbz(name = a35.name+"connected components", matrix=acomp35, vmax=acomp35.max(), vmin= -acomp35.max()//5, cmap='jet')
acomp35.copy().show2()

#ACOMP35.cmap = 'prism'
#ACOMP35.show4()

acomp35.backupMatrix()
acomp35.matrix.mask = acomp35.matrix.mask * (a10.matrix==1)   # intersect the mask with 
                                                        # 'non-edge' elements
                                                        
acomp35.matrix     += (a10.matrix==0) *99
acomp35.show4()
acomp35.cmap='prism'
acomp35.show4()

acomp35.cmap='jet'
acomp35.copy().show2()

acomp35.backupMatrix()
acomp35.restoreMatrix(0)

########
# split the regions

regions=[]
for i in range(int(acomp35.matrix.min()), int(acomp35.matrix.max())+1):
    regions.append((i, (acomp35.matrix==i).sum()))

########
# sort by descending order of size
regions.sort(key = lambda v: v[1], reverse=True)
print regions[:20]

########
# display one by one
for i in range(8):
    print 'order, (region index, region size):' , i, regions[i]
    atemp = dbz(matrix = (acomp35.matrix==regions[i][0]), vmax=2, vmin=-0.3)
    atemp.show2()

########
# compute centroids

import numpy as np
X, Y = np.meshgrid(range(921), range(881))

xcentroids =[]
ycentroids =[]
componentWeights = {}

for i in range(50):
    print 'order, (region index, region size):' , i, regions[i],
    matrix = (acomp35.matrix==regions[i][0])
    xcentroids.append( 1.*(matrix*X).sum()/matrix.sum() )
    ycentroids.append( 1.*(matrix*Y).sum()/matrix.sum() )
    #componentWeights[i] = matrix.sum()
    componentWeights[i] = (matrix *a.matrix).sum()      #weighted with values
    print xcentroids[i], ycentroids[i], componentWeights[i]


acomp35.show()


a10edges=a10

a10 = a.threshold(10)
seeds = np.vstack((xcentroids,ycentroids)).T

from armor.kmeans import clustering as clust

x = clust.getKmeans(a, k=seeds, threshold=10, minit='matrix')

x['pattern'].copy().show2()



#########
#a_k50_seeded_with_connected_components_threshold35_and_grouped_into_12_superclusters
ak = x['pattern']
ak2 = a.copy()
centroids = x['centroids'][0]
mapping ={}

clusterWeights ={}
for i in range(50):
    clusterWeights[i] = (x['centroids'][1]==i).sum()


############
# key step:  sorting and assigning the cluster to the supercluster.

for i in range(50): #cluster index  - can adjust
    dist = []
    for j in range(5): # connected component index  - can adjust
        # key criterion:  distance squared / component weight
        ################
        # option 1:  order by squared distance alone
        #dist.append( (j, (xcentroids[j]-centroids[i][0])**2 + (ycentroids[j]-centroids[i][1])**2 ))    
        ################
        # option 2:  order by squared distance divided by weight 
        # of connected components
        #  componentWeights[j] * power - power can be adjusted
        dist.append((j,1.*((xcentroids[j]-centroids[i][0])**2+\
                           (ycentroids[j]-centroids[i][1])**2  ) \
                                            /componentWeights[j]**.3333)) 
    #core step:  sorting
    dist.sort(key=lambda v: 1.*v[1]) 
    print i, dist[0]
    mapping[i] = dist[0][0]


data=  x['data']
for p in range(len(data)):
    j, i = data[p]
    ak2.matrix[i,j] = mapping[x['centroids'][1][p]]

ak2.cmap='prism'
ak2.copy().show2()

ak2.vmax = ak2.matrix.max() + 3
ak2.vmin = -5
ak2.cmap='jet'
ak2.copy().show2()

