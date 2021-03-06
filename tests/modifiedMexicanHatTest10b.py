"""
#   purpose:    to draw the numerical spectra weighed by response values
#   kongrey/march2014

    1.  get the file lists
    2.  load them one by one
    3.  compute the mean of the spectra
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from armor import pattern
from armor import defaultParameters as dp
dbz = pattern.DBZ
DS  = pattern.DBZstream

########################################################################
#   parameters and settings

fileNameKey1= 'responseImagesList.pydump'
fileNameKey2= 'numerical_spectrum.pydump'
dataFolder  = dp.root + "labLogs/2014-5-6-modifiedMexicanHatTest10/"
outputFolder= dataFolder
outputChartName = "Average_LOG_Numerical_Spectrum_weighed_by_Response_Intensity"
filesList       = os.listdir(dataFolder)
responseImageFiles  = [v for v in filesList if fileNameKey1 in v]
numSpecFiles        = [v for v in filesList if fileNameKey2 in v]
##############################################################################

streamMean  = 0.
dbzCount    = 0


for i in range(len(responseImageFiles)):
    #   loading
    responseFileName = responseImageFiles[i]
    numSpecFileName  = numSpecFiles[i]     
    print "\n================================="
    print responseFileName
    responseImages   = pickle.load(open(dataFolder+responseFileName, 'r'))
    numSpec          = pickle.load(open(dataFolder+numSpecFileName, 'r'))
    dbzCount        +=1
    #   processing
    sigmas= sorted([v['sigma'] for v in responseImages])
    print "sigmas=", sigmas
    weighedSpec = []    #initialise
    for sigma in sigmas:
        responseImage   = [v['matrix'] for v in responseImages if v['sigma']==sigma][0]
        weighedSpec.append((responseImage * (numSpec.matrix==sigma)).sum())    #   key line

    #   updating the average        
    weighedSpec = np.array(weighedSpec)
    streamMean  = (1 * (dbzCount-1) * streamMean + weighedSpec)/dbzCount
    print "streamMean=", streamMean
    
    #creating the charts
    plt.close()
    plt.plot(sigmas, streamMean)
    plt.title(outputChartName + "\n" +\
              "from " + str(dbzCount) + "Images" +\
              numSpec.name[:14])
    plt.savefig(outputFolder+ "!" + outputChartName + ".png")
        


#   run modifiedMexicanHatTest6a.py and then:

streamMeanWRF   = np.array([ 12460.94006035,  23620.91736223,  35058.68269145,  38812.64041611,
                            46380.50953056,  49557.61803704,  55127.16111245,  57473.54526046,
                            61328.413192  ,  61618.77713472,  56375.54510448,  50876.79599348,
                            32416.52249967])
sigmasWRF       = np.array([1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128])

streamMeanCOMPREF   = streamMean
sigmasCOMPREF       = np.array(sigmas)
plt.close()
plt.plot(sigmasCOMPREF, streamMeanCOMPREF)
plt.plot(sigmasWRF*4, streamMeanWRF*16)
plt.title("COMPREF and WRFs mean max-response LOG spectra from Kong-Rey data")
plt.show()

        
