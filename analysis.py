# armor/analysis.py
# 
# the basic entry point / user front module of the package armor
# 16-3-2013

"""
== USE == 
e.g. for installation on usb drive "KINGSTON":
cd /media/KINGSTON/ARMOR/2013/python
python

from armor import pattern
from armor import analysis
dbz = pattern.DBZ
a = dbz('20120612.0200')
b = dbz('20120612.0210')
a.load()
b.load()
#a.dt = 1./6
#a.dx = 1.3
#a.dy = 1.3

#  etc.
reload(analyse)
x=analysis.shhiba(a, b, display=False, toFile="")
reload(analyse)
a.load()
b.load()
x=analysis.shiibaLocal(a,b)

#############
#
x1=analysis.shiiba(a, b, searchWindowWidth=15, searchWindowHeight=5, useRecursion=True)
## <---- seconds

x2=analysis.shiiba(a, b, searchWindowWidth=15, searchWindowHeight=5, useRecursion=False)
##  <---- 44 seconds

result1 = x1['results'][0]
result2 = x2['results'][0]

(m1, n1), C1, R1 = result1
(m2, n2), C2, R2 = result2

a1 = x1['prediction']
a2 = x2['prediction']

a1.corr(b.shiftMatrix(-m1,-n1))
a2.corr(b.shiftMatrix(-m2,-n2))

(m1, n1)
(m2, n2)

C1
C2

(a1-a2).matrix.max()
(a1-a2).matrix.min()
(a1-a2).matrix.mean()
(a1-a2).matrix.var()



"""

#########################################################################
#  imports
import numpy as np
import numpy.ma as ma
from . import pattern
from graphics import spectrum3d #2014-07-04
from graphics import specContour #2014-07-04
from matplotlib import pyplot as plt
dbz = pattern.DBZ
import time
import copy
import os
try:
    from armor import objects as ob
except:
    pass
#reload(ob)
#reload(pattern)
#from armor.tests.roughwork20131106 import construct3by3
#from armor.geomtery import frames as fr

##########################################################################
#   Shiiba-ABLER
def shiiba(a,b, gridSize=20, searchWindowHeight=9, searchWindowWidth=9,\
                 display=False, useRecursion=True, toFile="", 
                 centre=(0,0),
                 ):
    """Shiiba global analysis
    """
    #   2014-01-24
    # imports
    from shiiba import regression2 as regression
    from shiiba import regressionCFLfree as cflfree
    results = cflfree.regressGlobal(a,b, gridSize, searchWindowHeight, searchWindowWidth,\
                 display, useRecursion, centre=centre)
    topResult = results[0]
    (m,n), C, Rsquared = topResult
    prediction  = regression.getPrediction(C, a)
    prediction6 = regression.getPrediction(C, a, coeffsUsed=6)
    corr        = b.corr(prediction)
    vect        = regression.convert(C,a)
    C1 = C.copy()
    C1[2] = 0
    C1[5] = 0
    deformation = regression.convert(C1, a)
    README = 'Results for shiiba global regression.  "mn" = shift, where the first coordinate is i=y, the second is j=x, "vect" =  total vector field, "deformation" = deformation vector field, "corr" = correlation between prediction and ground truth,  "prediction6"= prediction with 6 shiiba coeffs (instead of 9), "results" = list of (m,n), C, Rsquared in descending order of Rsquared'
    
    return {"mn": (m,n), "C":C, "Rsquared":Rsquared, 
            "prediction"    : prediction,
            "prediction6"   : prediction6,
            "vect"          : vect, 
            "deformation"   : deformation,
            "corr"          : corr, 
            "results"       : results, 
            "README"        :README}


def shiibaLocal(a, b, windowSize=100, iRange=range(000, 881, 100),\
                    jRange=range(000, 921, 100), searchWindowHeight=11,\
                    searchWindowWidth=11, useRecursion=True, plotting=True ):
    # imports
    from shiiba import regression2 as regression
    from shiiba import regressionCFLfree as cflfree
    import numpy.ma as ma
    #  results =dictionary with
    #         {'mn': mn, 'C':C, 'Rsquared':Rsquared, 'CR2':CR2, 'timeSpent':timeSpent}
    results=cflfree.regressLocalAll(a, b, windowSize, iRange, jRange, searchWindowHeight,\
                    searchWindowWidth, useRecursion, plotting)
    mn  = results['mn']
    C   = results['C']
    Rsquared    = results['Rsquared']
    # constructing the prediction
    a1 = dbz(name  = 'shiiba prediction for %s and %s' % (a.name, b.name),
            matrix = ma.zeros(a.matrix.shape))
    a1.matrix.fill_value = a.matrix.fill_value
    a1.mask = True
    # constructing the vector field
    U = ma.zeros(a.matrix.shape)
    U.fill_value = a.matrix.fill_value
    U.mask = True
    V = ma.zeros(a.matrix.shape)
    V.fill_value = a.matrix.fill_value
    V.mask = True
    vect = pattern.VectorField(U=U, V=V, \
                            title='shiiba prediction for %s and %s' % (a.name, b.name))
    # filling in the local values
    for i, j in mn.keys():
        aa  = a.getWindow(i, j, windowSize)
        a1.matrix[i:i+windowSize, j:j+windowSize] = regression.getPrediction(C[(i,j)], aa)

        vectLocal = regression.convert(C[(i,j)], aa)
        vect.U[i:i+windowSize, j:j+windowSize] = vectLocal.U
        vect.V[i:i+windowSize, j:j+windowSize] = vectLocal.V
        #########
        # added 15 july 2013 ; doesn't make sense to have a global vector map without adding in the mn[(i,j)]'s
        # adding the shift back to the regression result
        # (see pattern.py and regression2.py)
        vect.U[i:i+windowSize, j:j+windowSize] += mn[(i,j)][0]  # U = first (i-) component ; V = j-component 
        vect.V[i:i+windowSize, j:j+windowSize] += mn[(i,j)][1]
        #
        ##########




    results['prediction']   = a1
    results['vect']         = vect
    return results

###############################################################################
#   pattern matching

def gaussianSmooothNormalisedCorrelation(obs, wrf, sigma=20, sigmaWRF=5, thres=15, showImage=True,
                                         saveImage=True,  outputFolder=""):
    """
    to used normalised correlation to study the similarity between obs and wrf
    codes from
    armor.tests.gaussianSmoothNormalisedCorrelation2
    input:
        sigma = sigma for obs
        sigmaWRF    = sigma for wrf
    """
    if outputFolder =="":
        try:
            outputFolder = obs.imageFolder
        except AttributeError:
            outputFolder = pattern.defaultOutputFolderForImages
    if showImage:            
        import pylab
        pylab.ion()
    k = obs         # alias
    w = wrf

    matrix0   = copy.copy(k.matrix)
    k.getCentroid()
    k.setThreshold(thres)  #2014-05-30
    k.matrix = k.gaussianFilter(sigma).matrix
    #k.matrix = 100.* (k.matrix>=thres) 
    k.matrix.mask = np.zeros(k.matrix.shape)
    #k.makeImage(closeAll=True)
    #pylab.draw()
    #correlations = []

    w.getCentroid()
    w.setThreshold(thres)  #2014-05-30
    w1 = w.gaussianFilter(sigmaWRF)
    topRowName = w.name + ', gaussian(' + str(sigmaWRF) + ') and ' + k.name
    topRow = ma.hstack([w.matrix, w1.matrix, matrix0])
    #w1.matrix = 100.*(w1.matrix>=thres)
    w1.matrix.mask = np.zeros(w1.matrix.shape)
    try:
        ############################################
        #   punchlines
        w2 = w1.momentNormalise(k)
        corr    = w2.corr(k)
        w3 = w1.momentNormalise(k, extraAngle=np.pi)
        corr2   = w3.corr(k)
        if  corr2 > corr:
            print '180 degree switch: '
            print '   ', k.name, w.name ,corr, corr2, '\n................................' 
            corr = corr2
            w2 = w3 

        w2.matrix = ma.hstack([w1.matrix, w2.matrix, k.matrix])
        w2.name   = w.name + ', normalised, and ' + k.name + '\nnormalised correlation:  ' + str(corr)
        w2.matrix = ma.vstack([w2.matrix, topRow])
        w2.name  = topRowName + '\n' + "bottom row:" + w2.name
        w2.imagePath = outputFolder + w.name + '_' + k.name + '_sigma' + str(sigma) + '_thres' + str(thres) + '.png'
        w2.vmin= -20.
        w2.vmax = 100.
        if saveImage:
            w2.saveImage()
        if showImage:
            w2.makeImage(closeAll=True)
            pylab.draw()

        #
        ############################################
    #except IndexError:
    except SyntaxError:
        corr = -999
    # restoring the matrix
    k.backupMatrix('gaussian smooth normalised correlations, sigma='+ str(sigma) + 'threshold=' + str(thres)) 
    k.matrix = matrix0

    return corr

def gaussianCorr(*args, **kwargs):
    return gaussianSmooothNormalisedCorrelation(*args, **kwargs)



def drawShiibaTrajectory(a1, a2, L, 
                        k=12, 
                        backwards=True,
                        searchWindowHeight=9, searchWindowWidth=9,\
                        centre=(0,0),  
                        *args, **kwargs   
                        ):
    """
    2014-01-14
    shiiba regression, semilagrangian advection (forward or backward), 
    then plot the result

    input:  a1, a2  - DBZ objects
            L       - list of pairs of coordinates = points to be advected
            k       - steps in semilagrangian advection
    """
    x = a1.shiiba(a2, centre=centre, 
                  searchWindowHeight=searchWindowHeight,
                  searchWindowWidth=searchWindowWidth,
                  *args, **kwargs)
    vect    = x['vect'] 
    mn      = x['mn']
    vect2   = vect + mn       
    if backwards:
        vect2 = (0,0)-vect2
    L2  = vect2.semiLagrange(L, k)
    a1_new  = a1.drawCross(L, radius= 30)
    a1_new  = a1_new.drawCross(L2, radius=20)
    return a1_new

def HHT():
    pass

def wavelet():
    pass
    
def clustering():
    pass
    
def HMM():
    pass

###############################################################################
#   power spectrum



def powerSpec(a, b="", thres=0, outputFolder="", toReload=False, 
             toPlotContours=True,
             toPlot3d=True,
            #spectrumType = "numerical", 
            vmin="",
            vmax="",
            **kwargs):
    """
    updated 2014-07-03 
        including the new 3dplotting function from lin yen ting
        armor.graphics.spectrum3d
    new pipeline:
        WRF/RADAR  ->   response layers for various sigmas -> 1. max spec map
                                                              2. max internsity map
                                                              3. convolution intensity range for each sigma

                                                           -> 1.    3D max spec chart
                                                              2.    3D total spec chart
                                                          
    
    """
    plt.close()
    if outputFolder=="":
        outputFolder= a.outputFolder
    from armor.spectral import powerSpec1 as ps1
    #getLaplacianOfGaussianSpectrum(a, sigmas=sigmas, thres=thresPreprocessing, outputFolder=outputFolder, toReload=True)
    psResults = ps1.getLaplacianOfGaussianSpectrum(a, thres=thres, outputFolder=outputFolder,
                                                     toReload=toReload, 
                                                     #spectrumType=spectrumType, 
                                                     **kwargs)

    
    # all convolution results stored in a.responseImages
    #   max spectrum:  a.LOGspec
    #   convolution intensity corresponding to a.LOGspec: a.responseMax
    
    print "Results stored in file:", outputFolder
    print "Results stored in attribute:  a.maxSpec"
    maxSpec = psResults['maxSpec']
    XYZmax  = psResults['XYZmax']
    XYZtotal= psResults['XYZtotal']
    if toPlot3d:
        spectrum3d.spectrum3d(XYZmax, outputFolder=outputFolder, fileName  = str(time.time())+ 'maxSpec3d_' + a.name+ '.png')
        spectrum3d.spectrum3d(XYZtotal, outputFolder=outputFolder, fileName= str(time.time())+ 'totalSpec3d_' + a.name+'.png')

    if b != "":
        psResults_b = powerSpec(b, thres=thres, outputFolder=outputFolder, toReload=toReload, 
            #spectrumType = "numerical", 
            toPlotContours=toPlotContours, #2014-07-08
            toPlot3d=toPlot3d,
            vmin=vmin,
            vmax=vmax,
            **kwargs)
        XYZmax2     = psResults_b['XYZmax']
        XYZtotal2   = psResults_b['XYZtotal']
        fileName1   = str(time.time())+ "maxSpec_" + a.name + "_" + b.name + ".png"
        fileName2   = str(time.time())+ "totalSpec_" + a.name + "_" + b.name + ".png"
        if toPlotContours:
            try:
                plt.close()
                XYZ1 = XYZmax
                XYZ2 = XYZmax2
                if not XYZmax['Z'].max() <= 0 or not XYZmax2['Z'].max() <= 0:
                    specContour.specContour(XYZ1, XYZ2, outputFolder=outputFolder, fileName=fileName1,
                                                        vmin=vmin,
                                                        vmax=vmax,)
                else:
                    pass
                XYZ1 = XYZtotal
                XYZ2 = XYZtotal2
                plt.close()
                if not XYZtotal['Z'].max() <= 0 or not XYZtotal2['Z'].max() <= 0:
                    specContour.specContour(XYZ1, XYZ2, outputFolder=outputFolder, fileName=fileName2,
                                                        vmin=vmin,
                                                        vmax=vmax,)
                else:
                    pass
            except:
                print "Contour plot failure due to input data max = %f" % XYZmax['Z'].max()
                os.system("pause")
    # debug
    a.XYZmax = XYZmax
    a.XYZtotal = XYZtotal
    # end debug
    fileName1   = str(time.time())+ "maxSpec_" + a.name + ".png"
    fileName2   = str(time.time())+ "totalSpec_" + a.name + ".png"
    plt.close()
    specContour.specContour(XYZmax,  outputFolder=outputFolder, fileName=fileName1, vmin=vmin, vmax=vmax)   
    plt.close() 
    specContour.specContour(XYZtotal,  outputFolder=outputFolder, fileName=fileName2, vmin=vmin, vmax=vmax)    
    
    if toPlotContours:
        try:
            plt.close()
            XYZ1=XYZtotal
            XYZ2=XYZmax

            specContour.specContour(XYZ1, XYZ2, outputFolder=outputFolder, fileName=fileName2,
                                                        vmin=vmin,
                                                        vmax=vmax,)
        except:
            print "function specContour.specContour() failed!!"
            return {'XYZtotal': XYZtotal, 'XYZmax': XYZmax}
    #specContour.specContour(XYZ=XYZmax,  display=True)
    #specContour.specContour(XYZ=XYZmax,  display=True)
    return psResults

from armor.initialise import *
#WRFwindow = (200,200,600,560)

def powerSpecTest0709(a, 
                      filter="",
                      filterArgs={'sigma': 4, 'newCopy':True},
                      display=False, WRFwindow = (200,200,600,560),
                      outputFolder = "",
                      ):
    #a = march('0312.1200')[0]
    if outputFolder=="":
        outputFolder = a.outputFolder
    a.load()
    try:
        a.drawCoast()
        a.saveImage(imagePath=outputFolder+str(time.time())+a.name+'.png')
    except:
        a.saveImage(imagePath=outputFolder+str(time.time())+a.name+'.png')
    a.load()
    if display:
        a.show()

    if a.matrix.shape == (881,921):
        a.drawCoast()
        a.drawRectangle(*WRFwindow).saveImage()
        a.load()
        a1= a.getWindow(*WRFwindow)
        if filter != "":
            a1 = filter(a1, **filterArgs)
        a1.saveImage(imagePath=outputFolder+str(time.time())+a1.name+'.png')
        a2 = a1.coarser().coarser()
        a2.name = a1.name
        a2.saveImage(imagePath=outputFolder+str(time.time())+a2.name+'.png')
    else:
        a2 = a
    a2 = a2.threshold(0)
    if display:
        a2.show()
    a2.saveImage(imagePath=outputFolder+str(time.time())+a2.name+'.png')
    a2.powerSpec(outputFolder=outputFolder)


def powerSpecTest(a, outputFolder="", 
                sigmas  = [1, 2, 4, 5, 8 ,10 ,16, 20, 32, 40, 64, 80, 128],
                bins=[0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.],
                vmin=-1, vmax=5,
                *args, **kwargs):
    """
    2014-07-17
    
    """
    from graphics import spectrum3d
    from graphics import specContour
    timeStamp = str(int(time.time()))
    if outputFolder =="":
        outputFolder = a.outputFolder
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    plt.close()
    #   save the original image
    a.saveImage(outputFolder+str(time.time())+a.name+'.png')
    psResults = a.powerSpec(outputFolder=outputFolder, toPlot3d=True, toPlotContours=True, toReload=True, 
                            sigmas=sigmas, bins=bins,
                            *args, **kwargs)
    #   save the response for each gaussian filter with each sigma
    responseImages= psResults['responseImages']
    sigmas        = psResults['sigmas']
    maxSpec       = psResults['maxSpec']
    XYZmax        = psResults['XYZmax']
    XYZtotal      = psResults['XYZtotal']
    height, width, depth = responseImages.shape
    for i in range(depth):
        resp = responseImages[:,:,i]
        plt.close()
        plt.imshow(resp, origin='lower', cmap='jet',)
        plt.colorbar()
        plt.title("Filter Intensity for sigma=%d" % sigmas[i])
        plt.savefig(outputFolder+ str(time.time()) + a.name + "_LOG_sigma%d.png" %sigmas[i])

    #   save the max response sigma (2d maxspec)                            -DONE ("~LOG_numerical_spec.png")
    #   save the max responses for each max response sigma for each point  - DONE ("~_max_response.png")
    #   save all the responses                                           - DONE ("~responseImagesList.pydump")
    #   save the max spec data
    pickle.dump(maxSpec, open(outputFolder+ str(time.time()) + a.name + "maxSpec.pydump", 'w'))
    
    #   save the totalspec data                                         -pass (too big)
    #   3d plots
    plt.close()
    XYZ3dMax = spectrum3d.spectrum3d(XYZ=XYZmax, outputFolder=outputFolder, fileName=str(time.time())+a.name + "_maxSpec3d.png",
                                 title= a.name+"Max 3d Spectrum", display=True, vmin=vmin, vmax=vmax,**kwargs)
    plt.close()
    XYZ3dTotal = spectrum3d.spectrum3d(XYZ=XYZtotal, outputFolder=outputFolder, fileName=str(time.time())+a.name + "_totalSpec3d.png",
                                 title= a.name+"Total 3d Spectrum", display=True,vmin=vmin, vmax=vmax, **kwargs)

    #   contourplots

    plt.close()
    XYZcontourMax = specContour.specContour(XYZ=XYZmax, outputFolder=outputFolder, fileName=str(time.time())+a.name + "_maxSpecContour.png",
                                 title= a.name+"Max Spectrum Contours", display=True, vmin=vmin, vmax=vmax,**kwargs)
    plt.close()
    XYZcontourTotal = specContour.specContour(XYZ=XYZtotal, outputFolder=outputFolder, fileName=str(time.time())+a.name + "_totalSpecContour.png",
                                 title= a.name+"Total Spectrum Contours", display=True,vmin=vmin, vmax=vmax, **kwargs)



    #   XYZ max spec dump                                               - DONE ("~XYZmax.pydump")
    #   XYZ total spec dump                                              - DONE ("~XYZ.pydump")

    return {'XYZ3dMax'      : XYZ3dMax,
            'XYZ3dTotal'    : XYZ3dTotal,
            'XYZcontourMax' : XYZcontourMax,
            'XYZcontourTotal':XYZcontourTotal,
            'XYZmax':XYZcontourMax,
            'XYZtotal':XYZcontourTotal,
            }



def streamPowerSpecTest(ds,  outputFolder="", vmin=-1, vmax=5,*args, **kwargs):
    if outputFolder =="":
        outputFolder=ds.outputFolder
    N = len(ds)
    Ztotal=0
    Zmax  =0
    for a in ds:
        a.load()
        a1 = a.getWRFwindow()
        XYZs = powerSpecTest(a1, outputFolder=outputFolder, *args, **kwargs)
        XYZmax  = XYZs['XYZmax']
        XYZtotal= XYZs['XYZtotal']
        Zmax   += XYZmax['Z']
        Ztotal += XYZtotal['Z']
        a.matrix = np.ma.array([0]) # unload
    Zmax    /= N
    Ztotal  /= N

    XYZmax['Z']     = Zmax
    XYZtotal['Z']   = Ztotal
    plt.close()
    print "***************************************************************************************************************"    
    print "***************************************************************************************************************"    
    print "* *    Zmax, Ztotal:", Zmax, Ztotal
    print "***************************************************************************************************************"
    print "***************************************************************************************************************"
    print "sleep 5 seconds"
    time.sleep(5)

    XYZ3dMax = spectrum3d.spectrum3d(XYZ=XYZmax, outputFolder=outputFolder, fileName=str(time.time())+ ds.name+ "_mean_maxSpec3d.png",
                                 title= ("Mean Max 3d Spectrum from %d Images: " %N) + ds.name, display=True, vmin=vmin, vmax=vmax,**kwargs)
    plt.close()
    XYZ3dTotal = spectrum3d.spectrum3d(XYZ=XYZtotal, outputFolder=outputFolder, fileName=str(time.time())+ds.name+ "_mean_totalSpec3d.png",
                                 title= ("Mean Total 3d Spectrum from %d Images: " % N) + ds.name, display=True, vmin=vmin, vmax=vmax,**kwargs)

    #   contourplots
    plt.close()
    XYZcontourMax = specContour.specContour(XYZ=XYZmax, outputFolder=outputFolder, fileName=str(time.time())+ds.name+ "_mean_maxSpecContour.png",
                                 title= "Mean Max Spectrum: " + ds.name, display=True, vmin=vmin, vmax=vmax,**kwargs)
    plt.close()

    XYZcontourTotal = specContour.specContour(XYZ=XYZtotal, outputFolder=outputFolder, fileName=str(time.time())+ds.name+ "_mean_totalSpecContour.png",
                                 title= "Mean Total Spectrum: " + ds.name, display=True,vmin=vmin, vmax=vmax, **kwargs)
    plt.close()

    returnValues= {'XYZmax'    :   XYZmax,
                    'XYZtotal'  :   XYZtotal,
                    'ds'        : ds.dataFolder,
                    }
        
    pickle.dump(returnValues, open(outputFolder+str(time.time())+'dbzstreamSpec_returnValues.pydump','w'))
    return returnValues
    
def crossStreamsPowerSpecTest(ds1, ds2, outputFolder="", crossContourVmax=1, vmin=-1, vmax=5,crossContourVmin=-1, *args, **kwargs):
    """ 2014-07-17
    from armor.initialise import *; march.list=[v for v in march.list if '0311.1200' in v.dataTime or '0311.1230' in v.dataTime] ; marchwrf.list=[v for v in marchwrf.list if '0311.12' in v.dataTime and ('WRF01' in v.name or 'WRF02' in v.name)] ; from armor import analysis as an; res = an.crossStreamsPowerSpecTest(marchwrf,march, outputFolder='testing/')

    """
    plt.close()
    res1 = streamPowerSpecTest(ds1,  outputFolder=outputFolder, vmin=vmin, vmax=vmax,*args, **kwargs)
    plt.close()
    res2 = streamPowerSpecTest(ds2,  outputFolder=outputFolder, vmin=vmin, vmax=vmax,*args, **kwargs)


    XYZmax1 = res1['XYZmax']
    XYZmax2 = res2['XYZmax']
    XYZtotal1 = res1['XYZtotal']
    XYZtotal2 = res2['XYZtotal']

    if outputFolder =="":
        outputFolder = ds1.outputFolder
    
    #   contourplots
    plt.close()

    crossContourMax = specContour.specContour(XYZmax1,XYZmax2 ,outputFolder=outputFolder, fileName=str(time.time())+ds1.name+ "_versus_" + ds2.name + "_maxSpecContour.png",
                                 title= "Max Spectrum: " + ds2.name+ " (Red) - " +ds1.name , vmax=crossContourVmax, vmin=crossContourVmin, display=True)
    plt.close()

    crossContourTotal = specContour.specContour(XYZtotal1, XYZtotal2, outputFolder=outputFolder, fileName=str(time.time())+ds1.name+ "_versus_" + ds2.name + "_totalSpecContour.png",
                                 title= "Total Spectrum: " + ds2.name+ "(Red) - " +ds1.name, vmax=crossContourVmax, vmin=crossContourVmin, display=True)
    plt.close()

    returnValues= {'crossContourMax':crossContourMax, 
                'crossContourTotal':crossContourTotal,
                'ds1': ds1.dataFolder,
                'ds2': ds2.dataFolder,
                }

    pickle.dump(returnValues, open(outputFolder+str(time.time())+'crossSpec_returnValues.pydump','w'))
    return returnValues
    
##############################################################################

def randomEntropyTest(samples='all', iterations=50, sleep=3, *args, **kwargs):
    from . import objects4 as ob
    from . import initialise as ini 
    wrfsList = ini.wrfsList
    radarsList = ini.radarsList
    #wrfsList = sum([v.list for v in wrfsList],[])
    if samples == 'all':
        samples = radarsList + wrfsList
    elif samples == 'wrf' or samples =='wrfs':
        samples = wrfsList
    elif samples == 'radar' or samples =='radars' or samples =='compref':
        samples = radarsList
    N = len(samples)    
    print "name,\tsum,\tentropy:"
    for i in range(iterations):
        event = samples[int(np.random.random()*N)]
        a = event[int(np.random.random()*len(event))]
        a.load()
        entropy = a.entropy(display=True, *args, **kwargs)
        print a.name, "\t", a.matrix.sum(),"\t", a.entropy()
        #a.show(block=False)
        time.sleep(sleep)


########################################################################


def entropyLocal(a, cellSize="", region = "", iMin="", iMax="", jMin="", jMax="", stepSize="", 
                outputFolder = "", 
                display=True,threshold=-999, 
                #cmap=defaultCmap, 
                cmap = 'jet',
                verbose=True,
                *args, **kwargs):
    time0 = time.time()
    if outputFolder!="":
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
    a = a
    arr = a.matrix
    height, width = arr.shape
    if cellSize =="":
        cellSize = max(2, height//20)
    if stepSize =="":
        stepSize = max(1, cellSize//5)

    if region !="":
        iMin = region[0]
        jMin = region[1]
        iMax = iMin + region[2]
        jMax = jMin + region[3]
        
    if iMin =="":
        iMin = 0
    if jMin=="":
        jMin=0
    if iMax =="":
        iMax = height
    if jMax =="":
        jMax = width
    if verbose:
        print "Entropy for the region from (i,j) = (%d, %d) to (%d, %d)" % (iMin,jMin,iMax,jMax)
        print "stepSize  =", stepSize
    entropyMap = np.ma.zeros((height,width))
    entropyMap.mask = False
    for i in range(iMin, iMax-stepSize, stepSize):
        for j in range(jMin, jMax-stepSize, stepSize):
            #print i,j
            a1 = a.getWindow(i-cellSize//2, j-cellSize//2, cellSize, cellSize)
            ent = a1.entropy(threshold=threshold)
            if not(ent>0 or ent<=0):    #not a number, i.e. "nan" type
                ent = 0
            entropyMap[i: i+cellSize, j: j+cellSize] = ent

    #entropyMap.mask += (entropyMap== np.nan)
    EntropyMap = a.copy()
    EntropyMap.name="Entropy_Map_" + a.name
    EntropyMap.matrix = entropyMap
    EntropyMap.vmin=entropyMap.min()
    EntropyMap.vmax=entropyMap.max()
    EntropyMap.cmap=cmap
    
    if display:
        EntropyMap.show()
    a.entropyMap = EntropyMap                

    if outputFolder != "":
        EntropyMap.saveImage(outputFolder+str(time.time())+EntropyMap.name+".png")
    #############################################
    #   adopted from armor.tests.entropyTest2
    x = EntropyMap
    m = x.matrix
    mMin = m.min()
    mMax = m.max()
    entThres = 0.8 * mMax + 0.2 * mMin
    m1 = (m>entThres)

    x1=x.copy()
    x1.matrix=m1
    x2 = x1.connectedComponents()

    #a.backupMatrix(0)
    a1 = a.copy()
    for i in range(9):
        reg = (x2.getRegionForValue(i))
        if reg[0] + reg[2] > height-2 and reg[1] + reg[3]>width-2:  # if it's the entire frame
            pass
        else:
            x2 = x2.drawRectangle(*reg)
            x2.show()
            print reg
            a1=a1.drawRectangle(*reg)
            if display:
                a1.show()
    if outputFolder != "":
        a1.saveImage(outputFolder+str(time.time()) + "High_Entropy_Regions_"+a.name+".png")
    #
    ##############################################
    if verbose:
        print "time spent:", time.time() - time0
    #a.restoreMatrix(0)        
    plt.close()
    return EntropyMap

#####################################################################################################

            
def main():
    pass
    
if __name__ == '__main__':
    main()



