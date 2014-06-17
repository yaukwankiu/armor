# armor/advection/semiLagrangian.py
# to calculate advected scalar (or vector too) fields 
# will develop into the semi-Lagrangian scheme
# status:  still under development

import copy
import time
import os
import scipy
import numpy
import numpy as np
import numpy.ma as ma
#import matplotlib
import matplotlib.pyplot as plt
#import scipy.misc.pilutil as smp
#import numpy.fft as fft
#import shutil
#import sys

from .. import pattern

def shift(phi0, m=0, n=0):
    """
    shifting an array or a masked array
    returning a masked array
    """
    if not isinstance(phi0, ma.MaskedArray):
        phi0 = ma.array(phi0)
        phi0.fill_value = -999
    print phi0, m, n
    if isinstance(m, tuple):
        m, n = m
    phi0 = np.roll(phi0, m, axis=0)
    phi0 = np.roll(phi0, n, axis=1)

    return phi0

def getCoordinateGrid(m=0, n=0):
    """get the coordinate grid, [[[0,0],[0,1],[0,2]...],[[1,0],[1,1]...]]
    input:  two numbers, an ordered pair, or a numpy.ndarray
    """
    if isinstance(m, tuple):
        m, n= m
    if isinstance(m, np.ndarray):
        m, n= m.shape
    X, Y = np.meshgrid(range(m), range(n))
    XX   = X.flatten()
    YY   = Y.flatten()
    XY   = [(YY[i], XX[i]) for i in range(len(XX))]
    XY   = np.array(XY).reshape(m, n, 2)
    return XY

def interpolate1pt(phi, i=0, j=0):
    """interpolating one point only,6
    """
    #print i,j
    if isinstance(i, tuple):
        i,j = i
    try:
      val =phi[int(i)  ,int(j)  ]*(1-i%1)*(1-j%1) +\
           phi[int(i)  ,int(j)+1]*(1-i%1)*(  j%1) +\
           phi[int(i)+1,int(j)  ]*(  i%1)*(1-j%1) +\
           phi[int(i)+1,int(j)+1]*(  i%1)*(  j%1)
      return val
    except IndexError:
        return -999

def interpolate1(phi0, Ishifted, Jshifted):
    """ defining the interpolated scalar field 
    test:  820 seconds
    input: array phi0, components of a vector field (Ishifted, Jshifted)
    output: array phi2
    """
    width = len(phi0[0])
    height= len(phi0)
    phi2 = ma.zeros((height, width))      #initialise
    phi2.mask = True                    #initialise
    phi2.fill_value=-999        
    #phi2
    for i in range(height):
        for j in range(width):
            phi2[i,j] = interpolate1pt(phi0, Ishifted[i,j], Jshifted[i,j])
    return phi2    

def interpolate2(phi0, vect, scope=(9,9)):
    """interpolation with matrix operations
    see how much the speed up is
    scope = size of window to check (i.e. max speed allowed)
            default = (7,7) i.e from -3 to -3 in both i, j directions (i=y, x=j) 
    input:  phi0 - an armor.pattern.DBZ object          - a DBZ pattern
            vect - an armor.pattern.VectorField obejct  - the advection field
    output: phi2 - another armor.pattern.DBZ object

    """
    verbose     = phi0.verbose
    I_window    = range( -(scope[0]-1)/2, (scope[0]+1)/2)
    J_window    = range( -(scope[1]-1)/2, (scope[1]+1)/2)
    print "I_window, J_window =", I_window, J_window
    # 0. order of appearance:  initialisation of the variables
    # 1. set up: get the various shifted images
    # 2. compute the sums

    # ========= 0. set up ================================================
    matrix      = phi0.matrix.copy()
    width       = len(matrix[0])
    height      = len(matrix)
    X, Y        = np.meshgrid(range(width), range(height))  #standard stuff
    I_coord, J_coord = Y, X                                      #switching to I, J

    shiftedDBZ  = {}           # the dictionary is the simplest to implement, though an object list 
                               # may be slightly quicker
    matrix2        = ma.zeros((height,width))

    U           = vect.U.copy()        # the vector field
    V           = vect.V.copy()
    u           = U % 1
    v           = V % 1
    U_          = U - u
    V_          = V - v
    # debug
    print U, V, U_, V_
    # ========= 1. set up: get the various matrices  ===============================
    # shifted images
    for i in I_window:
        for j in J_window:
            shiftedDBZ[(i,j)] = phi0.shiftMatrix(i,j)

    # ========== 2. compute the sums =====================================================
    #             the square (U_==i) *(V_==j)   
    #
    #   shiftedDBZ(i,j+1)  | shiftedDBZ(i,j)
    #           .---->    _._   
    #                 ..   |
    #   advected pt- *      
    #           ________/  ^
    #          /           |
    #         .  __________.__ 
    #  shiftedDBZ(i+1,j+1)    shiftedDBZ(i+1,j)           
    #
    #
    #     u(1-v)       |  uv
    #     -------------+--------------
    #     (1-u)(1-v)   |  (1-u)v
    #
    
    for i in I_window[1:-1]:                # search window
        for j in J_window[1:-1]:
            #key line: to compute the contributions from the shifted images
            # need to sort this out.
            #??? 2013.1.31
            if verbose:
                print "\n-----------\ni = %d, j = %d, in I_window, J_window" % (i, j)
                print  shiftedDBZ[(i  ,j  )].matrix.shape,
                print  shiftedDBZ[(i+1,j  )].matrix.shape,
                print  shiftedDBZ[(i  ,j+1)].matrix.shape,
                print  shiftedDBZ[(i+1,j+1)].matrix.shape
            newTerm  = shiftedDBZ[(i  ,j  )].matrix *  (1-v) *(1-u) + \
                       shiftedDBZ[(i+1,j  )].matrix *     v  *(1-u) + \
                       shiftedDBZ[(i  ,j+1)].matrix *  (1-v) *   u  + \
                       shiftedDBZ[(i+1,j+1)].matrix *     v  *   u      
                       #upper right corner i,j
                       #lower right corner i+1,j
                       #upper left corner  j, j+1
                       #lower left corner i+1,j+1
            if phi0.verbose:
                print "\n.....\nnewterm", (i, j)
                print newTerm                    #Debug
                if  ((U_==j)*(V_==i)).sum() >0:
                    print "((U_==i)*(V_==j)).sum()", ((U_==j)*(V_==i)).sum()
            newTerm *= (U_==j) *(V_==i) 
            if phi0.verbose:            
                print "new term\n", newTerm
            matrix2 += newTerm
            print "(i, j), matrix2.sum()=\n", (i,j), matrix2.sum()     #debug

            #??? 2013.1.31
    name        = phi0.name+"_advected_by_"+vect.name
    outputPath  = phi0.outputPath + "_advected_by_"+vect.name+".dat" 
    dataPath    = outputPath
    imagePath   = phi0.outputPath + "_advected_by_"+vect.name+".png" 
    phi2 = pattern.DBZ(matrix=matrix2, name=name,\
                       dt=phi0.dt, dx=phi0.dx, dy=phi0.dy, dataPath=dataPath, outputPath=outputPath,\
                       imagePath=imagePath, database=phi0.database, cmap=phi0.cmap, verbose=phi0.verbose)

    return phi2
