#loadImage.py
#    to load image to matrix
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from armor import defaultParameters as dp


def loadImage(a, dataTime="", dataPath="", 
                inputFolder="",
                #imageType="hs1p", 
                imageType='charts2',
                imageSuffix='.jpg', verbose=True, 
               multiplier=50.,
               rawImage=False,
               medianFilterSize=20, #for removing unwanted lines in charts2
               *args, **kwargs):
    print 'inputFolder: ', inputFolder #debug
    if dataPath =="":
        if inputFolder=="":
            inputFolder= dp.root + '../CWB/'
        if dataTime!="":
            # '/media/TOSHIBA EXT/CWB/hs1p/2013-09-09/2013-09-09_1100.jpg'
            dataTimeString = a.dataTime[0:4] + '-' + a.dataTime[4:6] + '-' + a.dataTime[6:8] + "_" + a.dataTime[9:13]
            print 'dataTimeString', dataTimeString    # debug
            dataPath = inputFolder + imageType +  "/"+ dataTimeString[:10] + '/' + dataTimeString + imageSuffix
        elif a.dataTime!='':
            dataTime = a.dataTime
            dataTimeString = a.dataTime[0:4] + '-' + a.dataTime[4:6] + '-' + a.dataTime[6:8] + "_" + a.dataTime[9:13]
            dataFolder = inputFolder + imageType + "/"+ dataTimeString[:10] + '/'
            try:
                dataFolderList = os.listdir(dataFolder)
                dataFileName = [v for v in dataFolderList if dataTimeString in v and imageSuffix in v][0]
            except IndexError:
                dataFileName = dataFolderList[0]
            dataPath = dataFolder + dataFileName
            print "dataFileName:", dataFileName
        elif a.dataPath!="":
            dataPath = a.dataPath
        else:
            dataPath = a.imagePath

    if verbose:
        print "loading image from" , dataPath

    try:
        if imageType == 'hs1p' and rawImage==False:
    
            if "threshold" in kwargs.keys():
                threshold = kwargs['threshold']
            else:
                threshold=120
            img = plt.imread(dataPath)
            #img = np.flipud(img)
            img2= ((img[:,:,0] > threshold) * (img[:,:,1] > threshold) * (img[:,:,2]>threshold)).astype(int)
            a.matrix = np.ma.array(img2, fill_value=-999)
            a.matrix*=multiplier
            a.matrix.mask=False   
            a.matrix.set_fill_value(-999)
            a.setMaxMin()
            return a
        elif imageType == 'charts2' and rawImage==False:
            from scipy import ndimage
            l   = plt.imread(dataPath)
            # adapted from armor/tests/imageToData_chartsTest.py
            l5= ndimage.filters.median_filter(l[:,:,0], size=medianFilterSize)
            l6= ndimage.filters.median_filter(l[:,:,1], size=medianFilterSize)
            l7= ndimage.filters.median_filter(l[:,:,2], size=medianFilterSize)
            l8  = l.copy()
            l8[:,:,0] = l5
            l8[:,:,1] = l6
            l8[:,:,2] = l7
            l81 = (l5>160) *( l6>160) *( l7>160)
            if a.imageTopDown:  # ms windows and linux treat the jpg images differently!! one goes from bottom to top, one goes from top to bottom
                l81 = np.flipud(l81)
            l81[550:, :210] = 1
            l81[:250, :50] = 1
            if a.imageTopDown:  # ms windows and linux treat the jpg images differently!! one goes from bottom to top, one goes from top to bottom
                l81 = np.flipud(l81)
            
            l81 = 1- l81
            img = l81
            a.matrix = np.ma.array(img, fill_value=-999)
            a.matrix*=multiplier
            a.matrix.mask=False   
            a.matrix.set_fill_value(-999)
            a.setMaxMin()
            return a
        else:
            img = plt.imread(dataPath)
            #img = np.flipud(img)
            a.matrix = img
            a.setMaxMin()
            return a
    except IOError:
        if verbose:
            print "can't load image", a.dataTime
        else:
            pass
