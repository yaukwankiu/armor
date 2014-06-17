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
from armor.patternMatching import pipeline as pp, algorithms
from armor.filter import filters

kongreyDSS = pattern2.kongreyDSS
hualien4 = misc.getFourCorners(dp.hualienCounty)
yilan4   = misc.getFourCorners(dp.yilanCounty)
kaohsiung4  = misc.getFourCorners(dp.kaohsiungCounty)
taipei4     = misc.getFourCorners(dp.taipeiCounty)
taitung4    = misc.getFourCorners(dp.taitungCounty)

regions = [{'name': "hualien", 'points': hualien4, 'weight': 0.25},     # equal weights:  Yilan and Taipei are smaller but are visited by typhoons more
           # {'name': "kaohsiung", 'points':kaohsiung4, 'weight':0.3},  #commented out:  it's on the west coast and we want the window not to cross the central mountainous regions
            {'name': "taipei", 'points':taipei4, 'weight':0.25},
            {'name':"taitung", 'points':taitung4, 'weight':0.25},
            {'name':"yilan", 'points':yilan4, 'weight':0.25},        # no need to add to 1
            ]

regionsString   = "_".join([v['name']+str(round(v['weight'],2)) for v in regions])
outputFolder    = dp.defaultRootFolder + "labReports/2014-03-07-filter-matching-scoring-pipeline/"+regionsString +'/'
###     next up:  work on the i/o so that i don't need to exit/re-enter ipython every time
#   for loop added 18-03-2014
dss = kongreyDSS
obs = dss.obs
#obs.list = [v for v in obs if "00" in v.dataTime and v.dataTime>="20130828.0010"]   # trim it down
obs.list = [v for v in obs if "00" in v.dataTime and (not ".00" in v.dataTime) and v.dataTime>="20130829.1800"]   # trim it down

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
shutil.copyfile(dp.defaultRootFolder+"python/armor/start3.py", outputFolder+"start3.py")

for a in obs:
    #obsTime="20130829.1800"
    #kongreyDSS.load()   # reload
    dss.unload()
    obsTime = a.dataTime
    pp.pipeline(dss=kongreyDSS,
            filteringAlgorithm      = filters.gaussianFilter,
            filteringAlgorithmArgs  = {'sigma':5,
                                       'stream_key': "wrfs" },
            matchingAlgorithm       = algorithms.nonstandardKernel,
            matchingAlgorithmArgs   = {'obsTime': obsTime, 'maxHourDiff':7, 
                                       'regions':regions,
                                       'k'      : 24,   # steps of semi-lagrangian advections performed
                                        'shiibaArgs':{'searchWindowWidth':11, 'searchWindowHeight':11, },
                                        'outputFolder':outputFolder,
                                       } ,
            outputFolder=outputFolder,
            toLoad=False,
            #remarks= "Covariance used, rather than correlation:  algorithms.py line 221:   tempScore   = a1.cov(w1)[0,1]",
            remarks = "Correlation used"
            )


print 'start time:', startTime
print 'total time spent:', time.time()-time0

