# this is the platform for testing our matching algorithms. 
# we expect that every algorithm module comes with its own self-testing functions.

# problem:  all radarcv are in binary form.  need to learn to read it from python!!!
#dataFolder1='D:/ARMOR/data/SOULIK/RADARCV/'   # RADARCV from QPESUMS
#dataFolder2='D:/ARMOR/data/SOULIK/wrf_shue/'  # Mr. Shue's model data

dataFolder1='D:/ARMOR/data_temp/'   # RADARCV from QPESUMS
dataFolder2='D:/ARMOR/data_simulation/20120611_12/'  # Mr. Shue's model data

from armor import pattern
from armor.patternMatching import algorithm1 as algorithm
from armor.basicio import dataStream

dataStream1 = pattern.DBZstream(dataFolder=dataFolder1, name="RADARCV observation")
dataStream2 = pattern.DBZstream(dataFolder=dataFolder2, name="WRF output by Shue Hung Yu")

testResults = {}
for img1 in dataStream1:
    for img2 in dataStream2:
        if img1.dataTime == img2.dataTime:
            print img1.name, img2.name,
            img1.load()
            img2.load()
            res = algorithm.selfTest(img1, img2)
            print res
            testResults[(img1.name, img2.name)] = res
        
