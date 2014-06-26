thisScript =   "localMatchingShiftedCorr201403121140.py"

#################
#   codes for testing armor.patternMatching.pipeline and armor.patternMatching.algorithms

import time
import shutil
import os

time0   = time.time()
startTime   =time.asctime()

from armor import defaultParameters as dp
from armor import misc
from armor import pattern, pattern2
p2  = pattern2
from armor.patternMatching import pipeline as pp, algorithms
from armor.filter import filters
##################################################################################
#   set up
hualien4        = misc.getFourCorners(dp.hualienCounty)
yilan4          = misc.getFourCorners(dp.yilanCounty)
kaohsiung4      = misc.getFourCorners(dp.kaohsiungCounty)
taichung4        = misc.getFourCorners(dp.taichungCounty)
tainan4         = misc.getFourCorners(dp.tainanCounty)
taipei4         = misc.getFourCorners(dp.taipeiCounty)
taitung4        = misc.getFourCorners(dp.taitungCounty)

sector3 = misc.getFourCorners((342, 198, 453-342, 493-198))
sector6 = misc.getFourCorners((360, 287, 489-360, 541-287))
sector7 = misc.getFourCorners((423, 319, 561-423, 565-319))


regions = [ #{'name': "hualien",      'points': hualien4, 'weight': 0.25},
            #{'name': "kaohsiung",   'points':kaohsiung4,    'weight':0.5},  
            #{'name': "taipei",      'points':taipei4,       'weight':1.0},  # the rainband comes from north east
            #{'name': "taichung",    'points':taichung4,     'weight':0.2},
            #{'name': "tainan",      'points':tainan4,       'weight':0.2},
            #{'name':"taitung",      'points':taitung4, 'weight':0.25},
            #{'name':"yilan",        'points':yilan4, 'weight':0.25},        # no need to add to 1
            {'name': 'sector7' ,     'points':sector7, 'weight':1.},
            ]

regionsString   = "_".join([v['name']+str(round(v['weight'],2)) for v in regions])
dss = p2.march12            #   edit here
obs = dss.obs               #   edit here
#obs.list = [v for v in obs.list if dss.wrfs[0][0].dataTime[:8] in v.dataTime]            #   (e.g. "20140312")
#print "obs.list trimmed to length", len(obs.list)       #debug
scriptFileName = thisScript
volumeProportionWeight    = 0.1
testName       = "shiftedCorr" + str(1-volumeProportionWeight)+"_and_volume" + str(volumeProportionWeight)
outputFolder    = dp.defaultRootFolder + "labLogs/" + testName + "/" + dss.name + "/" +regionsString +'/'
#obs.shortlist = [v for v in obs if "00" in v.dataTime and (not ".00" in v.dataTime) and v.dataTime>="0"]   # trim it down
obs.shortlist = [v for v in obs if v.dataTime>="20140312.1100" and v.dataTime<="20140312.1500"]   # trim it down

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
shutil.copyfile(dp.defaultRootFolder+"python/armor/tests/"+ scriptFileName, outputFolder+ str(time.time()) + scriptFileName)
shutil.copyfile(dp.defaultRootFolder+"python/armor/patternMatching/algorithms.py", outputFolder+ str(time.time()) + "algorithms.py")
shutil.copyfile(dp.defaultRootFolder+"python/armor/patternMatching/pipeline.py", outputFolder+ str(time.time()) + "pipeline.py")

################################################################################
#   looping the code


for a in obs.shortlist:
    #obsTime="20130829.1800"
    #kongreyDSS.load()   # reload
    dss.unload()
    obsTime = a.dataTime
    pp.pipeline(dss=dss,
            #filteringAlgorithm      = filters.gaussianFilter,
            #filteringAlgorithmArgs  = {'sigma':5,
            #                           'stream_key': "obs" },
            filteringAlgorithm      = "",
            matchingAlgorithm       = algorithms.shiftedCorr,
            matchingAlgorithmArgs   = {'obsTime': obsTime, 'maxHourDiff':6, 
                                       'regions':regions,
                                        'outputFolder':outputFolder,
                                        'volumeProportionWeight':volumeProportionWeight,
                                        'maxLatDiff': 4,
                                        'maxLongDiff': 6,
                                        
                                       } ,
            outputFolder=outputFolder,
            toLoad=False,
            #remarks= "Covariance used, rather than correlation:  algorithms.py line 221:   tempScore   = a1.cov(w1)[0,1]",
            remarks = "Correlation used"
            )


print 'start time:', startTime
print 'total time spent:', time.time()-time0

