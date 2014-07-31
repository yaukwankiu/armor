import time
import numpy as np
from .. import defaultParameters as dp

def hausdorffDim(a, epsilon=2):
    """
    #codes from
    #   hausdorffDimensionTest.py
    #       http://en.wikipedia.org/wiki/Hausdorff_dimension
    #       http://en.wikipedia.org/wiki/Minkowski-Bouligand_dimension
    """
    dims = []
    arr1 = (a.matrix>0)     # turn it to 0-1 if it's not that form already
    height, width = arr1.shape
    arr2 = arr1[::epsilon, ::epsilon].copy()
    for i in range(0, epsilon):
        for j in range(0, epsilon):
             h, w = arr1[i::epsilon, j::epsilon].shape
             arr2[0:h, 0:w] += arr1[i::epsilon, j::epsilon]
    dimH = np.log(arr2.sum()) / np.log((height*width)**.5/epsilon)
    return dimH

def hausdorffDimLocal(a, epsilon=1, I=50, J=50, display=True, imagePath=""):
    height, width = a.matrix.shape
    dimLocal = {}
    a1 = a.hausdorffDim(epsilon)['a1']
    for i in range(height//I):
        for j in range(width//J):
            aa1 = a1.getWindow(i*I, j*J, I, J)
            # one epsilon for now, may extend to a list later 2014-07-29
            dimH = hausdorffDim(aa1, epsilon)
            aa1.name = str(dimH)
            #aa1.show()
            #time.sleep(1)
            dimLocal[(i,j)] = dimH
            #print dimH #debug
    a2 = a.copy()
    a2.matrix= a2.matrix.astype(float)
    #a2.show() # debug
    #time.sleep(5)
    a2.name = "Local Hausdorff Dimensions for\n" + a.name
    a2.imagePath = 'testing/' + str(time.time()) + '_local_hausdorff_dim_' + a.name[-19:] + '.png'
    for i in range(height//I):
        for j in range(width//J):
            a2.matrix[i*I:(i+1)*I, j*J:(j+1)*J] = dimLocal[(i,j)]
    a2.vmax=2
    a2.vmin=0
    a2.cmap='jet'
    if imagePath !="":
        a2.saveImage()
    if display:
        a2.show()
    return {'a2': a2, 'dimLocal': dimLocal}
