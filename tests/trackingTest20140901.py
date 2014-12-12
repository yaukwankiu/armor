"""20 may 2014
5pm
24-16 degrees N
120-121 degrees E
Test:
in:  COMPREF-10min, COMPREF0, WRFs +- 6 hours
out: matching results/ranking

cd /media/TOSHIBA\ EXT/ARMOR/python
ipython

"""
#   0. parameters, imports and set up
#   1. get the wrf filepaths
#   2. matching and scoring

#   imports
import os, time, pickle, datetime, shutil
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
plt = pattern.plt
dp  = pattern.dp
from armor.tests import localFeaturesSensitivityTest4 as lf
    
#   filepath parameters

doStats=False
thisScript = 'localFeaturesTest20141210.py'
lowerThreshold = 20.
upperThreshold=35.
radarFolder = '/media/TOSHIBA EXT/ARMOR/data/may14/RegriddedData/RADARCV/'
wrfFolder   = '/media/TOSHIBA EXT/ARMOR/data/may14/RegriddedData/WEPS/'
outputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs2/local_features_20141210/'
outputFolder += 'test' + str(len(os.listdir(outputFolder))+1) + "/"
os.makedirs(outputFolder)

radarFileName = 'COMPREF.20140519.2100.0p03.bin'
coastDataPath201='/media/TOSHIBA EXT/ARMOR/data/1may2014/RADARCV/taiwanCoast.dat'
rectangleRegion = (120,50,60,50)
featuresList = ['volume', ('centroid',0), ('centroid',1), ('skewness',0), ('skewness',1), ('kurtosis',0), ('kurtosis',1), 
                ('eigenvalues',0), ('eigenvalues',1), 'angle', 
                'highIntensityRegionVolume', 
                #('HuMoments',0),('HuMoments',1),('HuMoments',2),
                ]

#   functions
def sigmoid(x):
    if np.isnan(x): #regularisation
        x = -10
    return 1./(1+np.exp(-x))

def softMask(i,j,width):
    """ mask of dimensions i, j and width
    """
    Z = np.zeros((i,j))    
    i2=i//2+1
    j2=j//2+1
    I = range(i2)
    J = range(j2)
    I = [sigmoid(1.*(v-width)/(0.1*width)) for v in I]
    J = [sigmoid(1.*(v-width)/(0.1*width)) for v in J]
    J2, I2 = np.meshgrid(J,I)
    m = I2*J2
    Z[0:i2, 0:j2] = m
    Z[-i2:, 0:j2] = np.flipud(m)
    Z[-i2:, -j2:] = np.fliplr(np.flipud(m))
    Z[0:i2:, -j2:] = np.fliplr(m)
    return Z
    

def getTime(fileName):
    x = fileName.replace('.','')
    #print x
    Y,M,D,h,m = [int(v) for v in x[0:4], x[4:6], x[6:8], x[8:10], x[10:12]]
    T = datetime.datetime(Y,M,D,h,m)
    return T
    
#   setup
a   = dbz(dataPath=radarFolder+radarFileName).load()
a.vmin = -20.
a.vmax = 70.
a.name = 'COMPREF-2014-0519-2100z'
a.dataTime = '20140519.2100'
a.coastDataPath= coastDataPath201
a.show()
a1 = a.copy()
a1.drawRectangle(newObject=False, *rectangleRegion)
a1.name = a.name
a1.showWithCoast()

aa      = a.getRectangle(*rectangleRegion)
aa.name = a.name + ' West of Northern Taiwan'

mask    = softMask(width=5, *aa.matrix.shape)

aa.matrix *= mask
aa.show()
aa.globalShapeFeatures(lowerThreshold=lowerThreshold, upperThreshold=upperThreshold)

if doStats:
    #   tuning the parameters
    T0 = getTime(a.dataTime)
    L1 = os.listdir(wrfFolder)
    filePathsFull = []
    for i1 in L1:
        L2 = os.listdir(wrfFolder+i1)
        L2 = [v for v in L2 if '.dat' in v]
        #L2 = [v for v in L2 if (T0-getTime(v)).total_seconds()>= -6*3600 and (T0-getTime(v)).total_seconds()<= 6*3600 ] # +- 6 hours
        L2 = [wrfFolder + i1+'/' + v for v in L2]
        filePathsFull.extend(L2)
    print ',\t'.join(filePathsFull)
    R = filePathsFull
    scoresFull = []
    for r in R:
        b = dbz(dataPath=r).load()
        b.name = r.split('/')[-1]
        bb      = b.getRectangle(*rectangleRegion)
        bb.matrix *= mask
        bb.name = b.name + ' West of Northern Taiwan'
        if np.random.random() < 0.01:
            b.drawRectangle(*rectangleRegion).show()
        try:
            #gsf = bb.globalShapeFeatures(lowerThreshold=0, upperThreshold=100)
            gsf = bb.globalShapeFeatures(lowerThreshold=20, upperThreshold=100)
            print '-----------------------------------------------------------'
            print bb.name
            print gsf
            scoresFull.append((r, bb.globalFeatures))
        except:
            print 'Error!', bb.name
    #   extract stats for: skewness, kurtosis, angle, volume, position, 
    keys = lf.getKeys([scoresFull[0][1]])
    keywordArrays = []
    for k in keys:
        keywordArrays.append((k, lf.getKeywordArray([v[1] for v in scoresFull], k)))

    keywordArrayForAa = []
    for k in keys:
        keywordArrayForAa.append((k, lf.getKeywordArray([aa.globalFeatures], k)))
        
    for k, arr in keywordArrays:
        aaValue = [v[1] for v in keywordArrayForAa if v[0]==k][0]
        arr -= aaValue
        plt.clf()
        y, x = np.histogram(arr, len(arr/20))
        plt.plot(x[1:], y)
        plt.savefig(outputFolder+str(k) +'.png')
        plt.show(block=False)
        print '---------------------'
        print k
        print aaValue
        print arr[:10]

    #
#
###############################################################################

###############################################################################
#   decide upon the sigmoid width parameters
#  open the relevant files and load and match
#   get the wrf filepaths

 
sigmoidWidths = {
                 'eigenvectors'             :   0.1,
                 'numberOfComponents'       :   0.05,
                 'skewness'                 :   0.3,
                 'angle'                    :   0.2,
                 'highIntensityRegionVolume':   2., 
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

takeLogs  = {
                 'eigenvectors'             :   False,
                 'numberOfComponents'       :   False,
                 'skewness'                 :   False,
                 'angle'                    :   False,
                 'highIntensityRegionVolume':   True,   
                 'volume'                   :  True, # taking log first
                 'centroid'                 : False,
                 'eigenvalues'              : False,
                 'kurtosis'                 : False,
                 ('HuMoments',0)            :  False,
                 ('HuMoments',1)            : False, # can't get accurate figures for these
                 ('HuMoments',2)            : True,
                 ('HuMoments',3)            : True,
                 ('HuMoments',4)            : True,
                 ('HuMoments',5)            : True,
                 ('HuMoments',6)            : True,
                 'rectangle'                : False,
                }

relatives = [(v, False) for v in takeLogs.keys()]
relatives = dict(relatives)

weights = {
            'volume'    : 1.,
            'kurtosis'  : 1.,
            'skewness'  : 1.,
            'centroid'  : 1.,
            'eigenvalues': 1.,
            'angle'     : 1.,
            'highIntensityRegionVolume': 1.,
            }

def getMatchingScore(keys, feats_a, feats_b, sigmoidWidths=sigmoidWidths, sigmoidCentres=sigmoidCentres, 
                  takeLogs=takeLogs, relatives=relatives, weights=weights):
    score = 1.
    for key in keys:
        try:
            degrSim = lf.degreeOfSimilarity(key=key, L=sigmoidWidths[key], a=sigmoidCentres[key], 
                                          feats_a=feats_a, feats_b=feats_b, takeLog=takeLogs[key], relative=relatives[key],
                                        verbose=False)
        except:
            key0 = key[0]
            degrSim = lf.degreeOfSimilarity(key=key, L=sigmoidWidths[key0], a=sigmoidCentres[key0], 
                                          feats_a=feats_a, feats_b=feats_b, takeLog=takeLogs[key0], relative=relatives[key0],
                                        verbose=False)

        if key in weights.keys():
            power = weights[key]
        elif key[0] in weights.keys():
            power = weights[key[0]]
        else:
            power = 1
        score *= degrSim
    return score

T0 = getTime(a.dataTime)
L1 = os.listdir(wrfFolder)
filePaths = []
for i1 in L1:
    L2 = os.listdir(wrfFolder+i1)
    L2 = [v for v in L2 if '.dat' in v]
    #L2 = [v for v in L2 if (T0-getTime(v)).total_seconds()>0 and (T0-getTime(v)).total_seconds()< 24*1*3600 ] #1 days
    L2 = [v for v in L2 if (T0-getTime(v)).total_seconds()>= -6*3600 and (T0-getTime(v)).total_seconds()<= 6*3600 ] # +- 6 hours
    L2 = [wrfFolder + i1+'/' + v for v in L2]
    filePaths.extend(L2)

print ',\t'.join(filePaths)

feats_bb = []
for r in filePaths:
    b = dbz(dataPath=r).load()
    b.name = r.split('/')[-1]
    bb      = b.getRectangle(*rectangleRegion)
    bb.matrix *= mask
    bb.name = b.name + ' West of Northern Taiwan'
    if np.random.random() < 0.01:
        b.drawRectangle(*rectangleRegion).show()
    try:
        #gsf = bb.globalShapeFeatures(lowerThreshold=0, upperThreshold=100)
        gsf = bb.globalShapeFeatures(lowerThreshold=lowerThreshold, upperThreshold=upperThreshold)
        print '-----------------------------------------------------------'
        print bb.name
        print gsf
        feats_bb.append((r, bb.globalFeatures))
    except:
        print 'Error!', bb.name

scores = []
for filePath, feats_b in feats_bb:
    matchingScore = getMatchingScore(keys=featuresList, feats_a=aa.globalFeatures, feats_b=feats_b, sigmoidWidths=sigmoidWidths, sigmoidCentres=sigmoidCentres, 
                  takeLogs=takeLogs, relatives=relatives, weights=weights)

    scores.append((filePath, matchingScore))
scores.sort(key=lambda v:v[1], reverse=True)

print scores[:10]

topScores = scores[:50]
for count, (filePath, score) in enumerate(topScores):
    dz = dbz(dataPath=filePath, name=filePath+'\n'+str(score))
    dz.load()
    dz.coastDataPath = coastDataPath201
    dz.drawRectangle(*rectangleRegion, newObject=False)
    dz.drawCoast(newCopy=False)
    dz.imagePath = outputFolder + 'rank' + str(count) + "_"+filePath.split('/')[-1] +'.jpg'
    dz.vmin=a.vmin
    dz.vmax=a.vmax
    dz.saveImage()

a.drawCoast(newCopy=False)
a.drawRectangle(*rectangleRegion, newObject=False)
a.imagePath = outputFolder + a.dataPath.split('/')[-1] +'.jpg'
a.saveImage()

shutil.copyfile(dp.root+ 'python/armor/tests/'+ thisScript,  outputFolder+thisScript)


