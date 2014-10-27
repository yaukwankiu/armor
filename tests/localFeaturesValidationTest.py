#   localFeaturesValidationTest.py
#   to test the matching algorithm via local features
#   1.  load the COMPREF and WRF respectively
#   2.  construct local features after segmentation
#   3.  order local features according to volume, descending
#   4.  match the local features in COMPREF and WRF and compute the distances via the greedy algorithm
#   5.  compute the weighed distance between two images
#   6.  look for the closest WRF match to the COMPREF
#   7.  validation of the above algorithm
import time, os, pickle
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
np  = pattern.np
thisScript =  'localFeaturesValidationTest.py'

#########################################
#   defining the functions


def compareLocalShapeFeatures(lf1, lf2, 
                                keys=['volume', 'centroid', 'HuMoments','highIntensityRegionVolume',],  
                                powers=[.5,  1, 1, 1,],
                                useLogScale=[False, False, True, True,],
                                weights=[10., 1./600., 1., 1.,]):

    fmRows=[]
    for lf in lf1, lf2:
        features = [np.array(lf[v]) for v in keys]
        print features
        features = [features[i]*powers[i] * weights[i] for i in range(len(keys))]
        for i in range(len(keys)):
            if useLogScale[i]:
                features[i] = np.log(features[i])
        features = np.hstack(features)
        print features
        inds          = np.where(np.isnan(features))
        #features[inds]      = -99
        features[inds]      = 0.
        inds          = np.where(np.isinf(features))
        #features[inds]      = -999
        features[inds]      = 0.
        print features
        fmRows.append(features)
    
    squaredFeatureSpaceDistance = ((fmRows[0]-fmRows[1])**2).sum()
    print 'squared feature distance:', squaredFeatureSpaceDistance
    return squaredFeatureSpaceDistance
    

def compareLocalShapes(a, b, N=5, exactNumberOfComponents=True, volumeWeightPower=0.5, refresh=False, *args, **kwargs):
    if not hasattr(a, 'localFeatures') or refresh:
        a.localShapeFeatures()
    if not hasattr(b, 'localFeatures') or refresh:
        b.localShapeFeatures()
    lfa = a.localFeatures['localFeatures']  
    lfb = b.localFeatures['localFeatures']
    N1  = min(len(lfa), len(lfb), N) #number of features to match
    if exactNumberOfComponents and N1 <N:
        return np.inf
    else:
        N=N1
        
    totalScore=0
    for i in range(N):
        lf1 = lfa[i]
        lf2 = lfb[i]
        localScore = compareLocalShapeFeatures(lf1, lf2, *args, **kwargs)
        if volumeWeightPower > 0:
            localScore *= lf1['volume']*volumeWeightPower
        totalScore +=localScore
    return totalScore

#########################################
#   constructing the test objects

from armor import objects4 as ob
compref    = ob.kongrey
wrf       = ob.kongreywrf2
wrf.fix()

a   = compref('20130829.1300')[0].load()
a.show()
a.localShapeFeatures(lowerThreshold=10, upperThreshold=35)

b1  = wrf('20130829.1200')
b2  = wrf('20130829.1500')
b3  = wrf('20130829.0900')
b4  = wrf('20130829.0600')
b5  = wrf('20130829.1800')
B   = b1 +b2 + b3 + b4 + b5

########
#   test case
'''
b = B[0]
b.load()
b.localShapeFeatures(lowerThreshold=-5, upperThreshold=35)

b.localFeatures['localFeatures'].__len__()
b.localFeatures['localFeatures'][0]

score = compareLocalShapes(a,b)
'''  
########
#   experiment loop
timeString = str(int(time.time()))
outputFolder=dp.root+'labLogs2/charts2_local_global_matching/' + timeString +'/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

shutil.copyfile(dp.testFolder + thisScript, outputFolder+thisScript)
scores = []
#B.sort(reverse=True)
bestScoreSoFar = np.inf
bestMatch=""
a.saveImage(outputFolder+'0.png')

R   = (np.random.random(30)*len(B)).astype(int)
R   = list(set(R))

#for b in B:
for r in R:
    b = B[r]
    print '---------------------'
    print b.name
    b.load()
    if not hasattr(b, 'localFeatures'):
        b.localShapeFeatures(lowerThreshold=-5, upperThreshold=35)
    score= compareLocalShapes(a,b, N=8)
    print b.name, ':', score
    scores.append((b.name, score))
    plt.clf()
    a.above(10).showWith(b.above(-5), block=False)
    #time.sleep(2)
    b.saveImage(outputFolder+str(round(np.log(score),6)).ljust(9,'0') + '.jpg')
    if score < bestScoreSoFar:
        bestScoreSoFar=score
        bestMatch = b
        #b.saveImage(outputFolder+ 'b' + str(len(os.listdir(outputFolder))-1) + '.png')
    else:
        plt.clf()
        #a.above(10).showWith(bestMatch.above(-5), block=False)
    
    try:
        print "BEST MATCH SO FAR:", bestMatch.name, bestScoreSoFar
    except:
        pass
    print '---------------------'

