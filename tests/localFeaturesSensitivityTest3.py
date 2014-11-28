# localFeaturesSensitivityTest3.py
# streamlining the old code

#   plot/analyse/compare the distributions between physically related and physically unrelated datasets

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



###################
#   setup
list_a = ""
list_b = ""
outputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/local_features_sensitivity_test3/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

arrayShape = np.array((200, 200))
m   = np.ma.zeros(arrayShape)
m.mask=False
m   = dbz(matrix=m)
#m.show()
I, J = m.IJ()
#dg  = trc.doubleGaussian(I, J, centroid_i=100, centroid_j=150, sigma_i=20, sigma_j=50, theta=1 )
#DG  = dbz(matrix=np.ma.array(dg))
#DG.vmin=0


########################################################
#   empirical values
#   2014-11-25
#localFeaturesSensitivityTest4.py

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
                 ('HuMoments',0)            :  20.,
                 ('HuMoments',1)            : 2000., # can't get accurate figures for these
                 ('HuMoments',2)            :0.02,
                 ('HuMoments',3)            : 0.01,
                 ('HuMoments',4)            : 0.01,
                 ('HuMoments',5)            : 0.05,
                 ('HuMoments',6)            : 0.05,
                 'rectangle'                : 4,
                }

sigmoidWidths = [(v, sigmoidWidths[v]*0.2) for v in sigmoidWidths]
sigmoidWidths = dict(sigmoidWidths)
##########################################################
#   preliminary functions

def makeRandomLandscape():
    dgs = []
    paramsList = []
    N=20
    for i in range(N):                 #2014-11-04
        params = np.random.random(5)
        params *= [50, 50, 20, 15, np.pi]
        params[2] = params[3]   #hack
        params += [75, 75, 0, 0, 0]
        paramsList.append(params)
    #pickle.dump(paramsList, open(outputFolder + str(int(time.time())) + '_landscape' + "_" + ("000" + str(count))[-4:] + '.pydump','w'))  #2014-11-13
    for i in range(N):
        dg  = trc.doubleGaussian(I, J, *paramsList[i])
        dgs.append(dg)
    DG  = dbz(matrix = sum(dgs))
    DG.matrix *=10
    DG.matrix -=20
    DG.setMaxMin()
    DG.name='Sum of ' +str(N) + ' double gaussians' + str(int(time.time()))
    DG.imagePath = outputFolder+ DG.name + '.jpg'
    DG.outputPath = outputFolder+ DG.name + '.dat'
    DG.paramsList = paramsList 
    return DG
   

def perturb(DG, N2=5):
    dgs_2 = [] #for perturbation
    paramsList_2 = []
    N2=5
    for i in range(N2):                 #2014-11-04
        params = np.random.random(5)
        params *= [50, 50, 3,5, np.pi]
        params[2] = params[3]   #hack
        params += [75, 75, 0, 0, 0]
        paramsList_2.append(params)
    for i in range(N2):
        dg  = trc.doubleGaussian(I, J, *paramsList_2[i])
        dgs_2.append(dg)
    DG2  = dbz(matrix=sum(dgs_2))
    DG2.matrix *=5
    DG2.setMaxMin()
    DG3 = DG + DG2
    DG3.setMaxMin()
    DG3.imagePath = outputFolder+ DG.name + '_perturbed.jpg'
    DG3.outputPath = outputFolder+ DG.name + '_perturbed.dat'
    DG3.paramsList = DG.paramsList+paramsList_2
    return DG3


def getLargestComponents(a, N=3, threshold=0):
    #   default threshold=0
    a1 = a.above(threshold).connectedComponents()
    indices = range(a1.matrix.min(), a1.matrix.max()+1)
    indices = [(v, (a1.matrix==v).sum()) for v in indices]
    indices.sort(reverse=True, key=lambda v:v[1])
    largestComponents = [a1.levelSet(v[0]) for v in indices[1:1+N]]    
    return largestComponents

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


###########################################################
#   data collection


def makePerturbedPair(display=False):
    a = makeRandomLandscape()
    a.name = 'a'
    if display:
        a.show(block=True)
    aa = getLargestComponents(a)
    a1 = aa[0]
    #
    b = perturb(a)
    b.name='b'
    if display:
        b.show(block=True)    
    bb = getLargestComponents(b)
    b1 = bb[0]
    #
    f1 = a1.globalShapeFeatures()
    f2 = b1.globalShapeFeatures()
    return a, b, f1, f2


def constructGlobalFeaturesLists(N0=0, N1=30):
    list_a = []
    list_b = []
    for i in range(N0, N1):
        a, b, f1, f2 = makePerturbedPair()
        a.name = 'a' + str(i)
        b.name = 'b' + str(i)
        a.saveImage(outputFolder+a.name+'.png')
        b.saveImage(outputFolder+b.name+'.png')
        a.saveMatrix(outputFolder+a.name+'.dat')
        b.saveMatrix(outputFolder+b.name+'.dat')
        list_a.append(f1)
        list_b.append(f2)
        print f1
        print f2
        #time.sleep(0.5)
    return list_a, list_b


def fromImagesToFeatures(folder=outputFolder, key1='a', verbose=True, recompute=False):
    L = os.listdir(folder)
    L = [v for v in L if '.dat' in v and v.startswith(key1)]
    list_a = []
    for fileName in L:
        outputFilePath = folder+fileName[:-4] + '_features.pydump'
        if not recompute and os.path.exists(outputFilePath):
            continue
        else:
            a = dbz(name=fileName, dataPath=folder+fileName)
            a.load()
            a.globalShapeFeatures()
            list_a.append(a.globalFeatures)
            pickle.dump(a.globalFeatures, open(outputFilePath,'w'))
            if verbose:
                print '=========================='
                print fileName
                print a.globalFeatures
    return list_a

def loadSamplesList(folder=outputFolder, key1='a'):
    L = os.listdir(folder)
    L = [v for v in L if '.dat' in v and v.startswith(key1)]
    L.sort()
    list_a = []
    for fileName in L:
        a = dbz(name=fileName, dataPath=folder+fileName)
        a.load()
        a.globalShapeFeatures()
        list_a.append(a.globalFeatures)
    return list_a

def loadFeaturesList(folder=outputFolder, key1='a'):
    L = os.listdir(folder)
    L = [v for v in L if '.pydump' in v and v.startswith(key1)]
    list_a = []
    for fileName in L:
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
    
def degreeOfSimilarity(key, sigmoidWidth, feats_a, feats_b, takeLog=False, relative=False,
                        verbose=False):
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
        print "diff, L:", diff, sigmoidWidth
    diff = abs(diff)        # taking the absolute value
    similarity = misc.sigmoid(X=-(diff-sigmoidWidth*5), L=sigmoidWidth)
    return similarity


def analyseFeature(featureKey, dataFolder,outputFolder):
    pass

###
def main(list_a="", list_b=""):
    if list_a=="":
        list_a, list_b = constructGlobalFeaturesLists(N0=30, N1=50)
    return list_a, list_b

if __name__=='__main__':
    """
    if list_a=="":
        list_a, list_b = constructGlobalFeaturesLists(N0=50, N1=70)
    keys = getKeys(list_a) 
    for k in keys:
        arr1 = getKeywordArray(list_a, k)
        arr2 = getKeywordArray(list_b, k)
        arr3 = (arr2-arr1)/arr1
        y, x = np.histogram(arr3, 10)
        plt.plot(x[1:], y)
        if type(k)==str:
            plt.title(k)
        else:
            plt.title(k[0]+str(k[1]))
        plt.show()
    """
    # generating the data
    numberOfNewData=0   # <-- edit here
    L = os.listdir(outputFolder)
    L1 = [v for v in L if v.startswith('b') and '.dat' in v]
    N = len(L1)
    constructGlobalFeaturesLists(N0=N, N1=N+numberOfNewData)
    # generating the features
    fromImagesToFeatures(folder=outputFolder, key1='a', verbose=True, recompute=False)
    fromImagesToFeatures(folder=outputFolder, key1='b', verbose=True, recompute=False)
    # analysing the data
    list_a = loadFeaturesList()
    list_b = loadFeaturesList(key1='b')
    list_c = list_a[3:] + list_a[:3]
    #key=('centroid', 0)
    keys = getKeys(list_a)
    plt.clf()
    bins= N/40
    for key in keys:
        takeLog = ('volume' in str(key).lower())
        x, y   = compareFeature(key, list_a, list_b, bins=bins, takeLog=takeLog)
        x2, y2 = compareFeature(key, list_a, list_c, bins=bins, takeLog=takeLog)
        plt.legend(['Perturbation(A/B)', 'Control(A/C)'])
        if type(key)==str:
            fileName = key + '.png'
        else:
            fileName = key[0] + str(key[1]) + '.png'
        plt.savefig(outputFolder+fileName)
        plt.show(block=True)

if __name__=='__main__':
    testObject='a14'

    #   degrees of similarity
    
    #subjects = ['a0', 'b0', 'a1', 'b1', 'a2', 'b2', 'a3', 'b3', 'a0']
    #subjects = range(40)
    #subjects = [['a'+str(v), 'b'+str(v)] for v in subjects]
    #subjects = sum(subjects,[]) + ['a0']
    #outputFileName ='degreesOfSimilarity.log.txt'
    #    
    subjects = range(100)
    subjects = [[testObject, 'b'+str(v)] for v in subjects] #edit here
    #subjects = sum(subjects,[]) 

    outputFileName = 'degreesOfSimilarity_%s_.log.txt' %testObject
    #keys = getKeys(list_a)
    keys = ['volume', 'angle', ('eigenvalues',0), ('eigenvalues',1),  ('skewness',0), ('skewness',1), ('kurtosis',0), ('kurtosis',1)]
    outputStrings = []
    scores = []
    for i in range(len(subjects)):
        name_a, name_b = subjects[i]
        feats_a = pickle.load(open(outputFolder+name_a+'_features.pydump'))
        feats_b = pickle.load(open(outputFolder+name_b+'_features.pydump'))
        outputString =""
        outputString+= '-----------------------------\n'
        outputString+= 'degrees of similarity for: ' + name_a + ', ' + name_b + '\n'
        score = 1.
        for key in keys:
            takeLog= ('volume' in str(key).lower())
            try:
                sigmoidWidth = sigmoidWidths[key]
            except KeyError:
                sigmoidWidth = sigmoidWidths[key[0]]
            degrSim = degreeOfSimilarity(key=key, sigmoidWidth=sigmoidWidth, feats_a=feats_a, feats_b=feats_b, takeLog=takeLog, relative=False)
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
    print 'top matches:'
    print '\n'.join([str(v[0])+':\t'+str(v[1]) for v in scores][:10])
