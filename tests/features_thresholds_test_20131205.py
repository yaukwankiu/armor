secs = 0
dataSet = 'kongrey'
#dataSet = 'monsoon'
scale = 10
#scale = 10
#scale= 20

import time
print time.localtime()
print 'sleeping', secs, 'seconds'
time.sleep(secs)

from armor import pattern
from armor import objects3 as ob
from armor.geometry import localFeatures as lf
reload(pattern)
reload(ob)
reload(lf)


if dataSet == 'monsoon':
    m = ob.monsoon
    m.load('0612.02')
    m.load('0612.03')
    #m.load('0612.07')
    m.cutUnloaded()
elif dataSet== 'kongrey':
    m = ob.kongrey
    m.load('0828.08')
    m.load('0828.09')
    m.load('0828.10')
    m.cutUnloaded()

thres1 = 35
N1=20
thres2 = 20
N2     = 10

errorList=[]
for a in m:                                          
    try:
        print '-----------------------------------------------'
        print a.dataTime
        print 'thres, N:', thres1, N1
        if scale>0:
            print 'scale:', scale
        a1 = lf.thresholding(a, thres=thres1, N=N1, newObject=True, scale=scale, showImage=False)
        a1.imagePath = '/media/KINGSTON/ARMOR/python/armor/geometry/' +\
                       a.name + '_threshold' + str(thres1) + '_N' + str(N1) + '.png'
        if scale > 0:
            a1.imagePath = a1.imagePath[:-4] + '_scale' + str(scale) + a1.imagePath[-4:]
        print 'saving image:', a1.imagePath
        a1.saveImage()

        print 'thres, N:', thres2, N2
        a2 = lf.thresholding(a, thres=thres2, N=N2,scale=scale, newObject=True, showImage=False)
        a2.imagePath = '/media/KINGSTON/ARMOR/python/armor/geometry/' +\
                       a.name + '_threshold' + str(thres2) + '_N' + str(N2) + '.png'
        if scale > 0:
            a2.imagePath = a2.imagePath[:-4] + '_scale' + str(scale) + a2.imagePath[-4:]
        print 'saving image:', a2.imagePath
        a2.saveImage()
        print '...........'
        print a.name
        a3 = a.copy()
        for feat in a.features:
            if not ('threshold' in feat['type']):
                continue
            coords = feat['coordinates']
            print coords
            a3 = a3.drawRectangle(*coords)
        a3.name = a.name +  '\nthreshold ' + str(thres1) + ', N=' + str(N1) +\
                            ';  threshold ' + str(thres2) + ', N=' + str(N2)
        if scale>0:
            a3.name += ', scale=' + str(scale)
        a3.imagePath = '/media/KINGSTON/ARMOR/python/armor/geometry/' +\
                       a.name + '_threshold' + str(thres1) + '_N' + str(N1) + \
                                 '_threshold' + str(thres2) + '_N' + str(N2) + '.png'

        if scale > 0:
            a3.imagePath = a3.imagePath[:-4] + '_scale' + str(scale) + a3.imagePath[-4:]
        print 'saving image:', a3.imagePath
        a3.saveImage()
    except:
        print 'ERROR!!  - ', a.name
        errorList.append(a.name)

print "scale, dataSet, thres1, N1, thres2, N2", scale, dataSet, thres1, N1, thres2, N2


