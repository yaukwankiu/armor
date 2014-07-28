import numpy as np


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



