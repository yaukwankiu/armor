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
#
timeStamp0   = str(int(time.time()))
outputFolder = dp.root + 'labLogs2/charts2_local_features_distribution/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
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
        
