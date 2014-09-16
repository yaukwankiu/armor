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

####################################################################
#   edit here for input
#inputFolder='/media/TOSHIBA EXT/CWB/charts2/2014-06-03/'
#imageName = '2014-06-03_2330.2MOS0.jpg'
#inputFolder= dp.CWBfolder+'charts2/2014-05-20/'
#imageName = '2014-05-20_1700.2MOS0.jpg'
#inputFolder= dp.defaultImageDataFolder+'charts2/2014-05-19/'
#imageName = '2014-05-19_1200.2MOS0.jpg'

#inputFolder= dp.defaultImageDataFolder+'charts2/2014-07-07/'
#imageName = '2014-07-07_1230.2MOS0.jpg'

#inputFolder= dp.defaultImageDataFolder+'charts2/2014-07-19/'
#imageName = '2014-07-19_1330.2MOS0.jpg'

inputFolder= dp.defaultImageDataFolder+'charts2/2014-05-20/'
imageName = '2014-05-20_1200.2MOS0.jpg'

#
####################################################################

#outputFolder  = dp.CWBfolder+'temp/'
outputFolder = dp.root + 'labLogs2/charts/'

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
block=True

  

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
#colourBar   = [0,0,0]
for i in colourBarY:
    print l[i,j], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]
    colourBar.append((l[i,j], l[i+1, j+1], l[i-1,j-1], l[i+1,j-1], l[i-1,j+1]))
    #colourBar.append(l[i-2:i+2, j-2:j+2].mean(axis=0).mean(axis=0))    #doesn't work yet

colourbar = colourBar
colourbar   = [np.median(v, axis=0).astype(int).tolist() for v in colourBar]

colourbar   = np.array(colourbar).astype(np.uint8)
colourbar   = np.vstack([colourbar, [0,0,0],[150, 150, 150], [6, 141, 152], [0,150, 150], [150,0,150], [150,150,0]])
l9  = l.reshape((600*600, 3))
x=cluster.vq.vq(l9,colourbar)

x0  =x[0]
plt.close()
imshow(l, origin='lower')
plt.savefig(outputFolder+ '0_'+str(time.time())+ '.jpg')    
plt.show(block=block)


for i in range(len(colourbar)):
    try:
        plt.close()
        l10 = (x[0]==i).reshape((600,600))
        print i, colourbar[i]
        imshow(l10, origin='lower')
        plt.savefig(outputFolder+str(time.time())+'.jpg')
        plt.show(block=block)
    except AttributeError:
        print "attribute error!"

x0= x[0].reshape(600,600)
y= (x0>=16)
print "y= (x0>=16)"
plt.imshow(y, origin='lower'); plt.show(block=block)

z = (x0<=8) * (x0>0)
print "35+"
plt.imshow(z, origin='lower'); plt.show(block=block)


l81 = 1.*(l8[:,:,0]>160) *( l8[:,:,1]>160) *( l8[:,:,2]>160)
l81[550:, :210] = 1
l81[:250, :50] = 1
l81 = 1- l81

l82 = l81 + 1. *l81 *z  #35+

print "median filter"
imshow(l81, origin='lower',) ; plt.show(block=block)

print "median filter+ threshold35"
plt.subplot(221)
imshow(l, origin='lower',)
plt.subplot(222)
imshow(l8, origin='lower',)
plt.subplot(223)
#imshow((x[0]==0).reshape((600,600)), origin='lower')
imshow(l81, origin='lower',)
plt.subplot(224)
imshow(l82, origin='lower',)
plt.savefig(outputFolder+imageName[:20]+'medianFilter+threshold35.png')
plt.show(block=block)

###
#   now, cut out the specific colours!! need: 50+, 45+, 40+, 35+ and perhaps 30+
#   1. get the average colour values
#   2. recluster with these colour values

i1 = [201, 187, 171, 155, 138, 124, 109,  93, 76, 64, 50, 33, 25] + [33]
i2 = [212, 197, 181, 165, 149, 135, 118, 106, 90, 73, 58, 42, 28] + [120]
j1 = [18]*13 +[63]
j2 = [31]*13+ [140]
colourIntensities = range(50, -15, -5) + [-999]
colourAverages=[]
N = len(i1)
for i in range(N):
    colourValue=int(l2[i1[i]:i2[i], j1[i]:j2[i]].mean())
    colourAverages.append(colourValue)
    print i, colourIntensities[i], "+ : ", colourValue, colourValue%256, colourValue//256%256, colourValue//65536 


l51=cluster.vq.kmeans2(l2.flatten(), k=np.array(colourAverages+[0]), minit='matrix')
l61=l51[1].reshape((600,600))
plt.imshow(l61, origin='lower', cmap='jet') ; plt.colorbar() ; plt.show(block=block)


########################################
#   clustering with RGB triplets instead of a single scalar - for better accuracy
colourbar = dp.chart2ColourBar 
colourbar = [colourbar[v] for v in sorted(colourbar.keys(), reverse=True)]
colourbar += [[150, 150, 150], [212, 225, 233]]  #for the black lines, and the backgrounds
colourbar = np.array(colourbar)
print 'colourbar:', colourbar
l22  = l.reshape(600*600, 3).astype(int)
#np.histogram(l2)

l52= cluster.vq.kmeans2(l22, k=colourbar, minit='matrix')
l62=l52[1].reshape((600,600))
plt.savefig(outputFolder+ 'RGBclustering_'+ imageName)
plt.imshow(l62, origin='lower', cmap='jet') ; plt.colorbar() ; plt.show(block=block)

numberOfLayers = l62.max()+1
for i in range(numberOfLayers):
    print 'layer', i, ':', colourbar[i], (l62==i).sum()
    plt.imshow((l62==i), origin='lower') 
    plt.savefig(outputFolder+ 'RGBclustering_layer' + str(i) +"_"+ imageName)
    plt.show(block=block)
 
z = (l62<=8) 
print "35+"
plt.imshow(z, origin='lower'); plt.show(block=block)

l81 = 1.*(l8[:,:,0]>160) *( l8[:,:,1]>160) *( l8[:,:,2]>160)
l81[550:, :210] = 1
l81[:250, :50] = 1
l81 = 1- l81

l82 = l81 + 1. *l81 *z  #35+

print "median filter"
imshow(l81, origin='lower',) ; plt.show(block=block)

print "median filter+ threshold35"
plt.subplot(221)
imshow(l, origin='lower',)
plt.subplot(222)
imshow(l8, origin='lower',)
plt.subplot(223)
#imshow((x[0]==0).reshape((600,600)), origin='lower')
imshow(l81, origin='lower',)
plt.subplot(224)
imshow(l82, origin='lower',)
plt.savefig(outputFolder+imageName[:20]+'medianFilter+threshold35.png')
plt.show(block=block)
