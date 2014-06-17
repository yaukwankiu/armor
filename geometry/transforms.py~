#   armor.geometry.transforms
#   functions:  translation(arr, (a,b))
#               linear(arr, matrix 2x2)
#               affine(arr, matrix 2x3)
#   in this module we compute the linear/affine transformations of arrays
#   it is done in two steps
#       1.  the corresponding coordinates are calculated
#       2.  interpolation

##################################################
# imports
import numpy as np
ma  = np.ma
cos = np.cos
sin = np.sin
import matplotlib.pyplot as plt
import scipy.interpolate
RBS = scipy.interpolate.RectBivariateSpline
from armor import pattern
dbz=pattern.DBZ

###################################################
#   setups
#defaultOrigin   = pattern.a.coordinateOrigin
#defaultOrigin   = (492, 455)

defaultOrigin   = (0,0)

def IJ(arr1):
    if isinstance(arr1, pattern.DBZ):
        ARR1 = arr1
        arr1 = ARR1.matrix
    height, width = arr1.shape
    X, Y = np.meshgrid(range(width), range(height))
    I, J = 1.*Y, 1.*X
    return I, J

def translation(I, J, T=(0,0)):
    """
    translate arr0 onto arr1
    height width = that of arr1
    return: array of pointers to points on arr0 (need not be integers)
    vector: (i,j) = (y,x)
    """
    height, width = I.shape
    try:
        if T.shape == (2,1):
            T = (T[0,0], T[1,0])
    except AttributeError:
        pass
        
    I   -= T[0]
    J   -= T[1]
    return I, J

def rotation(rad=0):
    return np.matrix(   [[cos(rad), -sin(rad)],
                         [sin(rad),  cos(rad)]])
def rotationMatrix(*args, **kwargs):
    """alias
    """
    return rotation(*args, **kwargs)
    
    
def linear(I, J, T=np.matrix([[1,0],[0,1]]), origin=defaultOrigin ):
    """
    translate arr0 onto arr1
    height width = that of arr1
    return: arr1 = array of pointers to points on arr0 (need not be integers)
    convention for T: (i,j) = (y,x)
    we assume that T is nonsingular
    coordinate origin added, default = (0, 0) as set in the setup section above
    """
    height, width = I.shape
    I, J    = translation(I, J, origin)

    T       = np.matrix(T)
    T_inv   = np.linalg.pinv(T)
    for i in range(height):
        for j in range(width):
            v = T_inv * [ [I[i,j]],
                          [J[i,j]] ]
            I[i,j], J[i,j] = v[0,0], v[1,0]

    I, J    = translation(I, J, (-origin[0], -origin[1])) 
    return I, J
    
def affine(I, J, T=np.array([[1,0,0], [0,1,0]]), origin=defaultOrigin ):
    """
    translation + linear forward
    inverse linear + translation backward
    """
    if T.shape == (2,2):
       T = ma.hstack([T, [[0],[0]]])
    I, J = linear(I, J, T=T[:,0:2], origin=origin)
    I, J = translation(I, J, T=T[:,2])
    return I, J


    
def interpolation(arr0, I, J, useRBS=True):
    """
    
    """
    try:
        height0, width0   = arr0.shape
    except:
        arr0 = arr0.matrix
        height0, width0   = arr0.shape
    
    if isinstance(arr0, ma.MaskedArray):
        mask = arr0.mask.copy()
        mask1 = np.roll(mask, 1)
        mask += mask1 + np.roll(mask,1, axis=0) + np.roll(mask1, 1, axis=0)
    else:
        mask = np.zeros((height0, width0))
    #    arr0.mask = 0
    #    arr0 = arr0 - mask*999999
        
    height, width = I.shape
    arr1 = ma.ones((height, width))* (-99999)
    I   += (-999999) * ( (I<0) + (I>=height0-1) + (J<0) + (J>=width0-1) )   #unwanted portions
    if useRBS:
        arr0_spline  = RBS(range(height0), range(width0), arr0)
        for i in range(height):
            for j in range(width):
                if I[i,j] >=0 and not mask[i, j]:
                    arr1[i,j]   = arr0_spline(I[i,j],J[i,j])
                else:
                    continue
    else:
        #   the original loop, replaced by the new one above 2013-10-03
        for i in range(height):
            for j in range(width):
                if I[i,j]>=0:
                    arr1[i,j] = arr0[I[i,j],J[i,j]]
                else:
                    continue
    return arr1



def test(a="", transformationMatrix = np.array([[1, 0, 100],[0, 1, 100]]), showImage=True, saveImage=False):
    from armor import pattern
    if a =="":
        print 'loading armor.pattern...'
        a = pattern.a
        #b = pattern.b
        print 'loading a'
        a.load()
        #b.load()
    print 'computing the coordinates'
    I, J = IJ(a.matrix)
    #I, J = affine(I, J, np.array([[0.7, -0.7, 100],[0.7, 0.7, 100]]))
    I, J = affine(I, J, transformationMatrix, origin=a.coordinateOrigin)
    print I, J
    print 'interpolating'
    c = interpolation(a.matrix, I, J,  useRBS=False)
    c = pattern.DBZ(matrix=c, name=a.name + '_transformed_by_' + str(transformationMatrix.tolist()))
    if showImage:
        c.show4()
    if saveImage:
        print "saving to:", c.imagePath
        c.saveImage()
    return c
    
#########################################################################################
#   codes from transformedCorrelations.py
#   2013-10-08

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
    return np.array([i_centroid, j_centroid])

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
    #if eigenvalues[1]>eigenvalues[0]:
    if eigenvalues[1] < eigenvalues[0]:         # 2013-10-15
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

def showArrayWithAxes(arr, cmap='jet', verbose=True, imagePath="", imageTopDown=""):
    """ Intermediate step.  showing the array with the axes
    """
    ########
    # set up
    height, width = arr.shape
    if imageTopDown =="":
        imageTopDown = pattern.defaultImageTopDown  # default to false
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
    #   if not imageTopDown:FLIP Y-AXIS after all plotting
    if not imageTopDown:
        ax=plt.gca()
        ax.set_ylim(ax.get_ylim()[::-1])
    if imagePath != "":
        print 'saving image to', imagePath
        plt.savefig(imagePath, dpi=200)
    if verbose:
        plt.show()
    return {'eigenvalues'   : eigenvalues,
            'eigenvectors'  : eigenvectors,
            'momentMatrix'  : M,
            'centroid'      : (i0,j0),
            }

def transform(arr, centroid_i, centroid_j, 
              theta=-9999, scale_0=-9999, scale_1=-9999,
              eigenvectors=-9999, eigenvalues=-9999):
    """
            5.  Transform and normalise: 
            translate to centre of array, rotate axes to x,y, scale x, scale y
                first step:     compute the coordinates in reverse
                second step:    carry out the interpolation

    the former transform() function, 

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
    I   -= centroid_i     # 1. moving from the centre of the board back to zero
    J   -= centroid_j

    I   *= scale_0                           # 2. scale (2, 3 can't be interchanged)
    J   *= scale_1  

    I    = cos(theta) * I - sin(theta) * J   # 3. rotate to the appropriate angle
    J    = sin(theta) * I + cos(theta) * J

    I   += centroid_i                        # 4. moving to the centroid specified, finding
    J   += centroid_j                        # the point where it came from

    return I, J

#
#   end codes from transformedCorrelations.py
################################################################################

def momentNormalise(a1 = pattern.a, verbose=True, imagePath=""):
    """
    PURPOSE
        to set the image upright according to its moments
    USE

        cd /media/KINGSTON/ARMOR/python/
        python

        from armor import pattern
        from armor.geometry import transforms as tr
        import numpy as np
        dbz=pattern.DBZ

        #a = pattern.a
        #b = pattern.b

        a = dbz('20120612.0230')
        b = dbz('20120612.0900')
        a.load()
        a.setThreshold(0)
        b.load()
        b.setThreshold(0)


        a.show()
        b.show()
        x = tr.momentNormalise(a1=a)
        a2 = x['a2']
        centroid_a = x['centroid']
        eigenvalues_a = x['eigenvalues']

        y = tr.momentNormalise(a1=b)
        b2 = y['a2']
        centroid_b = y['centroid']
        eigenvalues_b = y['eigenvalues']

        a2.matrix = a2.drawCross(*centroid_a, radius=50).matrix
        a2.show()
        b2.matrix = b2.drawCross(*centroid_b, radius=50).matrix
        b2.show()
        a2.backupMatrix()
        b2.backupMatrix()

        I, J = tr.IJ(a2.matrix)
        I, J = tr.translation( I, J, (centroid_b - centroid_a))
        a2.matrix = tr.interpolation(a2.matrix, I, J)
        a2.setThreshold(0)

        a2.show()
        b2.show()

        #   adding in axial scalings

        print 'eigenvalues_a:', eigenvalues_a
        print 'eigenvalues_b:', eigenvalues_b

        a2.restoreMatrix()
        b2.restoreMatrix()

        displacement    = np.matrix(centroid_b - centroid_a)
        linearTr        = np.diag( (eigenvalues_b / eigenvalues_a) **.5 )
        affineTr        = np.hstack( [linearTr, displacement.T] )
        I, J = tr.IJ(a2.matrix)
        I, J = tr.affine(I, J, T=affineTr, origin=centroid_b)
        a2.matrix   = tr.interpolation(a2.matrix, I, J)
        a2.setThreshold(0)

        a2.show()
        b2.show()




    #######################    
    
    test:  normalising the given pattern with moments
        1.  load the pic, compute and draw the axes
            a.  compute the centroid and eigenvalues
            b.  get the IJs
            c.  interpolate
        2.  normalise (i.e. rotate the axes to x/y)
        3.  draw the new pic

    """
    arr1 = a1.matrix
    showArrayWithAxes(arr1, verbose=verbose, imagePath=imagePath, imageTopDown=a1.imageTopDown)
    i0, j0  = getCentroid(arr1)
    M       = getMomentMatrix(arr1)
    eigenvalues, eigenvectors = getAxes(M)

    # | from transformedCorrelations.transform():   |
    # v                                             v
    v0      = eigenvectors[:,0]
    v1      = eigenvectors[:,1]
    theta   = np.arctan(1.*v0[1]/v0[0]) #- np.pi /2
    if verbose:
        print 'theta =', theta          # theta = angle of the short arm with the i-(y-)axis
    T       = rotation(-theta)          # rotate by negative of theta
    translation     = [[0],[0]]
    T       = np.hstack([T, translation])
    rotationOrigin  = i0, j0
    I, J = IJ(arr1)
    I, J = affine(I, J, T=T, origin=rotationOrigin)
    arr2 = interpolation(arr1, I, J)
    a2   = pattern.DBZ(name=a1.name+'_normalised', 
                       matrix = arr2,
                       coordinateOrigin = (i0,j0), #taichung park make no sense any more
                       )
    if verbose:
        a2.show()
        plt.clf()
        showArrayWithAxes(a2.matrix, verbose=verbose, imagePath= a2.imagePath[:-4]+ '_with_axes' + a2.imagePath[-4:], imageTopDown=a2.imageTopDown)
    return {'IJ'        : (I, J),
            'a2'        : a2,
            'T'         : T,
            'centroid'  : np.array([i0, j0]),
            'eigenvalues'   : eigenvalues,
            'eigenvectors'  : eigenvectors,
            'theta'         : theta,
            }

def test2(*args, **kwargs):
    return momentNormalise(*args, **kwargs)
    
    
def momentMatch(a=pattern.a, b=pattern.b, verbose=True, saveImage=False):

    x = momentNormalise(a1=a, imagePath=a.imagePath[:-4] + '_withaxes' + a.imagePath[-4:])
    a1 = x['a2']
    a1.setThreshold(0)
    centroid_a = x['centroid']
    eigenvalues_a = x['eigenvalues']

    y = momentNormalise(a1=b, imagePath=b.imagePath[:-4] + '_withaxes' + b.imagePath[-4:])
    b1 = y['a2']
    b1.setThreshold(0)
    centroid_b = y['centroid']
    eigenvalues_b = y['eigenvalues']
    if saveImage:
        print "saving to", a1.imagePath
        a1.saveImage()
        print "saving to", b1.imagePath
        b1.saveImage()
    a2 = a1.drawCross(*centroid_a, radius=50)
    b2 = b1.drawCross(*centroid_b, radius=50)


    if verbose:
        a2.show()
        b2.show()
    a2.backupMatrix()
    b2.backupMatrix()

    I, J = IJ(a2.matrix)
    I, J = translation( I, J, (centroid_b - centroid_a))
    a2.matrix = interpolation(a2.matrix, I, J)
    a2.setThreshold(0)
    if verbose:
        a2.show()
        b2.show()
    if saveImage:
        print "saving to", a2.imagePath
        a2.saveImage()
        print "saving to", b2.imagePath
        b2.saveImage()
        
    #   adding in axial scalings
    print 'eigenvalues_a:', eigenvalues_a
    print 'eigenvalues_b:', eigenvalues_b

    a2.restoreMatrix()
    b2.restoreMatrix()

    displacement    = np.matrix(centroid_b - centroid_a)
    linearTr        = np.diag( (eigenvalues_b / eigenvalues_a) **.5 )
    affineTr        = np.hstack( [linearTr, displacement.T] )
    I, J = IJ(a2.matrix)
    I, J = affine(I, J, T=affineTr, origin=centroid_b)
    a3          = a2.copy()
    a3.matrix   = interpolation(a2.matrix, I, J)
    a3.setThreshold(0)
    if verbose:
        a3.show()
        b2.show()
    if saveImage:
        print "saving to", a.imagePath[:-4] + "_normalised_to_" + b.name + a.imagePath[-4:]
        a3.saveImage(imagePath= a.imagePath[:-4] + "_normalised_to_" + b.name + a.imagePath[-4:])

    a4          = a1.copy()
    a4.matrix   = interpolation(a1.matrix, I, J)

    b1.setThreshold(0)
    a4.setThreshold(0)
    if verbose:
        print 'a4 = a normalised to b'
        a4.show()
    
    rawCorr     = a.corr(b)
    normCorr    = b1.corr(a4)

    if verbose:
        b1.show()
        a4.show()
    outputString = 'raw correlation:  ' + str(rawCorr) + '\nnormalised correlation:' + str(normCorr)
    print outputString
    open(a.imagePath[:-4] + '_' + b.name + 'correlations.txt', 'w').write(outputString)
    return      {   'a momentnormalised to b'   : a4,
                    'raw correlation'           : rawCorr,
                    'normalised correlation'    : normCorr,
                    'a-momentnormalised': x,
                   'b-momentnormalised': y,
                   'a2-translation'    : a2,
                    'a3-affineTr'       : a3,
                                'b2'    : b2,
                            'IJaffine'  : (I, J),
                         'centroid_a'   : centroid_a,
                         'centroid_b'   : centroid_b,
                             'affineTr' : affineTr
                 }

def test3(aTime='0800', bTime='0900', verbose=False, saveImage=True):
    """
    from armor.geometry import transforms as tr ; reload(tr) ; from armor import pattern ; reload(pattern) ; x= tr.test3()
    """
    c=dbz('20120612.' + aTime)
    d = dbz('20120612.' + bTime)
    c.load()
    d.load()
    #c.show()
    #d.show()
    c.setThreshold(0)
    d.setThreshold(0)
    if verbose:
        c.show()
    reload(pattern) 
    x = momentMatch(c,d, verbose=verbose,saveImage=saveImage)
    return x
    
