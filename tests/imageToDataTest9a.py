# imageToDataTest9a.py
# to be used on terminal 801-a
# local-to-global
#################################
#   imports
import os
import time
import pickle
from armor import pattern
dbz = pattern.DBZ
dp  = pattern.dp
plt = pattern.plt
np  = pattern.np
###############################
#   setting up the parameters
inputFolder = dp.root + 'labLogs2/charts2_classification_local/'
resultFile  = 'result_1411378955.pydump'
#resultFile  = 'result_1411057730.pydump'
clusters    = pickle.load(open(inputFolder+resultFile))
centroids   = clusters[0]
N           = len(centroids)
a   = dbz('20140920.1200')
a.loadImage()
b   = dbz('20140920.1206')
c   = dbz('20140920.1300')
b.loadImage()
c.loadImage()

#a.globalShapeFeatures()
#a.localShapeFeatures()
#
#
#
#
def classify(a):
    classes = []
    localFeatureVectors = a.localShapeFeatures()['localFeatureVectors']
    for lf in localFeatureVectors:
        np.place(lf, np.isnan(lf), 0)
        np.place(lf, np.isinf(lf), 0)
        distances = []
        for centroid in centroids:
            distance = ((centroid - lf)**2).sum() **0.5  # key line
            distances.append(distance)
        distances = np.array(distances)
        #minDistance = distances.min()
        minIndex    = distances.argmin()
        classes.append(minIndex)
    return classes


classes = classify(a)
classes2 = classify(b)
classes3 = classify(c)

print '\n-------------------------------'
print a.dataTime, b.dataTime, c.dataTime
print classes
print classes2
print classes3
print '---------------------------------------------------'
time.sleep(3)
########
#   2014-09-24
timeString   = str(int(time.time()))
outputFolder = dp.root+'labLogs2/charts2_classification_global/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
logFileName  = 'log_imageToDataTest9.txt'
dates = ['20140520', '20140615', '20140920']
mins  = ['1200', '1206', '1230', '1300']

open(outputFolder+logFileName,'a').write('\n------------------------------\n'+time.asctime()+'\n')
dbz_classified = []
for d in dates:
    for m in mins:
        dataTime = str(d) + '.' + str(m)
        a = dbz(dataTime, name='chart2_'+dataTime)
        a.loadImage(rawImage=True)
        a.imagePath = outputFolder + a.name + '.jpg'
        a.saveImage()
        a.loadImage(rawImage=False)
        a.saveImage(outputFolder+a.name+'_' + str(classes)+'.jpg')
        classes = classify(a)
        dbz_classified.append((a.dataTime, classes))
        open(outputFolder+logFileName,'a').write(a.dataTime + ' , ')
        open(outputFolder+logFileName,'a').write(str(classes) +'\n')

L = os.listdir(dp.defaultImageDataFolder+'charts2-allinone-')
N = len(L)
R = (N*np.random.random(300)).astype(int).tolist()

open(outputFolder+logFileName,'a').write('\n------------------------------\n'+time.asctime()+'\n')

for index in R:
    DT =  L[index]
    DT = DT[0:4]+DT[5:7] + DT[8:10] + '.' + DT[11:15]
    dataTime = DT
    a = dbz(dataTime= dataTime, name = 'chart2_'+dataTime)
    a.loadImage(rawImage=True)
    a.imagePath = outputFolder + a.name + '.jpg'
    a.saveImage()
    a.loadImage(rawImage=False)
    classes = classify(a)
    dbz_classified.append((a.dataTime, classes))
    open(outputFolder+logFileName,'a').write(a.dataTime + ' , ')
    open(outputFolder+logFileName,'a').write(str(classes) +'\n')
    a.saveImage(outputFolder+a.name+'_' + str(classes)+'.jpg')


