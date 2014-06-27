"""
to fix the file names for the data from cwb
201403111800f006_M15.txt    ->  WRF15.20140312.0000.txt
"""
#from armor import pattern
#import shutil
import os
import datetime, time
from armor import defaultParameters as dp
root        = dp.defaultRootFolder
obsFolder   = root + "data/march2014/QPESUMS/"
wrfsFolder1 = root + "data/march2014/WEPS/20140311/"
wrfsFolder2 = root + "data/march2014/WEPS/20140312/"
wrfsFolder3 = root + "data/march2014/WEPS/20140313/"
kongreywrf  = root + "data/KONG-REY/WRFEPS/"
may19       = root + "data/may14/WRFEPS19[regridded]/"
may20       = root + "data/may14/WRFEPS20[regridded]/"
may21       = root + "data/may14/WRFEPS21[regridded]/"
may22       = root + "data/may14/WRFEPS22[regridded]/"
may23       = root + "data/may14/WRFEPS23[regridded]/"

folderList = [may19, may20, may21, may22, may23]   #<-- change here
folderList=[may19]

count = 0

#for folder in [wrfsFolder1, wrfsFolder2, wrfsFolder3]:
for folder in folderList:
    print "Folder", folder
    #time.sleep(2)
    L   = os.listdir(folder)
    L   = [v for v in L if v.endswith(".txt") and not v.startswith("WRF")]  
    L.sort()
    for f1 in L:
        count   +=1
        print count, f1,
        path1   = folder + f1
        year    = int(f1[0:4])
        month   = int(f1[4:6])
        day     = int(f1[6:8])
        hour    = int(f1[8:10])
        minute  = int(f1[10:12])
        hourDiff= int(f1[13:16])
        modelNo = f1[18:20]
        suffix  = f1[20:]
        T       = datetime.datetime(year, month, day, hour, minute) + datetime.timedelta(hourDiff*1./24)
        year2   = str(T.year)
        month2  = ("0"+str(T.month))[-2:]
        day2    = ("0"+str(T.day))[-2:]
        hour2   = ("0"+str(T.hour))[-2:]
        minute2 = ("0"+str(T.minute))[-2:]
        f2      = "WRF" + modelNo + "." + year2 + month2 + day2 + "." + hour2 + minute2 + suffix
        print "->", f2
        try:
            os.rename(folder+f1, folder+f2)
        except:
            print f1, "not found!!"
