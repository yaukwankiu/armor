#loadImage.py
#    to load image to matrix

import pickle
import numpy as np
import matplotlib.pyplot as plt
from armor import defaultParameters as dp


def loadImage(a, dataTime="", dataPath="", imageType="hs1p", imageSuffix='.jpg', verbose=True, 
               multiplier=50.,
               rawImage=False,
               *args, **kwargs):

    if dataPath =="":
        if dataTime!="":
            # '/media/TOSHIBA EXT/CWB/hs1p/2013-09-09/2013-09-09_1100.jpg'
            dataTimeString = a.dataTime[0:4] + '-' + a.dataTime[4:6] + '-' + a.dataTime[6:8] + "_" + a.dataTime[9:13]
            dataPath = dp.root + '../CWB/' + imageType +  "/"+ dataTimeString[:10] + '/' + dataTimeString + imageSuffix
        elif a.dataTime!='':
            dataTime = a.dataTime
            dataTimeString = a.dataTime[0:4] + '-' + a.dataTime[4:6] + '-' + a.dataTime[6:8] + "_" + a.dataTime[9:13]
            dataPath = dp.root + '../CWB/' + imageType + "/"+ dataTimeString[:10] + '/' + dataTimeString + imageSuffix
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