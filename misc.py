#   misc.py
#   miscellaneous codes
try:
    from scipy import signal
    from scipy import interpolate
except:
    print "scipy not installed properly!!"

import numpy as np

#   functions for regions
def getFourCorners(reg):
    i, j, height, width = reg
    return [(i,j), (i+height, j), (i, j+width), (i+height, j+width)]

def getRectangularHull(L):
    """
    input:  a list of points [(i1,j1), (i2,j2),...] - where i=y, j=x
    output: four numbers:  (lower left corner i, j , height, width)
    """
    I   = [v[0] for v in L]
    J   = [v[1] for v in L]
    Imax    = max(I)
    Jmax    = max(J)
    Imin    = min(I)
    Jmin    = min(J)
    return np.array([Imin, Jmin, Imax-Imin, Jmax-Jmin])


#   mathematical functions for signal processing
def sigmoid(X, L=1):
    """sigmoid function, on a scalar or an array
    c.f. https://en.wikipedia.org/wiki/Sigmoid_function
    """
    return 1./ (1 + np.exp(-X/L))

def mexHat(x, a=1):
    A = 2/ (np.sqrt(3*a)*np.pi**1/3)
    return A * (1 - x**2/a**2) *np.exp(-x**2/a**2)

def morlet(N, **kwargs):
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.morlet.html#scipy.signal.morlet
    return signal.morlet(N, **kwargs)

    
def morletSpline(N=200, **kwargs):
    morlet_x    = range(N//2-N, N//2)
    morlet_y    = signal.morlet(N, **kwargs)
    #return interpolate.UnivariateSpline(morlet_x, morlet_y)
    return interpolate.interp1d(morlet_x, morlet_y, kind="quadratic")

def morlet2(s=1, w=5, width=11, **kwargs):
    #  http://en.wikipedia.org/wiki/Morlet_wavelet
    z = np.zeros((width, width))
    m = signal.morlet(M=width*2, s=s, w=w , **kwargs)
    for i in range(width):
        for j in range(width):
            r       = ( (i-w//2)**2 + (j-w//2)**2 )**.5
            z[i,j]  = m[r]
    return z

def morlet3(t, s=1):
    #http://en.wikipedia.org/wiki/Morlet_wavelet
    k   = np.exp(-0.5* s**2)
    c   = (1 + np.exp(-s**2) - 2*np.exp(-0.75*s**2)) **0.5
    psi = c * np.pi**(-0.25) * np.exp(-0.5*t**2) * (np.exp(1j*s*t) - k)
    return psi

def morlet2d(x, y, **kwargs):
    t   = (x**2 + y**2)**.5
    res = morlet(t, **kwargs)
    return res


##########
#   tests start
def morletFunction2d(x, y, scale=1, N=200, x0=0, y0=0, renormalisation=0.1,realPart=True, **spline_kwargs):
    """
    input:  x, y    - arrays
    output: z       - array
    """
    f   = morletSpline(N, **spline_kwargs)
    t   = ((x-x0)**2 + (y-y0)**2) **.5 / scale 
    #print t                 #debug
    z   = f(t) / (abs(t) + renormalisation)     # scaling by the radius to make it sum to zero
                                        #   +0.5 - designularisation; we take 0.5 to be the grid radius
                                        #   renormalisation =0.slightly - 1 better performance (summing to a smaller value)
    if realPart:
        z = z.real
    if z.shape == ():
        z +=0   #hack
    return z

def morletFilter2d(scale=1, renormalisation=0.1, N=200):
    """
    input: scale
    uses:  morletFunction3
    ouput: 2d array (the mask for the filter)
    """
    width = int(scale * (N/2)) 
    height= int(scale * (N/2))
    X, Y = np.meshgrid(range(-height//2, height//2), range(-width//2, width//2))
    Z    = morletFunction2d(X, Y, renormalisation=renormalisation, N=N)
    return Z

#   tests end
##########




def morlet2dFilter(dbzpattern, scale=1, N=200, renormalisation=0.1, realPart=True, **spline_kwargs):
    """
    steps:
    #   1. construct the function and filter
    #   2. perform filtering

    input:
        N       - parameter for morletSpline
        scale   - parameter for morlet function
                
    """
    #   1. construct the function and filter
    f   = morletSpline(N, **spline_kwargs)
    def morletFunction2d(x, y, x0=0, y0=0):
        """
        input:  x, y    - arrays
        output: z       - array
        """
        #t   = ((x-x0)**2 + (y-y0)**2) **.5 / scale  * (N//4)
        t   = ((x-x0)**2 + (y-y0)**2) **.5 / scale
        z   = f(t) / (abs(t)+renormalisation)       # scaling by the radius to make it sum to zero
                                        #   +0.5 - designularisation; we take 0.5 to be the grid radius
        if realPart:
            z = z.real
        if z.shape == ():
            z +=0   #hack
        return z

    def morletFilter2d(scale):
        """
        input: scale
        uses:  morletFunction3
        ouput: 2d array (the mask for the filter)
        """
        width = int(scale * (N/2)) 
        height= int(scale * (N/2))
        X, Y = np.meshgrid(range(-height//2, height//2), range(-width//2, width//2))
        Z    = morletFunction2d(X, Y)
        return Z
        
    #   2. perform filtering
    mask = morletFilter2d(scale=scale)
    arr  = dbzpattern.matrix
    arr2 = signal.convolve2d(arr, morletFilter2d(scale), mode='same', 
                                           boundary='fill')
                                           
    dbzpattern.backupMatrix()
    dbzpattern.matrix = arr2
    dbzpattern2 = dbzpattern.copy()
    dbzpattern2.name += "morletFilter_scale" + str(scale)
    dbzpattern2.vmin = arr2.min()
    dbzpattern2.vmax = arr2.max()
    return dbzpattern2

def embed881921(a):
    a.backupMatrix()
    height, width = a.matrix.shape
    z = np.ma.zeros((881,921), fill_value=-999.)
    z.mask = False
    z[0:height, 0:width] = a.matrix
    a.matrix = z
    return a






