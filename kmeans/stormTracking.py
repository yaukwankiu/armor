# armor.kmeans.stormTracking.py
# codes taken from armor.tests.trackingTest20140901

import numpy as np
#from armor import objects4 as ob

def stormTracking(a0, 
                upperThreshold=40, lowerThreshold=20,
                lowerLimit1=10, upperLimit1=100000,
                lowerLimit2=30000,
                minAcceptedDensity = 5,
                verbose=True, display=True, block=False,
                minUnmaskedValue=-50, #hack
                newObject=True,
                *args, **kwargs):
    if newObject:
        a = a0.copy()
    else:
        a = a0
    a.backupMatrix(0)
    a1 = a.above(upperThreshold)
    x = a1.connectedComponents()
    x.show(block=block)
    if verbose:
        print x.matrix.max()

    N = x.matrix.max()
    for i in range(N):
        size= x.levelSet(i).matrix.sum()
        if size> lowerLimit1 and size<upperLimit1:
            print i, ":", size, "||",

    S = [v for v in range(N) if x.levelSet(v).matrix.sum()>lowerLimit1 and x.levelSet(v).matrix.sum()<upperLimit1]
    print S

    centroids = [x.levelSet(v).getCentroid().astype(int) for v in S]    
    if display:
        a.restoreMatrix(0)
        for i, j in centroids:
            try:
                a.drawRectangle(max(0, i-30), max(0,j-30), min(880-30-i, 60), min(920-30-j, 60), newObject=False)
            except:
                pass

        a.show(block=block)

    a.restoreMatrix(0) #for safety
    y = a.getKmeans(threshold=lowerThreshold, k=np.vstack(centroids), minit='matrix')
    a2 = y['pattern']

    N2 = a2.matrix.max()

    regionsToTrack = [a2.getRegionForValue(v) for v in range(int(N2))]
    regionsToTrack = [v for v in regionsToTrack if v!=(-1,-1,0,0)]

    a.restoreMatrix(0)   

    for i, R in enumerate(regionsToTrack):
        print i, R
        a3 = a.getWindow(*R)
        a3.matrix.mask = (a3.matrix < minUnmaskedValue) #hack
        #print a3.matrix.mask.sum()
        #print a3.matrix.sum(), a3.matrix.shape
        #a3.show(block=block)
        #time.sleep(2)
        if verbose:
            print a3.matrix.sum()
            print a3.matrix.shape[0]*a3.matrix.shape[1]*20 
        if a3.matrix.sum()< lowerLimit2 or (a3.matrix.sum() < a3.matrix.shape[0]*a3.matrix.shape[1] * minAcceptedDensity):
            regionsToTrack[i]=(-1,-1,0,0)    # to be removed

    regionsToTrack = [v for v in regionsToTrack if v!=(-1,-1,0,0)]
    for R in regionsToTrack:
        print R
        a.drawRectangle(*R, newObject=False)

    if display:
        a.show(block=block)

    return {'regionsToTrack':regionsToTrack,
            'a':a,
            'a2':a2
            }



