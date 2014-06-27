"""
    matching algorithms for pattern2.DataStreamSets
    format:
        def alg(obs, w, obsTime, maxHourDiff, **kwargs):
        input: 
            obs - observation stream, a pattern.DBZstream object
            w   - wrf (model) stream, another pattern.DBZstream object
            obsTime     - time at which obs is compared with the wrfs, e.g. "20140612.0200'
            maxHourDiff - the maximal time difference (in hours) between obs and wrfs, e.g. 7 (hours)
            kwargs - key-worded parameters (a=1, b=2, etc)
        output:
            a dict: {'score':score, 'timeShift':timeShift}
                where   score       - a real number, representing the alikeness/degree of matching
                        timeShift   - a number, in hours, the optimal timeShift for the wrf


    to do:
        combinations of - correlations, adjusted correlations, histogram, moments, other features
        (2014-04-15)


"""
#######################
#   imports

import os, time, datetime
from datetime import timedelta
import numpy as np
from armor import pattern
dp  = pattern.dp    # defaultParameters
###########################
#   functions

def normalisedCorrelation():
    """
    1 May, 2014
    """
    pass
    
def plainCorr(obs, wrf, obsTime, maxHourDiff=7, verbose=False):
    a   = obs(obsTime)[0]   # getting the DBZ object from the observation stream to be compared
    T   = a.datetime()      # getting the time range
    maxTime = T + timedelta(maxHourDiff * 1./24)
    minTime = T - timedelta(maxHourDiff * 1./24)
    maxTime = a.getDataTime(maxTime)    # converting it into string format for pattern.DBZ
    minTime = a.getDataTime(minTime)    # converting it into string format for pattern.DBZ
    if verbose:
        print "minTime, obsTime, maxTime:", minTime, obsTime, maxTime
    scores = []
    for w in wrf:
        if w.dataTime > maxTime or w.dataTime < minTime:
            continue
        else:
            if a.matrix.var()==0:    # test if it is empty
                a.load()
            if w.matrix.var()==0:
                w.load()
            score = a.corr(w)       # <<<<<<<< key comparison step >>>>>>>>>>>>>>
            scores.append( {'time':w.dataTime, 'score': score} )
    scores.sort(key=lambda v:v['score'], reverse=True)
    topScore = scores[0]['score']
    topScoreTime = scores[0]['time']
    timeShift = (a.datetime(topScoreTime) - a.datetime()).total_seconds()   # the time difference is a datetime.timedelta object
    timeShift = 1. * timeShift/3600                             # convert it into hours
    
    return {'score':topScore, 'timeShift':timeShift}    #score - depending on the algorithm; timeShift - in hours


def nonstandardKernel(obs, wrf, regions, shiibaAlg="",
                      shiibaArgs={},  obsTime="", maxHourDiff=7, 
                      k=24,     # number of 10-minute steps to semi-lagrange advect
                      verbose=False,
                      outputFolder= dp.defaultLabReportsFolder +'2014-03-07-filter-matching-scoring-pipeline/',
                      volumevolumeProportionWeight  =0.,
                      **kwargs      #just in case
                      ):
    """
    "Non-standard Kernel matching":
    see ARMOR RFP 2014

    inputs:
        obs                 - one observation stream
        wrf                 - one wrf (NWP model) stream
        regions             - list of regions of interest (listed in descending order of priority?!)
                              {'name':name, 'points':points, 'weight':weight}
        regionalWeights     - to get a weighed averge if necessary
        shiibaAlg - pointer to the function for shiiba Regression
        shiibaArgs- parameters for shiiba regression
        maxHourDiff         - max temporal difference (in hours) you would consider for the WRF to match the OBS
    outputs:
        {'score': a list, top weighed average score followed by a list of regional scores
         'timeShift':   time shift for the top score}

    USE:
        from armor import defaultParameters as dp
        from armor import misc
        from armor import pattern, pattern2
        from armor.patternMatching import pipeline as pp, algorithms
        from armor.filter import filters
        hualien4 = misc.getFourCorners(dp.hualienCounty)
        yilan4   = misc.getFourCorners(dp.yilanCounty)
        kaohsiung4  = misc.getFourCorners(dp.kaohsiungCounty)
        regions = [{'name': "hualien", 'points': hualien4, 'weight': 0.5},
                    {'name': "kaohsiung", 'points':kaohsiung4, 'weight':0.3},
                    {'name':"yilan", 'points':yilan4, 'weight':0.2},
                    ]
        pp.pipeline(filteringAlgorithm         = filters.gaussianFilter,
                filteringAlgorithmArgs              = {'sigma':20},
                matchingAlgorithm       = algorithms.nonstandardKernel,
                matchingAlgorithmArgs   = {'obsTime':"20130829.0300", 'maxHourDiff':7, 'regions':regions} ,
                outputFolder=dp.defaultRootFolder + "labReports/2014-03-07-filter-matching-scoring-pipeline/",
                toLoad=False)
    2014-03-11
     
    """
    # codes adapted from plainCorr above
    timeString      = str(int(time.time()))
    miscRemarks     = ""
    outputFolder   += timeString + wrf.name + '/'
    print "\n\n\n................................................................."
    print "outputFolder:", outputFolder
    print "volumevolumeProportionWeight:",volumevolumeProportionWeight
    os.makedirs(outputFolder)
    print "sleeping 5 seconds", time.sleep(5)
    if obsTime == "":
        obsTime = obs[0].dataTime
    a   = obs(obsTime)[0]   # getting the DBZ object from the observation stream to be compared
    #a.show()                #debug
    T   = a.datetime()      # getting the time range
    T_string    = a.getDataTime(T)
    T2  = sorted([v.dataTime for v in obs if v.dataTime>T_string])[0]  # the next time, assumed 10 mins apart - or else
                                                                #     or else need to adjust the k for vect.semiLagrange below
    b   = obs(T2)[0]
    if b.datetime() - a.datetime() > datetime.timedelta(600./86400):    # 600 seconds
        td          = b.datetime() - a.datetime()
        miscRemarks += "\nTime difference between %s and %s is " % (b.name, a.name)
        miscRemarks += str(td.days) + " days " + str(td.seconds) + "seconds.\n"
    #b.debug()               #show
    if a.matrix.var()==0:    # test if it is empty
        a.load()
    if b.matrix.var()==0:
        b.load()
    #a.saveImage()
    #b.saveImage()

    if shiibaAlg == "":
        from armor import analysis
        shiibaAlg = analysis.shiiba

    maxTime = T + timedelta(maxHourDiff * 1./24)
    minTime = T - timedelta(maxHourDiff * 1./24)
    maxTime = a.getDataTime(maxTime)    # converting it into string format for pattern.DBZ
    minTime = a.getDataTime(minTime)    # converting it into string format for pattern.DBZ
    if verbose:
        print "minTime, obsTime, maxTime:", minTime, obsTime, maxTime

    #   check if there's no corresponing wrf for the time
    if [v.dataTime for v in wrf if v.dataTime>=minTime and v.dataTime<=maxTime] == []:
        return {}

    scores = []
    #   get the ABLER-Shiiba vector field
    
    try:
        shiibaResults   = a.shiibaResultLocalCopy   #   need to regress at least once!!!
    except AttributeError:    
        shiibaResults   = shiibaAlg(a, b, **shiibaArgs)
        a.shiibaResultLocalCopy = shiibaResults
        
    vect            = shiibaResults['vect'] + shiibaResults['mn']
    a.backupMatrix('good_copy')
    a.drawCoast()
    for R in regions:
        a.drawRectangularHull(R['points'])

    a.saveImage(imagePath=outputFolder+ a.name +dp.defaultImageSuffix)
    a.restoreMatrix('good_copy')
    b.backupMatrix('good_copy')
    b.drawCoast()
    for R in regions:
        b.drawRectangularHull(R['points'])

    b.saveImage(imagePath=outputFolder+ b.name +dp.defaultImageSuffix)
    b.restoreMatrix('good_copy')

    print "a saved to", outputFolder+ a.name +dp.defaultImageSuffix # debug
    print "b saved to", outputFolder+ b.name +dp.defaultImageSuffix # debug 
    
    vect.saveImage(imagePath=outputFolder+ "abler_vector_field" + dp.defaultImageSuffix)

    #   looping
    a_with_windows  = a.copy()
    a_with_windows.drawCoast()
    for w in wrf:
        if w.dataTime > maxTime or w.dataTime < minTime:
            continue
        else:
            if w.matrix.var()==0:   # test if it is empty
                w.load()
            #w.backupMatrix('good_copy')
            ####################################################################
            #   matching core
            #   1. shiiba regression    -> find the vector field
            #   2. semi-lagrangian      -> find the extended region
            #   3. cut out the region in obs
            #   4. match the appropriate region in wrf
            regionalScores = []
            for R0 in regions:
                name            = R0['name']
                points          = R0['points']
                weight          = R0['weight']
                #   extract the "nonstandard kernel" as a1
                points1         = vect.semiLagrange(L=points, k=k, direction=-1, verbose=verbose)   # back advection
                points2         = points + points1
                iMax            = int(max(v[0] for v in points2))
                iMin            = int(min(v[0] for v in points2))
                jMax            = int(max(v[1] for v in points2))
                jMin            = int(min(v[1] for v in points2))
                height  = iMax-iMin
                width   = jMax-jMin
                a1              = a.getWindow(iMin, jMin, height, width)
                a1.name         = a.name + '_' + name
                a1.imagePath    = outputFolder + a1.name + dp.defaultImageSuffix    # suffix = ".png"
                a1.saveImage(imagePath=a1.imagePath)
                a_with_windows.drawRectangle(iMin, jMin, height, width, newObject=False)
                #   match a1 with a similar rectangle on the wrf, scoring by correlation
                #   we shift the kernel by 1/10 of it's width/height
                #   4 times left, right, up and down respectively
                iStep   = int(height//10 + 1)
                jStep   = int(width//10 + 1)
                print "points (corners for the region):", points     #debug
                print "iStep, jStep", iStep, jStep  #debug
                
                score   = 0
                shift   = (-999,-999)   #initialise
                for i in range(-4*iStep, 4*iStep+1, iStep):
                    for j in range(-4*jStep, 4*jStep+1, jStep):
                        #w.restoreMatrix('good_copy')
                        w1 = w.getWindow(iMin+i, jMin+j, height, width)
                        tempScore   = a1.corr(w1)     # <<<<<<<< key comparison step >>>>>>>>>>>>>>
                        # adding a step to compare the relative volume,  2014-03-28
                        proportion  = a1.matrix.sum() / w1.matrix.sum()
                        if proportion > 1:
                            proportion = 1./proportion
                        #diffLog     = abs(np.log(a1.matrix.sum()) - np.log(w1.matrix.sum()))
                        #tempScore   = a1.cov(w1)[0,1]
                                                    #   use straight corr for now, will convert to shiiba or normalised corr later
                                                    #   or can use covariance rather than correlation
                        tempScore   = tempScore*(1-volumevolumeProportionWeight  ) + proportion*volumevolumeProportionWeight  
                        if score < tempScore:
                            score       = tempScore     # get the highest
                            #scoreTime   = w.dataTime
                            shift     = (i,j)        # this info is probably not needed
                regionalScores.append({'name'    : name,  # name of the region
                                      'score'   : score,
                                      'shift'   : shift,
                                      'weight'  : weight,
                                      })

                
            #   compute weighed average over regions
            averageScore    = np.sum([v['score']*v['weight'] for v in regionalScores])

            #
            #
            #####################################################################

            scores.append( {'time':w.dataTime, 'score': averageScore, 'regionalScores': regionalScores} )
    scores.sort(key=lambda v:v['score'], reverse=True)
    topScore            = scores[0]['score']
    topScoreTime        = scores[0]['time']
    topScoresRegional   = scores[0]['regionalScores']     # actually regional scores for the top score
    timeShift = (a.datetime(topScoreTime) - a.datetime()).total_seconds()   # the time difference is a datetime.timedelta object
    timeShift = 1. * timeShift/3600                             # convert it into hours

    #   saving images
    w   = wrf(topScoreTime)[0].copy()   # temp image object
    #########
    #   2014-06-26
    for R0 in regions:
        print "extracting window for", R0['name']
        name            = R0['name']
        points          = R0['points']
        #weight          = R0['weight']
        #   extract the "nonstandard kernel" as a1
        iMax            = int(max(v[0] for v in points))
        iMin            = int(min(v[0] for v in points))
        jMax            = int(max(v[1] for v in points))
        jMin            = int(min(v[1] for v in points))
        height  = iMax-iMin
        width   = jMax-jMin
        print "iMin, jMin=", iMin, jMin
        print "topScoresRegional:",topScoresRegional     #debug
        iShift, jShift = [v['shift'] for v in topScoresRegional if v['name']==name][0]
        iMin           += iShift
        jMin           += jShift
        print "iShift, jShift=", iShift, jShift

        w1              = w.getWindow(iMin, jMin, height, width)
        w1.name         = w.name + '_' + name + " with shift: (x, y) = " + str((jShift, iShift))
        w1.imagePath    = outputFolder + w.name + "_window_" + name + "_with_shift"+ dp.defaultImageSuffix    # suffix = ".png"
        #print w1.imagePath  #debug
        #w1.show()           #debug
        w1.saveImage(imagePath=w1.imagePath)
    #
    #########    
    
    w.coastDataPath=obs[0].coastDataPath
    w.drawCoast()
    a_frames = (a_with_windows.matrix > 999)        # hack, getting the window frames for w
    w.matrix += a_frames * 9999                     # hack, getting the window frames for w
    w.saveImage(imagePath=outputFolder+w.name+dp.defaultImageSuffix)
    a_with_windows.saveImage(imagePath=outputFolder+ a.name + "_with_windows" + dp.defaultImageSuffix)
    
    return {'score':topScore, 'timeShift':timeShift, 'topScoresRegional': topScoresRegional,
            'Remarks': "'topScoresRegional' stands for regional scores for the top score",
            'miscRemarks': miscRemarks,
            }    #score - depending on the algorithm; timeShift - in hours



def shiftedCorr(obs, wrf, regions="", obsTime="", maxHourDiff=7,  maxLatDiff=4, maxLongDiff=6,
                     shiftStep = 2,     #2014-06-25
                      verbose=False,
                      outputFolder= dp.defaultLabLogsFolder ,
                      volumevolumeProportionWeight  =0.,
                      **kwargs      #just in case
                      ):


    """
    adapted from nonStandardKernel() above
    2014-06-24
    first applied to 20140312.1100 etc
    maxLatDiff / maxLongDiff:   maximal latitudinal / longitudinal difference between obs frame and wrf frame

    """
    timeString      = str(int(time.time()))
    miscRemarks     = ""
    outputFolder   += timeString + wrf.name + '/'
    print "\n\n\n................................................................."
    print "outputFolder:", outputFolder
    print "volumevolumeProportionWeight:",volumevolumeProportionWeight
    os.makedirs(outputFolder)
    print "sleeping .5 second", time.sleep(.5)
    if obsTime == "":
        obsTime = obs[0].dataTime
    a   = obs(obsTime)[0]   # getting the DBZ object from the observation stream to be compared
    #a.show()                #debug

    if regions == "":
        regions = [(0, 0, a.matrix.shape[0], a.matrix.shape[1])]    # a list of one region consisting of the full array, if none given

    T   = a.datetime()      # getting the time range
    T_string    = a.getDataTime(T)
    T2  = sorted([v.dataTime for v in obs if v.dataTime>T_string])[0]  # the next time, assumed 10 mins apart - or else
                                                                #     or else need to adjust the k for vect.semiLagrange below
    b   = obs(T2)[0]
    if b.datetime() - a.datetime() > datetime.timedelta(600./86400):    # 600 seconds
        td          = b.datetime() - a.datetime()
        miscRemarks += "\nTime difference between %s and %s is " % (b.name, a.name)
        miscRemarks += str(td.days) + " days " + str(td.seconds) + "seconds.\n"
    #b.debug()               #show
    if a.matrix.var()==0:    # test if it is empty
        a.load()
    if b.matrix.var()==0:
        b.load()
    #a.saveImage()
    #b.saveImage()
    maxTime = T + timedelta(maxHourDiff * 1./24)
    minTime = T - timedelta(maxHourDiff * 1./24)
    maxTime = a.getDataTime(maxTime)    # converting it into string format for pattern.DBZ
    minTime = a.getDataTime(minTime)    # converting it into string format for pattern.DBZ
    if verbose:
        print "minTime, obsTime, maxTime:", minTime, obsTime, maxTime

    #   check if there's no corresponing wrf for the time
    if [v.dataTime for v in wrf if v.dataTime>=minTime and v.dataTime<=maxTime] == []:
        return {}

    scores = []

    a.backupMatrix('good_copy')
    a.drawCoast()
    for R in regions:
        a.drawRectangularHull(R['points'])

    a.saveImage(imagePath=outputFolder+ a.name +dp.defaultImageSuffix)
    a.restoreMatrix('good_copy')
    b.backupMatrix('good_copy')
    b.drawCoast()
    for R in regions:
        b.drawRectangularHull(R['points'])

    b.saveImage(imagePath=outputFolder+ b.name +dp.defaultImageSuffix)
    b.restoreMatrix('good_copy')

    print "a saved to", outputFolder+ a.name +dp.defaultImageSuffix # debug
    print "b saved to", outputFolder+ b.name +dp.defaultImageSuffix # debug 
    
    #   looping
    a_with_windows  = a.copy()
    a_with_windows.drawCoast()
    for w in wrf:
        if w.dataTime > maxTime or w.dataTime < minTime:
            continue
        else:
            if w.matrix.var()==0:   # test if it is empty
                w.load()
            #w.backupMatrix('good_copy')
            ####################################################################
            #   matching core
            #   1. shiiba regression    -> find the vector field
            #   2. semi-lagrangian      -> find the extended region
            #   3. cut out the region in obs
            #   4. match the appropriate region in wrf
            regionalScores = []
            for R0 in regions:
                name            = R0['name']
                points          = R0['points']
                weight          = R0['weight']
                #   extract the "nonstandard kernel" as a1
                iMax            = int(max(v[0] for v in points))
                iMin            = int(min(v[0] for v in points))
                jMax            = int(max(v[1] for v in points))
                jMin            = int(min(v[1] for v in points))
                height  = iMax-iMin
                width   = jMax-jMin
                a1              = a.getWindow(iMin, jMin, height, width)
                a1.name         = a.name + '_' + name
                a1.imagePath    = outputFolder + a1.name + dp.defaultImageSuffix    # suffix = ".png"
                a1.saveImage(imagePath=a1.imagePath)
                a_with_windows.drawRectangle(iMin, jMin, height, width, newObject=False)
                #   match a1 with a similar rectangle on the wrf, scoring by correlation
                #   we shift the kernel by 1/10 of it's width/height
                #   4 times left, right, up and down respectively
                iStep   = shiftStep
                jStep   = shiftStep
                print "points (corners for the region):", points     #debug
                #print "iStep, jStep", iStep, jStep  #debug
                
                score   = 0
                shift   = (-999,-999)   #initialise
                for i in range(-maxLatDiff, maxLatDiff+1, iStep):
                    for j in range(-maxLongDiff, maxLongDiff+1, jStep):
                        #w.restoreMatrix('good_copy')
                        w1 = w.getWindow(iMin+i, jMin+j, height, width)
                        tempScore   = a1.corr(w1)     # <<<<<<<< key comparison step >>>>>>>>>>>>>>
                        # adding a step to compare the relative volume,  2014-03-28
                        proportion  = abs(np.log(a1.matrix.sum() / w1.matrix.sum()))

                        #diffLog     = abs(np.log(a1.matrix.sum()) - np.log(w1.matrix.sum()))
                        #tempScore   = a1.cov(w1)[0,1]
                                                    #   use straight corr for now, will convert to shiiba or normalised corr later
                                                    #   or can use covariance rather than correlation
                        tempScore   = tempScore*(1-volumevolumeProportionWeight  ) + proportion*volumevolumeProportionWeight  
                        if score < tempScore:
                            score       = tempScore     # get the highest
                            #scoreTime   = w.dataTime
                            shift     = (i,j)        # this info is probably not needed
                regionalScores.append({'name'    : name,  # name of the region
                                      'score'   : score,
                                      'shift'   : shift,
                                      'weight'  : weight,
                                      })

                
            #   compute weighed average over regions
            averageScore    = np.sum([v['score']*v['weight'] for v in regionalScores])

            #
            #
            #####################################################################

            scores.append( {'time':w.dataTime, 'score': averageScore, 'regionalScores': regionalScores} )
    scores.sort(key=lambda v:v['score'], reverse=True)
    topScore            = scores[0]['score']
    topScoreTime        = scores[0]['time']
    topScoresRegional   = scores[0]['regionalScores']     # actually regional scores for the top score
    timeShift = (a.datetime(topScoreTime) - a.datetime()).total_seconds()   # the time difference is a datetime.timedelta object
    timeShift = 1. * timeShift/3600                             # convert it into hours

    #   saving images
    w   = wrf(topScoreTime)[0].copy()   # temp image object

    #########
    #   2014-06-26
    for R0 in regions:
        print "extracting window for", R0['name']
        name            = R0['name']
        points          = R0['points']
        #weight          = R0['weight']
        #   extract the "nonstandard kernel" as a1
        iMax            = int(max(v[0] for v in points))
        iMin            = int(min(v[0] for v in points))
        jMax            = int(max(v[1] for v in points))
        jMin            = int(min(v[1] for v in points))
        height  = iMax-iMin
        width   = jMax-jMin
        print "iMin, jMin=", iMin, jMin
        print "topScoresRegional:",topScoresRegional     #debug
        iShift, jShift = [v['shift'] for v in topScoresRegional if v['name']==name][0]
        iMin           += iShift
        jMin           += jShift
        print "iShift, jShift=", iShift, jShift

        w1              = w.getWindow(iMin, jMin, height, width)
        w1.name         = w.name + '_' + name + " with shift: (x, y) = " + str((jShift, iShift))
        w1.imagePath    = outputFolder + w.name + "_window_" + name + "_with_shift"+ dp.defaultImageSuffix    # suffix = ".png"
        #print w1.imagePath  #debug
        #w1.show()           #debug
        w1.saveImage(imagePath=w1.imagePath)
    #
    #########
    try:
        w.coastDataPath=obs[0].coastDataPath
        w.drawCoast()
    except:
        print "can't draw coast for ", w.name
    a_frames = (a_with_windows.matrix > 999)        # hack, getting the window frames for w
    w.matrix += a_frames * 9999                     # hack, getting the window frames for w
    w.saveImage(imagePath=outputFolder+w.name+dp.defaultImageSuffix)
    a_with_windows.saveImage(imagePath=outputFolder+ a.name + "_with_windows" + dp.defaultImageSuffix)
    
    return {'score':topScore, 'timeShift':timeShift, 'topScoresRegional': topScoresRegional,
            'Remarks': "'topScoresRegional' stands for regional scores for the top score",
            'miscRemarks': miscRemarks,
            }    #score - depending on the algorithm; timeShift - in hours














