"""
tests to do/data to collect:
1.  lower/higher threshold
2.  averaged/unaveraged RADAR
3.  wrf/ radar


"""
import time, os, pickle, shutil, pickle
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
np  = pattern.np
from armor import objects4 as ob
outputFolder = dp.root + 'labLogs2/charts2_local_features_distribution/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

##############################################################################
#   collecting data
#
timeStamp0   = str(int(time.time()))
#
comprefs    = sum([v.list for v in ob.comprefs], [])
wrfs        = sum([v.list for v in ob.wrfs], [])

testCases   = [(comprefs, 0, False),
               (comprefs, 0, True), (wrfs,0, False), 
               (comprefs, 10, True), (wrfs,-10, False),
               (wrfs,10, False), (comprefs, 20, True)]

for imageList, threshold, toAverage in testCases:
    #logFile      = open(outputFolder + "log" + timeStamp0 + ".txt", 'a')
    #a           = pattern.a.load()
    #gf          = a.globalShapeFeatures()
    #outputString = "#" + '\t'.join(gf.keys()) + '\n'
    #outputString += "#" + imageList[0].name + '\tThreshold: ' + str(threshold) + "\tAveraged: " + str(toAverage) + "\n"
    #logFile.write(outputString)
    for a in imageList:
        a.load()
        a.localShapeFeatures()
        filePath  = outputFolder + str(int(time.time())) + "_" + a.name + '.pydump'
        pickle.dump(a.localFeatures, open(filePath,'w'))
#
#   end collecting data
#
##############################################################################

##############################################################################
#   summarising
#

#def summarising(folder=outputFolder):
folder  = outputFolder
chartsFolder = folder + 'charts/'
if not os.path.exists(chartsFolder):
    os.makedirs(chartsFolder)
L   = os.listdir(folder)
L   = [v for v in L if '.pydump' in v]
fileName = L[0]
x   = pickle.load(open(folder+fileName))

lf  = x['localFeatures'][0]
keys = lf.keys()

def keySize(dic, k):
    try:
        n = dic[k].size
    except AttributeError:
        try:
            n = dic[k].__len__()
        except AttributeError:
            n = 1
    return n 

keySizes = [keySize(lf, v) for v in lf]   
print keySizes
print [(keys[v], keySizes[v]) for v in range(len(keys))]
keysFull =  sum([[keys[i]]*keySizes[i] for i in range(len(keys))],[])
print keysFull

#for lf in x['localFeatures']:
feats = []
for k in keys:
    print k,
    try:
        feats.extend(lf[k].flatten())
    except AttributeError:
        try:
            feats.extend(lf[k])
        except TypeError:
            feats.append(lf[k])
#print feats

featsArr = np.zeros((1, len(keysFull)))
for fileName in L:
    x   = pickle.load(open(folder+fileName))
    for lf in x['localFeatures']:
        feats = []
        for k in keys:
            #print k,
            try:
                feats.extend(lf[k].flatten())
            except AttributeError:
                try:
                    feats.extend(lf[k])
                except TypeError:
                    feats.append(lf[k])
        featsArr = np.vstack([featsArr, feats])
        print feats[:4]

featsFile = open(folder+str(int(time.time()))+'featuresArr.dat','a')
featsFile.write('#' + '  '.join(keysFull) + '\n')
np.savetxt(featsFile, featsArr)
featsFile.close()

###############################################################################
#   plotting
#
folder = outputFolder
fileName = '1414755088featuresArr.dat'
featsFile = open(folder+fileName)
featsArr = np.loadtxt(featsFile)

for i in range(len(keysFull)):
    feat0 = featsArr[:,i]
    y, x = np.histogram(feat0, 50)
    plt.clf()
    plt.plot(x[:-1], y)
    plt.title(keysFull[i]+str(i))
    plt.savefig(chartsFolder+str(int(time.time()))+keysFull[i]+str(i))
    plt.show(block=False)
    
