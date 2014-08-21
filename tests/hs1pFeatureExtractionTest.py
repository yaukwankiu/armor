#   imports
import time, os, shutil, pickle, re
import numpy as np
import matplotlib.pyplot as plt
from armor import pattern
from armor import defaultParameters as dp
DBZ     = pattern.DBZ

#   setup
#a   = DBZ('20130920.0000') #USAGI  http://rdc28.cwb.gov.tw/TDB/ntdb/pageControl/ty_warning


#for dataTime in ['20140312.1000', '20140312.1100', '20140312.1200', '20140311.1000', '20140311.1100', '20140311.1200']:

for dataTime in ['20140816.1400', '20140816.1500', '20140816.1530', '20140816.1600',]:
    plt.close()
    a   = DBZ(dataTime)
    a.loadImage()
    a.show()
    x=a.granulometry([1,2,4,8,16,32,64], outputFolder=dp.root+'labLogs2/hs1p/'+dataTime)

