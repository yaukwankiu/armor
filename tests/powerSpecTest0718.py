from armor.initialise import *; 
#march.list=[v for v in march.list if '0311.1200' in v.dataTime or '0311.1230' in v.dataTime] ; 
#marchwrf.list=[v for v in marchwrf.list if '0311.12' in v.dataTime and ('WRF01' in v.name or 'WRF02' in v.name)] ; 
from armor import analysis as an; 


march.name = "COMPREF"
marchwrf.name = "WRF14"
marchwrf.list = [v for v in marchwrf if ("WRF14" in v.name)and v.dataTime<="20140313.0000"]


marchwrf.list = marchwrf.list[:2]
march.list = march.list[:2]
res = an.crossStreamsPowerSpecTest(marchwrf, march, outputFolder='testing/', vmin=-1, vmax=4, crossContourVmax=-2, crossContourVmin=2)

