#	clusteringTest20140710.py
#1.	~ 40 as thresholad
#2.	k-means clustering

from armor.initialise import *
from scipy.ndimage import morphology as mor
from armor.geometry import morphology as morph

def getTimeString():
    return str(time.time())

outputFolder = 'testing/'

m   = march('0312.2130')[0].load()

##############################
"""
m.show()
m.backupMatrix(0)
m.drawCoast()
m.saveImage()
m.restoreMatrix(0)
"""
##################################

"""
res = {}
for threshold in [20, 25, 30,35,40,45,50]:
    m1 = m.threshold(threshold)
    #m1.show()
    for k in [10, 20]:
        m1.saveImage(outputFolder+ timeString() + m1.name + ".png")
        x = m.getKmeans(k =k, threshold = threshold)
        x['pattern'].saveImage(outputFolder+ getTimeString() + m.name + "threshold%d_clusters%d.png" % (threshold,k))
        res[(threshold, k)] = x['pattern']

"""
#########################################

threshold = 40
k =  10

m.load()
m1=m.threshold(0)
m1.show()
m1.matrix = mor.grey_opening(m1.matrix, 5) ####
m1.matrix = mor.grey_closing(m1.matrix, 5) ####

m1.show()
m1.backupMatrix(0)
m1.showWithCoast()
m1.saveImage(outputFolder+m.name+'grey_opening_closing5.png')
m1.restoreMatrix()

threshold=30
x = m1.getKmeans(k =k, threshold = threshold)
x['pattern'].saveImage(outputFolder+ getTimeString() + m.name + "threshold%d_clusters%d.png" % (threshold,k))
threshold=40

m.load()
m.show()
x = m.getKmeans(k =k, threshold = threshold)
x['pattern'].saveImage(outputFolder+ getTimeString() + m.name + "threshold%d_clusters%d.png" % (threshold,k))
m2 = x['pattern']
m2.cmap = 'jet'
m2.show()

m3 = m2.copy()
m3.matrix = mor.grey_closing(m3.matrix, 2)
m3.matrix = mor.grey_opening(m3.matrix, 2)
m3.cmap = m.cmap
m3.show()
m3.matrix = np.ma.array(m3.matrix)
m3.matrix.mask = (m3.matrix==0)
m3.show()

m3.saveImage(outputFolder+getTimeString() + m.name + "threshold_cluster_close_open.png")

reg = []
for N in range(10):
    reg.append((N, m2.getRegionForValue(N, )))

for N in range(10):
    m2 = m2.drawRectangle(*reg[N][1])
m2.show()
m2.saveImage(outputFolder + m.name + 'threshold_cluster_regions.png')

m3 = m.copy()
for N in range(10):
    m3 = m3.drawRectangle(*reg[N][1])
m3.name = m.name + 'Rain Cell Regions'
m3.show()
m3.saveImage(outputFolder + m.name + 'rain_cell_regions.png')

