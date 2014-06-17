#regrid.py
# to redraw the grids, to interpolate, etc
"""
    USE:
from armor import pattern
from armor.geometry import regrid
reload(pattern); reload(regrid)
a = pattern.a ; c = pattern.c ; a.load(); c.load(); e = regrid.regrid(a,c)
e.show()

"""


""" input: DBZ object, new_horizontal_dimension, new_vertical_dimension,
                     , new coords for the lowerleft corner
output:  new DBZ object"""

import numpy as np
from armor import defaultParameters
from armor.defaultParameters import *
from armor import pattern
DBZ = pattern.DBZ

def interpolate(arr_old, arr_new, I_old, J_old):
    """
    input:  array, i, j
    output: value

    (int(x),
    int(y)+1)
    +       +   (int(x)+1, int(y)+1)

      (x,y)

    +       +   (int(x)+1, int(y))
    (int(x),   
    int(y))
    
    be careful - floor(x)=ceil(x)=x for integer x,
                 so we really want floor(x) and floor(x)+1    
    """
    I = I_old.copy()
    J = J_old.copy()
    arr_new2 = arr_new * 0
    arr_new2 += (-999)
    height_new, width_new = arr_new.shape
    height_old, width_old = arr_old.shape
    # set all out-of-bounds to (0,0) for convenience
    I = (I>=0) * (I<height_old-1) * I   #e.g. i>=0 and i<=4 for i=[0,1,2,3,4], width=5
    J = (J>=0) * (J<width_old -1) * J

    # the loopings are necessary since we don't know beforehand where the (i_old, j_old)
    #                                  would land

    for i in range(height_new):
        for j in range(width_new):
            i0 = int(I[i,j])
            j0 = int(J[i,j])
            i1 = i0 + 1
            j1 = j0 + 1
            i_frac = i % 1
            j_frac = j % 1
            f00 = arr_old[i0,j0]
            f01 = arr_old[i0,j1]
            f10 = arr_old[i1,j0]
            f11 = arr_old[i1,j1]
            arr_new2[i, j] = (1-i_frac)*(1-j_frac) * f00 + \
                             (1-i_frac)*(  j_frac) * f01 + \
                             (  i_frac)*(1-j_frac) * f00 + \
                             (  i_frac)*(  j_frac) * f00 

    return arr_new2


def regrid(a, b):
    """
    a is the object to be resized
    b provides the relevant shape information for the process
    """
    gridSizeOld = a.matrix.shape
    gridSizeNew = b.matrix.shape
    height, width = gridSizeNew
    X, Y = np.meshgrid(range(width), range(height))
    J, I = X, Y        
    # I, J = I_new, J_new
    a_new = DBZ(name=a.name+"rescaled to "+str(gridSizeNew),
                matrix = np.zeros(gridSizeNew), 
                lowerLeftCornerLatitudeLongitude=b.lowerLeftCornerLatitudeLongitude,
                )

    latOld, longOld = a.lowerLeftCornerLatitudeLongitude
    latNew, longNew = b.lowerLeftCornerLatitudeLongitude
    latDegreePerGridOld = 1.*(a.upperRightCornerLatitudeLongitude[0]-latOld)/gridSizeOld[0]
    longDegreePerGridOld= 1.*(a.upperRightCornerLatitudeLongitude[1]-longOld)/gridSizeOld[1]
    latDegreePerGridNew = 1.*(b.upperRightCornerLatitudeLongitude[0]-latOld)/gridSizeNew[0]
    longDegreePerGridNew= 1.*(b.upperRightCornerLatitudeLongitude[0]-longOld)/gridSizeNew[1]


    #I_old = (1.* I/gridSizeNew[0]+latNew -latOld) * gridSizeOld[0]  # this is wrong
    #J_old = (1.* J/gridSizeNew[0]+latNew -latOld) * gridSizeOld[0]  # we should convert
                                                                # with the degree per grid
                                                                # as the replacement below

    I_old = (1.* I*latDegreePerGridNew  +latNew  -latOld) / latDegreePerGridOld 
    J_old = (1.* J*longDegreePerGridNew +longNew -longOld) /longDegreePerGridOld 
    # debug
    print I, J
    print I_old, J_old, I_old.shape
    print "latDegreePerGridOld , longDegreePerGridOld", latDegreePerGridOld , longDegreePerGridOld 
    print "latDegreePerGridNew , longDegreePerGridNew", latDegreePerGridNew , longDegreePerGridNew
    print "gridSizeOld", gridSizeOld
    print "gridSizeNew", gridSizeNew
    print "I_old[0,0], J_old[0,0]", I_old[0,0], J_old[0,0]
    testmat = np.zeros((1000,1000))
    for ii in range(I_old.shape[0]):
        for jj in range(I_old.shape[1]):
            testmat[I_old[ii,jj]*(I_old[ii,jj]>0), J_old[ii,jj]*(J_old[ii,jj]>0)] = 1
    from matplotlib import pyplot as plt
    plt.imshow(testmat)
    plt.show()
    # end debug                                                                
    arr_old = a.matrix
    arr_new = np.zeros((height, width))
    a_new.matrix = interpolate(arr_old, arr_new, I_old, J_old)
    return a_new

########################
# samples

a = pattern.a
c = pattern.c

