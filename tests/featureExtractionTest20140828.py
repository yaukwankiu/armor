import pickle, time
from armor import pattern ; reload(pattern) ; a=pattern.a.load() ; a.initialiseFeatures()

thresholds=[20, 25, 30, 35, 40]
scales = [2,4,8,16]
for thres in thresholds:
    a.thresholdFeatures(thres)
a.gaborFeatures(scales=scales)
a.granulometryFeatures()
for thres in thresholds:
    x = a.classify(scope='selected', threshold=thres)
    pickle.dump(x, open(pattern.root+'labLogs2/featureExtraction/'+str(int(time.time())) +\
            '0200classificationResults_thres' + str(thres) + '_scales'+str(scales) +'.pydump','w'))
    x['a2'].saveImage(imagePath=pattern.root+'labLogs2/featureExtraction/'+str(int(time.time())) +\
    '0200classificationResults_thres' + str(thres) + '_scales'+str(scales) +'.png')

