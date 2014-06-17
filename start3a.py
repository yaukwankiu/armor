import time

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
regions = [{'name': "hualien", 'points': hualien4, 'weight': 0.4},
            {'name': "kaohsiung", 'points':kaohsiung4, 'weight':0.3},
            {'name':"yilan", 'points':yilan4, 'weight':0.3},
            ]

###     next up:  work on the i/o so that i don't need to exit/re-enter ipython every time
#   for loop added 18-03-2014
for a in kongreyDSS.obs:    
    kongreyDSS.load()   # reload
    pp.pipeline(dss=kongreyDSS,
            filteringAlgorithm         = filters.gaussianFilter,
            filteringAlgorithmArgs              = {'sigma':5},
            matchingAlgorithm       = algorithms.nonstandardKernel,
            matchingAlgorithmArgs   = {'obsTime': a.dataTime, 'maxHourDiff':7, 
                                       'regions':regions,
                                       'k'      : 48,   # steps of semi-lagrangian advections performed
                                        'shiibaArgs':{'searchWindowWidth':11, 'searchWindowHeight':11, },
                                       } ,
            outputFolder=dp.defaultRootFolder + "labReports/2014-03-07-filter-matching-scoring-pipeline/",
            toLoad=False,
            remarks= "Covariance used, rather than correlation:  algorithms.py line 221:   tempScore   = a1.cov(w1)[0,1]",
            )


print 'start time:', startTime
print 'time spent:', time.time()-time0

