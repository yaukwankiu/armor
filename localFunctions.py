"""
local functions adapted from
test102.py


"""


###########
#imports

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from scipy import signal
import numpy as np
import numpy.ma as ma
from armor import pattern
from armor.shiiba import regression2 as regression
from armor.advection import semiLagrangian
sl = semiLagrangian
from imp import reload
import time
from copy import deepcopy
lsq = np.linalg.lstsq

time0= time.time()

def tic():
    global timeStart
    timeStart = time.time()

def toc():
    print "time spent:", time.time()-timeStart

dbz=pattern.DBZ

windowBottom    = 300
windowTop       = 400
windowLeft      = 300
windowRight     = 400

################
# set up

a = dbz('20120612.0200')
b = dbz('20120612.0210')

a.load()
b.load()

################################
# test


def getMatrixShifts(a, scope=(9,9),verbose=True):
    L = []
    for i in range(-scope[0]//2+1, scope[0]//2+1):
        for j in range(-scope[1]//2+1, scope[1]//2+1):
            if verbose:
                print (i,j), "..., ",
            L.append(a.shiftMatrix(i,j).matrix)
    return L

def getLocalVariance(a, scope=(5,5), verbose=True):
    """ to get the local variance in a neighbourhood of every point of a
    variance = mean(X^2) - mean(X)^2
    """
    matrixShifts = getMatrixShifts(a, scope, verbose=verbose)        # matrixShifts[i+Nj]=a.shiftMatrix(i,j)
                                                    # where N=9 for the moment
    height, width   = a.matrix.shape
    matrixShifts    = [v.reshape(height*width) for v in matrixShifts]   #flatten before stacking
    matrixShifts    = ma.vstack(matrixShifts)

    #matrixCounts    = (1-matrixShifts.mask).sum(axis=0)         #count the valid entries at each position
    #matrixSums      = matrixShifts.sum(axis=0)
    #matrixSquares   = matrixShifts**2
    #matrixSquareSums= matrixSquares.sum(axis=0)
    #localVariance = matrixSquareSums*1./matrixCounts - (matrixSums*1./matrixCounts)**2
    localVariance   = matrixShifts.var(axis=0)
    localVariance   = localVariance.reshape(height, width)      # reform the matrix
    if verbose:
        print "local variance sum, var=", localVariance.sum(), localVariance.var()
    return localVariance

def getLocalMean(a, scope=(5,5), verbose=True):
    
    matrixShifts = getMatrixShifts(a, scope)       
    height, width   = a.matrix.shape
    matrixShifts    = [v.reshape(height*width) for v in matrixShifts]   #flatten before stacking
    matrixShifts    = ma.vstack(matrixShifts)

    localMean = matrixShifts.mean(axis=0)
    localMean = localMean.reshape(height,width)
    if verbose:
        print "the mean and var for localMean:", localMean.mean(), localMean.var()
    return localMean
    
def getLocalVarianceOverMean(a, scope, smoothingCoefficient=21., verbose=True):
    """ not the most efficient but it suffices
    """
    localMean = getLocalMean(a=a, scope=scope, verbose=verbose)
    localVariance = getLocalVariance(a=a, scope=scope, verbose=verbose)
    return 1.* (smoothingCoefficient + localVariance)/(smoothingCoefficient +localMean )

def getLocalProduct(a, b, scope=(9,9)):
    """ to get the local "dot product" in a neighbourhood of every point of a 
    11 march 2013
    """ 
    height, width = a.matrix.shape
    aShifts = getMatrixShifts(a, scope)
    bShifts = getMatrixShifts(b, scope)
    aShifts    = [v.reshape(height*width) for v in aShifts]   #flatten before stacking
    aShifts    = ma.vstack(aShifts)    
    bShifts    = [v.reshape(height*width) for v in bShifts]   #flatten before stacking
    bShifts    = ma.vstack(bShifts) 
    localProduct    = (aShifts * bShifts)
    localProduct    = 1. * localProduct.mean(axis=0)
    localProduct    = localProduct.reshape(height,width)
    return localProduct

def getLocalCovariance(a, b, scope=(9,9), verbose=True):
    localProduct = getLocalProduct(a=a, b=b, scope=scope)
    aMean        = getLocalMean(a=a, scope=scope, verbose=False)
    bMean        = getLocalMean(a=b, scope=scope, verbose=False)

    localCovariance =  localProduct - aMean * bMean
    if verbose:
        print "the mean and var for localCovariance:", localCovariance.mean(), localCovariance.var()

    return localCovariance
    
def getLocalCorrelation(a, b, scope=(7,7), verbose=True):
    """
    (811401,) (811401,) (811401,)
    208.300295858
    54067.9823039
    localCorr.max() 1.0
    the mean and var for local corr: 0.18482584644 0.189520182231
    time spent: 19.9111940861
    >>> LC=dbz(matrix=lc)
    """
    #localCov    = getLocalCovariance(a=a, b=b, scope=scope)
    #aVar        = getLocalVariance(a=a, scope=scope)
    #bVar        = getLocalVariance(a=b, scope=scope)
    #localCorr   = localCov / (aVar * bVar)**0.5
    tic()
    aa = a.copy()
    bb = b.copy()
    height, width = aa.matrix.shape
    commonMask = aa.matrix.mask + bb.matrix.mask
    aa.matrix.mask = commonMask
    bb.matrix.mask = commonMask
    aa.matrix.unshare_mask
    bb.matrix.unshare_mask
    
    aShifts = getMatrixShifts(aa, scope)
    bShifts = getMatrixShifts(bb, scope)
    aShifts    = [v.reshape(height*width) for v in aShifts]   #flatten before stacking
    aShifts    = ma.vstack(aShifts)    
    bShifts    = [v.reshape(height*width) for v in bShifts]   #flatten before stacking
    bShifts    = ma.vstack(bShifts) 
    #print "\n........................."
    #print aShifts.shape
    localProduct    = (aShifts * bShifts)
    localProduct    = localProduct.mean(axis=0)
    #print 'local product', localProduct.shape
    
    aVar            = aShifts.var(axis=0)
    bVar            = bShifts.var(axis=0)
    aMean           = aShifts.mean(axis=0)
    bMean           = bShifts.mean(axis=0)
    
    #print "........................."
    #print aVar.shape, aMean.shape, localProduct.shape
    #print (localProduct-aMean*bMean).max()
    #print (aVar*bVar).max()
    localCorr       = (localProduct - aMean*bMean) / (aVar * bVar)**.5
    #localCorr    = localCorr * (localCorr>=-1.0000001) * (localCorr<=1.0000001)    #cutting the pathologies
    localCorr.mask+= (localCorr<-1.0000001) + (localCorr>1.0000001)    #masking the pathologies

    #print "localCorr.max()", localCorr.max()
    if verbose:
        print "the mean and var for local corr:", localCorr.mean(), localCorr.var()
    localCorr    = localCorr.reshape(height,width)
    toc()
    return localCorr

def correlation(a, b, scope=(9,9), verbose=True):
    """alias        
    """    
    return getLocalCorrelation(a=a,b=b,scope=scope, verbose=verbose)
        
################################
# output

def main1(a=a, b=b, scope=(5,5)):
    """ to compute for the variance in a neighbourhood 
    with dimensions defined by the scope variable
    """
    tic()
    var_a   = getLocalVariance(a, scope=scope)     # a 881x921 matrix
    print var_a
    print sum(var_a)
    print a.matrix.shape
    toc()
    #cov_ab  = getLocalCovariance(a, b, scope=scope)
    return var_a

def main2(a=a, b=b, scope=(5,5),smoothingCoefficient=21.):
    lv = getLocalVarianceOverMean(a=a, scope=scope, smoothingCoefficient=smoothingCoefficient)
    print "\n-------------\n local variance over mean:", lv
    return lv

def main(a=a, b=b, scope=(5,5)):
    return main2(a=a, b=b, scope=scope)
if __name__ == '__main__':
    main()
    
