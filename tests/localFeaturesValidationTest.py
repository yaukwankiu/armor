#   localFeaturesValidationTest.py
#   to test the matching algorithm via local features
#   1.  load the COMPREF and WRF respectively
#   2.  construct local features after segmentation
#   3.  order local features according to volume, descending
#   4.  match the local features in COMPREF and WRF and compute the distances via the greedy algorithm
#   5.  compute the weighed distance between two images
#   6.  look for the closest WRF match to the COMPREF
#   7.  validation of the above algorithm
import time, os, pickle, shutil
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
                                #weights=[10., 1./600., 1., 1.,],
                                weights = [0.1, 1./60., 1., 1./200.]  # new weights for COMPREF, 2014-10-28
                                ):

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
#a   = ob.kongrey('20130829.1100')[0]
#a.show()
#a.localShapeFeatures(lowerThreshold=10, upperThreshold=35)
#b1  = ob.kongreywrf2('20130829.1200')
#b2  = ob.kongreywrf2('20130829.1500')
#b3  = ob.kongreywrf2('20130829.0900')
#b4  = ob.kongreywrf2('20130829.0600')
#b5  = ob.kongreywrf2('20130829.1800')
#B   = b1 +b2 + b3 + b4 + b5

#compref    = ob.kongrey             #<-- edit here
#wrf       = ob.kongreywrf2          #<-- edit here
#wrf.fix()

compref    = ob.march2014             #<-- edit here
wrf       = pattern.DBZstream(name='March2014 WRF', dataFolder=dp.root+'data/march2014/WRFEPS[regridded]/all/')          #<-- edit here

#compref   = ob.may2014 #doesn't work
#wrf      = ob.may2014wrf19.list + ob.may2014wrf20.list + ob.may2014wrf21.list + ob.may2014wrf22.list + ob.may2014wrf23.list

compref   = ob.may2014('20140520')
wrf      = ob.may2014wrf20
wrf.fix()

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

def experimentLoop(a,B, N=5, sampleSize=30, exactNumberOfComponents=False, *args, **kwargs):
    ########
    #   experiment loop
    print 'experiment starts'
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

    R   = (np.random.random(sampleSize)*len(B)).astype(int)
    R   = list(set(R))

    #for b in B:
    for r in R:
        b = B[r]
        print '---------------------'
        print b.name
        b.load()
        b.show()
        if not hasattr(b, 'localFeatures'):
            b.localShapeFeatures(lowerThreshold=-5, upperThreshold=35)
        score= compareLocalShapes(a,b, exactNumberOfComponents=exactNumberOfComponents, N=N, *args, **kwargs)
        print b.name, ':', score
        scores.append((b.name, score))
        plt.clf()
        a.above(10).showWith(b.above(-5), block=False)
        #time.sleep(2)
        if score < np.inf:
            b.saveImage(outputFolder+str(round(np.log(score),6)).ljust(9,'0') + '.jpg')
        else:
            b.saveImage(outputFolder+"inf_" + b.name +'.jpg')
        
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
    sample = [B[v].name for v in R]
    return bestMatch, bestScoreSoFar, sample 

#####################################################
#   general test case

Ra   = (np.random.random(30)*len(compref)).astype(int)
Ra   = list(set(Ra))
results = []
for ra in Ra:
    a = compref[ra].load()
    T0 = a.getDataTime(a.datetime(dh=-6))
    T1 = a.getDataTime(a.datetime(dh=+6))
    B  = [v for v in wrf if v.dataTime>=T0 and v.dataTime<=T1]
    print "========================"
    print "Test case:"
    print a.name
    print "number of wrf outputs to match:", len(B)
    #bestMatch, bestScore, sample = experimentLoop(a,B, sampleSize=60)
    bestMatch, bestScore, sample = experimentLoop(a,B, sampleSize=60,
                                                    volumeWeightPower=0.5,
                                                    exactNumberOfComponents=True,
                                                    N=5,
                                                    keys=['volume', 'centroid', 'HuMoments','highIntensityRegionVolume',], 
                                                    #weights = [0.1, 1./60., 1., 1./200.]  ,
                                                    weights = [0.2, 1./60., 1., 1./100.]  ,
                                                    powers=[0.75, 1, 1, 1],
                                                    )
    try:
        results.append((a.name, bestMatch.name, bestScore, sample))
    except:
        pass
