#   powerSpec1.py
#   test script for computing power spectrum
#   2014-06-10
"""
== Spectral analysis ==

0.  RADAR domain -> normalise to WRF domain

tests to do - 
1.  average each 4x4 grid in RADAR then compare the spectrum of the resulting image
    to the original RADAR image
    
2.  filter (gaussian with various sigmas)   and then averge each 4x4 grid
3.  oversampling (compute 4x4 averages 16 times)

4.  plot power spec for WRF and various preprocessings
    A.  WRF + RADAR/4x4 normalised (with or without oversampling)/no pre-filtering
    B.  WRF + RADAR/4x4 normalised (with or without oversampling)/pre-filter 1,2,3...
        (unspecified/trial and error)
    C.  RADAR/normalise/no filtering  + RADAR/normalised/pre-filtered 1,2,3...
        + difference
        
    D.  test successive gaussian filtering - is the result the same as doing it once
        with a variance equal to the sum of variances?
        

USE

from armor.tests import powerSpec1 as ps
from armor import pattern
from armor import objects4 as ob
from armor import defaultParameters as dp
import numpy as np
import matplotlib.pyplot as plt

reload(ps); a_LOGspec = ps.testA(dbzList=ob.kongrey)

reload(ps); a_LOGspec = ps.testAwrf(dbzList=ob.kongreywrf)


"""
#   imports

import pickle, os, shutil, time
from armor import defaultParameters as dp
from armor import pattern
from armor import objects4 as ob
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from scipy import ndimage
from scipy import signal

dbz=pattern.DBZ
root = dp.rootFolder
timeString  = str(int(time.time()))
ob.march2014wrf.fix()
ob.kongreywrf.fix()

###############################################################################
#   defining the parameters

thisScript      = "powerSpec1.py"
testName        = "powerSpec1"
scriptFolder    = root + "python/armor/tests/"
outputFolder    = root + "labLogs/powerSpec1/" + timeString + "/"

sigmaPreprocessing=20
thresPreprocessing=0

radarLL = np.array([18., 115.]) # lat/longitude of the lower left corner for radar data grids
wrfLL   = np.array([20.,117.5])
wrfGrid = np.array([150,140])
radarGrid=np.array([881,921])
wrfGridSize = 0.05              #degrees
radarGridSize=0.0125
radar_wrf_grid_ratio = wrfGridSize / radarGridSize
#sigmas  = [1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128, 160, 256,]
sigmas  = [1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128]
scaleSpacePower = 0
dbzList = ob.kongrey

############################################################################
#   setting up the output folder
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

shutil.copyfile(scriptFolder+thisScript, outputFolder+ thisScript)

#   defining the functions:
#       filtering, averaging, oversampling

def filtering(a, sigma=sigmaPreprocessing):
    """gaussian filter with appropriate sigmas"""
    a.matrix = a.gaussianFilter(sigma=sigma).matrix

def averaging(a, starting=(0,0)):
    """4x4 to 1x1 averaging
    oversampling 4x4 to 1x1 avaraging with various starting points"""

    starting = (wrfLL - radarLL)/radarGridSize + starting
    ending   = starting + wrfGrid * radar_wrf_grid_ratio
    mask      = 1./16 * np.ones((4,4))
    a1  = a.copy()
    a1.matrix = signal.convolve2d(a1.matrix, mask, mode='same')  #http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html

    a1.matrix = a1.matrix[starting[0]:ending[0]:radar_wrf_grid_ratio,
                            starting[1]:ending[1]:radar_wrf_grid_ratio,
                          ]
    a1.matrix=np.ma.array(a1.matrix)
    print 'starting, ending:',starting, ending  #debug
    return a1

def oversampling():
    """use averaging() to perform sampling
        oversampling 4x4 to 1x1 avaraging with various starting points
        and then average/compare"""

    pass
    
def getLaplacianOfGaussianSpectrum(a, sigmas=sigmas, thres=thresPreprocessing, outputFolder=outputFolder, toReload=True):
    L=[]
    a.responseImages=[]
    if toReload:
        a.load()
    a.backupMatrix(0)
    for sigma in sigmas:
        print "sigma:", sigma
        a.restoreMatrix(0)
        a.setThreshold(thres)
        arr0 = a.matrix
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
    ###
    #   numerical spec
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
    #
    ######

    print "saving to:", a_LOGspec.imagePath
    a_LOGspec.saveImage()
    print a_LOGspec.outputPath
    a_LOGspec.saveMatrix()
    a_LOGspec.histogram(display=False, outputPath=outputFolder+a1.name+"_LOGspec_histogram.png")
    pickle.dump(a_LOGspec, open(outputFolder+ a_LOGspec.name + ".pydump","w"))    
    return a_LOGspec


def plotting(folder):
    pass


#   defining the workflows
#       testA, testB, testC, testD

def testA(dbzList=ob.march2014,sigmas=sigmas):
    for a in dbzList:
        a.load()
        a.matrix = a.threshold(thresPreprocessing).matrix
        a1 = averaging(a)
        filtering(a1)
        a_LOGspec = getLaplacianOfGaussianSpectrum(a1, sigmas=sigmas)
    #return a_LOGspec

    
#def testAwrf(dbzList=ob.kongreywrf, sigmas=sigmas):
def testAwrf(dbzList=ob.march2014wrf, sigmas=sigmas):
     for a in dbzList:
        a.load()
        a.matrix = a.threshold(thresPreprocessing).matrix
        #a1 = averaging(a)
        a1=a
        filtering(a1)
        a_LOGspec = getLaplacianOfGaussianSpectrum(a1, sigmas=sigmas)
    #return a_LOGspec
   

def testB():
    '''
    oversampling
    '''
    pass

def testC():
    pass

def testD():
    pass
###   loading /setting up the objects ################################
##   old type
#   kongrey
kongrey     = ob.kongrey
kongreywrf  = ob.kongreywrf 

#   march2014
march2014   = ob.march2014
march2014wrf= ob.march2014wrf

#   may2014

##   new type
#   may2014

#   run

