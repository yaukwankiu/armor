import time
timeString = str(int(time.time()))
from armor.initialise import *; 
#march.list=[v for v in march.list if '0311.1200' in v.dataTime or '0311.1230' in v.dataTime] ; 
#marchwrf.list=[v for v in marchwrf.list if '0311.12' in v.dataTime and ('WRF01' in v.name or 'WRF02' in v.name)] ; 
from armor import analysis as an; 
from armor import defaultParameters as dp

#march.name = "COMPREF"
#marchwrf.name = "WRF14"
#marchwrf.list = [v for v in marchwrf if ("WRF14" in v.name)and v.dataTime<="20140313.0000"]

ds1 = march         # <-- edit these lines
ds2 = marchwrf
#ds1 = kongrey
#ds2 = kongreywrf

N = 200

n1 = len(ds1)
n2 = len(ds2)
L1 = []
L2 = []

if N>0:
    for i in range(N):
        i1 = int(np.random.random()* n1)
        i2 = int(np.random.random()* n2)
        L1.append(ds1[i1])
        L2.append(ds2[i2])
    
    ds1.list = L1
    ds2.list = L2

res = an.crossStreamsPowerSpecTest2(ds1, ds2, outputFolder= dp.root  + 'labLogs2/powerSpec3/' + timeString + '/', 
                                    toDumpResponseImages=False, vmin=-1, vmax=4, crossContourVmax=-2, crossContourVmin=2,
                                    randomise=False,
                                    numberOfShuffles=10,
                                    numberOfTrials=300,
                                    prefilterSigmas=(4,0),          #2014-08-05
                                    )

