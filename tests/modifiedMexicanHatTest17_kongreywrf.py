#   modified mexican hat wavelet test.py
#   spectral analysis for RADAR and WRF patterns
#   NO plotting - just saving the results:  LOG-response spectra for each sigma and max-LOG response numerical spectra
#   pre-convolved with a gaussian filter of sigma=10

import os, shutil
import time, datetime
import pickle
import numpy as np
from scipy import signal, ndimage
import matplotlib.pyplot as plt
from armor import defaultParameters as dp
from armor import pattern
from armor import objects4 as ob
#from armor import misc as ms
dbz = pattern.DBZ
kongreywrf  = ob.kongreywrf
kongreywrf.fix()
kongrey     = ob.kongrey
monsoon     = ob.monsoon
monsoon.list= [v for v in monsoon.list if '20120612' in v.dataTime] #fix
march2014   = ob.march2014
march2014wrf11  = ob.march2014wrf11
march2014wrf12  = ob.march2014wrf12
march2014wrf    = ob.march2014wrf
march2014wrf.fix()

################################################################################
#   hack

#kongrey.list = [v for v in kongrey.list if v.dataTime>="20130828.2320"]


################################################################################
#   parameters
testName    = "modifiedMexicanHatTest17_kongreywrf"
sigmas  = [1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128, 160, 256,]
dbzstreams = [kongreywrf]
sigmaPower=0
scaleSpacePower=0       #2014-05-14
testScriptsFolder = dp.root + 'python/armor/tests/'
#sigmaPreprocessing  = 10    # sigma for preprocessing, 2014-05-15
sigmaPreprocessing  = 0 
timeString  = str(int(time.time()))
outputFolder = dp.root + 'labLogs/%d-%d-%d-%s/' % \
                (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, testName)
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
shutil.copyfile(testScriptsFolder+testName+".py", outputFolder+ timeString + testName+".py")
#   end parameters
################################################################################
summaryFile = open(outputFolder + timeString + "summary.txt", 'a')


for ds in dbzstreams:
    summaryFile.write("\n===============================================================\n\n\n")
    streamMean  = 0.
    dbzCount    = 0
    #hack
    #streamMean  = np.array([135992.57472004235, 47133.59049120619, 16685.039217734946, 11814.043851969862, 5621.567482638702, 3943.2774923729303, 1920.246102887001, 1399.7855335686243, 760.055614122099, 575.3654495432361, 322.26668666562375, 243.49842951291757, 120.54647935045809, 79.05741086463254, 26.38971066782135])
    #dbzCount    = 140
    for a in ds:
        print "-------------------------------------------------"
        print testName
        print
        print a.name
        a.load()
        a.setThreshold(0)
        a.saveImage(imagePath=outputFolder+a.name+".png")

        L   = []
        a.responseImages = []   #2014-05-02
        for sigma in sigmas:
            print "sigma:", sigma
            a.load()
            a.setThreshold(0)
            arr0 = a.matrix
            #####################################################################
            if sigmaPreprocessing>0:
                arr0    = ndimage.filters.gaussian_filter(arr0, sigma=sigmaPreprocessing)           # <-- 2014-05-15
            #####################################################################
            #arr1 = signal.convolve2d(arr0, mask_i, mode='same', boundary='fill')
            #arr1    = ndimage.filters.gaussian_laplace(arr0, sigma=sigma, mode="constant", cval=0.0)        #2014-05-07
            #arr1    = ndimage.filters.gaussian_laplace(arr0, sigma=sigma, mode="constant", cval=0.0) * sigma**2 #2014-04-29
            arr1    = ndimage.filters.gaussian_laplace(arr0, sigma=sigma, mode="constant", cval=0.0) * sigma**scaleSpacePower #2014-05-14
            a1 = dbz(matrix=arr1.real, name=a.name + "_" + testName + "_sigma" + str(sigma))
            L.append({  'sigma'     : sigma,
                        'a1'   :  a1,
                        'abssum1': abs(a1.matrix).sum(),
                        'sum1'  : a1.matrix.sum(),
                      }) 
            print "abs sum", abs(a1.matrix.sum())
            #a1.show()
            #a2.show()
            plt.close()
            #a1.histogram(display=False, outputPath=outputFolder+a1.name+"_histogram.png")
            ###############################################################################
            #   computing the spectrum, i.e. sigma for which the LOG has max response
            #   2014-05-02
            a.responseImages.append({'sigma'    : sigma,        
                                     'matrix'   : arr1 * sigma**2,
                                     })

        pickle.dump(a.responseImages, open(outputFolder+a.name+"responseImagesList.pydump",'w'))

        a_LOGspec     = dbz(name= a.name + "Laplacian-of-Gaussian_numerical_spectrum",
                            imagePath=outputFolder+a1.name+"_LOGspec.png",
                            outputPath = outputFolder+a1.name+"_LOGspec.dat",
                            cmap = 'jet',
                            )
        a.responseImages    = np.dstack([v['matrix'] for v in a.responseImages])
        #print 'shape:', a.responseImages.shape    #debug
        a.responseMax       = a.responseImages.max(axis=2)  # the deepest dimension
        a_LOGspec.matrix = np.zeros(a.matrix.shape)
        for count, sigma in enumerate(sigmas):
            a_LOGspec.matrix += sigma * (a.responseMax == a.responseImages[:,:,count])
        a_LOGspec.vmin  = a_LOGspec.matrix.min()
        a_LOGspec.vmax  = a_LOGspec.matrix.max()
        print "saving to:", a_LOGspec.imagePath
        #a_LOGspec.saveImage()
        print a_LOGspec.outputPath
        #a_LOGspec.saveMatrix()
        #a_LOGspec.histogram(display=False, outputPath=outputFolder+a1.name+"_LOGspec_histogram.png")
        pickle.dump(a_LOGspec, open(outputFolder+ a_LOGspec.name + ".pydump","w"))
        #   end computing the sigma for which the LOG has max response
        #   2014-05-02
        ##############################################################################
                        

        #pickle.dump(L, open(outputFolder+ a.name +'_test_results.pydump','w'))     # no need to dump if test is easy
        sigmas      = np.array([v['sigma'] for v in L])
        y1 = [v['abssum1'] for v in L]
        plt.close()
        plt.plot(sigmas,y1)
        plt.title(a1.name+ '\n absolute values against sigma')
        plt.savefig(outputFolder+a1.name+"-spectrum-histogram.png")
        plt.close()

        #   now update the mean
        streamMeanUpdate = np.array([v['abssum1'] for v in L])
        dbzCount    += 1
        streamMean  = 1.* ((streamMean*(dbzCount -1)) + streamMeanUpdate ) / dbzCount
        print "Stream Count and Mean so far:", dbzCount, streamMean
        #   now save the mean and the plot
        summaryText = '\n---------------------------------------\n'
        summaryText += str(int(time.time())) + '\n'
        summaryText += "dbzStream Name: " + ds.name + '\n'
        summaryText += "dbzCount:\t" + str(dbzCount) + '\n'
        summaryText +="sigma=\t\t" + str(sigmas.tolist()) + '\n'
        summaryText += "streamMean=\t" + str(streamMean.tolist()) +'\n'
        print summaryText
        print "saving..."
        #   release the memory

        a.matrix = np.array([0])
        summaryFile.write(summaryText)
        plt.close()
        plt.plot(sigmas, streamMean* (sigmas**sigmaPower))
        plt.title(ds.name + '- average laplacian-of-gaussian numerical spectrum\n' +\
                   'for ' +str(dbzCount) + ' DBZ patterns\n' +\
                   'suppressed by a factor of sigma^' + str(sigmaPower) )
        plt.savefig(outputFolder + ds.name + "_average_LoG_numerical_spectrum.png")
        plt.close()
        
summaryFile.close()

