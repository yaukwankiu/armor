# gabor filter for image processing
"""

reference: 
    Tropical Cyclone Identification and Tracking System
    Using Integrated Neural Oscillatory Elastic Graph
    Matching and Hybrid RBF Network Track Mining
    Techniques  (00846739.pdf)

    Raymond S. T. Lee, Member, IEEE, and James N. K. Liu, Member, IEEE
    IEEE TRANSACTIONS ON NEURAL NETWORKS, VOL. 11, NO. 3, MAY 2000

USE:

cd /media/Seagate\ Expansion\ Drive/ARMOR/python
python

from armor import pattern
a = pattern.a
from armor.filter import gabor
fvf = gabor.main(a,scales  = [1, 2, 4, 8, 16, 32, 64], NumberOfOrientations = 6,  memoryProblem=True)

"""
# imports

import numpy as np
from numpy.fft import fft2, ifft2
from scipy import signal
from matplotlib import pyplot as plt
import time
import os
import pickle
#from PIL import Image

# defining the parameters

def gaborFunction(x, y, sigma, phi, theta):
    """
    sigma = wavelet packet width
    phi = frequency
    theta = orientation
    """
    A = 1. / (sigma * (np.pi)**(.5))
    B = np.exp(-(x**2+y**2)/(2*sigma**2))
    C = np.exp(2*np.pi*complex(0,1)* phi * (x*np.cos(theta)+y*np.sin(theta)))
    return A*B*C
    
def gaborFilter(img, sigma, phi, theta):
    """
    reference: 
      http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html
    input:
        img - a numpy array
        sigma, phi, theta  - parameters for gaborFunction
    output:
        feature scalar field for the particular filter with given parameter
    """
    # define he window size to be 2 sigmas for convenience
    kernelX, kernelY    = np.meshgrid(range(2*sigma), range(2*sigma))
    gaborKernel         = gaborFunction(kernelX, kernelY, sigma, phi, theta)
    img2                = signal.convolve2d(img, gaborKernel, mode='same', 
                                           boundary='fill',fillvalue=-999)
    return img2                      

def main(a,sigma=20, scales  = [1, 2, 4, 8, 16], NumberOfOrientations = 4, memoryProblem=False):
    """test function
    import os
    
from armor import pattern
dbz = pattern.DBZ
a = pattern.a
from armor.filter import gabor
reload(gabor)
gabor.main(a)

    """
    from armor import pattern
    dbz = pattern.DBZ
    a.matrix.fill_value = -20.
    img = a.matrix.filled()
    import numpy as np
    from armor.filter import gabor
    #sigma   = 20
    #scales  = [1, 2, 4, 8, 16]
    #NumberOfOrientations = 12
    N = NumberOfOrientations
    orientations    = [v*np.pi/N for v in range(N)]
    filterdim       = len(scales)*N *2      # *2:  real+complex
    if not memoryProblem:
        filterVectorField = np.zeros((img.shape[0], img.shape[1], filterdim))  #not if array is too big
    print "\n............................................................\n"
    print "sigma, scales, NumberOfOrientations: ", sigma, scales, NumberOfOrientations
    print "filterdim: ", filterdim
    xxx = raw_input('press enter to continue:')
    ############
    # ready? -  let's go
    time0 =    int(time.time())
    outputFolder = 'armor/filter/gaborFeatures%d/' % time0
    os.makedirs(outputFolder)
    for i in range(len(scales)):
        phi = scales[i]
        for j in range(len(orientations)):
            theta = orientations[j]
            print 'scale(phi), orientation(theta): ', phi, theta
            img2 = gabor.gaborFilter(img, sigma, phi, theta)
            a_gabor = dbz(matrix=img2.real, vmin=-5, vmax=5)
            a_gabor.imagePath = outputFolder + str(i*NumberOfOrientations+j*2) +'.png'
            a_gabor.saveImage()
            a_gabor2 = dbz(matrix=img2.imag, vmin=-5, vmax=5)
            a_gabor2.imagePath = outputFolder + str(i*NumberOfOrientations+j*2+1) +'.png'
            a_gabor2.saveImage()
            if not memoryProblem:
                filterVectorField[:, :, i*NumberOfOrientations+j*2] = img2.real
                filterVectorField[:, :, i*NumberOfOrientations+j*2+1] = img2.imag
            else:
                outputPath1=outputFolder+str(i*NumberOfOrientations+j*2) +'.pydump'
                outputPath2=outputFolder+str(i*NumberOfOrientations+j*2+1) +'.pydump'
                pickle.dump(img2.real, open(outputPath1,'w'))
                pickle.dump(img2.imag, open(outputPath2,'w'))
    
    if not memoryProblem:
        d = {}
        d['content']  = filterVectorField
        d['README']   = 'test result for gabor filter: armor.filter.gabor.main()'+\
                        'acting on armor.pattern.a'
        d['parameters']=  'sigma: ' + str(sigma) + '\nscales: ' + str(scales) + \
                      '\nNumberOfOrientations: ' + str(NumberOfOrientations)
        pickle.dump(d, open(outputFolder+'filterVectorField%d.pydump' % time0, 'w'))
    import shutil
    shutil.copy('armor/filter/gabor.py', outputFolder)
    shutil.copy('/media/KINGSTON/ARMOR/python/roughwork.py', outputFolder)
    explanationText = "sigma = " + str(sigma) + "\nscales = " + str(scales)
    explanationText += "NumberOfOrientations=" +str(NumberOfOrientations)
    explanationText += "filterdim" + str(filterdim)
    open(outputFolder+'notes.txt').write(explanationText)
    if not memoryProblem:
        return filterVectorField
    else:
        return 0

#if __name__ == '__main__':     #doesnt work - commented out
#    main()


"""
g= gaborFunction
g(1,1,10,5,1)    
    
x, y = np.meshgrid(range(10), range(10))
G = g(x,y,5,4,2) 
plt.imshow(G.real)
plt.show()

cd /media/KINGSTON/ARMOR/python
python

from armor import pattern
dbz = pattern.DBZ
a = pattern.a
a.matrix.fill_value = -20.
img = a.matrix.filled()

import numpy as np
from armor.filter import gabor
sigma   = 10
phi     = 2
theta   = np.pi / 4
img2 = gabor.gaborFilter(img, sigma, phi, theta)

a_gabor = dbz(matrix=img2.real)
a_gabor.show4()


"""
