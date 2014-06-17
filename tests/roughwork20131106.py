# -*- coding: utf-8 -*-
#   rough works - runnable and importable scripts from 2013-11-06
################################################################################
"""
USE
    from armor.tests import roughwork as rw
    reload(rw) ; from armor.tests.roughwork import *
    # then run your tests

THIS SET OF TESTS:
    towards the final report 2013

"""

################################################################################
#   imports and settings
import time, os, sys, pickle
import numpy as np
import numpy.ma as ma
from armor import pattern
dbz = pattern.DBZ
from armor.geometry import transforms as tr

from armor.geometry import frames
from armor.objects3 import kongrey     # the data 
from armor.objects3 import kongreywrf2  # the models

timeString = str(int(time.time()))
outputFolder = '/home/k/ARMOR/documents/2013-final-report/' 
################################################################################
#
#   2013-11-06
#   to carry out the tests as agreed last week

"""

Conclusion
    We have described the Laplacian of Gaussian filter and applied it to our images.  
    We looked at the features it provides us in varying sigma's and thus information 
    in varying scales.  We can use these features as tools to compare our (heterogeneous) images,
    either by comparing them directly (after suitable normalisations) or by computing certain statistics with them.

    Here is a proposal for a human-machine matching process. (1 November 2013)
        1.      Assume for the moment we have no boundary problems (which would require 
            a more careful use of finer scale features).  We are given a set of RADAR 
            data (with 10-minute intervals) and Model outputs from the Central Weather Bureau 
            (with 3-hour intervals).  We filter our the given images with a LoG kernal with large sigma 
            (large scale), and then pick out the best 8 matches for the RADAR out of a pool of 20 Models 
            with time + or - 6 hours which gives a total of 100 candidates.
        2.      We study the relationships between the intensity thresholds and shape volumes.
            We also have our own WRF simulations (ask Mr. Shue Hung Yu).  In a sense the Level 4 
            simulation outputs are similar to our RADAR data and the Level 3 simulation outputs 
            are similar to the Model outputs from the Central Weather Bureau.
        3.      In picking the 8 best matches in (1), consider the effect of various 
            stages of normalisation, or the utilisation of successively finer scales.
        4.      We tabulate the results in a 3-by-3 grid, with the RADAR data in the centre.
        5.      We include also the centroids of the patterns under time-translations forward and backward. 

"""

def construct3by3(listOfDBZs, showCoast=True, 
                  plotCentroidTrajectory=True,  #   this parameter and below added 2013-11-18
                  DBZstream="",
                  verbose=False,
                  ):                #   
    """   set the 0th in the middle, with 1-8 around it """
    from armor.geometry.frames import setSideBySide, setUpDown
    L = listOfDBZs  #alias
    #print [type(v) for v in L]  #debug
    #time.sleep(3)               #debug
    #L = [v for v in L if isinstance(v, dbz)]
    for im in L:
        if not isinstance(im.matrix, np.ma.MaskedArray):
            im.matrix = np.ma.array(im.matrix)
        im.load()
        im.setThreshold(0)
        if plotCentroidTrajectory:
             im.matrix= im.shortTermTrajectory(hours=6, timeInterval=3, radius=40, verbose=verbose, drawCoast=showCoast).matrix
        im.drawFrame(intensity=9999)
        #im.show()
        #im.showWithCoast(intensity=68)
        #if showCoast:
        #    im.drawCoast(intensity=9999)
        #im.show()

    #debug
    #print L
    #print L.name
    #print '\n'.join([v.name for v in L])
    #time.sleep(1)
    #print "shapes for L[5], L[0], L[6]:", L[5].matrix.shape, L[0].matrix.shape, L[6].matrix.shape
    #debug end
    if len(L) < 9:
        for i in range(9-len(L)):
            L.append(dbz(name='', matrix=L[0].matrix*0))
    #print [type(v) for v in L]  #debug
    #time.sleep(3)               #debug
    #L = [v for v in L if isinstance(v, dbz)]

    a = setSideBySide(L[1:4])
    b = setSideBySide([L[4],L[0],L[5]]) #bug fixed 2013-11-22
    c = setSideBySide(L[6:9])
    #output = setUpDown([a,b,c])
    output = setUpDown([c, b, a])   # 2013-11-22 
    output.name = L[1].name + ', ' + L[2].name + ', ' + L[3].name + '\n' +\
                  L[4].name + ', ' + L[0].name + ', ' + L[5].name + '\n' +\
                  L[6].name + ', ' + L[7].name + ', ' + L[8].name
    return output
        
def testA(startingFrom='20130828.0600', endsAt='20130830.0900', threshold=-9999):
    """
    testA : get all the correlations
    """

    """
    1.  apply LoG(sigma=100) + threshold to models (M01-M20, +- 6 hours) and observations
    2.  extract regional "features" and compare
    3.  output the results to '/home/k/ARMOR/documents/2013-final-report/'
    """
    #   1.  apply LoG(sigma=100) + threshold to models (M01-M20, +- 6 hours) and observations
    #   set up
    
    
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    #   loading the stuff
    from armor.objects3 import kongrey     # the data 
    from armor.objects3 import kongreywrf2  # the models
    kongreywrf2.fix()    #fixing the w.name's for w in kongreywrf
    kongrey.fix()
    
    scores = {}
    for count, k in enumerate([v for v in kongrey if (v.dataTime>=startingFrom) and (v.dataTime<=endsAt)]):
        #   set up
        #   k = kongrey radar data
        #   w = wrf output
        #   to compare w to k, we use w.momentNormalise(k)
        k.load()
        k.setThreshold(0)
        k.backupMatrix()
        T0 = k.timeDiff(hours=-6)
        T1 = k.timeDiff(hours= 6)
        wrfs = [w for w in kongreywrf2 if w.dataTime>=T0 and w.dataTime<=T1]
        k.mask = k.gaussianMask(100)

        for w in wrfs:
            # loading
            #k.load()
            #k.setThreshold(0)
            k.restoreMatrix(0)                          # 2013-11-11
            w.load()
            w.setThreshold(0)
            if threshold != -9999:                      # added 2013-11-11
                if isinstance(threshold, int):
                    k.matrix *= (k.matrix>=threshold)
                    w.matrix *= (w.matrix>=threshold)
                elif threshold == "volume":

                    #k.matrix   *= (k.matrix>=threshold)
                    #vol_k       = k.volume(threshold)
                    #threshold_w =threshold-20
                    #vol_w   = w.volume(threshold_w)
                    #while vol_w > vol_k:
                    #    theshold_w +=5
                    #    vol_w       = w.volume(threshold_w)
                    #w.matrix    *= (w.matrix>=threhold_w)
                    #print "thresholds for RADAR and WRF:", threshold, threshold_w
                    #print "volumes for RADAR and WRF:"   , vol_k, vol_w

                    k.matrix   *= (k.matrix>=30)     # fixed 2013-11-15  ; default threshold=30
                    vol_k       = k.volume(30)
                    threshold_w =threshold-10
                    vol_w   = w.volume(threshold_w)
                    while vol_w > vol_k:
                        theshold_w +=5
                        vol_w       = w.volume(threshold_w)
                    w.matrix    *= (w.matrix>=threhold_w)
                    print "thresholds for RADAR and WRF:", threshold, threshold_w
                    print "volumes for RADAR and WRF:"   , vol_k, vol_w

                    
            # matching: 
                #   1. filter;  2. get component;  3.construct masking functions;
                #   4. mask;    5. normalise    ;  6. compare
            w.mask = w.gaussianMask(sigma=100, fraction=0.8)
            # compare
            k.matrix *= k.mask
            w.matrix *= w.mask
            ##################################################
            #   punchlines
            w2 = w.momentNormalise(k)
            scores[(k.name, w.name)] = w2.corr(k)
            #
            ##################################################

            # ordering
            # output
            print k.name, ',', w.name, scores[(k.name, w.name)] 
            pickle.dump(scores, open(outputFolder+ 'testA' + timeString + 'from'+startingFrom + 'to' +endsAt +\
                       'threshold_' + str(threshold) + '.pydump', 'w'))
            kongreywrf2.unload(w.name)
    return scores

def testB(scores=""):

    """
    order/arrange the WRFs according to proximity to COMPREF
    """
    """
    USE
        from armor.tests import roughwork as rw
        reload(rw)
        rw.testB('/home/k/ARMOR/documents/2013-final-report/1383883165/testA.pydump')
    """
    #from armor.objects3 import kongrey     # the data 
    #kongrey.fix()
    from armor.objects3 import kongreywrf2  # the models
    kongreywrf2.fix()    #fixing the w.name's for w in kongreywrf
    
    testBfolder = outputFolder + 'testB' + timeString + '/'
    if not os.path.exists(testBfolder):
        os.makedirs(testBfolder)
    if scores == "" :
        testAfile = [v for v in sorted(os.listdir(outputFolder), reverse=True) if 'testA' in v][0]
        print 'loading', outputFolder + testAfile
        scores = pickle.load(open(outputFolder + testAfile))
    elif isinstance(scores, str):
        print 'loading', scores
        scores = pickle.load(open(scores))
        testAfile = scores
    else:
        testAfile = ""
    print 'sleeping 1 seconds'
    time.sleep(1)
    Tlist  = [v.dataTime for v in kongrey]
    top8matches = {}
    for T in Tlist:
        print '\n...............................\nTime:', T
        pairList = [v for v in scores.keys() if T in v[0]]
        print pairList[:5]
        if len(pairList) == 0:
            continue
        pairList.sort(reverse=True, key=lambda v:scores[v])
        top8matches[T] = [v[1] for v in pairList][:8]
        v0       = pairList[0][0]   # temporary variable
        print 'Top 8 matches:', '\n'.join([v+ '\t' + str(scores[(v0,v)]) for v in top8matches[T]])
        pickle.dump(top8matches, open(testBfolder+ 'top8matches.pydump', 'w'))

        # construct the 3x3 panel
        imList  = kongrey(T) + [kongreywrf2(M)[0]  for M in top8matches[T]]
        #kongrey.load(T)
        #for im in imList[1:]:
        #    im.load()
        #debug
        #print imList
        img9    = construct3by3(imList)
        img9.imagePath = testBfolder + 'best8matches' + T + '.png'
        print 'saving images to', img9.imagePath
        img9.saveImage(dpi=600)
    try:
        open(testBfolder + 'notes.txt').write('source:\n'+ testAfile + '\n\n' +str(scores))
    except:
        print 'error in writing ' + testBfolder + 'notes.txt' 
        pass
    return top8matches

def testC(days=[29,28], hours=range(0000, 2300, 100), threshold=-9999):
    """
    looping, stringing testA and testB together
    """
    top8matches = {}
    count = 0
    for day in days:
        for hour in hours:
            count += 1
            if count < 0:   #Hack 2013-11-12
                continue
            startingFrom = '201308' + str(day) + '.' + ('0'+ str(hour))[-4:]
            endsAt       = '201308' + str(day) + '.' + ('0'+ str(hour+100))[-4:]
            print 'starting from:'  , startingFrom
            print 'ends at:'        , endsAt
            try:
                scores  = testA(startingFrom, endsAt, threshold=threshold)
                print scores
                top8matches[(startingFrom, endsAt)] = testB(scores)
            except:
                print 'error from testA!'
                print 'sleep for 2 seconds'
                time.sleep(2)
                print 'now running testB!'
                top8matches[(startingFrom, endsAt)] = 'error'
            #top8matches[(startingFrom, endsAt)] = testB()
    return top8matches


def testD():
    """
    same as before, but with thresholds taken at 30DBZ
    """
    results = {}
    for threshold in ['volume', 25, 35,40, 20, ]:        #adjust here
        print threshold
        results[threshold] = testC(threshold=threshold)
    return results
    
"""
def test20131106():
    pass
    scores  = testA()
    x       = testB(scores)
"""

def main(*args, **kwargs):
    #return test20131006(*args, **kwargs)    
    return testC()
if __name__ == "__main__":
    main()











