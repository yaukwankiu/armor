# /media/KINGSTON/ARMOR/python/armor/geometry/transformedCorrelations.py
#   2013-10-03
#   migrated from /media/KINGSTON/ARMOR/python/armor/tests/transformedCorrelationTest.py
    # transformed correlation test
    # as described in Ch.4.4 of the ARMOR report 2013-07-10
    # as proposed by Professor Lee in the previous meeting at CWB
    # 2013-07-05

"""
USE
cd /media/KINGSTON/ARMOR/python
python

import numpy as np
from armor.tests import transformedCorrelationTest as test
from armor import pattern
a = pattern.a
arr= np.flipud(a.matrix)

reload(test); test.test2()

reload(test); test.showArrayWithAxes(arr, cmap='gray')


reload(test)
x, y = np.meshgrid(range(100), range(200))
arr = test.doubleGaussian(y,x, 50,50,20,30,theta=1)
plt.imshow(arr)
plt.show()

#reload(test); x = test.main() ; print "x['correlation']=", x['correlation']

#####################################
###
##
#
reload(test); x = test.main() ; print x['text']
#
##
###
#####################################
PLAN
1.  Define the objects (two double gaussian distributions)
2.  Compute the centroids
3.  Compute the moment of inertia matrix
4.  Compute the major and minor axes
5.  Transform
6.  Interpolate
7.  Compute correlation
"""
################################################################################
# imports
import numpy as np
from scipy.signal import convolve
from matplotlib import pyplot as plt
cos = np.cos
sin = np.sin
exp = np.exp

from armor import pattern
a = pattern.a
b = pattern.b
dbz = pattern.DBZ
################################################################################
# defining the functions

def doubleGaussian(I, J, centroid_i, centroid_j, sigma_i, sigma_j, theta=0):

    I1  = I-centroid_i
    J1  = J-centroid_j
    I2  = cos(theta)*I1 - sin(theta)*J1
    J2  = sin(theta)*I1 + cos(theta)*J1
    I2 += centroid_i
    J2 += centroid_j

    return np.exp( - (I2-centroid_i)**2 / (2*sigma_i**2) \
                   - (J2-centroid_j)**2 / (2*sigma_j**2) )

def sample1():
    x, y = np.meshgrid(range(500), range(500))
    arr = doubleGaussian(y,x, 300, 300, 40, 50, theta=2)
    return arr

def sample2():
    x, y = np.meshgrid(range(500), range(500))
    arr = doubleGaussian(y,x, 200, 200, 20, 70, theta=1)
    return arr

def sample3():
    x, y = np.meshgrid(range(500), range(500))
    arr = doubleGaussian(y,x, 200, 200, 50, 50, theta=1)
    return arr


def weight(height=881, width=921):
    """
    weight function, indicating significance/reliability of the data point at (x,y)
    """
    return np.ones((height,width))   # placeholder

def getCentroid(arr):
    """
    input:      an array
    output:     centroid of the array
    """
    height, width = arr.shape
    a           = arr * weight(height,width)
    height, width = a.shape
    X, Y = np.meshgrid(range(width), range(height))
    I, J    = Y,X                               # numpy order:  (i,j) = (x,y)
    a_mean      = a.mean()
    i_centroid  = (I*a).mean() / a_mean     #
    j_centroid  = (J*a).mean() / a_mean     # 
    return (i_centroid, j_centroid)

def getMomentMatrix(arr, display=False):
    height, width = arr.shape
    a           = arr * weight(height, width)
    height, width   = a.shape
    X, Y            = np.meshgrid(range(width), range(height))
    I, J            = Y,X                       # numpy order:  (i,j) = (x,y)
    a_mean        = a.mean()
    i0, j0 = getCentroid(a)
    I   -= i0                               # resetting the centre
    J   -= j0
    cov_ii  = (I**2 * a).mean() / a_mean
    cov_jj  = (J**2 * a).mean() / a_mean
    cov_ij  = (I*J  * a).mean() / a_mean
    M =     np.array([[cov_ii, cov_ij],
                     [cov_ij, cov_jj]])
    if display:
        print M
    return M

def getAxes(M, display=False):
    #print 'getAxes'
    """ 
    input:  moment matrix M
    output: eigenvalues, eigenvectors
    """
    eigenvalues, eigenvectors =  np.linalg.eig(M)
    if eigenvalues[1]>eigenvalues[0]:
        eigenvectors = np.fliplr(eigenvectors)  #flip
        eigenvalues[1], eigenvalues[0] = eigenvalues[0], eigenvalues[1]
    if display:
        print "eigenvalues, eigenvectors = ", eigenvalues, eigenvectors
    return eigenvalues, eigenvectors


def drawArrow(x=.5, y=.7, dx=.2, dy=-0.3, fc="k", ec="k"):
    """wrapping the matplotlib.pyplot.arrow function
    """
    # plt.arrow( x, y, dx, dy, **kwargs )
    head_width = (dx**2 +dy**2)**.5 *0.05
    head_length = (dx**2 +dy**2)**.5 *0.1
    plt.arrow(x, y, dx, dy, fc=fc, ec=ec, head_width=head_width, head_length=head_length)

def showArrayWithAxes(arr, cmap='jet'):
    """ Intermediate step.  showing the array with the axes
    """
    ########
    # set up
    height, width = arr.shape
    ########
    # computation
    i0, j0  = getCentroid(arr)
    M       = getMomentMatrix(arr)
    eigenvalues, eigenvectors   = getAxes(M)
    
    v0 = eigenvectors[:,0]
    v1 = eigenvectors[:,1]
    v0_size = eigenvalues[0]**.5
    v1_size = eigenvalues[1]**.5
    
    ########
    # display
    #plt.xlim(0, width)     # or other attributes of arr if desired?!
    #plt.ylim(0, height)
    plt.imshow(arr, cmap=cmap)
    drawArrow(x=j0, y=i0, dx=v0[1]*v0_size, dy=v0[0]*v0_size)
    drawArrow(x=j0, y=i0, dx=v1[1]*v1_size, dy=v1[0]*v1_size, fc="r", ec="r")
    plt.show()
    
def transform(arr, centroid_i, centroid_j, 
              theta=-9999, scale_0=-9999, scale_1=-9999,
              eigenvectors=-9999, eigenvalues=-9999):
    """
    5.  Transform and normalise: 
    translate to centre of array, rotate axes to x,y, scale x, scale y
        
    """
    #print 'transform'
    if theta ==-9999:
        v0 = eigenvectors[:,0]
        v1 = eigenvectors[:,1]
        theta = np.arctan(1.*v0[1]/v0[0])       # rotate the long axis to x
                                           # two choices differing by pi - will try both later
                                           #                        in the comparison function
        print 'theta=', theta
    if scale_0==-9999:
        scale_0=eigenvalues[0]**.5 *  0.04
        scale_1=eigenvalues[1]**.5 *  0.04
    height, width = arr.shape
    centre_i, centre_j  = height//2, width//2
    X, Y = np.meshgrid(range(width), range(height))
    I, J = Y, X         # python array convention:  vertical first
                        # tracking backwards
    I   -= centre_i     # 1. moving from the centre of the board back to zero
    J   -= centre_j
    I   *= scale_0                           # 2. scale (2, 3 can't be interchanged)
    J   *= scale_1  
    I    = cos(theta) * I - sin(theta) * J   # 3. rotate to the right angle
    J    = sin(theta) * I + cos(theta) * J
    I   += centroid_i                        # 4. moving to the centroid specified, finding
    J   += centroid_j                        # the point where it came from

    return I, J

def interpolate(arr, I, J):
    print 'interpolate'
    """
    6.  Interpolate     - with nearest neighbour for simplicity
    I, J - from function transform()
    """
    height, width = arr.shape
    arr2 = np.zeros((height,width))
    I  = I.round()
    J  = J.round()
    I *= (I>=0) * (I<height)       # cut out the out of bound points
    J *= (J>=0) * (J<width)
    for i in range(height):
        for j in range(width):
            arr2[i,j] = arr[I[i,j],J[i,j]]
    return arr2

def getCorrelation(arr1, arr2):
    """
    7.  Compute correlation
    """
    #print 'getCorrelation'
    return np.corrcoef(arr1.reshape(arr1.size), arr2.reshape(arr2.size))[0,1]

def correlationTest(arr1, arr2, display=False):
    print "correlation test"
    if display:
        print 'arr1'
        showArrayWithAxes(arr=arr1)
        print 'arr2'
        showArrayWithAxes(arr=arr2)
    i_arr1, j_arr1 = getCentroid(arr1)
    i_arr2, j_arr2 = getCentroid(arr2)
    M1 = getMomentMatrix(arr1, display=display)
    M2 = getMomentMatrix(arr2, display=display)
    eigenvalues1, eigenvectors1 = getAxes(M1, display=display)
    eigenvalues2, eigenvectors2 = getAxes(M2, display=display)
    arr1_coords = transform(arr1, i_arr1, j_arr1, eigenvectors=eigenvectors1,
                            eigenvalues=eigenvalues1)
    arr2_coords = transform(arr2, i_arr2, j_arr2, eigenvectors=eigenvectors2,
                            eigenvalues=eigenvalues2)

    arr1_transformed = interpolate(arr1, arr1_coords[0], arr1_coords[1])
    arr2_transformed = interpolate(arr2, arr2_coords[0], arr2_coords[1])
    correlation = getCorrelation(arr1_transformed, arr2_transformed)
    if display:
        print 'arr1_transformed'
        showArrayWithAxes(arr1_transformed)
        print 'arr2_transformed'
        showArrayWithAxes(arr2_transformed)
        print 'correlation', correlation
        print 'arr1.sum()', arr1.sum()
        print 'arr2.sum()', arr2.sum()
        print 'arr1_transformed.sum()', arr1_transformed.sum()
        print 'arr2_transformed.sum()', arr2_transformed.sum()

    return_value= {'correlation':correlation, 'arr1_transformed': arr1_transformed, 
            'arr2_transformed': arr2_transformed, }
    return return_value
    
def test1():
    x={}
    #arr1 = a.matrix
    #arr2 = b.matrix
    #x[(a.name,b.name)] = correlationTest(arr1.filled(), arr2.filled())['correlation']
    for aname,bname in [('0200','0210'), ('0210','0220'),('0220','0230'), ('0230','0240'),
                  ('0200','0220'),('0200','0230'), ('0200','0240'),]:
        a = dbz(dataTime = '20120612.'+aname)
        b = dbz(dataTime = '20120612.'+bname)
        a.load()
        b.load()
        a.matrix.fill_value=0
        b.matrix.fill_value=0
        arr1 = a.matrix.filled()
        arr2 = b.matrix.filled()
        #showArrayWithAxes(arr=arr1)
        #showArrayWithAxes(arr=arr2)
        x1 = correlationTest(arr1, arr2)['correlation']
        x2 = correlationTest(arr1, np.flipud(np.fliplr(arr2)))['correlation']  # maynot work actually ?!!?!?!! may get the same eigenvectors!!!!
        x[(a.name,b.name)] = max(x1,x2)
        print a.name, b.name, x[(a.name,b.name)]
    text1 = "Pattern1		    Pattern2			Correlation after Transformation"
    text2 = '\n'.join(sorted(['\t'.join([v[0],v[1],str(x[v])]) for v in x.keys()]))
    text3 = text1 + '\n' + text2
    print text3
    return {'dict': x, 'text': text3}
    
def test2():
    arr1 = sample1()
    arr2 = sample2()
    #print '\n......................\narr1'
    #showArrayWithAxes(arr=arr1)
    #print '\n......................\narr2'
    #showArrayWithAxes(arr=arr2)
    x = correlationTest(arr1, arr2, display=True)
    print 'correlation between arr1 and arr2:', x['correlation']
    return {'correlation':x['correlation'],
            'x' : x,
            'arr1': 'doubleGaussian(y,x, 100, 100, 40, 50, theta=2)',
            'arr2': 'doubleGaussian(y,x, 200, 200, 20, 70, theta=1)',
            }

def test3(display=True):
    arr1 = sample1()
    arr2 = sample3()
    x = correlationTest(arr1, arr2, display=display)
    return x
###################

def main():
    print "=========test 1=================================="
    test1_result = test1()
    print "=========test 2=================================="
    test2_result = test2()
    print "=========test 3=================================="
    test3_result = test3()
    return{ 'test1_result': test1_result,
            'test2_result': test2_result,
            'test3_result': test3_result,
          }
