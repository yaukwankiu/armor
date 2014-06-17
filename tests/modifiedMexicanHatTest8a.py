#   supplementing modifiedMexicanHatTest5.py
#   outputing the charts, given the results

import numpy as np
import matplotlib.pyplot as plt
from armor import pattern
from armor import defaultParameters as dp
dbz = pattern.DBZ
DS  = pattern.DBZstream

dataFolder  = dp.root + "labLogs/2014-5-5-modifiedMexicanHatTest8/"
outputFolder= dataFolder
#WRFnames    = [ "WRF"+("0"+str(v))[-2:] for v in range(1,21)]


ds  = DS(dataFolder=dataFolder,                         #creating the LOGspec data stream
             name="RainbandMarch2014" ,
             outputFolder="",
             imageFolder="",
             key1="COMPREF_Rainband_March",               # keywords to pick out specific files
             key2="LOGspec.dat",
             key3="", #safety check
             preload=False,
             imageExtension = '.png',     #added 2013-09-27
             dataExtension  = '.dat',
             )
print "\n==================\nSaving histograms for ", ds.name


sigmas      = [1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128, 160, 256, 320,]
streamMean  = 0.
dbzCount    = 0
for dbzpattern in ds:
    dbzpattern.load()
    dbzCount    += 1
    streamMeanUpdate = np.array([(dbzpattern.matrix==v).sum()   for v in sigmas])
    streamMean  = 1.* ((streamMean*(dbzCount -1)) + streamMeanUpdate ) / dbzCount
    histogramName   = "rainband_march_2014" + dbzpattern.dataTime  + "_LOGspec_histogram"+ ds.imageExtension
    print dbzpattern.name, "->", histogramName
    plt.clf()
    dbzpattern.histogram(display=False, outputPath=outputFolder+histogramName)

plt.close()
plt.plot(sigmas, streamMean)
plt.title(ds.name + '- average laplacian-of-gaussian max-response spectrum for ' +str(dbzCount) + ' DBZ patterns')
plt.savefig(outputFolder + ds.name + "_average_LoG_max_response spectrum.png")
plt.close()
