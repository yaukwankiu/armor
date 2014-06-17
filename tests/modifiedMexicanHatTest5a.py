#   supplementing modifiedMexicanHatTest5.py
#   outputing the charts, given the results
import numpy as np
import matplotlib.pyplot as plt
from armor import pattern
from armor import defaultParameters as dp
dbz = pattern.DBZ
DS  = pattern.DBZstream

dataFolder  = dp.root + "labLogs/2014-5-2-modifiedMexicanHatTest5/"
outputFolder= dataFolder
WRFnames    = [ "WRF"+("0"+str(v))[-2:] for v in range(1,21)]

sigmas      = [1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128, 160, 256, 320,]
allWRFsStreamMean  = 0.
dbzCount    = 0

for WRFname in WRFnames:
    ds  = DS(dataFolder=dataFolder,
                 name="kongrey" + WRFname,
                 outputFolder="",
                 imageFolder="",
                 key1=WRFname,               # keywords to pick out specific files
                 key2="LOGspec.dat",
                 key3="kongreywrf", #safety check
                 preload=True,
                 imageExtension = '.png',     #added 2013-09-27
                 dataExtension  = '.dat',
                 )
    print "\n==================\nSaving histograms for ", ds.name
    for dbzpattern in ds:
        dbzCount    += 1
        streamMeanUpdate = np.array([(dbzpattern.matrix==v).sum()   for v in sigmas])
        allWRFsStreamMean  = 1.* ((allWRFsStreamMean*(dbzCount -1)) + streamMeanUpdate ) / dbzCount
        histogramName   = "kongreywrf" + dbzpattern.dataTime + WRFname + "_LOGspec_histogram"+ ds.imageExtension
        print dbzpattern.name, "->", histogramName
        plt.clf()
        dbzpattern.histogram(display=False, outputPath=outputFolder+histogramName)


plt.close()
plt.plot(sigmas, allWRFsStreamMean)
plt.title(ds.name + '- average laplacian-of-gaussian max-response spectrum for ' +str(dbzCount) + 'WRF patterns')
plt.savefig(outputFolder + ds.name + "_all_wrfs_average_LoG_max_response spectrum.png")
plt.close()

"""
#   run modifiedMexicanHatTest6a.py and then:
allWRFsStreamMean   = array([ 2562.4375,   655.5625,   526.15  ,   741.51  ,   858.6425,
                            1457.79  ,  1710.095 ,  2971.355 ,  3561.9125,  4406.915 ,
                            1488.0375,    59.5925,     0.    ,     0.    ,     0.    ,     0.    ])

streamMeanCOMPREF   = streamMean
sigmas  = np.array(sigmas)
plt.close()
plt.plot(sigmas, streamMeanCOMPREF)
plt.plot(sigmas[:-4]*4, allWRFsStreamMean[:-4]*16)
plt.title("COMPREF and WRFs mean max-response LOG spectra from Kong-Rey data")
plt.show()

"""
