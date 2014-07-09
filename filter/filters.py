
import numpy as np
import numpy.ma as ma
from armor import pattern

def gaussianFilter(a, sigma=20, newCopy=False):
    """
    #adapted from armor.pattern
    returns a dbz object
    2014-03-07
    """
    from scipy import ndimage
    a1  = a.copy()
    a1.matrix   = ndimage.filters.gaussian_filter(a.matrix, sigma)
    a1.matrix   = ma.array(a1.matrix, fill_value=-999.)
    a1.matrix.mask = np.zeros(a1.matrix.shape)
    a1.name = a.name + "gaussian-sigma" + str(sigma)
    a1.imagePath    = a.imagePath[:-4]  + "gaussian-sigma" + str(sigma) +  a.imagePath[-4:]  #hack
    a1.outputPath   = a.outputPath[:-4] + "gaussian-sigma" + str(sigma) + a.outputPath[-4:]  #hack
    mx = a1.matrix.max()
    mn = a1.matrix.min()
    #a1.vmax = mx + (mx-mn)*0.2  # to avoid red top     # replaced by lines below 2014-02-20
    #a1.vmin = mn
    a1.matrix.mask = (a1.matrix< a.missingDataThreshold)
    a1.vmax = a.vmax
    a1.vmin = a.vmin
    if newCopy:
        return a1
    else:
        a.matrix = a1.matrix
        return a