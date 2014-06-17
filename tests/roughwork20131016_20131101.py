# -*- coding: utf-8 -*-
#   rough works - runnable and importable scripts from 2013-10-16
################################################################################
"""
USE
from armor.tests import roughwork as rw
reload(rw) ; from armor.tests.roughwork import *
a, b, c = loadN(0)


"""

################################################################################
#   imports and settings

from armor import pattern
dbz = pattern.DBZ
from armor.geometry import transforms as tr

from armor.geometry import frames
################################################################################
#
#   2013-10-16
#   moment-normalisation and other tests
#   work to be reported this friday at CWB
#
#   yau kwan kiu
#

############################
#   parameters
pattern.defaultOutputFolder = '/media/KINGSTON/ARMOR/labReports/2013-10-14/0200-0300/'
pattern.defaultOutputFolderForImages = pattern.defaultOutputFolder


############################
#   functions
def sidebyside(a, b):
    """
    ported to armor.geometry.frames.setSideBySide()
    """
    cmatrix = ma.hstack([a.matrix, b.matrix])
    c = dbz(name=a.name + '+' + b.name, matrix=cmatrix)
    return c

def loadN(*args):
    """
    from armor.tests import roughwork
    a,b,c = rw.load3('0200','0230','0300')
    """
    if len(args)==0:
        args = ['0200','0230','0300']
    res = []
    for t in args:
        a = dbz('20120612.'+t)
        a.load()
        a.setThreshold(0)
        res.append(a)
    return res


def computeCutoff(arr):
    """
    input: a 0-1 array (True/False; the mask of a masked array)
    output: a smoothed version - as a gradual cutoff
    idea: let the edge to slope slowly to zero in a length of about 100 pixels
    """





def test20131016():
    """
    data sets:  (1) 20120612.0200-0230-0300
                (2) 20120612.0210-0240-0310
    algorithms: (1) plain correlation
                (2) correlation with axes aligned and shift by centroid matching
                (3) correlation with axes aligned and shift by ABLER
                (4) correlation with axes aligned and shift by ABLER and axes rescaled
                (5) (4) with cutoffs
                (6) invariant moments feature comparison
    """
    #   1. get the centroids and moment matrices for both arrays a, b
    #   2. compute both thetas and moment arms
    #   3. translate, backrotate, and scale array a
    #   4. translate and rotate the result to match with b (ABLER or centroid matching)
    #   5. get the correlation of the result with b
    import time
    outputFolder = '/media/KINGSTON/ARMOR/labReports/2013-10-14/0200-0310/'
    outputSting = ''
    logFileName      = 'log' + str(int(time.time())) + '.txt'
    logFile = open(outputFolder+logFileName, 'a')
    import os
    result = []
    try:
        os.makedirs(outputFolder)
    except:
        pass
    from armor.shiiba import regressionCFLfree as cflfree
    reload(cflfree)
    from armor import analysis
    reload(analysis)
    from armor import pattern
    reload(pattern)
    from armor import objects
    reload(objects)
    from armor.objects import a,b,c,d,e,f
    L = [a,b,c,e,d,f]
    LL = {a: [b,c], d: [e,f]}
    LL = {a: [b,c ], d: [e,f]}     #after break
    results = []
    for p in [d, a]:
        for q in LL[p]:
            print '.......................'
            print p.name, '/', q.name
            print 'no shiiba'
            p1 = p.momentNormalise(q, useShiiba=False)
            outputString =  '......................\nno shiiba\n'
            outputString += p.name + '/'+ q.name +'\n'
            outputString += str( p.corr(q) ) +'\n'
            outputString += p1.name + '/'+ q.name +'\n'
            outputString += str( p1.corr(q) )+'\n'
            
            print outputString
            logFile.write(outputString)
            
            p1.imagePath = outputFolder+ p1.name+'.png'
            p1.outputPath = outputFolder+ p1.name+'.txt'
            p1.saveImage()
            p1.saveMatrix()

            pq1 = frames.setSideBySide(q, p1)
            pq1.imagePath = outputFolder+ pq1.name+'.png'
            pq1.outputPath = outputFolder+ pq1.name+'.txt'
            #pq1.saveImage()
            pq1.saveMatrix()
            
            ##############################################################################
            
            print '\n\nwith shiiba'
            xx = raw_input(' \n................\ncentre ?')
            xx = xx.split()
            while len(xx)==2:
                i0, j0 = [int(v) for v in xx]
                p2 = p.momentNormalise(q, centre=(i0, j0), searchWindowHeight=7, searchWindowWidth=13, useShiiba=True)
                print p2.Maffine
                xx = raw_input(' do again? centre ?')
                xx = xx.split()
    

            outputString =  '......................\nwith shiiba\n'
            outputString += p.name + '/'+ q.name+'\n'
            outputString += str( p.corr(q) )+'\n'
            outputString += p.name + '/'+ q.name+'\n'
            outputString += str( p2.corr(q) )+'\n'

            outputString += '\nMaffine: ' + str(p2.Maffine) + '\n\n'
            p2.imagePath = outputFolder+ p2.name+'.png'
            p2.outputPath = outputFolder+ p2.name+'.txt'
            p2.saveImage()
            p2.saveMatrix()

            pq2 = frames.setSideBySide(q, p2)
            pq2.imagePath = outputFolder+ pq2.name+'.png'
            pq2.outputPath = outputFolder+ pq2.name+'.txt'
            #pq2.saveImage()
            pq2.saveMatrix()
            
            print outputString
            logFile.write(outputString)
                        
        result.append( (p, p1, p2, pq1, pq2) )

    return result

################################################################################
#   2013-10-25
#   use of the Laplacian of Gaussian filter
'''
cd /media/KINGSTON/ARMOR/python/
ipython

'''
from armor import pattern
from armor import objects2
from armor.objects2 import *

def kongreyAnalyse():
    kongrey.fix('0828') #loading the images with the key '0828' and setting threshold=0
    kongrey.setOutputFolder('/home/k/ARMOR/data/KONG-REY/OBS/charts/')
    kongrey.setImageFolder('/home/k/ARMOR/data/KONG-REY/OBS/charts/')

    kongrey[0].show()
    ##kongrey.load(verbose=True)
    ##kongrey.setThreshold(0)
    #kongrey.saveImages(flipud=False,drawCoast=True)

    from scipy import ndimage
    LoG = ndimage.filters.gaussian_laplace

    sigma = 20

    outputFolder = '/home/k/ARMOR/data/KONG-REY/OBS/charts-laplaceofgaussian%d/' %sigma
    #try:
    #    os.makedirs(outputFolder)
    #except:
    #    pass

    kongrey.setImageFolder(outputFolder)

    for k in kongrey:
        #   laplaceofgaussian filter
        #   save image to a new folder
        #   test for typhoon eye
        #k.backupMatrix()
        k.matrix = LoG(k.matrix, sigma)
        mx = k.matrix.max()
        mn = k.matrix.min()
        k.vmax = mx
        k.vmin = mn - (mx-mn) *0.2
        print k.name,
        #k.show()
    #k=kongrey[0]
    #k.show()

    kongrey.setImageFolder(outputFolder)
    kongrey.saveImages(flipud=False, drawCoast=True)
    
################################################################################

##############
outputFolder = '/home/k/ARMOR/data/SOULIK/charts/'
def initialise(ds=soulik, outputFolder=outputFolder, key1='', drawCoast=False):
    ds.fix(key1) #loading the images with the key '0828' and setting threshold=0
    ds.setOutputFolder(outputFolder)
    ds.setImageFolder(outputFolder)
    ds[0].show()
    ds.saveImages(flipud=False,drawCoast=drawCoast)

##ds.load(verbose=True)
##ds.setThreshold(0)
#############

from scipy import ndimage
LoG = ndimage.filters.gaussian_laplace

#############
sigma = 5
outputFolder = '/home/k/ARMOR/data/SOULIK/charts-laplaceofgaussian%d/' %sigma
def LoGanalyse(ds=soulik, outputFolder=outputFolder, drawCoast=False, sigma=sigma):
    ds.setImageFolder(outputFolder)
    for k in ds:
        #   laplaceofgaussian filter
        #   save image to a new folder
        #   test for typhoon eye
        #k.backupMatrix()
        k.matrix = LoG(k.matrix, sigma)
        #mx = k.matrix.max()
        #mn = k.matrix.min()
        #mx  =   0.10
        #mn  =  -0.05
        #k.vmax = mx
        #k.vmin = mn - (mx-mn) *0.2
        print k.name,
        #k.show()
    mx = max([k.matrix.max() for k in ds])
    mn = min([k.matrix.min() for k in ds])
    #mx = 0.1
    #mn = -0.1
    ds.setVmin(mn)
    ds.setVmax(mx)
    ds.setImageFolder(outputFolder)
    ds.saveImages(flipud=False, drawCoast=drawCoast)
    return ds



#############
#############
from armor import pattern
from armor.objects2 import *

#def test20131027(ds=kongrey, key1='0829', drawCoast=True):
def test20131027(ds=kongrey, key1='', drawCoast=True):
    ds.fix(key1)
    #for sigma in [5, 20, 40, 60, 100]:
    for sigma in [5, 20, 40, 60, 100]:
        ds.fix(key1)
        outputFolder='/home/k/ARMOR/data/KONG-REY/OBS/' +key1 +'laplaceofgaussian' +str(sigma) + '/'
        LoGanalyse(ds=ds, outputFolder=outputFolder, drawCoast=drawCoast, sigma=sigma)

def test20131028(folder  = '/home/k/ARMOR/data/KONG-REY/summary/WRF[regridded]/',
                key1='',
                drawCoast=True,
                ):
    """kongrey WRF regridded 
    from armor.tests import roughwork as rw
    reload(rw) ; x = rw.test20131028()

    """
    import pickle
    for i in range(1, 21):
        fileName = 'dbzstream' + ('0'+str(i))[-2:] + '.pydump'
        filePath  = folder + fileName
        print '..................................'
        print filePath
        ds = pickle.load(open(filePath, 'r'))
        if i ==1:
            print ds[0].name
            ds[0].showWithCoast()
        for sigma in [5,20,40,60,100]:
            ds = pickle.load(open(filePath, 'r'))
            outputFolder = folder + ds.name + '_laplaceofgaussian' + str(sigma) + '/'
            LoGanalyse(ds=ds, outputFolder=outputFolder, drawCoast=drawCoast, sigma=sigma)
            pickle.dump(ds, open(outputFolder+ ds.name + '.pydump','w'))

#############

def test20131028b(outputFolder='/home/k/ARMOR/data/KONG-REY/WRFEPS/LaplacianOfGaussian/'):
    """kongrey WRF original data - not regridded
    from armor.tests import roughwork as rw
    reload(rw) ; x = rw.test20131028b()

    """
    from armor.filter import laplacianOfGaussian as LoG
    from armor import objects2
    reload(objects2)
    #from armor.objects2 import kongreymodels
    for M in range(1, 21):
        km = objects2.kongreyModel(M)
        km.fix()
        if 'M01' in km.name:        #test
            km[2].showWithCoast() 
            km[2].show3()
        for sigma in [1,2,5,10, 20]:
            km = objects2.kongreyModel(M)
            km.fix()
            LoG.analyse(ds=km, outputFolder=outputFolder + km.name + '_sigma' + str(sigma) + '/', 
                        drawCoast=True, sigma=sigma)

def test20131028c():
    """
    plotting all kongrey model outputs
    """
    from armor import objects2
    import os
    for i in range(1, 21):
        try:
            os.makedirs('/home/k/ARMOR/data/KONG-REY/WRFEPS/charts2/M' + ('0'+str(i))[-2:] +'/')
        except:
            continue
    kms = objects2.kongreymodelsall
    #kms.setImageFolder('/home/k/ARMOR/data/KONG-REY/WRFEPS/charts/')
    fileNameLength = len('201308280000f000_M01.txt')
    extLength      = len('.txt')
    for k in kms:
        k.modelLabel = k.dataPath[-extLength-3:-extLength]      # 'M01'
        k.name      =  k.dataPath[-fileNameLength:-extLength]
        hr          = int(k.name[8:10]) + int(k.name[14:16])
        hr          = ('0'+str(hr))[-2:]
        #k.name      = k.name[:8] +  hr + k.name[10:]
        k.name      = 'WRF' + k.modelLabel + '.DBZ' + k.name[:8] +  hr + '00'
        k.imagePath =  '/home/k/ARMOR/data/KONG-REY/WRFEPS/charts2/' + k.modelLabel +'/' + k.name + '.png'
        if os.path.exists(k.imagePath):
            print 'EXISTS1', k.imagePath
            continue
        else:
            k.load()
            k.setThreshold(0)
            k.drawCoast()
            k.saveImage()
            del k.matrix    # to save space

################################################################################    
import os
import numpy as np
from scipy import misc
from pylab import *
import re
import time
def saveArrayImage(im, path):
    im = misc.toimage(im)
    im.save(path)

def getDataTimeList(folder, verbose=True):
    L = os.listdir(folder)
    dataTimeList = [re.findall(r'[\d]{4}', v) for v in L]
    dataTimeList = [v[0]+v[1]+'.'+v[2] for v in dataTimeList]
    dataTimeList.sort()
    if verbose:
        print dataTimeList
    return dataTimeList

def getImage(folder, dataTime, verbose=True):
    L = os.listdir(folder)
    imageFile = [v for v in L if dataTime[:8] in v and dataTime[-4:] in v]
    if verbose:
        print folder, imageFile
    im = imread(folder+imageFile[0])
    return im

def resized(im, toSize):
    im = misc.imresize(im, toSize)
    return im
    
def makePanel6(images, verbose=False):
    height, width, depth = images[0].shape
    panel = np.zeros((height*2, width*3, depth))
    for n, im in enumerate(images):
        heightoffset = (n//3) * height
        widthoffset  = (n %3) * width
        panel[heightoffset:heightoffset+height, widthoffset: widthoffset+width, : ] = im
    return panel


def test20131030prep(M=1, 
                outputFolder='/home/k/ARMOR/data/KONG-REY/WRFEPS/charts6/??/',

                inputFolders= ['/home/k/ARMOR/data/KONG-REY/WRFEPS/charts/M??/',
                               '/home/k/ARMOR/data/KONG-REY/WRFEPS/LaplacianOfGaussian/WRF??.DBZ_sigma1/',
                               '/home/k/ARMOR/data/KONG-REY/WRFEPS/LaplacianOfGaussian/WRF??.DBZ_sigma2/',
                               '/home/k/ARMOR/data/KONG-REY/WRFEPS/LaplacianOfGaussian/WRF??.DBZ_sigma5/',
                               '/home/k/ARMOR/data/KONG-REY/WRFEPS/LaplacianOfGaussian/WRF??.DBZ_sigma10/',
                               '/home/k/ARMOR/data/KONG-REY/WRFEPS/LaplacianOfGaussian/WRF??.DBZ_sigma20/',
                              ],
                 toSize=(300,400),
                 ):
    """
    constructing composite images of filtered images of various scales
    """
    if M > -100:
        modelLabel = ('0'+str(M))[-2:]
        outputFolder = re.sub(r'\?\?', modelLabel, outputFolder)
        inputFolders = [re.sub(r'\?\?', modelLabel, v) for v in inputFolders]
        print '-----------------------------------'
        print 'Model:', modelLabel
        print 'output folder:', outputFolder
        print 'input folders:', inputFolders
        print 'sleeping 1 second'
        time.sleep(1)

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    dataTimeList = getDataTimeList(inputFolders[0])
    for dataTime in dataTimeList:
        image_out = np.zeros((toSize[0]*2, toSize[1]*3))
        images_in = []
        for folder in inputFolders:
            images_in.append(resized(getImage(folder,dataTime), toSize))
        image_out = makePanel6(images_in)
        saveArrayImage(image_out, outputFolder+dataTime+'.jpg')

def test20131030a():
    for M in range(1, 21):
        test20131030prep(M=M)

def test20131030b():
    """
    time.sleep(1000); from armor.tests import roughwork as rw ; reload(rw) ; rw.test20131030b()
    """
    test20131030prep(M=-9999,
                     outputFolder='/home/k/ARMOR/data/KONG-REY/OBS/charts6/',
                     inputFolders= ['/home/k/ARMOR/data/KONG-REY/OBS/charts/',
                                    '/home/k/ARMOR/data/KONG-REY/OBS/laplaceofgaussian5/',
                                    #'/home/k/ARMOR/data/KONG-REY/OBS/laplaceofgaussian10/',
                                    '/home/k/ARMOR/data/KONG-REY/OBS/laplaceofgaussian20/',
                                    '/home/k/ARMOR/data/KONG-REY/OBS/laplaceofgaussian40/',
                                    '/home/k/ARMOR/data/KONG-REY/OBS/laplaceofgaussian60/',
                                    '/home/k/ARMOR/data/KONG-REY/OBS/laplaceofgaussian100/',
                                    ],
                     )


#############################

def test20131031a(outputFolder = '/home/k/ARMOR/data_temp/'):
    """
    constructing the LoG filtered images of monsoon
    * 1.  construct the individual filtered images
    2. construct the combined images

    """
    from armor import objects3
    monsoon = objects3.monsoon
    monsoon.fix()
    #outputFolder = '/home/k/ARMOR/data_temp/'
    for sigma in [5, 20,40, 60,100]:    
        monsoon.setImageFolder(outputFolder+ 'laplaceofgaussian' + str(sigma) + '/' )
        monsoon.fix()
        LoGanalyse(ds=monsoon, outputFolder=outputFolder+ 'laplaceofgaussian' + str(sigma) + '/', drawCoast=True, sigma=sigma)


def test20131031b():
    """
    constructing the LoG filtered images of monsoon
    1.  construct the individual filtered images
    *2. construct the combined images

    """
    test20131030prep(M=-9999, 
                outputFolder='/home/k/ARMOR/data_temp/charts6/',

                inputFolders= ['/home/k/ARMOR/data_temp/charts/',
                               '/home/k/ARMOR/data_temp/laplaceofgaussian5/',
                               '/home/k/ARMOR/data_temp/laplaceofgaussian20/',
                               '/home/k/ARMOR/data_temp/laplaceofgaussian40/',
                               '/home/k/ARMOR/data_temp/laplaceofgaussian60/',
                               '/home/k/ARMOR/data_temp/laplaceofgaussian100/',
                              ],
                 toSize=(300,400),
                 )


def test20131101(dbzstream, sigma, outputFolder, threshold=-0.01, type='upper'):
    """
    from armor import objects3;  reload(objects3) ; kongrey=objects3.kongrey
    kongrey.fix()
    from armor.tests import roughwork as rw; reload(rw)
    rw.test20131101(kongrey, 10, '/media/KINGSTON/ARMOR/labReports/LaplacianOfGaussian/kongreySigma10/', -0.01)
    """
    ds = dbzstream
    ds.setImageFolder(outputFolder)
    try:
        os.makedirs(outputFolder)
    except:
        print 'folder exists!'
    for m in ds:                                                 
        m1 = m.laplacianOfGaussian(sigma)
        m1 = m1.threshold(threshold,type='upper')
        m1.saveImage()

###################################################    
################################################################################    
################################################################################    






