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
dataFolder  = dp.root + "labLogs/2014-5-7-modifiedMexicanHatTest9/"
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
              "from " + str(dbzCount) + "Images")
    plt.savefig(outputFolder+ "!" + outputChartName + ".png")



        
