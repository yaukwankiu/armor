#   hausdorffDimensionTest.py
#       http://en.wikipedia.org/wiki/Hausdorff_dimension
#       http://en.wikipedia.org/wiki/Minkowski-Bouligand_dimension
#start_image.py

#   parameters
bins = [0, 0.001, 0.003, 0.01, 0.3, 1., 3., 10., 30., 100.]
sigmas=[1, 2, 4, 8 , 16, 32, 64, 128, 256]

#   imports
import numpy as np
from armor import pattern
dbz = pattern.DBZ

#   defining the functions

def hausdorffDim(a, epsilon=1):
    """
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



#   setups
reload(pattern)
dbz= pattern.DBZ
a=dbz(dataTime='20140722.1300')
a.loadImage()
a.setMaxMin()

#   getting the edges before the computation of minkowski dimension
a1 = a.laplacianOfGaussian(sigma=1.5)
a1 = a1.copy()
a1.matrix= (abs(a1.matrix>1))
a1.setMaxMin()
a1.cmap ='jet'
a1.show()

dimH = {}
for epsilon in [64,32,16,8,4,2,1]:
    dimH[epsilon] = hausdorffDim(a1, epsilon=epsilon)

print dimH


#############################################################################
import os, time
from armor import defaultParameters as dp
from armor import pattern
reload(pattern)
dbz= pattern.DBZ

inputFolder = dp.root+'../CWB/hs1p/2014-07-22/'
outputFolder = dp.root+ 'labLogs2/hausdorffDim/'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
for DT in os.listdir(inputFolder):
    a=dbz(dataPath=inputFolder+DT)
    a.loadImage(dataPath=a.dataPath, imageType='hs1p')
    a.setMaxMin()
    x  = a.hausdorffDimPlot(ylim=[1.5,2.05], imagePath=outputFolder+ str(time.time()) + "hausdorffDim_plot_" + DT)

a.name = a.dataPath[-35:]
a.saveImage(outputFolder+a.dataPath[-19:])


