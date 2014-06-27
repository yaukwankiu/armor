#   armor/spectral/powerSpec1.py
#   migrated from armor/test/
#   2014-06-17
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
if __name__ == "__main__":
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
    
def getLaplacianOfGaussianSpectrum(a, sigmas=sigmas, thres=thresPreprocessing, outputFolder=outputFolder,
                                     #spectrumType="numerical",      #2014-06-23
                                     useLogScale= False,        #2014-06-23
                                     responseThreshold=0.01 ,      #2014-06-23
                                     scaleSpacePower=scaleSpacePower, # 2014-06-24
                                     tipSideUp = True,               #2014-06-24
                                     useOnlyPointsWithSignals=True,    #2014-06-26
                                     toReload=True,):

    shutil.copyfile(scriptFolder+thisScript, outputFolder+ thisScript)  #2014-06-25
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
        ###################################
        #   key line
        arr1    = (-1) ** tipSideUp * \
                  ndimage.filters.gaussian_laplace(arr0, sigma=sigma, mode="constant", cval=0.0) *\
                   sigma**scaleSpacePower       # #2014-06-25       
        #
        ###################################

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

        ##########################################
        #   key - to set up an appropriate mask to cut out unwanted response signals
        #   2014-06-24
        mask    = (arr1 < responseThreshold)    #2014-06-24
        #mask    += (ndimage.filters.median_filter(a.matrix,4)>0) #2014-06-25
        #mask    += (arr1>10000)
        if useOnlyPointsWithSignals:
            mask    += (a.matrix <=0)
       
        arr1    = np.ma.array(arr1, mask=mask, fill_value=0)
        #print "useOnlyPointsWithSignals", useOnlyPointsWithSignals
        #plt.imshow(arr1) ; plt.show()  #debug
        
        #
        ############################################


        ###############################################################################
        #   computing the spectrum, i.e. sigma for which the LOG has max response
        #   2014-05-02
        a.responseImages.append({'sigma'    : sigma,        
                                 'matrix'   : arr1 * sigma**scaleSpacePower,
                                 })

    a.restoreMatrix(0)
    pickle.dump(a.responseImages, open(outputFolder+a.name+"responseImagesList.pydump",'w'))

    a_LOGspec     = dbz(name= a.name + "Laplacian-of-Gaussian_numerical_spectrum",
                        imagePath=outputFolder+a1.name+"_LOG_numerical_spec.png",
                        outputPath = outputFolder+a1.name+"_LOG_numerical_spec.dat",
                        cmap = 'jet',
                        coastDataPath = a.coastDataPath
                        )
    a.responseImages    = np.ma.dstack([v['matrix'] for v in a.responseImages])
    a.responseMax       = a.responseImages.max(axis=2)  # find max along the deepest dimension
    a.responseMax       = np.ma.array(a.responseMax, mask = 0)
    a.responseMax.mask += (a.responseMax <responseThreshold)

    if useLogScale:
        aResponseMax = np.log10(a.responseMax)
    else:
        aResponseMax = a.responseMax
    aResponseMax = np.ma.array(aResponseMax)
    #aResponseMax.mask = 0
    vmax = aResponseMax.max()
    vmin = aResponseMax.min()
    print "vmax, vmin for ", a.name, ":", vmax, vmin
    a.drawCoast(matrix=aResponseMax)
    a.saveImage(imagePath=outputFolder+a.name+"LOG_max_response.png", 
                matrix =aResponseMax,
                title=a.name+" Max Responses of L-O-G filter",
                vmax = vmax, vmin=vmin)
    #a.restoreMatrix('goodcopy')
    a_LOGspec.matrix = np.zeros(a.matrix.shape)
    for count, sigma in enumerate(sigmas):
        a_LOGspec.matrix += sigma * (a.responseMax == a.responseImages.filled()[:,:,count])
    mask = (a_LOGspec.matrix ==0)
    a_LOGspec.matrix = np.ma.array(a_LOGspec.matrix, mask=mask)
    #else:
    a.LOGtotalSpec    = a.responseImages.sum(axis=0).sum(axis=0)  # leaving the deepest dimension -the sigmas
    #   end numerical spec / total spec fork
    ###
    if useLogScale:
        a_LOGspec.matrix = np.log10(a_LOGspec.matrix)
        a.LOGtotalSpec   = np.log10(a.LOGtotalSpec)
    a_LOGspec.setMaxMin()
    ##########################################
    #   2014-06-24
    #mask    = (a_LOGspec.matrix <=0.001)
    #a_LOGspec.matrix = np.ma.array(a_LOGspec.matrix, mask=mask, fill_value=-999.)
    #
    ##########################################
    pickle.dump(a_LOGspec, open(outputFolder+ a_LOGspec.name + ".pydump","w"))    
    print a_LOGspec.outputPath
    print "saving to:", a_LOGspec.imagePath
    a_LOGspec.backupMatrix('goodCopy')
    a_LOGspec.drawCoast()
    a_LOGspec.saveImage()
    a_LOGspec.restoreMatrix('goodCopy')
    a_LOGspec.saveMatrix()


    a_LOGspec.histogram(display=False, matrix=a_LOGspec.matrix, outputPath=outputFolder+a1.name+\
                        "_LOGspec_numerical" +  ("_logScale" * useLogScale) + "_histogram.png")
    plt.close()
    plt.plot(sigmas, a.LOGtotalSpec)      # plot(xs, ys)
    plt.title(a.name+" Total Spectrum for the L-O-G Kernel")
    plt.savefig(outputFolder + a.name + "_LOGspec_total"+  \
                        ("_logScale" * useLogScale) + "_histogram.png")
    pickle.dump(a.LOGtotalSpec, open(outputFolder+ a.name + "LOGtotalSpec.pydump","w"))        


    ########################################################
    #   3d plots
    #   1. total/full spec
    #   2. max spec
    #   2014-06-27
    dataSource = a.name
    responseImages = pickle.load(open(outputFolder+a.name+"responseImagesList.pydump")) #load it back up
    X, Y    = np.meshgrid(range(20), sigmas)
    I, J    = Y, X
    Z       = np.zeros(X.shape)
    z       = np.zeros(X.shape)
    for j in range(len(responseImages)):
        M       = responseImages[j]['matrix']
        #M       = M*(M>0)
        sigma   = responseImages[j]['sigma']
        print j, sigma, '\t', M.min(), '\t', M.max()
        h   = np.histogram(M, bins=20, range=(0,20))
        z[j,:] = h[0]
    Z   +=z 
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
    plt.title(dataSource+ " DBZ images\n"+\
              "x-axis:  response intensity(from 0 to 20)\n"+\
              "y-axis:  log_2(sigma)\n"+\
              "z-axis:  log_2(count)\n")
    plt.xlabel('response intensity')
    plt.ylabel('log2(sigma)')
    #   saving
    fig.savefig(outputFolder+ "3d_numspec_plot_log2scale.png", dpi=200)
    pickle.dump({"X": X, "Y":Y, "Z":Z}, open(outputFolder+'XYZ.pydump','w'))
    #pickle.dump(fig,open(outputFolder+"fig.pydump","w"))   #doesn't work

    #   end 3d plots
    #########################################################



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

