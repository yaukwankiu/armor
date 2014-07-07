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
            #spectrumType = "numerical", 
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
    psResults = ps1.getLaplacianOfGaussianSpectrum(a, thres=0, outputFolder=outputFolder,
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

    spectrum3d.spectrum3d(XYZmax, outputFolder=outputFolder, fileName  = str(time.time())+ 'maxSpec3d_' + a.name+ '.png')
    spectrum3d.spectrum3d(XYZtotal, outputFolder=outputFolder, fileName= str(time.time())+ 'totalSpec3d_' + a.name+'.png')

    if b != "":
        psResults_b = powerSpec(b, thres=thres, outputFolder=outputFolder, toReload=toReload, 
            #spectrumType = "numerical", 
            **kwargs)
        XYZmax2     = psResults_b['XYZmax']
        XYZtotal2   = psResults_b['XYZtotal']
        fileName1   = str(time.time())+ "maxSpec_" + a.name + "_" + b.name + ".png"
        fileName2   = str(time.time())+ "totalSpec_" + a.name + "_" + b.name + ".png"
        
        #specContour.specContour(XYZ=XYZmax, XYZ2=XYZmax2, outputFolder=outputFolder, fileName=fileName1)
        #specContour.specContour(XYZ=XYZtotal, XYZ2=XYZtotal2, outputFolder=outputFolder, fileName=fileName2)

    fileName1   = str(time.time())+ "maxSpec_" + a.name + ".png"
    fileName2   = str(time.time())+ "totalSpec_" + a.name + ".png"
    ##specContour.specContour(XYZ=XYZmax,  outputFolder=outputFolder, fileName=fileName1)
    ##specContour.specContour(XYZ=XYZtotal,outputFolder=outputFolder, fileName=fileName2)
    #specContour.specContour(XYZ=XYZmax,  display=True)
    #specContour.specContour(XYZ=XYZmax,  display=True)
    return psResults


##############################################################################s


def main():
    pass
    
if __name__ == '__main__':
    main()





