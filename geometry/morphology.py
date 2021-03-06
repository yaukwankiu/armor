# -*- coding: utf-8
'''
adapted from old code:  morphology.py (July 2012)
we used x,y rather than i, j then.

USE: 

reload(mor)
from armor.morphology import morphology as mor
from armor import pattern 

a=pattern.a

mor.erode(a)

'''

"""
* morphology.py
* module for mathematical morphologies
* reference:  e.g. http://www.idi.ntnu.no/emner/tdt4265/lectures/lecture3b.pdf -  Introduction to Mathematical Morphology, by Ole Christian Eidheim, Department of Computer and Information Science

functions:
shift(M,x,y)
erode(M)
dilate(M)
beucherGradient(M)
opening(M) - morphological opening
closing(M) -    " "        closing

"""
import numpy as np
import itertools
from armor import pattern
dbz=pattern.DBZ


def shift(M, x, y, fill_value=-999):
    """ shifting the image to the right and down by x and y respectively
        padding with -999 for missing values
    """
    if isinstance(M, dbz):
        M, fill_value = M.matrix.filled(), M.matrix.fill_value
    height, width = M.shape
    
    M = np.roll(np.roll(M, y, axis=0), x, axis=1)
    if x>0:
        M[ :, 0:x] = fill_value
    if x<0:
        M[ :, x: ] = fill_value
    if y>0:
        M[0:y, : ] = fill_value
    if y<0:
        M[y:,  : ] = fill_value
    
    return M


def squareNeighbourhood(size=3):
    """ to be used in function erode, dilate, etc.
    min size = 2 (including the centre)
    """
    return list(itertools.product(range(-size//2+1,size//2+1), range(-size//2+1,size//2+1)))

def disc(radius=5):
    square = squareNeighbourhood(size=int(radius)*2+1)
    d = []
    for i, j in square:
        if i**2+j**2 <= radius**2 :
            d.append((i,j))
    return d

def erode(M, neighbourhood=squareNeighbourhood(), fill_value=-999):
    """
    18 July 2012

    generalisation of the function erode in morphology20120718.py
    experimental - to be part of a ridge detector
    input:  a 2-dim numpy array M
            a list "neighbourhood", e.g, =[(0,-1),(0,0),(0,1)] 
                                     if we want to erode along the y-direction
             
    do : erode along that neighbourhood
    """
    if isinstance(M, dbz):
        M, fill_value = M.matrix.filled(), M.matrix.fill_value
    height, width = M.shape

    #if neighbourhood =="":
    #    neighbourhood = squareNeighbourhood()
    
    fullGrid = list(itertools.product(range(height),range(width)))
    shiftedGrid = {}
    for (i,j) in neighbourhood:
        shiftedGrid[(i,j)] = shift(M, i,j)
    Meroded =    [ min([shiftedGrid[(i,j)][q,p] for (i,j) in neighbourhood]) for (q,p) in fullGrid]
    Meroded = np.array(Meroded).reshape(height,width)
    return Meroded


def dilate(M, neighbourhood=squareNeighbourhood()):
    """
    18 July 2012
    similar as above

    generalisation of the function dilate in morphology20120718.py
    experimental - to be part of a trough detector
    input:  a 2-dim numpy array M
            a list "neighbourhood", e.g, =[(0,-1),(0,0),(0,1)] 
                                     if we want to dilate along the y-direction
             
    do : dilate along that neighbourhood
    """
    if isinstance(M, dbz):
        M, fill_value = M.matrix.filled(), M.matrix.fill_value
    height, width = M.shape

    #if neighbourhood =="":
    #    neighbourhood = squareNeighbourhood()


    fullGrid = list(itertools.product(range(height),range(width)))
    shiftedGrid = {}
    for (i,j) in neighbourhood:
        shiftedGrid[(i,j)] = shift(M,i,j)
    Mdilated =    [ max([shiftedGrid[(i,j)][q,p] for (i,j) in neighbourhood]) for (q,p) in fullGrid]
    Mdilated = np.array(Mdilated).reshape(height,width)
    return Mdilated



def beucherGradient(M, neighbourhood=squareNeighbourhood(5)):
    """
    Dilation and erosion can be used to extract edge information from
    images
    – Example: Beucher gradient
     B = B − B
    16-7-2012
    """
    return dilate(M, neighbourhood=neighbourhood) - erode(M, neighbourhood= neighbourhood)

def openeth(M, neighbourhood=squareNeighbourhood(5)):
    """
    Used to remove unwanted structures in the image (e.g. noise)
    Morphological opening is simply an erosion followed by a dilation
    16-7-2012
    """
    return dilate(erode(M, neighbourhood=neighbourhood), neighbourhood=neighbourhood)

def closeth(M, neighbourhood=squareNeighbourhood(5)):
    """
    similar to openeth()
    see help(openeth) for information
    16-7-2012
    """
    return erode(dilate(M,neighbourhood = neighbourhood), neighbourhood = neighbourhood)

def hitAndMiss(M):
    pass

def intersect(M1, M2):
    """intersection of two functions = take the minimum (and zero when the domains don't overlap)
     for the moment, M1, M2 are two functions with the same domain (e.g. over all of taiwan)
    """
    return np.minimum(M1,M2)
    pass

def union(M1, M2):
    """union of two functions = take the maximum (and the existing value when the domains don't overlap)
    """
    return np.maximum(M1,M2)
    pass

def geodesicDilate(marker, mask, neighbourhood=squareNeighbourhood(3)):
    """dilate the marker, then intersect with the mask
    ~ 17 July 2012
    """
    M = dilate(marker,neighbourhood=neighbourhood)
    return np.minimum(M, mask)

def geodesicErode(marker,mask,neighbourhood=squareNeighbourhood(3)):
    """the reverse of the function geodesicDilate above
    can be used in getMinima
    18 July 2012
    NOT TESTED ALONE
    """
    M = erode(marker, neighbourhood=neighbourhood)
    return np.maximum(M, mask)

def grayscaleReconstruct(marker, mask, neighbourhood=squareNeighbourhood(3)):
    """
    ~ 17 July 2012
    J. C. Nunes et. al. (2005), p.179 top right corner
    - gray scale reconstruction
    Irec_I(J) = union over all n's >=1 of geodesic dilations of J inside I
    """
    Irec = marker
    done = False
    while not done:
        IrecNew = geodesicDilate(Irec, mask, neighbourhood = neighbourhood)
        if np.array_equal(IrecNew ,Irec):     # if stabilises then done, else continue
            done = True
        Irec = IrecNew
    return Irec

def getMaxima(M, neighbourhood=squareNeighbourhood(3)):
    """
    ~ 17 July 2012
    J. C. Nunes et. al. (2005), p.179 top right corner
    M is an array
    """
    I = M  # image
    J = I -1
    return I-grayscaleReconstruct(marker = J, mask = I, neighbourhood=neighbourhood)

def getMinima(M):
    """The reverse of the function getMaxima above.
    18 July 2012
    """
    return 1 - getMaxima(-M)   # lazy solution

def findRidges(M):
    """
    18 July 2012
    experimental:  to find ridges with erosions along x- and y-directions respectively
    """
    neighbourhoodx = [(-1,0) , (0,0) , (1,0)]
    neighbourhoody = [( 0,-1), (0,0) , (0,1)]
    neighbourhoodxy =[(-1,-1), (0,0) , (1,1)]
    neighbourhoodxy_=[(-1, 1), (0,0) ,(1,-1)]

    Mx =   getMaxima(M, neighbourhood = neighbourhoodx)
    My =   getMaxima(M, neighbourhood = neighbourhoody)
    Mxy =  getMaxima(M, neighbourhood = neighbourhoodxy)
    Mxy_ = getMaxima(M, neighbourhood = neighbourhoodxy_)
    return Mx, My, Mxy, Mxy_








