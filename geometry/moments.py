# functions to compute the moments of patterns

import numpy as np
from numpy import ma

def measure(phi, lower=0., upper=120.):
    """
    input:  phi = a (masked) array.  think of phi = a.matrix
    output: weight = the weight of the pattern in the region, unmasked, and 
                     between the inside the numerical range [lower,upper]

    will write a.measure() specifically for a = armor.pattern.DBZ objects
    """
    phi = phi.view(ma.MaskedArray)        
    meas = (phi* (phi>=lower) * (phi<=upper)).sum()
    return meas

def mean(phi, lower=0., upper=120.):
    """wrapping the numpy.ma.average function for weighed average of masked arrays
    here weight = the image intensity,
    and the coordinates  X, Y = np.meshgrid(range(921), range(881))
        are to be averaged out.
    """
    phi1 = phi.view(ma.MaskedArray).copy()    # to be safe (slow?)
    try:
        phi1.mask += (phi1<lower) + (phi1>upper)  # masking the out-of-range regions
    except:
        phi1.mask  = (phi1<lower) + (phi1>upper)
    height, width = phi1.shape
    X, Y = np.meshgrid(range(width), range(height))
    I, J = Y, X             # always work with I, J internally
    Ibar = ma.average(I, weights=phi1)
    Jbar = ma.average(J, weights=phi1)
    return {'i':Ibar, 'j':Jbar}

def firstMoment(phi, lower=0., upper=120.):
    """wrapping the numpy.ma.average function for weighed average of masked arrays
    here weight = the image intensity,
    and the coordinates  X, Y = np.meshgrid(range(921), range(881))
        are to be averaged out.
        
    use:
    from armor import pattern
    a = pattern.a
    from armor.geometry import moments
    print moments.firstMoment(a.matrix)

    """
    phi1 = phi.view(ma.MaskedArray).copy()    # to be safe (slow?)
    phi1.mask += (phi1<lower) + (phi1>upper)  # masking the out-of-range regions
    height, width = phi1.shape
    X, Y = np.meshgrid(range(width), range(height))
    I, J = Y, X             # always work with I, J internally
    M11 = ma.average(I*J, weights=phi1)
    return M11

def moment(phi, p, q, Iorigin=0, Jorigin=0, lower=0., upper=120.):
    """
    to compute the nth raw moment of phi
    centre at origin
    will define a method in armor.pattern.DBZ calling this function
            in which (Iorigin, Jorigin) = coordinateOrigin
    a=pattern.a
    a.moment(p,q)
    """
    phi1 = phi.view(ma.MaskedArray)
    phi1.mask += (phi1<lower) + (phi1>upper)  # masking the out-of-range regions
    height, width = phi1.shape
    X, Y = np.meshgrid(range(width), range(height))
    I, J = Y, X             # always work with I, J internally
    I   -= Iorigin
    J   -= Jorigin
    Mpq = ma.average(I**p * J**q, weights=phi1)
    return Mpq

def Mpq(*args, **kwargs):
    """
    alias for moment
    """
    return moment(*args, **kwargs)

def centralMoment(phi, p, q, lower=0., upper=120.):
    """calling moment and first moment
    """
    x = mean(phi=phi, lower=lower, upper=upper)
    Ibar    = x['i']
    Jbar    = x['j']
    mu_pq   = moment(phi=phi, p=p, q=q, Iorigin=Ibar, Jorigin=Jbar, \
                     lower=lower, upper=upper)
    return mu_pq
        
def mu(*args, **kwargs):
    """alias for centralMoment()
    """
    return centralMoment(*args, **kwargs)

def scaleInvariantMoments(phi, p, q, lower=0., upper=120.):
    """
    see Hu's original article
    or wikipedia http://en.wikipedia.org/wiki/Image_moment#Scale_invariant_moments
    2013-09-28
    """
    mu_00   = mu(phi, 0, 0)
    mu_pq   = mu(phi, p, q)
    eta_pq  = mu_pq / (mu_00)**(1 + 0.5 * (p+q))
    return eta_pq


def eta(*args, **kwargs):
    """
    alias
    """
    return scaleInvariantMoments(*args, **kwargs)

    
def HuMoments(phi, **kwargs):
    """
    HU's invariant moments, c.f.: Guido Gerig,
        Lecture on Shape Analysis and Moment Invariants, 2010
    input:  a shape, a masked array
    output: a vector (list) of seven moments
    """
    eta02 = eta(phi, p=0, q=2, **kwargs)
    eta03 = eta(phi, p=0, q=3, **kwargs)
    eta11 = eta(phi, p=1, q=1, **kwargs)
    eta12 = eta(phi, p=1, q=2, **kwargs)
    eta20 = eta(phi, p=2, q=0, **kwargs)
    eta21 = eta(phi, p=2, q=1, **kwargs)
    eta30 = eta(phi, p=3, q=0, **kwargs)

    Hu=[0.,0.,0.,0.,0.,0.,0.]  # seven invariants, the last of which is skew
    Hu[0] =  eta20  +eta02
    Hu[1] = (eta20  -eta02)**2    +   4 * eta11**2
    Hu[2] = (eta30-3*eta12)**2    +  (3  *eta21 - eta03)**2
    Hu[3] = (eta30+  eta12)**2    +  (    eta21 + eta03)**2
    Hu[4] = (eta30-3*eta12) * (eta30 + eta12) * (   (eta30+eta12)**2 - 3*(eta21+eta03)**2) +\
          (3*eta21-  eta03) * (eta21 + eta03) * ( 3*(eta30+eta12)**2 -   (eta21+eta03)**2)
    Hu[5] = (eta20 - eta02) *((eta30 + eta12)**2  - (eta21+eta03)**2) +\
                  4*eta11  * (eta30 + eta12) *     (eta21+eta03)
    Hu[6]=(3*eta21-  eta03) * (eta30 + eta12) * (   (eta30+eta12)**2 - 3*(eta21+eta03)**2) -\
          (  eta30-3*eta12) * (eta21 + eta03) * ( 3*(eta30+eta12)**2 -   (eta21+eta03)**2)

    return Hu




def skewness(phi, lower="", upper="", axis=1, *args, **kwargs):  #2014-11-11
    """http://en.wikipedia.org/wiki/Skewness#Definition
    return: skewness in the j axis
    """
    if lower=="":
        lower = phi.min()
    if upper=="":
        upwer = phi.max()
    if axis == 1:
        M03 = mu(phi=phi, p=0, q=3, lower=lower, upper=upper, *args, **kwargs)
        M02 = mu(phi=phi, p=0, q=2, lower=lower, upper=upper, *args, **kwargs)
    elif axis == 0:
        M03 = mu(phi=phi, p=3, q=0, lower=lower, upper=upper, *args, **kwargs)
        M02 = mu(phi=phi, p=2, q=0, lower=lower, upper=upper, *args, **kwargs)
    gamma = 1.* M03 / M02**1.5
    return gamma
    
def skewness2(phi, lower="", upper="", *args, **kwargs): #2014-11-11
    """http://en.wikipedia.org/wiki/Skewness#Definition
    return:  skewnesses in the (i,j) axes
    """
    gamma0 = skewness(phi, lower, upper, axis=0, *args, **kwargs)
    gamma1 = skewness(phi, lower, upper, axis=1, *args, **kwargs)
    return gamma0, gamma1

def kurtosis(phi, lower="", upper="", axis=1, *args, **kwargs):  #2014-11-11
    """http://en.wikipedia.org/wiki/Kurtosis#Pearson_moments
    return: excess kurtosis in the j axis
    """
    if lower=="":
        lower = phi.min()
    if upper=="":
        upwer = phi.max()
    if axis == 1:
        M04 = mu(phi=phi, p=0, q=4, lower=lower, upper=upper, *args, **kwargs)
        M02 = mu(phi=phi, p=0, q=2, lower=lower, upper=upper, *args, **kwargs)
    elif axis == 0:
        M04 = mu(phi=phi, p=4, q=0, lower=lower, upper=upper, *args, **kwargs)
        M02 = mu(phi=phi, p=2, q=0, lower=lower, upper=upper, *args, **kwargs)
    gamma = 1.* M04 / M02**2 -3
    return gamma
    
def kurtosis2(phi, lower="", upper="", *args, **kwargs): #2014-11-11
    """http://en.wikipedia.org/wiki/Skewness#Definition
    return:  skewnesses in the (i,j) axes
    """
    gamma0 = kurtosis(phi, lower, upper, axis=0, *args, **kwargs)
    gamma1 = kurtosis(phi, lower, upper, axis=1, *args, **kwargs)
    return gamma0, gamma1




