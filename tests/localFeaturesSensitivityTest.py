import pickle
import time, os
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
dp  = pattern.dp
plt = pattern.plt
ma  = pattern.plt
from armor.geometry import transforms
from armor.geometry import transformedCorrelations as trc
outputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/local_features_sensitivity_test/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

arrayShape = np.array((200, 200))
m   = np.ma.zeros(arrayShape)
m.mask=False
m   = dbz(matrix=m)
m.show()
I, J = m.IJ()
dg  = trc.doubleGaussian(I, J, centroid_i=100, centroid_j=150, sigma_i=20, sigma_j=50, theta=1 )
DG  = dbz(matrix=np.ma.array(dg))
DG.vmin=0


###########################################################
#   data collection

for count in range(100):
    dgs = []
    paramsList = []
    N=20
    for i in range(N):                 #2014-11-04
        params = np.random.random(5)
        params *= [50, 50, 20, 15, np.pi]
        params[2] = params[3]   #hack
        params += [75, 75, 0, 0, 0]
        paramsList.append(params)

    for i in range(N):
        dg  = trc.doubleGaussian(I, J, *paramsList[i])
        dgs.append(dg)

    DG  = dbz(matrix = sum(dgs))
    DG.setMaxMin()
    DG.name='Sum of ' +str(N) + ' double gaussians' + str(int(time.time()))
    DG.saveImage(outputFolder+ DG.name + '.jpg')
    DG.show()
    DG.outputPath = outputFolder+ DG.name + '.dat'
    DG.saveMatrix()

    DG.globalShapeFeatures(lowerThreshold=1.2, upperThreshold=4)
    #DG.localShapeFeatures(lowerThreshold=1.2, upperThreshold=4, minComponentSize=0)

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
    DG2.setMaxMin()
    DG2.show()

    DG3 = DG + DG2
    DG3.setMaxMin()
    DG3.saveImage(outputFolder+ DG.name + '_perturbed.jpg')
    DG3.show()
    DG3.outputPath = outputFolder+ DG.name + '_perturbed.dat'
    DG3.saveMatrix()


    res1 = DG.globalShapeFeatures(lowerThreshold=1.2, upperThreshold=4)
    res2=  DG3.globalShapeFeatures(lowerThreshold=1.2, upperThreshold=4)

    print res1
    print res2

    pickle.dump(res1, open(outputFolder+str(int(time.time()))+ 'res1.dat', 'w'))
    pickle.dump(res2, open(outputFolder+str(int(time.time()))+ 'res2.dat', 'w'))


##########################################################
#   analysis
folder = outputFolder
L=os.listdir(folder)
L = [v for v in L if '.dat' in v]
L1 = [v for v in L if 'res1' in v]
L2 = [v for v in L if 'res2' in v]

#   test case
x = pickle.load(open(outputFolder+L1[0],'r'))
x

#   stats
L = os.listdir(folder)
def summarise(folder=folder, L=L, key1='res1', key2='.dat', nokey1=None,):
    ##################################################################################################
    ##################################################################################################
    ##  adapted from armor/tests/localFeaturesDistributionTest.py
    #   
    #def summarising(folder=outputFolder):
    summaryFolder = folder + 'summaries/'
    if not os.path.exists(summaryFolder):
        os.makedirs(summaryFolder)
    L = [v for v in L if key1 in v and key2 in v]
    print '\n'.join([str(v) for v in L][:20]) #check
    time.sleep(3)

    if nokey1 is not None:
        L = [v for v in L if not nokey1 in v]
    fileName = L[0]
    lf   = pickle.load(open(folder+fileName))
    keys = sorted(lf.keys(), key=lambda v:v.lower())

    def keySize(dic, k):
        try:
            n = dic[k].size
        except AttributeError:
            try:
                n = dic[k].__len__()
            except AttributeError:
                n = 1
        return n 

    keySizes = [keySize(lf, v) for v in keys]   
    print keySizes
    print [(keys[v], keySizes[v]) for v in range(len(keys))]
    keysFull =  sum([[keys[i]]*keySizes[i] for i in range(len(keys))],[])
    print keysFull
    time.sleep(3)
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

    featsArr = np.zeros((1, len(keysFull)))
    for fileName in L:
            lf   = pickle.load(open(folder+fileName))
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

    featsArr = featsArr[1:,:]
    featsFileName = 'featuresArr_' + key1 + "_" + '.dat'
    featsFile = open(summaryFolder+featsFileName,'a')
    featsFile.write('#' + '  '.join(keysFull) + '\n')
    np.savetxt(featsFile, featsArr)
    featsFile.close()

    ###############################################################################
    #   plotting
    #
    folder = summaryFolder
    fileName = featsFileName
    featsFile = open(folder+fileName)
    featsArr = np.loadtxt(featsFile)

    for i in range(len(keysFull)):
        feat0 = featsArr[:,i]
        y, x = np.histogram(feat0, 50)
        plt.clf()
        plt.plot(x[:-1], y)
        plt.title(keysFull[i]+str(i))
        plt.savefig(summaryFolder+ keysFull[i] + "_" + str(i)+ "_" + key1 + '.jpg')
        plt.show(block=False)
        
    #
    ##  end adapted from armor/tests/localFeaturesDistributionTest.py
    ##################################################################################################
    ##################################################################################################

for key1 in ['res1', 'res2']:
    summarise(key1=key1)
