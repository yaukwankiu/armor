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


marchwrf.list = marchwrf.list
march.list = march.list

res = an.crossStreamsPowerSpecTest(marchwrf, march, outputFolder= dp.root  + 'labLogs2/powerSpec3/' + timeString + '/', vmin=-1, vmax=4, crossContourVmax=-2, crossContourVmin=2)

