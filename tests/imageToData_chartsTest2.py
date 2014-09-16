#   imageToData_charts2.py
#   to extract information from CWB charts and convert them to regular data

#interpolation:
#http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html#multivariate-data-interpolation-griddata
"""

"""

import os, shutil
import numpy as np
import matplotlib.pyplot as plt
imshow = plt.imshow
from scipy import ndimage
from scipy import interpolate
import matplotlib as mpl
from scipy import cluster
import time
from armor import defaultParameters as dp


#inputFolder='/media/TOSHIBA EXT/CWB/charts2/2014-06-03/'
#imageName = '2014-06-03_2330.2MOS0.jpg'

#inputFolder= dp.CWBfolder+'charts2/2014-05-20/'
#inputFolder= dp.CWBfolder+'charts2/2014-08-16/'
inputFolder = dp.defaultImageDataFolder + 'charts2-allinone-/'
outputFolder = dp.root + 'labLogs2/imageToData/'
block=False
#outputFolder  = dp.CWBfolder+'temp/'

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

print 'InputFolder:', inputFolder
print 'sleeping 2 seconds:'
time.sleep(2)

################################################
imageNames = os.listdir(inputFolder)
#imageNames = [v for v in imageNames if '2014-08-16_1200'< v and v<'2014-08-16_1900'] #afternoon convective storms?!
N = len(imageNames)
xs = (np.random.random(30)*N).astype(int)
imageNames = [imageNames[v] for v in xs]
print '\n'.join(imageNames)
print 'sleeping 3 seconds'
time.sleep(3)
#################################################
for imageName in imageNames:
    #imageName = '2014-05-20_1700.2MOS0.jpg'


    l   = plt.imread(inputFolder+imageName)
    if os.sep == '\\':
        l = np.flipud(l)    #2014-09-16 
    plt.imshow(l, origin='lower') ; plt.show(block=block)

    l2  = np.zeros((600,600))
    l2  = l[:,:,0].astype(int) + l[:,:,1].astype(int) * 256 + l[:,:,2].astype(int) * 65536 
    np.histogram(l2)

    l5=cluster.vq.kmeans2(l2.flatten(), k=50)
    l6=l5[1].reshape((600,600))
    plt.imshow(l6, origin='lower', cmap='jet') ; plt.colorbar() ; plt.show(block=block)

    l3  = l[:,:,2].astype(int) + l[:,:,1].astype(int) * 256 + l[:,:,0].astype(int) * 65536 

    thres=150
    l4  = (l[:,:,2].astype(int)< thres) * (l[:,:,1].astype(int)<thres) * (l[:,:,0].astype(int)<thres)

    l4.sum()
    imshow(l4, origin='lower') ; plt.colorbar() ; plt.show(block=block)

    filterSize=20
    l5= ndimage.filters.median_filter(l[:,:,0], size=filterSize)
    l6= ndimage.filters.median_filter(l[:,:,1], size=filterSize)
    l7= ndimage.filters.median_filter(l[:,:,2], size=filterSize)

    l8  = l.copy()
    l8[:,:,0] = l5
    l8[:,:,1] = l6
    l8[:,:,2] = l7

    imshow(l8, origin='lower') ; plt.colorbar() ; plt.show(block=block)

    imshow(l, origin='lower') ;plt.show(block=block)

    colourBarY =[273, 253, 238, 219, 206, 193, 175,160, 145, 130, 115, 100, 80,67,52,34,19]
    colourBarX = 25

    j = colourBarX
    colourBar   = []
    colourBarSampleFile = open(outputFolder+'colourBarSample.log.txt','a')
    for i in colourBarY:
        Ri, Rj = (np.random.random(2)*4).astype(int)
        colourBarSampleString = '\t'.join([str(v) for v in [l[i+Ri,j+Ri], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]]])
        print colourBarSampleString
        #colourBar.append((l[i,j], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]))
        colourBar.append((l[i+Ri,j+Rj], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]))
        colourBarSampleFile.write(imageName+'\t'+str(i)+'\t'+colourBarSampleString+ '\t'+str(Ri)+'\t'+str(Rj) +'\n')
    colourBarSampleFile.write('\n------------------------------------------------------------------------\n')
    colourBarSampleFile.close()

    colourbar = colourBar

    colourbar   = [np.median(v, axis=0).astype(int).tolist() for v in colourBar]
    colourbar   = np.array(colourbar).astype(np.uint8)
    l9  = l.reshape((600*600, 3))
    x=cluster.vq.vq(l9,colourbar)

    x0  =x[0]
    plt.close()
    imshow(l, origin='lower')
    plt.savefig(outputFolder+ imageName + "_0_"+str(time.time())+ '.jpg')    
    plt.show(block=block)


    for i in range(16):
        plt.close()
        l10 = (x[0]==i).reshape((600,600))
        imshow(l10, origin='lower')
        plt.savefig(outputFolder+ imageName + "_" + str(time.time())+'.jpg')
        plt.show(block=block)

    x0= x[0].reshape(600,600)   #2014-09-16
    y= (x0>=16)
    print "y= (x0>=16)"
    plt.imshow(y, origin='lower'); plt.show(block=block)
    z = (x0<=8) * (x0>0)
    print "35+"
    plt.imshow(z, origin='lower'); plt.show(block=block)


    l81 = (l8[:,:,0]>160) *( l8[:,:,1]>160) *( l8[:,:,2]>160)
    l81[550:, :210] = 1
    l81[:250, :50] = 1
    l81 = 1- l81
    l82 = l81 + 1. *l81 *z  #35+  #2014-09-16

    imshow(l81, origin='lower',) ; plt.show(block=block)
    plt.subplot(221)
    imshow(l, origin='lower',)
    plt.subplot(222)
    imshow(l8, origin='lower',)
    plt.subplot(223)
    #imshow((x[0]==0).reshape((600,600)), origin='lower')
    imshow(l81, origin='lower',)
    plt.subplot(224)
    imshow(l82, origin='lower',)
    plt.savefig(outputFolder+ 'cleaned_'+imageName+"_"+str(time.time())+'.jpg')
    plt.show(block=block)



