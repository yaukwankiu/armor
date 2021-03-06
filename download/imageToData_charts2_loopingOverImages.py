#   imageToData_charts2.py
#   to extract information from CWB charts and convert them to regular data
"""

"""


import numpy as np
import matplotlib.pyplot as plt
imshow = plt.imshow
from scipy import ndimage
from scipy import interpolate
import matplotlib as mpl
from scipy import cluster
import time
import os

#inputFolder='/media/TOSHIBA EXT/CWB/charts2/2014-06-03/'
#imageName = '2014-06-03_2330.2MOS0.jpg'


outputFolder  ='/media/TOSHIBA EXT/CWB/temp/2014-06/'               # <-- edit here
#inputFolder='/media/TOSHIBA EXT/CWB/charts2/2014-05-20/'    # <-- edit here
inputFolder='/media/TOSHIBA EXT/CWB/charts2-allinone-/'

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
L   = os.listdir(inputFolder)
L.sort()
print L
time.sleep(2)

#L = L[0:2]                                                    # hack

for imageName in L:
    #imageName = '2014-05-20_1700.2MOS0.jpg'
    print imageName
    l   = plt.imread(inputFolder+imageName)
    plt.imshow(l, origin='lower')
    plt.savefig(outputFolder+str(time.time())+'.'+imageName)
    plt.close()
    #plt.show()

    l2  = np.zeros((600,600))
    l2  = l[:,:,0].astype(int) + l[:,:,1].astype(int) * 256 + l[:,:,2].astype(int) * 65536 
    np.histogram(l2)

    l5=cluster.vq.kmeans2(l2.flatten(), k=50)
    l6=l5[1].reshape((600,600))
    plt.imshow(l6, origin='lower', cmap='jet') ; #plt.colorbar()
    plt.savefig(outputFolder+str(time.time())+'.kmeans2.jpg')
    plt.close()
    #plt.show()

    l3  = l[:,:,2].astype(int) + l[:,:,1].astype(int) * 256 + l[:,:,0].astype(int) * 65536 

    thres=150
    l4  = (l[:,:,2].astype(int)< thres) * (l[:,:,1].astype(int)<thres) * (l[:,:,0].astype(int)<thres)

    l4.sum()
    imshow(l4, origin='lower') ; #plt.colorbar() 
    plt.savefig(outputFolder+str(time.time())+'.darklines.jpg')
    #plt.show()
    plt.close()
    
    filterSize=20
    l5= ndimage.filters.median_filter(l[:,:,0], size=filterSize)
    l6= ndimage.filters.median_filter(l[:,:,1], size=filterSize)
    l7= ndimage.filters.median_filter(l[:,:,2], size=filterSize)

    l8  = l.copy()
    l8[:,:,0] = l5
    l8[:,:,1] = l6
    l8[:,:,2] = l7

    imshow(l8, origin='lower') ; #plt.colorbar() 
    plt.savefig(outputFolder+str(time.time())+".median_image.jpg")
    #plt.show()
    plt.close()

    #imshow(l, origin='lower') 
    #plt.show()

    colourBarY =[273, 253, 238, 219, 206, 193, 175,160, 145, 130, 115, 100, 80,67,52,34,19]
    colourBarX = 25

    j = colourBarX
    colourBar   = []
    for i in colourBarY:
        print l[i,j], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]
        colourBar.append((l[i,j], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]))

    colourbar = colourBar

    colourbar   = [np.median(v, axis=0).astype(int).tolist() for v in colourBar]
    colourbar   = np.array(colourbar).astype(np.uint8)
    l9  = l.reshape((600*600, 3))
    x=cluster.vq.vq(l9,colourbar)

    x0  =x[0]

    imshow(l, origin='lower')
    plt.savefig(outputFolder+str(int(time.time())) + '.00' + imageName)    
    plt.close()
    #plt.show()


    for i in range(16):
        l10 = (x[0]==i).reshape((600,600))
        imshow(l10, origin='lower', cmap='gray')
        plt.savefig(outputFolder+str(time.time())+'.jpg')
        plt.close()
        #plt.show()




#interpolation:
#http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html#multivariate-data-interpolation-griddata
