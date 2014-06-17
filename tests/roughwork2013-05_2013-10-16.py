# -*- coding: utf-8 -*- 
############ 16-10-2013 ######################

In [12]: def sidebyside(a, b):
   ....:     cmatrix = ma.hstack([a.matrix, b.matrix])
   ....:     c = dbz(name=a.name + '+' + b.name, matrix=cmatrix)
   ....:     return c
   ....: 

pattern.defaultOutputFolderForImages  = '/media/KINGSTON/ARMOR/labReports/2013-10-14/0200-0300'


############ 13-10-2013 ######################
#   finish the testing and write up
#   1.  plan the testing
#       * setting:  A doesnt move; B normlised to A
#   2.  write up the planning
#   3.  conduct the testing
#   4.  write up the testing
#   5.  summarise

############ 11-10-2013 ######################
exit()
python

from armor import pattern
dbz=pattern.DBZ

from armor.geometry import transforms as tr

x=tr.test3('0200','0210')

res = []
for startTime in range(200, 700, 100):
    for endTime in [startTime + 30, startTime+100]:
        start = ("00" + str(startTime))[-4:]
        end   = ("00" + str(endTime))[-4:]
        res.append(tr.test3(start, end))



print len(res)

############ 09-10-2013 ######################
exit()
python

from armor import pattern
dbz=pattern.DBZ
import armor.geometry.transforms as tr
c=dbz('20120612.0800')
d = dbz('20120612.0900')
c.load()
d.load()
#c.show()
#d.show()
c.setThreshold(0)
d.setThreshold(0)
c.show()
reload(pattern) ; reload(tr) ; x=tr.momentMatch(c,d, verbose=False,saveImage=True)

############ 09-10-2013 ######################

exit()

cd /media/KINGSTON/ARMOR/python/
python

from armor import pattern
from armor.geometry import transforms as tr
import numpy as np
dbz=pattern.DBZ

#a = pattern.a
#b = pattern.b

a = dbz('20120612.0230')
b = dbz('20120612.0900')
a.load()
a.setThreshold(0)
b.load()
b.setThreshold(0)


a.show()
b.show()
x = tr.momentNormalise(a1=a)
a2 = x['a2']
centroid_a = x['centroid']
eigenvalues_a = x['eigenvalues']

y = tr.momentNormalise(a1=b)
b2 = y['a2']
centroid_b = y['centroid']
eigenvalues_b = y['eigenvalues']


a2.backupMatrix()
b2.backupMatrix()

a2.matrix = a2.drawCross(*centroid_a, radius=50).matrix
a2.show()
b2.matrix = b2.drawCross(*centroid_b, radius=50).matrix
b2.show()
I, J = tr.IJ(a2.matrix)
I, J = tr.translation( I, J, (centroid_b - centroid_a))
a2.matrix = tr.interpolation(a2.matrix, I, J)
a2.setThreshold(0)

a2.show()
b2.show()

#   adding in axial scalings

print 'eigenvalues_a:', eigenvalues_a
print 'eigenvalues_b:', eigenvalues_b

a2.restoreMatrix()
b2.restoreMatrix()

displacement    = np.matrix(centroid_b - centroid_a)
linearTr        = np.diag( (eigenvalues_b / eigenvalues_a) **.5 )
affineTr        = np.hstack( [linearTr, displacement.T] )
I, J = tr.IJ(a2.matrix)
I, J = tr.affine(I, J, T=affineTr, origin=centroid_b)
a2.matrix   = tr.interpolation(a2.matrix, I, J)
a2.setThreshold(0)

a2.show()
b2.show()

############ 08-10-2013 ######################
#   moment normalisation test for given DBZ patterns

cd /media/KINGSTON/ARMOR/python
python

import matplotlib.pyplot as plt
from armor import pattern
a   = pattern.a
b   = pattern.b

from armor.geometry import transforms as tr

reload(tr)
x = tr.test2(a)
y = tr.test2(b)

dbz = pattern.DBZ
d   = dbz('20120612.0700')
d.load()
d.setThreshold(0)
tr.test2(d)


############ 07-10-2013 ######################

cd /media/KINGSTON/ARMOR/python
python

import numpy as np
from armor import pattern
a=pattern.a
a.load()

aa= a.drawCross(radius=50)
aa.show2()
aa.vmin=-50

aa.matrix = np.flipud(aa.matrix)

import armor.geometry.transforms as tr
reload(tr)
#for rad in  sorted([0.1, 0.2, 0.3, 0.4, 0.6, 1, 2,  2.2,2.5, 3, 3.5, 0.5, 0.8, 1.2, 1.5, 1.8, 2.2,2.5, 3, 3.5]):
for rad in  sorted([0.1, 0.2, 0.3]):
    for scales in [(1.2,0.8), (1.1, 0.9), (1,1), (0.9, 1.1), (0.5,2)]:
        I, J = tr.IJ(aa)
        print "I, J:", I, '\n..............\n', J
        mat = tr.rotation(rad)
        mat = [[scales[0]], [scales[1]]] * np.array(mat)
        print "mat:", mat
        mat = np.hstack([mat, [[0],[0]]])
        print "rad:", rad
        #tr.test(aa, mat, showImage=True, saveImage=True)
        #tr.test(aa, mat, showImage=False, saveImage=True)
        tr.test(aa, mat, showImage=True, saveImage=False)


############ 06-10-2013 ######################
#   continue:   the algorithm evaluations
#   /media/KINGSTON/ARMOR/documents/2013-10-01-armor-evaluating-matching-algorithms-with-kongrey-proposal.doc

cd /media/KINGSTON/ARMOR/python
python


import numpy as np
import matplotlib.pyplot as plt
from armor.geometry import transforms as tr
from armor.geometry import transformedCorrelations as trc
from armor import pattern
reload(pattern)
reload(tr)

m1  = 50* trc.sample1()
m2  = 50* trc.sample2()
m3  = 50* trc.sample3()

for m in [m1, m2, m3]:
    plt.imshow(m)
    plt.show()

for m in [m1, m2, m3]:
    for rad in [0, 0.2, 0.6,1, 1.2, 1.4,1.8]:
        I, J = tr.IJ(m)
        M    = pattern.DBZ(matrix=m, vmin=-1, vmax=5)
        M.show()
        I, J = tr.translation(I, J, (10, 20))
        m_rot    = tr.interpolation(m, I, J, True)
        M_rot    = pattern.DBZ(matrix=m_rot, vmin=-1, vmax=5)
        M_rot.show()   
        trc.showArrayWithAxes(m_rot)


        I, J = tr.IJ(m)
        i0, j0 = trc.getCentroid(m)
        print i0, j0
        I, J = tr.translation(I, J, (i0, j0))
        m_rot    = tr.interpolation(m, I, J, False)
        trc.showArrayWithAxes(m_rot)
        I, J = tr.linear(I, J, tr.rotation(rad))
        m_rot    = tr.interpolation(m, I, J, False)
        trc.showArrayWithAxes(m_rot)
        I, J = tr.translation(I, J, (-i0, -j0))
        m_rot    = tr.interpolation(m, I, J, False)
        trc.showArrayWithAxes(m_rot)



'''
        M   = trc.getMomentMatrix(m_rot)
        eigenvalues, eigenvectors = trc.getAxes(M, display=False)
        print "eigenvalues/vectors:", eigenvalues, eigenvectors
        centroid_i, centroid_j = trc.getCentroid(m_rot)
        I, J = trc.transform(m_rot, centroid_i, centroid_j,  eigenvalues=eigenvalues, eigenvectors=eigenvectors)
        m_tr = trc.interpolate(m_rot, I, J)
        #plt.imshow(m_tr)
        #plt.show()
        trc.showArrayWithAxes(m_tr)
'''     
    
    

#############################



import numpy as np
import matplotlib.pyplot as plt
from armor.geometry import transforms as tr
from armor.geometry import transformedCorrelations as trc
from armor import pattern
reload(pattern)
reload(tr)
A = pattern.a
A.load()
a=A.matrix
A.coordinateOrigin = (492, 455)
dbz= pattern.DBZ
#for rad in [0,0.1,0.2,0.3,0.4,0.5,0.6,1, 1.2, 1.4,1.8,2.2,2.6,3,3.4,3.8,4.2,4.6,5]:
for rad in [0.2]:
    for sheer in [0, 0.1, 0.2, 0.3, 0.4,0.5, 0.6,.7]:
        I, J = tr.IJ(a)
        i0, j0 = A.coordinateOrigin
        I, J = tr.translation(I, J, (i0, j0))
        I, J = tr.linear(I, J, tr.rotation(rad)+ [[0, sheer], [sheer,0]])
        I, J = tr.translation(I, J, (-i0, -j0))
        c    = tr.interpolation(a, I, J, False)
        C    = dbz(matrix=c, name= 'a_rotated_by_'+str(rad) + '_radians')
        C.imagePath = 'armor/geometry/transformsPics/' + C.name +'.png'
        #C.saveImage()
        C.show4()



############ 03-10-2013 ######################
#   conduct the study as outlined in 
#   /media/KINGSTON/ARMOR/documents/2013-10-01-armor-evaluating-matching-algorithms-with-kongrey-proposal.doc
#   first, complete the renormalised correlation module
#   next, re-read Hu's paper and decide on how to match with invar moments

cd /media/KINGSTON/ARMOR/python
python

from armor.geometry import transforms as tr
from armor import pattern
reload(pattern)
reload(tr)
A = pattern.a
A.load()
a=A.matrix
A.coordinateOrigin = (492, 455)
dbz= pattern.DBZ
#for rad in [0,0.1,0.2,0.3,0.4,0.5,0.6,1, 1.2, 1.4,1.8,2.2,2.6,3,3.4,3.8,4.2,4.6,5]:
for rad in [0.6,1, 1.2, 1.4,1.8,2.2,2.6,3,3.4,3.8,4.2,4.6,5]:
    I, J = tr.IJ(a)
    i0, j0 = A.coordinateOrigin
    I, J = tr.translation(I, J, (i0, j0))
    I, J = tr.linear(I, J, tr.rotation(rad))
    I, J = tr.translation(I, J, (-i0, -j0))
    c    = tr.interpolation(a, I, J, False)
    C    = dbz(matrix=c, name= 'a_rotated_by_'+str(rad) + '_radians')
    C.imagePath = 'armor/geometry/transformsPics/' + C.name +'.png'
    C.saveImage()
    #C.show4()



############ 03-10-2013 ######################
#   make a video of compref from typhoon kong-rey

#   1.  construct the stream
#   2.  feed it to the video maker
# ref: http://stackoverflow.com/questions/16897480/making-a-video-with-opencv-getting-only-1-frame

cd /home/k/ARMOR/data/KONG-REY/OBS/graphs/
ipython

import os
L = os.listdir('.')
L.sort()
import cv2
from cv import *

imgs = [cv2.imread(filename) for filename in L]
height, width, layers = imgs[0].shape


video=cv2.VideoWriter('compref-kongrey2.avi', CV_FOURCC('D', 'I', 'V', 'X'),1,(width,height))
for im in imgs:
    video.write(im)

cv2.destroyAllWindows()
video.release()

##############################################

############ 27-09-2013 ######################
# per yesterday (802 weekly meeting)
#   to do:
#   1. set all x:  -100<x<0 to 0 in compref and wrf [note to self: -150 for safety]
#   2. find the effective common region for compref + wrf
#   3. draw a picture for WRF+COMPREF common effective region

#   so now:  redo everything; first, reset pattern.py to mask=-150
#       no reset yet, do it dynamically
#   these lines added to kongrey.py:
#        ds1.setFloor(0)     # added 2013-09-27
#        ds2.setFloor(0)     # added 2013-09-27
# redo the stuff on 26-09-2013 and 24-09-2013



############ 26-09-2013 ######################

cd /media/KINGSTON/ARMOR/python

python

###############################################
# 2013-09-26
# date splits for prediction-validation

import time
import pickle
#time.sleep(1500)
print time.asctime()

from armor.dataStreamTools import kongrey
from armor.dataStreamTools import makeVideo
mv = makeVideo
kr = kongrey
reload(mv)
reload(kr)

averageScoreOrdering = True
#L = ['0828.0', '0828.1', '0829.0', '0829.1', '0828', '0829', '0830' , '']
#L = [ '0830']
L =['']
try:
    results
except:
    results = []


for key1 in L:
    time1 = str(int(time.time()))
    #reload(kr)
    #reload(mv)
    print '=================================================================='
    print 'key1:', key1
    print 'kr.timeString:', kr.timeString
    #for algor in [kr.moments, kr.regionalGlobalMoments, kr.plain_correlation, ]:
    #for algor in [kr.modelNumber]: #2013-10-1
    #for algor in [kr.pick19_18_16]: #2013-10-1
    for algor in [ kr.pick11_20, kr.pick1_10, ]: #2013-10-1
        print "timeStamp, algorithm / to average the score ordering?(True/False)", kr.timeString, algor, averageScoreOrdering
        result = kr.pmt(algor,
                    #makeSmallImages=True, 
                    makeSmallImages=False, #2013-09-26
                    smallDpi= 60, 
                    frameDpi= 300,
                    panel_cols = 4,
                    panel_rows = 3,
                    #panel_cols = 2,#2013-10-1
                    #panel_rows = 2,
                    #panel_cols = 5,
                    #panel_rows = 5,
                    loadFormerAnalysisResult=False, 
                    averageScoreOrdering = averageScoreOrdering,
                    #loadFormerAnalysisResult=True,
                    #summary_folder="",              # needed if loadFormerAnalysisResult is True
                    #matching_algorithm_name= 'plain_correlation',     # needed if loadFormerAnalysisResult is True
                    key1 = key1,  # 2013-09-26
                    # kwargs:
                    )
        print time.asctime()
    results.append({'date':key1, 'kr.timeString':kr.timeString, 'timeString':kr.timeString, 'result': result}) 

print results[0].keys()

for v in results:
    print '....................................'
    print v['date'],
    print v['timeString']
    ordering =  v['result']['ordering']
    print '_'.join([str(w) for w in ordering]) 

import pickle
pickle.dump(results, open('/home/k/ARMOR/data/KONG-REY/summary/' +kr.timeString+ '/results.pydump','w'))





exit()

################################################################################


exit()
exit



############ 24-09-2013 ######################


cd /media/KINGSTON/ARMOR/python

python

###############################################
# 2013-09-24

import time

#time.sleep(2000)
print time.asctime()

from armor.dataStreamTools import kongrey
from armor.dataStreamTools import makeVideo
mv = makeVideo
kr = kongrey
reload(mv)
reload(kr)

#for averageScoreOrdering in [True,False]:
for averageScoreOrdering in [False]:
    reload(kr)
    reload(mv)
    for algor in [kr.plain_correlation, kr.moments, kr.regionalGlobalMoments]:
        print "timeStamp, algorithm / to average the score ordering?(True/False)", kr.timeString, algor, averageScoreOrdering
        result = kr.pmt(algor,
                    makeSmallImages=True, 
                    smallDpi= 60, 
                    frameDpi= 300,
                    #panel_cols = 3,
                    #panel_rows = 3,
                    panel_cols = 5,
                    panel_rows = 5,
                    loadFormerAnalysisResult=False, 
                    averageScoreOrdering = averageScoreOrdering,
                    #loadFormerAnalysisResult=True,
                    #summary_folder="",              # needed if loadFormerAnalysisResult is True
                    #matching_algorithm_name= 'plain_correlation',     # needed if loadFormerAnalysisResult is True
                    )
        print time.asctime()


#reload(kr) ; result = kr.pmt(kr.plain_correlation, makeSmallImages=False, frameDpi=600)


################################


############ 23-09-2013 ######################
#   today
#   1.  construct the basic DSS object - 
#           class dataStreamSet:  DSS = dataStreamSet(ds0, ds1, ds2,...dsN) where ds0 = observations, ds1, ds2,.. = models
#           with the bare basic methods of analysis and output to panel of 20+ images
#   2.  do the various tests
#   3.  pattern is getting long.  start pattern2 ?!
'''
import time
from armor import pattern2
from armor.dataStreamTools import kongrey as kr
DSS = pattern2.dataStreamSet

obs     = mv.loadDataStreams(mv.defaultInput1)[0]
wrfs    = mv.loadDataStreams(mv.defaultInputs2)
'''
###############################################
import time
print time.asctime()

from armor.dataStreamTools import kongrey
from armor.dataStreamTools import makeVideo
mv = makeVideo
kr = kongrey
reload(mv) ; reload(kr) ; result = kr.pmt(kr.plain_correlation, 
            makeSmallImages=True, 
            smallDpi=40, 
            frameDpi= 400,
            loadFormerAnalysisResult=False, 
            #loadFormerAnalysisResult=True,
            #summary_folder="",              # needed if loadFormerAnalysisResult is True
            matching_algorithm_name= 'plain_correlation',     # needed if loadFormerAnalysisResult is True
            )

print time.asctime()

#reload(kr) ; result = kr.pmt(kr.plain_correlation, makeSmallImages=False, frameDpi=600)


################################
#   loop starts
timeStamp = str(int(time.time()))
kongreyDSS = DSS(obs, *wrfs)
ordering = kongreyDSS.analyse(algorithm=algorithm1)  # algorithm1 to be defined
print ordering
kongreyDSS.makeVideo1(ordering, outputFolder=mv.sandbox)
kongreyDSS.makeVideo2(ordering, outputFolder=mv.sandbox)
#   loop ends
################################

############ 18-09-2013 ######################
#   two things
#   1. make 20 videos for 2 (COMPREF: WRF N ; N=01 to 20)
#   2. make panel video for 21 ( [ CMPREF WRF01, WRF02,...])
cd /media/KINGSTON/ARMOR/python
python
from armor.dataStreamTools import makeVideo as mv
reload(mv) ; DSS=mv.main(toMakeImages=True, dpi=80)

#
cd /media/KINGSTON/ARMOR/python
python
from armor.dataStreamTools import makeVideo as mv
reload(mv) ; DSS=mv.main(toMakeImages=True, dpi=30, constructDSS=True)


############ 16-09-2013 ######################
#   continued from 13-09-2013
exit()
cd /media/KINGSTON/ARMOR/python
python


import time
import numpy as np
from armor import pattern
from armor.tests.patternMatching import kongrey
kr = kongrey

#reload(kr) ; x = kr.constructOBSstream()  ; print time.asctime()
#reload(kr) ; x2 = kr.constructAllWRFstreams() ; print time.asctime()
reload(kr) ; x3 = kr.constructAllWRFstreamsRegridded() ; print time.asctime()
#reload(kr) ; x4 = kr.createDBZimages() ; print time.asctime()
reload(kr) ; x5 = kr.createAllWRFimages(withCoast=False) ; print time.asctime()
reload(kr) ; x6 = kr.createAllWRFimages(withCoast=True, toLoad=False, folder=kr.summary_folder+'WRF[regridded]/') ; print time.asctime() # no need to reload the regridded stuff since the pointer would be wrong.




for matchingAlgorithm in [kr.plain_correlation, kr.moments, kr.regionalGlobalMoments,]:
    for Test in [kr.pmt, kr.pmt3d]: 
        reload(pattern) ; reload(kr);  R1= Test(matchingAlgorithm)





############ 13-09-2013 ######################
# today
# redo the stuff, remove the omitted regions, recompute everything
# check accuracy of the regridded maps
# 
# per weekly meeting 2013-09-12:
#Suggested fixes:
#
#  1. fix the pattern.py module to allow for data values < -20.0 ←DONE
#  2. focus on the section DBZ=20 to 70
#  3. focus on the region with radar echo
#  4. problem with spin-up [e.g. 20130828.0000 model 8]
#  5. try - using satellite data for initial selection
#  6. put all pics on a panel for comparison

exit()
cd /media/KINGSTON/ARMOR/python
python

import numpy as np
from armor import pattern
from armor.tests.patternMatching import kongrey
kr = kongrey

reload(kr) ; x = kr.constructOBSstream()
reload(kr) ; x2 = kr.constructAllWRFstreams()
reload(kr) ; x3 = kr.constructAllWRFstreamsRegridded()
##reload(kr) ; x4 = kr.createDBZimages()

reload(kr) ; x5 = kr.createAllWRFimages()
for matchingAlgorithm in [kr.plain_correlation, kr.moments, kr.regionalGlobalMoments,]:
    for Test in [kr.pmt, kr.pmt3d]: 
    reload(pattern) ; reload(kr);  R1= Test(matchingAlgorithm)





############ 11-09-2013 ######################
# today
#   0.  write up on invariant moment theory
#   1.  perform lee's test
#   2.  analyse the results

############ 12-09-2013 ######################
#   today 
#   write up

#   1. loading the test results


############ 10-09-2013 ######################
# today
# construct test moments, etc
#   construct the matching results
exit()

cd /media/KINGSTON/ARMOR/python
python

import numpy as np
from armor import pattern
from armor.tests.patternMatching import kongrey
kr = kongrey

for matchingAlgorithm in [kr.plain_correlation, kr.moments, kr.regionalGlobalMoments,]:
    reload(pattern) ; reload(kr);  R1= kr.pmt(matchingAlgorithm)
    reload(pattern) ; reload(kr);  R2= kr.pmt3d(matchingAlgorithm)



############ 29-08-2013 ######################
# today
# construct a few series test
# start with correlations

## code snippet from class armor.pattern.DBZstream :
#
    def corr(self, ds2, verbose=False):
        """
        returns a list of correlation of the streams
                  [(dataTime <str>, corr <float>),...]
        """
        # ~~~ blablabla ~~~
        for T in dataTimeList:
            a = ds1(T)[0]
            b = ds2(T)[0]
            L.append((T, a.corr(b)))
        return L
#
## code snippet ends

###############################################
#   take two - full

exit()
cd /media/k/KINGSTON/ARMOR/python
python

from armor import pattern as pt
reload(pt)
ds1=pt.ds1
ds3=pt.ds3
ds1.load('20120612.0')
ds3.load('20120612.0')
ds1.cutUnloaded()
ds3.cutUnloaded()

import time
t0 = time.time()
ds3.regrid(ds1[0])
t1 = time.time()-t0
print t1

# save
ds3.saveImages()
ds3.saveMatrices()

# compute correlations
t0 = time.time()
ds1_corr_ds3 = ds1.corr(ds3)
xx = ds1_corr_ds3
t2 = time.time()-t0
print t2

print ds1_corr_ds3
print len(ds1_corr_ds3)


ds4 = pattern.DBZstream(dataFolder=ds3.outputFolder, name='WRFregrid' )
ds4.load('20120612.02')
ds4.cutUnloaded()

for v in ds4:
    v.show2()
###############################################
#   take one
exit()
cd /media/k/KINGSTON/ARMOR/python
python

# construct the objects
from armor import pattern as pt
reload(pt)
ds1 = pt.ds1
ds3 = pt.ds3

# load the data
ds1.load('20120612.02')     # a short list for quick testing
ds3.load('20120612.02')

# cut of the unloaded sections
ds1.cutUnloaded()
ds3.cutUnloaded()

# check
ds1.list
ds3.list

# regrid ds3
import time
t0 = time.time()
ds3.regrid(ds1[0])
print "time spent in regrid:", time.time() - t0

# check
ds1[0].matrix.shape
ds3[0].matrix.shape

# test
xx = ds1.corr(ds3)

# test result
for v in xx:
    print v[0], v[1]

## and save the results             # not needed any more
# set image and data folder
#ds1.setImageFolder('../labReports/20130827/COMPREF/')
#ds3.setImageFolder('../labReports/20130827/WRF/')
#ds1.setOutputFolder('../labReports/20130827/COMPREF/')
#ds3.setOutputFolder('../labReports/20130827/WRF/')

#check
ds1[3].imagePath
ds1[3].outputPath

ds3[3].imagePath
ds3[3].outputPath

# set imageFolders
#ds1.imageFolder  = '../labReports/20130827/COMPREF/'
#ds1.outputFolder = '../labReports/20130827/COMPREF/'
#ds3.imageFolder  = '../labReports/20130827/WRF/'
#ds3.outputFolder = '../labReports/20130827/WRF/'

xxx = raw_input('press enter to continue:')

# save 
# images first - for safety
ds1.saveImages()
ds3.saveImages()

# ds1.saveMatrices()  # no need - this is original data, untransformed
ds3.saveMatrices()

# reload the saved regridded ds3 as a verification
reload(pattern)
reload(pt)
ds4 = pattern.DBZstream(dataFolder=ds3.outputFolder, name='WRFregrid' )
ds4.load()

############ 28-08-2013 ######################

exit()

cd /media/k/KINGSTON/ARMOR/python
python

import numpy as np
from armor import pattern

reload(pattern)
ds1 = pattern.ds1
ds3 = pattern.ds3

ds1.load('20120612.0', verbose=True)
ds3.load('20120612.0', verbose=True)

ds1.load('20120612.0', verbose=True)
ds3.load('201206120', verbose=True)
ds1.setImageFolder('../labReports/20130827/COMPREF/')
ds3.setImageFolder('../labReports/20130827/WRF/')
ds1.setOutputFolder('../labReports/20130827/COMPREF/')
ds3.setOutputFolder('../labReports/20130827/WRF/')


# debug
print ds1[0].imagePath
print ds1[0].outputPath
print ds3[0].imagePath
print ds3[0].outputPath
# end debug


l1 = [v.dataTime for v in ds1 if v.matrix.sum()>0]
l3 = [v.dataTime for v in ds3 if v.matrix.sum()>0]
dataTimeList = [v for v in l1 if v in l3]
print dataTimeList

from armor.geometry import regrid
for T in dataTimeList:
    print '==== ', T, ' ===='
    a = [v for v in ds1 if v.dataTime==T][0]
    b = [v for v in ds3 if v.dataTime==T][0]
    e = regrid.regrid(b, a)
    e.imagePath = b.imagePath
    e.outputPath = b.outputPath
    e.imageFolder = b.imageFolder
    e.outputFolder= b.outputFolder
    a.drawCoast()
    e.drawCoast()
    a.matrix = np.flipud(a.matrix)
    e.matrix = np.flipud(e.matrix)
    #a.show()
    #e.show()
    print 'a.imagePath:', a.imagePath
    print 'e.imagePath:', e.imagePath
    #x = raw_input('press enter:')
    a.saveImage()
    e.saveImage()

############ 27-08-2013 ######################
# home
# to do:
# 1. construct DBZstream datasets for Mr. Shue's output and COMPREF from CWB
# 2. compare them
# 3. try to understand the C programme for decoding the CWB binary datasets
# 4. i forget something i thought of during the swim today as i always do.

############ 27-08-2013 ######################
# testing regrid.py, then test algorithm

exit()
python
from armor import pattern
a=pattern.a
c=pattern.c
a.load()
c.load()
from armor.geometry import regrid
reload(regrid); e=regrid.regrid(a,c) ; f=regrid.regrid(c,a)

e.recentre()
e.drawCross().show4()
a.drawCross().show()
a.drawCross(radius=20).show2()
f.drawCross(radius=20).show2()

dbz=pattern.DBZ
import numpy as np
g = dbz(matrix=np.zeros((1800,1500)), upperRightCornerLatitudeLongitude=((35,135)))
h = regrid.regrid(a,g)
h.show()
h.recentre()
h.drawCross(radius=60).show()


############ 17-08-2013 ######################
# to do - ditto (16-08-2013)
# interpolation module - a bit messy, a bit tired.
# learn opencv today
#   /media/k/KINGSTON/OpenCV
#     OReilly Learning OpenCV.pdf 
#     opencv2refman.pdf
# watch weather videos and understand the weather pattern evolutions and the
#   correlation between wind and rain and clouds and the temperature cycle
#   ACER:  /media/k/DATA/ARMOR/videos/  


############ 16-08-2013 ######################
# to do
# 1. deformation module
# 2. interpolation module
# 3. perform matching:1
#       model:  /KINGSTON/ARMOR/data_simulation/20120611_12/
#                       20120611.1500 - 20120612.2350
#       data:   /Seagate Expansion Drive/ARMOR/data_temp/
#            or /KINGSTON/ARMOR/data_temp/
#                       20120612.0000-20120612.0940



############ 16-08-2013 ######################
# to do
# 1. deformation module
# 2. interpolation module
# 3. perform matching:1
#       model:  /KINGSTON/ARMOR/data_simulation/20120611_12/
#                       20120611.1500 - 20120612.2350
#       data:   /Seagate Expansion Drive/ARMOR/data_temp/
#            or /KINGSTON/ARMOR/data_temp/
#                       20120612.0000-20120612.0940

# makeVideo - for today
import armor.video.makeVideo as mv
reload(mv) ; mv.main(inputDate='2013-07-12', inputType='charts2')

mv.main(inputDate='2013-07-12', inputType='satellite1')
mv.main(inputDate='2013-07-12', inputType='satellite4')

############ 08-08-2013 ######################
# testing the matching algorithms proposed so far
# switching to enthought because the only operating system i have is win 8
# new codes:
# armor.basicio.dataStream   # for i/o of streams of dbz files
# armor.patternMatching.algorithmX      # each with a self-test embedded
# armor.patternMatching.algorithmTest   # running tests on the code scripts

# 1 . turn on enthought
# 2. open session 2012-08-08
# 3. run the following

cd h:/ARMOR/python/
#
from armor import pattern
from armor.basicio import dataStream as ds
x = ds.test(ds.dataFolder2)
x[1].show()

from armor.patternMatching import algorithmTest
res = algorithmTest.testResults

from armor.patternMatching import algorithm1
res = algorithm1.main()

############ 29-07-2013 ######################
folder1 = '/media/Seagate Expansion Drive/ARMOR/data/20120612_testdata/'
folder2 = '/media/Seagate Expansion Drive/ARMOR/data/20120612_testdata_pics/'
def f(folder_in, folder_out):
     L = os.listdir(folder_in)
     for filename in L:
       a = pattern.DBZ(name=filename, dataPath=folder_in+filename,
                       imagePath=folder_out+filename[:-4]+'.png')
       a.load()
       a = a.flipud()
       a.saveImage()
       print a.name,"||", 



f(folder1, folder2)


############ 22-07-2013 ######################

"""
THIS WEEK-
EXPECTED
    1.  Miss Chan 陳姿瑾 may come to meeting this tuesday?

TO DO
    1.  A basic scoring model based on data given by Miss Chan 
        a. try to retest their method
        b. do my own
    2.  develop a testing platform based on comparing machine/human judgements, incorporating criteria
        based on specifications from weather forecasters etc
    3.  Understand the moment invariants (read the papers, run the tests etc)
    4.  start a doc - documentation and report at the same time

--------
PROBLEMS:
    1.  陳姿瑾's data are in binary form.  Shue hung-yu will decode them and he will
        put them on the server.


"""




############ 19-07-2013 ######################
"""
time for reflection, picking up the pieces, and reinstalling ubuntu

1.  Yesterday we finally got some idea from Dr. 黃椿喜's mouth, on what they are really looking for (balancing the location of the storms and the precipitation over the land of Taiwan).  

2.  So we should strive towards it and work on refining such ideas, interact more and learn what they have done as well as checking if what we are doing suit their needs.  That's what the work meeting is for.

3.  Next up:  what should we do before the next work meeting?
    a)  set up some basic schemes as follows from our midterm report
    b)  do some basic tests with the data given by 陳姿瑾
    c)  understand what's going on and what these quantitative features are like 
        and how they behave
    d)  start writing a report/journal

"""


############ 18-07-2013 ######################

"""
2pm - meeting at 4th floor, CWB
"""
############ 16-07-2013 ######################
"""
*   continued from yesterday 15-07-2013:
    a single SHIIBA regression may still suffer from defects.
    so should we use a single TREC instead??    
"""

############ 15-07-2013 ######################
"""
TO-DO
** from before **
(A) continue / finish the transformed correlation test
(B) continue the texture analysis, perferrably clarify stuff before the 
    next meeting on Tuesday

** new idea **
(C) clustering with flow direction (from shiiba) as new feature
"""
# -  can't use global shiiba for simplcity because the vector field would be linear 
#    so clustering is simply based on distance
# -  algorithm: 1. shiiba advection  ; 
#               2. threshold at 30 or 35 and find the centroids for the 20 connected components
#               3. k-means clustering with location, intensity and shiiba velocity field (u,v) as features 
#                  after normalisation by dividing by the variances


from armor import pattern
dbz = pattern.DBZ
a   = pattern.a
b   = pattern.b
#   1. shiiba advection  ; 
shiiba_result   = a.shiibaLocal(b)
vect            = shiiba_result['vect']
mn              = shiiba_result['mn']
#  <--- from here, vect.U and vect.V, each being an 881x921 array, is one feature layer.


#   2. threshold at 30 or 35 and find the centroids for the 20 connected components


from armor.geometry import components
phi = (a.matrix.filled()<35)
phiComponents = components.connected(phi)
#PHI         = dbz(name="0200threshold35", matrix=phiComponents, vmin=-5, vmax=10, cmap="prism")
#PHI.copy().show2()

import numpy as np
import matplotlib.pyplot as plt
plt.imshow(np.flipud(phiComponents))
plt.show()

#   3. k-means clustering with location, intensity and shiiba velocity field (u,v) as features 
#      after normalisation by dividing by the variances
"""2013-07-16"""




#   4. output the result










############ 12-07-2013 ######################
"""
to do
(A) continue / finish the transformed correlation test
(B) continue the texture analysis, perferrably clarify stuff before the 
    next meeting on Tuesday
    
"""

############ 10-07-2013 ######################
"""
(A) organising powerpoint into document -> Liu Cheng Sin
(B) Testing Prof Lee's stuff -> now

Plan
1.  Define the functions (two double gaussians)
2.  Compute the centroids
3.  Compute the moment of inertia matrix
4.  Compute the major and minor axes
5.  Transform
6.  Interpolate
7.  Compute correlation

"""
cd /media/KINGSTON/ARMOR/python
python

from armor.tests import transformedCorrelationTest as test
x = test.main()


######### WEEK OF 24-06-2013 #################
"""
(A) THIS WEEK:
1. weather bureau meeting tuesday
2. other stuff

(B) TO-DO this week:
1. testing  -moments

2. writing  - ppt

(C) TO-DO from previous weeks:
1. speed up/reduce memory use:  morphology operations (dilation/erosion)
2. finish implementing texture segmentation
3. write ppt presentation
"""
############ 28-06-2013 ######################

"""
1.  Liu Yu Ming from CWB is visiting our work meeting (next week? tuesday?)
2.  Two things to do by next week: (a) finish up the moments test and write it up and (b) write prof lee's adjusted correlation test.
    question:  do we really need the transformation and interpolation of images?

3.  actuarial homework!!!
"""

# prof lee's adjusted correlation test.
"""
step 1:  compute the centroids, and axes
step 2:  transform the NWP data to RADAR data linearly
step 3:  calculate the correlation
step 4:  set the threshold and estimate the f1 score
"""

from armor.tests import lee20130628.py as test
x= test.main()



############ 21-06-2013 ######################


######### WEEK OF 17-06-2013 #################
"""
to do this week:
1. speed up/reduce memory use:  morphology operations (dilation/erosion)
2. finish implementing texture segmentation
3. write ppt presentation
"""
############ 21-06-2013 ######################
# 1. simulation
# 2. write up

cd /media/Seagate\ Expansion\ Drive/ARMOR/python
python

##########
# edit parameters here
k = 18
#x_factor, y_factor, intensity_factor = 0.05, 0.05, 10    
x_factor, y_factor, intensity_factor = 0.01, 0.01, 1
scales=[1, 2,4,8,]
NumberOfOrientations = 8
#
###########

import time
time_overall = time.time()

import numpy as np
from armor.texture import analysis
from armor import pattern
dbz = pattern.DBZ
from armor.tests import nwp
a = nwp.loadNWP('201206120200')
#a.show
print a.matrix.shape

reload(analysis)
#analysis_return_value = analysis.main(a=a,k=k, scales=[1, 2,4,8,16,32,64], doSegmentation=False)
analysis_return_value = analysis.main(a=a,k=k, scales=scales,NumberOfOrientations =NumberOfOrientations,
                                      doSegmentation=False)
#analysis_return_value = analysis.main(a=b)

"""    return_value = {'texturelayer': texturelayer, 
                    'segmentation': segmentation,
                    'timestamp'   : timestamp,
                    'clust'       : clust,
                    'a'           : a,}

"""
x = analysis_return_value

timestamp = x['timestamp']
texturelayer = x['texturelayer']
segmentation = x['segmentation']
clust= x['clust']
a = x['a']

featureFolder='armor/texture/%d/gaborFeatures/'%timestamp

# then copy and paste from armor/tests/textureclustering.py 
#  line 19   params = (x_factor, y_factor, intensity_factor)  to
#  just before line 100      "a very slow process"

print time.time()-time_overall

############ 20-06-2013 ######################
# stuff to do by tomorrow: 
# tests for sit hung yue's data
# write up
# powerpoint
"""ARMOR:  影象分析（Image processing）與氣象系統追逐與移動預測
-各種算法評估

2013-06-06
簡介 (2013-06-20)
2013上半年，我們初步測試了。。。方法
得到。。。經驗
打算。。。（以後如何做）
希望得到。。。資料
"""


############ 19-06-2013 ######################

cd /media/Seagate\ Expansion\ Drive/ARMOR/python
python

k = 30
x_factor, y_factor, intensity_factor = 0.05, 0.05, 10    

import numpy as np
import time
#time.sleep(12000)
time_overall = time.time()
from armor.texture import analysis
from armor import pattern

dbz = pattern.DBZ
a=pattern.a
b=pattern.b
reload(analysis)
analysis_return_value = analysis.main(a=b,k=k, scales=[2,4,8,16,32,64], doSegmentation=False)
#analysis_return_value = analysis.main(a=b)

"""    return_value = {'texturelayer': texturelayer, 
                    'segmentation': segmentation,
                    'timestamp'   : timestamp,
                    'clust'       : clust,
                    'a'           : a,}

"""
x = analysis_return_value

timestamp = x['timestamp']
texturelayer = x['texturelayer']
segmentation = x['segmentation']
clust= x['clust']
a = x['a']

featureFolder='armor/texture/%d/gaborFeatures/'%timestamp

# then copy and paste from armor/tests/textureclustering.py 
#  line 19   params = (x_factor, y_factor, intensity_factor)  to the end

print time.time()-time_overall

############ 17-06-2013 ######################
# the stuff below moved to textureclustering.py
# just cut and paste again

############ 17-06-2013 ######################
>>> len(clust)
2
>>> len(clust[1])
811401
>>> a
<armor.pattern.DBZ object at 0x2bc3310>
>>> dbz
<class 'armor.pattern.DBZ'>
>>> CLUST=dbz(matrix=clust[1].reshape((881,921)))
>>> CLUST.show()
>>> CLUST.cmap
'hsv'
>>> params
(1, 1, 500)
>>> k
144
CLUST.name = "k=144, x,y,intensity multiplication factors = 1,1,4"
CLUST.show4()
CLUST.imagePath='/media/Seagate Expansion Drive/ARMOR/python/armor/texture/1370506584/textureLayers144_1_1_4/texturelayers_hsv_2.png'
CLUST.saveImage()
CLUST.flipud().saveImage()

a
a.imagePath='/media/Seagate Expansion Drive/ARMOR/python/armor/a.png'>>> a.imagePath='/media/Seagate Expansion Drive/ARMOR/python/armor/0200.png'
a.flipud().saveImage()

############ 17-06-2013 ######################
""" cut and paste Seagate Extension Drive: python : armor: tests: textureclustering.py
testing various combinations of params = (x_factor, y_factor, intensity_factor)
results in folder 'armor/texture/1370506584/textureLayers%d_%d_%d_%d/' % ((k,)+params)
"""
######### WEEK OF 10-6-2013 ##################


#

######### WEEK OF 10-6-2013 ##################
"""
to do this week:
1. speed up/reduce memory use:  morphology operations (dilation/erosion)
2. finish implementing texture segmentation
3. write ppt presentation
"""
############ 14-06-2013 ############################################
###   First Task: 1. load the data ; 2. append the space-time coordinates ; 3 cluster
##
#
cd /media/Seagate\ Expansion\ Drive/ARMOR/python/
python
from armor import pattern
dbz=pattern.DBZ
import pickle
import time
import numpy as np
from armor.texture import analysis
t0=time.time()
a =  pattern.a
featureFolder='armor/texture/1370506584/gaborFeatures/'
reload(analysis)
data = analysis.load(folder=featureFolder)

data.shape
height,width,depth = data.shape

X,Y = np.meshgrid(range(width), range(height))

data= data.reshape(height*width, depth)
X   = X.reshape(height*width)
Y   = Y.reshape(height*width)
Z   = a.matrix.filled().reshape(height*width)

XYZ = np.vstack([X,Y, Z]).T
data3 = np.hstack([data,XYZ])

del XYZ
del X
del Y
del Z

height3=height
width3=width
depth3 = depth+3
data3=data3.reshape(height3,width3,depth3)

data3.shape
k = 72
textureFolder = 'armor/texture/1370506584/textureLayerswithtimeandintensity72/'
textureThickFolder = 'armor/texture/1370506584/textureLayerswithtimeandintensity72thick/'
clust, texturelayer = analysis.computeClustering(data=data3, k=k, textureFolder=textureFolder)
segmentation = analysis.computeSegmentation(clust=clust, outputFolder=textureThickFolder)

print 'time used:', time.time()-t0

# pickle it
pickle.dump({'a':a, 'clust':clust,  #'texturelayer':texturelayer, 'data':data, 
                'segmentation':segmentation, 'timeused': 6724.52}, 
               open(textureFolder+'dataclustsegmentationetc.pydump','w'))

# output to screen

for i in range(k):
    print i
    if (texturelayer[i]*(1-a.matrix.mask)).sum() < 50: continue
    dbz(matrix=texturelayer[i],vmin=-2, vmax=1).show()

#
##
### First Task End ########################################################


############ 13-06-2013 ############################################

"""Note: meeting tomorrow.  Have PPT ready
today:  write up algorithms and do a few test cases.

# Three ideas to complete the story:
# 1.  introduce location (x,y coords) as features as suggested by Liu Cheng Shin
#       as well as intensity, a total of three new feature dimensions
# 2.  introduce time into the picture, with 10 minutes separation as a unit,
#       another feature dimension, the idea being that we have space-time clusters
#       of coherent textures.  
# 3.  Those with strong intensities and time-persistence
#       should be physical features

"""
# plan:
#   two tasks
#   First Task: 1. load the data ; 2. append the space-time coordinates ; 3 cluster
#   Second Task:  Create feature vectors for three more time points

###   Second Task:  Create feature vectors for three more time points ####
##  do this first - it takes longer
#
cd /media/Seagate\ Expansion\ Drive/ARMOR/python/
python
from armor import pattern
dbz=pattern.DBZ
import time
import numpy as np
from armor.texture import analysis

reload(analysis)
img = dbz('20120612.0210')
img.load()
img.show4()
del img

for t in ["20120612.0210", "20120612.0220", "20120612.0230", "20120612.0240"]:
    img = dbz(dataTime=t)
    try:
        x = analysis.main()
    except:
        print "error! - dataTime", t
#
##
###   Second Task End #####################################################

###   First Task: 1. load the data ; 2. append the space-time coordinates ; 3 cluster
##
#
cd /media/Seagate\ Expansion\ Drive/ARMOR/python/
python
from armor import pattern
dbz=pattern.DBZ
import time
import numpy as np
from armor.texture import analysis

featureFolder='armor/texture/1370506584/gaborFeatures/'
reload(analysis)
data = analysis.load(folder=featureFolder)

data.shape
height,width,depth = data.shape

X,Y = np.meshgrid(range(width), range(height))

data= data.reshape(height*width, depth)
X   = X.reshape(height*width)
Y   = Y.reshape(height*width)

XY = np.vstack([X,Y]).T
data2 = np.hstack([data,XY])

del XY
del X
del Y

height2=height
width2=width
depth2 = depth+2
data2=data2.reshape(height2,width2,depth2)

data2.shape
k = 72
textureFolder = 'armor/texture/1370506584/textureLayerswithtime72/'
textureThickFolder = 'armor/texture/1370506584/textureLayerswithtime72thick/'
clust, texturelayer = analysis.computeClustering(data=data2, k=k, textureFolder=textureFolder)
segmentation = analysis.computeSegmentation(clust=clust, outputFolder=textureThickFolder)

"""
import pickle
from armor import pattern
a=pattern.a
textureFolder = 'armor/texture/1370506584/textureLayerswithtime72/'
pickle.dump({'a':a, 'clust':clust,  #'texturelayer':texturelayer, 'data':data, 
                'segmentation':segmentation, 'timeused': 6724.52}, 
               open(textureFolder+'dataclustsegmentationetc.pydump','w'))

"""


#
##
### First Task End ########################################################



############ 11-06-2013 ############################################


cd /media/Seagate\ Expansion\ Drive/ARMOR/python/
python

import numpy as np
import os
from armor import pattern
from armor.texture import analysis
dbz = pattern.DBZ
import time

testpath = '/media/Seagate Expansion Drive/ARMOR/python/armor/texture/1370506584/'
x  = analysis.load(testpath+'gaborFeatures/')

height, widht, depth = x.shape


#imagesum = x.sum(axis=2)

imagesum= np.zeros((881,921))
for i in range(depth):
    imagesum+=x[:,:,i] * 2**(3-i//10)

vmax=500
IMGSUM = dbz(matrix=imagesum, name="sum of 36 texture layers dilated, with weights 2**(3-i/10), vmax=%d" %vmax, vmax=vmax, imagePath = testpath + 'texturelayersum2-vmax%d.png'%vmax)
IMGSUM.show4()

IMGSUM.flipud().saveImage()



############ 10-06-2013 ############################################
###
## try run - full process again
#
cd /media/Seagate\ Expansion\ Drive/ARMOR/python/
python

import numpy as np
import os
from armor import pattern
from armor.texture import analysis
dbz = pattern.DBZ
import time

x = analysis.main(scales=[1,2,4,8,16,32,64,128], NumberOfOrientations = 8, memoryProblem=True)

# the above - 
#   may or may not work!  may have cholesky decomposition problem!!

matched3 = x['segmentation']['matchedlayers3']
matched1 = x['segmentation']['matchedlayers1']
matched2 = x['segmentation']['matchedlayers2']

texturelayer = x['texturelayer']
k = len(x['texturelayer'])

timestamp = x['timestamp']
outputFolder='armor/texture/%d/pictures/' %timestamp
os.makedirs(outputFolder)
usedlayer=[]
for i in range( k):    
    if i in usedlayer:
        continue
    print i
    usedlayer.append(i)
    #######
    ### 0.7
    listofmatchedtextures = [v[1] for v in matched3 if v[0]==i]
    print '\nlistofmatchedtextures at 0.7 correlation for i=', i, ':', listofmatchedtextures
    ### 0.3
    #listofmatchedtextures = [v[1] for v in matched1 if v[0]==i]
    #print '\nlistofmatchedtextures at 0.3 correlation for i=', i, ':', listofmatchedtextures
    ### 0.5
    #listofmatchedtextures = [v[1] for v in matched2 if v[0]==i]
    #print '\nlistofmatchedtextures at 0.5 correlation for i=', i, ':', listofmatchedtextures
    #######
    usedlayer.extend(listofmatchedtextures)
    combinedtexturelayer = texturelayer[i].copy()
    for j in listofmatchedtextures:
        print j, '|',
        combinedtexturelayer += texturelayer[j]
    print 'combinedtexturelayer[100:-100, 100:-100].sum():', combinedtexturelayer[100:-100, 100:-100].sum()
    if combinedtexturelayer[100:-100, 100:-100].sum()<50:
        continue
    img = dbz(name = 'Texture layers ' + str(i) + ' '.join([str(v) for v in listofmatchedtextures]),
              matrix=combinedtexturelayer, vmax=10, vmin=-10, 
              imagePath= outputFolder+'combined_textures'+ str(i)+'.png')
    #img.show2()
    img.matrix= np.flipud(img.matrix)
    img.saveImage()

#
##   end - try run full process
###
#####################################################################




######### END WEEK OF 10-6-2013 ##################
######## 6-6-2013 over night ###########
import time
from armor.texture import analysis
from armor import pattern
dbz = pattern.DBZ

x = analysis.main(scales=[1,2,4,8,16,32,64,128], NumberOfOrientations = 6, memoryProblem=True)
matched3 = x['segmentation']['matchedlayers3']
matched1 = x['segmentation']['matchedlayers1']
matched2 = x['segmentation']['matchedlayers2']
texturelayer = x['texturelayer']
k = len(x['texturelayer'])

import numpy as np
import os
timestamp = 1370506584
outputFolder='armor/texture/%d/pictures/' %timestamp
os.makedirs(outputFolder)
usedlayer=[]
for i in range( k):    
    if i in usedlayer:
        continue
    print i
    usedlayer.append(i)
    #######
    ### 0.7
    listofmatchedtextures = [v[1] for v in matched3 if v[0]==i]
    print '\nlistofmatchedtextures at 0.7 correlation for i=', i, ':', listofmatchedtextures
    ### 0.3
    #listofmatchedtextures = [v[1] for v in matched1 if v[0]==i]
    #print '\nlistofmatchedtextures at 0.3 correlation for i=', i, ':', listofmatchedtextures
    ### 0.5
    #listofmatchedtextures = [v[1] for v in matched2 if v[0]==i]
    #print '\nlistofmatchedtextures at 0.5 correlation for i=', i, ':', listofmatchedtextures
    #######
    usedlayer.extend(listofmatchedtextures)
    combinedtexturelayer = texturelayer[i].copy()
    for j in listofmatchedtextures:
        print j, '|',
        combinedtexturelayer += texturelayer[j]
    print 'combinedtexturelayer[100:-100, 100:-100].sum():', combinedtexturelayer[100:-100, 100:-100].sum()
    if combinedtexturelayer[100:-100, 100:-100].sum()<50:
        continue
    img = dbz(name = 'Texture layers ' + str(i) + ' '.join([str(v) for v in listofmatchedtextures]),
              matrix=combinedtexturelayer, vmax=10, vmin=-10, 
              imagePath= outputFolder+'combined_textures'+ str(i)+'.png')
    #img.show2()
    img.matrix= np.flipud(img.matrix)
    img.saveImage()



######## 6-6-2013 ###########
cd /media/Seagate\ Expansion\ Drive/ARMOR/python/
python


from armor import pattern
from armor.texture import analysis
dbz = pattern.DBZ

reload(analysis); x = analysis.main(scales=[4,8,16,32], NumberOfOrientations = 6, memoryProblem=True)
pickle.dump(x, open('/media/Seagate Expansion Drive/ARMOR/python/armor/texture/1370491948/matchedlayers.pydump','w'))

matched3 = x['segmentation']['matchedlayers3']
matched1= x['segmentation']['matchedlayers1']
matched2= x['segmentation']['matchedlayers2']
texturelayer = x['texturelayer']

[v[1] for v in matched if v[0]==0]

k = len(x['texturelayer'])

for i in range(k):
    dbz(matrix=texturelayer[i], vmax=5, vmin=-5).show4()

for i in range( k):    
    #listofmatchedtextures = [v[1] for v in matched3 if v[0]==i]
    #print '\nlistofmatchedtextures at 0.8 correlation for i=', i, ':', listofmatchedtextures
    #listofmatchedtextures = [v[1] for v in matched1 if v[0]==i]
    #print '\nlistofmatchedtextures at 0.5 correlation for i=', i, ':', listofmatchedtextures
    listofmatchedtextures = [v[1] for v in matched2 if v[0]==i]
    print '\nlistofmatchedtextures at 0.6 correlation for i=', i, ':', listofmatchedtextures
    combinedtexturelayer = texturelayer[i].copy()
    for j in listofmatchedtextures:
        print j, '|',
        combinedtexturelayer += texturelayer[j]
    print 'combinedtexturelayer[100:-100, 100:-100].sum():', combinedtexturelayer[100:-100, 100:-100].sum()
    if combinedtexturelayer[100:-100, 100:-100].sum()<50:
        continue
    dbz(matrix=combinedtexturelayer, vmax=10, vmin=-10).show4()



######  4-6-2013 ###########
# contiued from 3-6-2013

"""
to do:
1.  segmentation by texture
2.  anomalous propagation

1.  gabor filter bank -> clustering -> texture layers -> thicken each
    -> find intersection regions -> plot

2.  what kind of filter/spectral analysis tool should we use?
"""
#  1.  segmentation by texture
#  gabor filter bank -> clustering -> texture layers -> thicken each
#    -> find intersection regions -> plot
"""
plan:
    a. load the filter bank data
    b. check the data
    c. cluster the data -> texture layers
    d. check
    e. thickening (with a tunable neighbourhood/scale/dilation mask)
    f. segment via intersections of various texture layers
"""
#    a. load the filter bank data
#    b. check the data
#    c. cluster the data -> texture layers
#-------------------------------------------

# redo, removing the unwanted empty/edge layers

os.makedirs('armor/texture/k_'+str(k))
#pickle.dump({'content':texturelayer, 'notes':"%d texture layers from 'armor/filter/gaborFilterVectorField.pydump' " %k}, open('armor/texture/k_'+ str(k)+'/texturelayer.pydump','w'))


# initialising the texture layer array
texturelayer= []
for i in range(k):
    thislayer = (clust[1]==i).reshape(881,921)
    print i, '\tall / interior sums:',
    print thislayer.sum(), thislayer[20:-20,20:-20].sum()
    if thislayer[20:-20,20:-20].sum() <100:       # only layer 53 is missing. should be ok
        continue
    texturelayer.append( thislayer )
    #plt.imshow(cluster[i])
    #plt.show()
    # only those with values away from the border
    pic = dbz(  name='texture layer'+str(i),
              matrix= np.flipud(thislayer), vmin=-2, vmax=1,
           imagePath='/media/KINGSTON/ARMOR/python/armor/texture/k_' + \
                     str(k) + '/texturelayer'+ str(i) + '.png')
    #pic.show()
    pic.saveImage()

########
#    d. check
########
#    e. thickening (with a tunable neighbourhood/scale/dilation mask)

from armor.geometry import morphology as morph
disc = morph.disc
dilate = morph.dilate

plt.imshow(texturelayer[20])
plt.show()

outputFolder = '/media/Seagate Expansion Drive/ARMOR/python/armor/texture/k_80_thick/'
os.makedirs(outputFolder)
t0=time.time()

texturelayer_thick = []
for i in range(k):
    thislayer = (clust[1]==i).reshape(881,921)
    print i, '\tall / interior sums:',
    print thislayer.sum(), thislayer[20:-20,20:-20].sum()
    #if thislayer[50:-50,50:-50].sum() < 40:       # only layer 53 is missing. should be ok
    #    continue
    #if thislayer.sum() < 3000:                    # an arbitrary threshold, first consider the bigger ones
    #    continue                   
    layer_thick = dilate(M=thislayer, neighbourhood = disc(3))  ## <--- dilation with disc of radius 3
    texturelayer_thick.append( layer_thick )
    #plt.imshow(cluster[i])
    #plt.show()
    # only those with values away from the border
    pic = dbz(  name='texture layer %d thicked' %i,
              matrix= np.flipud(layer_thick), vmin=-2, vmax=1,
           imagePath= outputFolder+ '/texturelayer_thick'+ str(i) + '.png')
    #pic.show()
    pic.saveImage()
    

print 'time spent:', time.time()-t0

pickle.dump({'content':texturelayer, 'notes':"%d texture layers from 'armor/filter/gaborFilterVectorField.pydump' " %k}, open(outputFolder+'/texturelayer_thick.pydump','w'))

########
#    f. segment via intersections of various texture layers
#   i. compute correlations between layers with thickened texture layers
#   ii. grouping


###
# fixing the index problem (if ever needed)
texturelayer2thick_dict={}
count =-1
for i in range(k):
    thislayer = (clust[1]==i).reshape(881,921)
    print i, '\tall / interior sums:',
    print thislayer.sum(), thislayer[20:-20,20:-20].sum()
    if thislayer[20:-20,20:-20].sum() <100:       # only layer 53 is missing. should be ok
        continue
    if thislayer.sum() < 3000:                    # an arbitrary threshold, first consider the bigger ones
        continue                   
    count+=1
    texturelayer2thick_dict[i] = count



#######
# computing the correlations of thickened textures      
import numpy.ma as ma
D= texturelayer2thick_dict
corr_matrix = ma.ones((k,k)) * (-999.)
corr_matrix.mask = True
corr_matrix.fill_value=-999.

for i in range(len(texturelayer)):
    print "\n"
    if i not in D.keys():
        print '||            ',
        continue
    for j in range(len(texturelayer)):
        if j not in D.keys():
            continue
        layer1 = texturelayer_thick[D[i]]
        layer2 = texturelayer_thick[D[j]]
        corr_matrix[i,j] = (layer1*layer2).sum() / (layer1.sum() * layer2.sum())**.5
        print '||', i,',', j,',', corr_matrix[i,j],


###########
# grouping

matchedlayers1 =[]
matchedlayers2 =[]
matchedlayers3 =[]
for i in range(k):
    for j in range(k):
        if i==j:
            continue
        if corr_matrix[i,j]>0.3:
            matchedlayers1.append((i,j))
        if corr_matrix[i,j]>0.5:
            matchedlayers2.append((i,j))
        if corr_matrix[i,j]>0.6:
            matchedlayers3.append((i,j))


print matchedlayers1
print matchedlayers2
print matchedlayers3

combinedtextureregions={}
matchedlayers= matchedlayers1 #choosing one of the above
for L in set(v[0] for v in matchedlayers):
    L_partners = [v[1] for v in matchedlayers if v[0] == L]
    tt = texturelayer[L]
    print L, L_partners
    for j in L_partners:
        tt += texturelayer[j]
    combinedtextureregions[L] = tt
    plt.imshow(tt)
    plt.show()


#################################################################
# 3-6-2013

"""
to do:
1.  segmentation by texture
2.  anomalous propagation

1.  gabor filter bank -> clustering -> texture layers -> thicken each
    -> find intersection regions -> plot

2.  what kind of filter/spectral analysis tool should we use?
"""

#######
#  1.  segmentation by texture
#  gabor filter bank -> clustering -> texture layers -> thicken each
#    -> find intersection regions -> plot
"""
plan:
    a. load the filter bank data
    b. check the data
    c. cluster the data -> texture layers
    d. check
    e. thickening (with a tunable neighbourhood/scale/dilation mask)
    f. segment via intersections of various texture layers
"""
#    a. load the filter bank data
#    b. check the data
#    c. cluster the data -> texture layers

############
# load data
import time
t0 = time.time()
import pickle
d = pickle.load(open('armor/filter/gaborFilterVectorField.pydump','r'))

timespent = time.time()-t0; print "time spent:",timespent

##############
# set up

t0 = time.time()
import os
import numpy as np
from armor import pattern
import matplotlib.pyplot as plt
dbz=pattern.DBZ
from scipy.cluster.vq import kmeans2
import pickle

#############
# run

data = d['content'].copy()
data = data.reshape(881*921, 20)
#k=25
#k=40
#k=60
k    = 80           ### <--------- change here ###########################
clust = kmeans2(data=data[:,1::2], k=k, iter=10, thresh=1e-05,\
                 minit='random', missing='warn')

os.makedirs('/media/KINGSTON/ARMOR/python/armor/texture/k_' + str(k))
texturelayer= []
for i in range(k):
    print i
    texturelayer.append( (clust[1]==i).reshape(881,921) )
    #plt.imshow(cluster[i])
    #plt.show()
    if texturelayer[i].sum()==0:
        continue
    pic = dbz(  name='texture layer'+str(i),
              matrix= np.flipud(texturelayer[i]), vmin=-2, vmax=1,
           imagePath='/media/KINGSTON/ARMOR/python/armor/texture/k_' + \
                     str(k) + '/texturelayer'+ str(i) + '.png')
    #pic.show()
    pic.saveImage()

timespent= time.time()-t0;  print "time spent:",timespent

os.makedirs('armor/texture/k_'+str(k))
pickle.dump({'content':texturelayer, 'notes':"%d texture layers from 'armor/filter/gaborFilterVectorField.pydump' " %k}, open('armor/texture/k_'+ str(k)+'/texturelayer.pydump','w'))


#    d. check

#    e. thickening (with a tunable neighbourhood/scale/dilation mask)
#    f. segment via intersections of various texture layers




######################################################################
# 30-5-2013
"""
to do

1.  understand RADAR + anomalous propagations (anoprops)
2.  understand features and stuff, and scales thereof
3.  study the use of features in removing anoprops
4.  segmentation via textures:  image -> feature layers -> feature clusters -> translate back to texture layers
                                                                     (e.g.) -> dilate -> take intersections
                                                                            => texture segmentation
                                                                            then use texture segmentation as an input
                                                                            for regional segmentation
5.  get a better/finer feature extraction sample
"""
#############
"""
filter info:
    a.matrix.fill_value = -20.
    img = a.matrix.filled()
    import numpy as np
    from armor.filter import gabor
    sigma   = 20
    scales  = [1, 2, 4, 8, 16]
    NumberOfOrientations = 12
"""
cd /media/KINGSTON/ARMOR/python

cd /media/Seagate\ Expansion\ Drive/ARMOR/python
python

from armor import pattern
a=pattern.a
from armor.filter import gabor
#fvf  = gabor.main(a)
#fvf = gabor.main(a,scales  = [4, 8, 32, 64], NumberOfOrientations = 6,  memoryProblem=False)
#fvf = gabor.main(a,scales  = [4, 8, 32, 64], NumberOfOrientations = 6,  memoryProblem=True)

def dummyfunction():
    fvf = gabor.main(a,scales  = [16, 32, 64, 128], NumberOfOrientations = 8,  memoryProblem=True)
    fvf = gabor.main(a,scales  = [256, 512], NumberOfOrientations = 8,  memoryProblem=True)
    fvf = gabor.main(a,scales  = [1, 2, 4, 8], NumberOfOrientations = 6,  memoryProblem=True)
    fvf = gabor.main(a,scales  = [16, 32, 64, 128], NumberOfOrientations = 6,  memoryProblem=True)
    fvf = gabor.main(a,scales  = [256, 512], NumberOfOrientations = 6,  memoryProblem=True)


fvf = gabor.main(a,scales  = [1, 2, 4, 8], NumberOfOrientations = 8,  memoryProblem=True)

#################################
# 30-5-2013
"""
to do
...

4.  segmentation via textures:  image -> feature layers -> feature clusters -> translate back to texture layers
                                                                     (e.g.) -> dilate -> take intersections
                                                                            => texture segmentation
                                                                            then use texture segmentation as an input
                                                                            for regional segmentation
"""

##################################
# 28-05-2013 
# try more sophisticated method
# make more clusters and group them spatially as in
# [1, p.7]
# [1] Contour and Texture Analysis for Image Segmentation
#     /media/KINGSTON/ARMOR/References/imagesegmentation/
#   https://mail.google.com/mail/u/0/?shva=1#search/thlee%40ntu.edu.tw+feature+extraction/13e5993eeb54c83a

28-05-2013

"""
cd /media/KINGSTON/ARMOR/python
python

"""
############
# load data
import time
t0 = time.time()
import pickle
d = pickle.load(open('armor/filter/gaborFilterVectorField.pydump','r'))

timespent = time.time()-t0; print "time spent:",timespent

##############
# set up

t0 = time.time()
import os
import numpy as np
from armor import pattern
import matplotlib.pyplot as plt
dbz=pattern.DBZ
from scipy.cluster.vq import kmeans2

#############
# run

data = d['content'].copy()
data = data.reshape(881*921, 20)
#k=25
#k=40
#k=60
k    = 80           ### <--------- change here ###########################
clust = kmeans2(data=data[:,1::2], k=k, iter=10, thresh=1e-05,\
                 minit='random', missing='warn')

os.makedirs('/media/KINGSTON/ARMOR/python/armor/filter/k_' + str(k))
texturelayer= []
for i in range(k):
    print i
    texturelayer.append( (clust[1]==i).reshape(881,921) )
    #plt.imshow(cluster[i])
    #plt.show()
    if texturelayer[i].sum()==0:
        continue
    pic = dbz(  name='texture layer'+str(i),
              matrix= np.flipud(texturelayer[i]), vmin=-2, vmax=1,
           imagePath='/media/KINGSTON/ARMOR/python/armor/filter/k_' + \
                     str(k) + '/texturelayer'+ str(i) + '.png')
    #pic.show()
    pic.saveImage()

timespent= time.time()-t0;  print "time spent:",timespent
 
#####################################
# pre 26-5-2013 stuff lost but ok
# now working on pattern recognition

#  today - texture analysis and pattern recognition
27-5-2013

# problem:  /media/KINGSTON/media/ARMOR/python/armor/filter/a-gaborfiltered-clustered.jpg   - the boundary is too strong that it obliterates all the find texture differences

# possible solution  - find out the boundary and then smooth it out first??

# or, do the multi-channel stuff?

"""

cd /media/KINGSTON/ARMOR/python
python


"""


import pickle
d = pickle.load(open('armor/filter/gaborFilterVectorField.pydump','r'))

import numpy as np
from armor import pattern
dbz=pattern.DBZ

dbz(matrix=fvf[:,:,0]).show4()

for i in range(20):
  print i
  pic = dbz(matrix=np.flipud(fvf[:,:,i]), vmin=-5, vmax=5,
            imagePath='/media/KINGSTON/ARMOR/python/armor/filter/gabor'+\
                      str(i) + '.png')
  pic.saveImage()







