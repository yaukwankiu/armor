#   local features module
#   to detect local scales and features 
#   input:  armor.pattern.DBZ objects
#   output:  (tentative)    DBZ objects with marked rectangles

"""
cd /media/KINGSTON/ARMOR/python/
ipython -pylab

from armor import pattern
a=pattern.a
a.load()

from armor.geometry import localFeatures as lf
a.load()
a1 = lf.thresholding(a, thres=15, N=10, newObject=True )
a.load()
a4 = lf.thresholding(a, thres=15, N=10, newObject=True , scale=4)
a.load()
a10 = lf.thresholding(a, thres=15, N=10, newObject=True , scale=10)
a.load()
a20 = lf.thresholding(a, thres=15, N=10, newObject=True , scale=20)
a.load()


a10c    = lf.thresholding(a, thres=15, N=10, scale=10, operator='closing')
"""

#################################################################################
#   imports
#from armor import pattern

#################################################################################
#   parameters

#################################################################################
#   functions

def thresholding(a, thres=15, N=10, newObject=True, scale=0, operator="opening", verbose=True, showImage=True):
    """
    input:  a   = DBZ object
            N   = number of features 
    output: either a new object or the original

    default newObject set to True - 2013-12-10
    """
    height, width = a.matrix.shape
    try:
        a.features
    except AttributeError:
        a.features = []    # initialise if not found
    if newObject:
        a1 = a.copy()
    else:
        a1 = a
    if scale > 0:
        a2 = a1.copy()
        if operator=="opening":
            a2.matrix = a1.binaryOpening(scale=scale, threshold=thres)
        elif operator=="closing":
            a2.matrix = a1.binaryClosing(scale=scale, threshold=thres)  #2013-12-10           
    else:
        a2  = a1.above(thres)
    a2  = a2.connectedComponents(N=N)
    N = min(N, a2.matrix.max()+1)
    if not isinstance(N, int):
        print "N=", N #debug
        N = int(N)   # safety measure
    for i in range(N):
        #   get the rectangles
        #debug
        #print ((a2.matrix==1).sum(axis=1))[0]
        #end debug
        #try:
        minI = min([j for j in range(height) if ((a2.matrix==i).sum(axis=1))[j]>0 ])
        maxI = max([j for j in range(height) if ((a2.matrix==i).sum(axis=1))[j]>0 ])
        minJ = min([j for j in range(width)  if ((a2.matrix==i).sum(axis=0))[j]>0 ])
        maxJ = max([j for j in range(width)  if ((a2.matrix==i).sum(axis=0))[j]>0 ])
        #except IndexError:
        #    continue
        if verbose:
            print "rectangle at (i,j):", minI, minJ, ", with size:" ,maxI-minI, maxJ-minJ
        a.features.append({ 'type'      :   'threshold' + str(thres),
                           'coordinates':   (minI, minJ, maxI-minI, maxJ-minJ)
                           })       # keep the record in the original object
        a1 = a1.drawRectangle(minI, minJ, maxI-minI, maxJ-minJ, newObject=False)  #here newObject = False since a1 is already a copy of a 
        a1.name = a.name + '\nthreshold at ' + str(thres) + ', N=' + str(N)
        if scale>0:
            a1.name += ', scale=' + str(scale)
            a1.name += ', operator=' + str(operator)
    if showImage:
        a1.show()
    a1.imagePath = a.imagePath[:-4] + "_thres"  + str(thres) +\
                                     "_N"      + str(N)     +\
                                     "_scale"  + str(scale) +\
                                     "_operator-" + operator  +\
                                     a.imagePath[-4:]
    return a1
#################################################################################
#   tests
