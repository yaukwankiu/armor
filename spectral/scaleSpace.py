# -*- coding: utf-8 -*-

"""
== References ==  
1.
    Principles for Automatic scale selection - DiVA
    www.diva-portal.org/smash/get/diva2:450871/FULLTEXT01.pdf‎
    by T Lindeberg - ‎1999 - ‎Cited by 98 - ‎Related articles
    Principles for Automatic scale selection. Tony Lindeberg. Computational Vision and Active Perception Laboratory (CVAP). Department of Numerical Analysis ...

2.  Wikipedia:  scale space, scale-space segmentation, feature detection, object recognition

3.  Scholarpedia: http://www.scholarpedia.org/article/Scale_Invariant_Feature_Transform

4.  SciPy:  
        http://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.derivative.html
        http://docs.scipy.org/doc/scipy-0.8.x/reference/generated/scipy.ndimage.filters.gaussian_laplace.html
        http://docs.scipy.org/doc/scipy-0.8.x/reference/generated/scipy.ndimage.filters.gaussian_filter.html
----

"""


from scipy import ndimage
import numpy as np

def L(image, sigma, order=0):
    """
    purpose:
        to compute spatial gaussian derivatives
    Reference:
        http://docs.scipy.org/doc/scipy-0.8.x/reference/generated/scipy.ndimage.filters.gaussian_filter.html
    inputs:
        image   - array-like
        sigma   - scalar or sequence of scalars 
        order   - scalar or sequence of scalars,
                  order of derivative of gaussian, 
                  taking values 0, 1, 2 or 3
    """
    return ndimage.filters.gaussian_filter(image, sigma, order)
    
    
    
def L_normalised(image, sigma, order=0, gamma=1):
    """
    normalised derivatives
    c.f.   
        p. 12, (equation 1.25), Principles for Automatic scale selection - DiVA 
        www.diva-portal.org/smash/get/diva2:450871/FULLTEXT01.pdf‎
    """
    if isinstance(sigma, int):
        t       = 2 *sigma**2   # assumed dimension=2 if nothing else is provided
    else:
        t       = (np.array(sigma)**2).sum()        
    if isinstance (order, int):
        mn  = order * 2         # assumed dimension=2 if nothing else is provided
    else:
        mn  = np.array(order).sum()

    L_pre   = L(image, sigma, order)
    L_normalised    = t**(mn*gamma/2) * L_pre
    #print t, gamma, mn, L_normalised.max()  #debug
    return L_normalised
    




