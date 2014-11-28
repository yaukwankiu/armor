#   localFeaturesSensitivityTest4.py
#   to test and optimise the logistic parameters

###########################################
#   imports

import pickle
import time, os
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
dp  = pattern.dp
plt = pattern.plt
ma  = pattern.plt
from armor import misc
from armor.geometry import transforms
from armor.geometry import transformedCorrelations as trc

###########################################
#   settings
inputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/local_features_sensitivity_test3/'
outputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/local_features_sensitivity_test4/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
 
sigmoidWidths = {
                 'eigenvectors'             :   0.1,
                 'numberOfComponents'       :   0.05,
                 'skewness'                 :   0.3,
                 'angle'                    :   0.2,
                 'highIntensityRegionVolume':   1.,     # didn't test it this time
                 'volume'                   :  0.1, # taking log first
                 'centroid'                 : 0.1,
                 'eigenvalues'              : 10.,
                 'kurtosis'                 : 0.5,
                 ('HuMoments',0)            :  20,
                 ('HuMoments',1)            : 2000, # can't get accurate figures for these
                 ('HuMoments',2)            :0.02,
                 ('HuMoments',3)            : 0.01,
                 ('HuMoments',4)            : 0.01,
                 ('HuMoments',5)            : 0.05,
                 ('HuMoments',6)            : 0.05,
                 'rectangle'                : 4,
                }
sigmoidCentres = [(v, sigmoidWidths[v]) for v in sigmoidWidths]
sigmoidCentres = dict(sigmoidCentres)
sigmoidWidths = [(v, sigmoidWidths[v]*0.2) for v in sigmoidWidths]
sigmoidWidths = dict(sigmoidWidths)
###########################################
#   old functions (from localFeaturesSensitivityTest3)

def getKeys(L):
    x = L[0]
    keys = x.keys()
    keys2 =[]
    for k in keys:
        try:
            m = len(x[k])
            keys2.extend([(k, v) for v in range(m)])
        except TypeError:
            keys2.append(k)
    return keys2
    
def getKeywordArray(L, keys):
    if type(keys)==str:
        key = keys
        return np.array([v[key] for v in L])
    else:
        key=keys[0]
        ind=keys[1]
        return np.array([v[key][ind] for v in L])

def loadFeaturesList(folder=inputFolder, key1='a', N=100):
    L = os.listdir(folder)
    L = [v for v in L if '.pydump' in v and v.startswith(key1)]
    L.sort()
    list_a = []
    for fileName in L[:N]:
        feat = pickle.load(open(folder+fileName,'r'))
        list_a.append(feat)
    return list_a
    
def compareFeature(featureKey, list_a, list_b, toShow=False, block=False, relativeResults=False,
                   bins=50, takeLog=False):
    arr1 = getKeywordArray(list_a, featureKey)
    arr2 = getKeywordArray(list_b, featureKey)
    if takeLog:
        arr3 = np.log(arr2) - np.log(arr1)
    elif relativeResults:
        arr3 = (arr2-arr1)/arr1
    else:
        arr3 = (arr2-arr1)
    y, x = np.histogram(arr3, bins)
    plt.plot(x[1:], y)
    if type(featureKey)==str:
        plt.title(featureKey)
    else:
        plt.title(featureKey[0]+str(featureKey[1]))
    if toShow:
        plt.show(block=block)
    return x,y
    
def degreeOfSimilarity(key, L, a, feats_a, feats_b, takeLog=False, relative=False,
                        verbose=False
                        ):
    """
    return the degrees of similiarity from the numerical features 
    computed from the empirical sigmoid function
    """
    if type(key)==str:
        fa = feats_a[key]
        fb = feats_b[key]
    else:
        fa = feats_a[key[0]][key[1]]
        fb = feats_b[key[0]][key[1]]
    if verbose:
        print 'fa:', fa
        print 'fb:', fb
    if takeLog:
        diff = np.log(fa) - np.log(fb)
    elif relative:
        diff = 1. * (fa-fb)/fa
    else:
        diff = fa - fb
    if verbose:
        print "diff, L:", diff, L
    diff = abs(diff)        # taking the absolute value
    similarity = misc.sigmoid(X=-(diff-a), L=L)
    return similarity

###########################################
#   new functions

def score(testObject='a10', testSubjects=["b10"], parameters_L= sigmoidWidths, parameters_a=sigmoidCentres):

    #   degrees of similarity
    
    #subjects = ['a0', 'b0', 'a1', 'b1', 'a2', 'b2', 'a3', 'b3', 'a0']
    #subjects = range(40)
    #subjects = [['a'+str(v), 'b'+str(v)] for v in subjects]
    #subjects = sum(subjects,[]) + ['a0']
    #outputFileName ='degreesOfSimilarity.log.txt'
    #    
    subjects = [[testObject, v] for v in testSubjects] #edit here
    #subjects = sum(subjects,[]) 

    outputFileName = 'degreesOfSimilarity_%s_%d.log.txt' %(testObject, int(time.time()))
    #keys = getKeys(list_a)
    keys = ['volume', 'angle', ('eigenvalues',0), ('eigenvalues',1),  ('skewness',0), ('skewness',1), ('kurtosis',0), ('kurtosis',1)]
    outputStrings = []
    scores = []
    for i in range(len(subjects)):
        name_a, name_b = subjects[i]
        feats_a = pickle.load(open(inputFolder+name_a+'_features.pydump'))
        feats_b = pickle.load(open(inputFolder+name_b+'_features.pydump'))
        outputString =""
        outputString+= '-----------------------------\n'
        outputString+= 'degrees of similarity for: ' + name_a + ', ' + name_b + '\n'
        score = 1.
        for key in keys:
            takeLog= ('volume' in str(key).lower())
            try:
                sigmoidWidth = sigmoidWidths[key]
                sigmoidCentre =sigmoidCentres[key]
            except KeyError:
                sigmoidWidth = sigmoidWidths[key[0]]
                sigmoidCentre= sigmoidCentres[key[0]]
            degrSim = degreeOfSimilarity(key=key, L=sigmoidWidth, a=sigmoidCentre, feats_a=feats_a, feats_b=feats_b, takeLog=takeLog, relative=False)
            degrSim = round(degrSim,4)
            outputString+= str(key) + ':\t' + str(degrSim)  + '\n'
            score *= degrSim    # combine by multiplication
        print outputString
        scores.append((i, score))
        outputStrings.append(outputString)
    open(outputFolder+outputFileName,'a').write('=================================\n'+time.asctime()+'\nTest Object:'+testObject+'\n')
    open(outputFolder+outputFileName,'a').write('\n\n'.join(outputStrings))
    scores.sort(key=lambda v:v[1], reverse=True)
    open(outputFolder+outputFileName,'a').write('\n\nTop matches:\n')    
    open(outputFolder+outputFileName,'a').write('\n'.join([str(v[0])+':\t'+str(v[1]) for v in scores][:10]))
    print 'top matches for %s:' % testObject
    print '\n'.join([str(v[0])+':\t'+str(v[1]) for v in scores][:10])
    return scores


def main(n0, n1):
    summaryFolder = outputFolder+'summaries/'
    if not os.path.exists(summaryFolder):
        os.makedirs(summaryFolder)
    scores = []
    topScores = []
    #n0=300
    #n1=400
    logFileName = 'results_for_test_range_%d_to_%d.log.txt' %(n0, n1)
    testRange = range(n0, n1)
    testSubjects = ['b'+str(v) for v in testRange]
    for n in testRange:
        testObject = 'a'+str(n)

        x = score(testObject=testObject, testSubjects=testSubjects)
        scores.append((n,x))
        topScores.append((n,x[0]))
    finalScore= len([v for v in topScores if v[0]==n0+v[1][0]])
    print "number of matches:", finalScore
    open(summaryFolder+logFileName, 'a').write(time.asctime()+'\n'+ str(finalScore)+'\n')    
    open(summaryFolder+logFileName, 'a').write('\n'.join([str(v) for v in topScores]))    
    return topScores, finalScore

if __name__=='__main__':

    scores = []
    details=[]
    n = 100
    for N in range(2500, 3000, n):
        topScores, finalScore = main(N,N+n)
        scores.append(finalScore)
        details.append(topScores)


"""
if __name__ == '__main__':
    summaryFolder = outputFolder+'summaries/'
    if not os.path.exists(summaryFolder):
        os.makedirs(summaryFolder)
    scores = []
    topScores = []
    n0=300
    n1=400
    logFileName = 'results_for_test_range_%d_to_%d.log.txt' %(n0, n1)
    testRange = range(n0, n1)
    testSubjects = ['b'+str(v) for v in testRange]
    for n in testRange:
        testObject = 'a'+str(n)

        x = score(testObject=testObject, testSubjects=testSubjects)
        scores.append((n,x))
        topScores.append((n,x[0]))
    finalScore= len([v for v in topScores if v[0]==n0+v[1][0]])
    print "number of matches:", finalScore
    open(summaryFolder+logFileName, 'a').write(time.asctime()+'\n'+ str(finalScore)+'\n')    
    open(summaryFolder+logFileName, 'a').write('\n'.join([str(v) for v in topScores]))    
"""
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################

