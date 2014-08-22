#comprefFeatureExtractionTest.py
import pickle
import time
import os
from matplotlib import pyplot as plt
from armor import objects4 as ob
from armor import defaultParameters as dp
outputFolder = dp.root + 'labLogs2/featureExtraction/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
testComprefs = ob.may2014.list[20:60:6] + ob.monsoon[20:40:6] + \
               ob.march2014.list[20:40:6] + ob.kongrey.list[20:40:6]

classificationResults = []
for a in testComprefs:
    t0 = time.time()
    plt.close()
    print '\n------------------------------------------\n', a.name
    a.load()
    a.initialiseFeatures()
    print 'granulometry features'
    a.granulometryFeatures(multiplier=1.)
    print 'gabor features'
    a.gaborFeatures(multiplier=10.)
    result = a.classify()
    classificationResults.append(result)
    pickle.dump(result, open(outputFolder + 'feature_classification' +\
                 str(time.time()) + a.name + '.pydump', 'w'))
    t1 = time.time()
    print 'time spent for', a.name, t1 - t0, 'seconds'
    print '\n-------------------------------------------\n'
