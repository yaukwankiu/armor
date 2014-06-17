"""

    ds2 = DBZstream(dataFolder='%sdata/SOULIK/wrf_shue/' %externalHardDriveRoot, 
                    lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
                    upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                     )

"""

import pickle
import numpy as np

print "loading module 'objects'"
import datetime
from armor import defaultParameters as dp
from armor import pattern

dbz =pattern.DBZ
DBZ =pattern.DBZ
DS  = pattern.DBZstream

a = DBZ('20120612.0200')
b = DBZ('20120612.0210')
c = DBZ('20120612.0230')
d = DBZ('20120612.0240')
e = DBZ('20120612.0300')
f = DBZ('20120612.0310')

kongrey = DS(name='kongrey',
             dataFolder=dp.defaultRootFolder + 'data/KONG-REY/OBS/')

kongreywrf  =  DS(name='kongreywrf',
                  dataFolder=dp.defaultRootFolder + 'data/KONG-REY/WRFEPS/')

kongreywrf2 = DS(name='kongrewrf[regridded]',
                 dataFolder=dp.defaultRootFolder + 'data/KONG-REY/summary/WRF[regridded]/')

soulik  = DS(name='soulik',
             dataFolder=dp.defaultRootFolder + 'data/SOULIK/wrf_shue/',
             lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
             upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
             )

monsoon = DS(name='monsoon',
             dataFolder= dp.defaultRootFolder+'/data_temp/'
             )


################################################################################
#   2014-03-26

march2014       = DS(name='COMPREF_Rainband_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/march2014/QPESUMS/')

march2014wrf11  = DS(name='WRF_Rainband_11_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/march2014/WRFEPS/20140311/')

march2014wrf12  = DS(name='WRF_Rainband_12_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/march2014/WRFEPS/20140312/')

march2014wrf13  = DS(name='WRF_Rainband_13_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/march2014/WRFEPS/20140313/')

march2014wrf    = DS(name='WRF_Rainband_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/march2014/WRFEPS/all/')

###################################################################

tw881 = dp.defaultTaiwanReliefDataFolder881
tw150 = dp.defaultTaiwanReliefDataFolder150

may2014         = DS(name='COMPREF_Rainband_May_2014',
                      dataFolder=dp.root + 'data/may14/QPESUMS/',
                      taiwanReliefFolder = tw881,
                      )

may2014wrf19    = DS(name='WRF_Rainband_19_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/may14/WRF/20140519/',
                      taiwanReliefFolder = tw150,
                      )

may2014wrf20    = DS(name='WRF_Rainband_20_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/may14/WRF/20140520/',
                      taiwanReliefFolder = tw150,
                      )


may2014wrf21    = DS(name='WRF_Rainband_21_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/may14/WRF/20140521/',
                      taiwanReliefFolder = tw150,
                      )


may2014wrf22    = DS(name='WRF_Rainband_22_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/may14/WRF/20140522/',
                      taiwanReliefFolder = tw150,
                      )


may2014wrf23    = DS(name='WRF_Rainband_23_March_2014',
                      dataFolder=dp.defaultRootFolder + 'data/may14/WRF/20140523/',
                      taiwanReliefFolder = tw150,
                      )




###################################################################

kongreyregridFolder = dp.defaultRootFolder + 'data/KONG-REY/summary/WRF[regridded]/'

kongreymodelsall = DS(name='kongreymodelsall',
                      dataFolder=dp.defaultRootFolder + 'data/KONG-REY/WRFEPS/'
                      )
for k in kongreymodelsall:
    k.name += k.dataPath[-8:-4] #add model label

###############################################
#

from armor.dataStreamTools import kongrey as kr
def kongreyModel(M):
    return kr.constructWRFstream(folder=dp.defaultRootFolder + 'data/KONG-REY/WRFEPS/', M=M, dumping=False)

#
#############################################
def kongreyregrid(index):
    if isinstance(index, int):
        index = ("0" + str(index))[-2:]
    ds = pickle.load(open(kongreyregridFolder+'dbzstream'+index+'.pydump'))
    for d in ds:
        d.imageTopDown = False
        def setThreshold(self, threshold=-9999):
            mask = self.matrix.mask.copy()
            self.matrix.mask = 0
            self.matrix = self.matrix + (self.matrix<threshold) * (threshold-self.matrix) #setting the threshold to 0
            self.matrix.mask = mask
        d.setThreshold(0)        
    return ds



def fix(dbzstream, key1='', key2='', threshold=0, cutUnloaded=True):
    print 'loading', dbzstream.name, 'with key', key1
    dbzstream.load(N=key1,key2=key2)
    if cutUnloaded:
        print 'cutting the excess'
        dbzstream.cutUnloaded()
    print 'setting threshold', threshold
    dbzstream.setThreshold(threshold)
    dbzstream.setTaiwanReliefFolder()


def monsoonfix(key1='0612.', threshold=0):
    fix(monsoon, key1=key1, threshold=threshold)


def soulikfix(key1='', threshold=0):
    fix(soulik, key1=key1, threshold=threshold)

def kongreyfix(key1='', threshold=0):
    fix(kongrey, key1=key1, threshold=threshold)

def kongreywrffix(ds=kongreywrf):
    #from armor.dataStreamTools import kongrey as kr
    for w in ds:
        
        w.name += w.dataPath[-23:-18]
        #w.dataTime=w.getDataTime(w.datetime()+datetime.timedelta(1./24*int(w.dataPath[-11:-8])))
        #w.outputPath="kongreywrf"+
        #w.imagePath=

def kongreywrf2fix(key1='', key2='', threshold=0, cutUnloaded=False):
    try:
        kongreywrf2.fixed
    except AttributeError:
        for w in kongreywrf2:
            w.name = w.dataPath[-23:-18] + '.' + w.name[-13:]
            w.matrix.mask = np.zeros(w.matrix.shape)
    #fix(kongreywrf2, key1=key1, key2=key2, cutUnloaded=cutUnloaded)

def march2014wrffix(ds=march2014wrf):
    #from armor.dataStreamTools import kongrey as kr
    for w in ds:
        w.name += w.dataPath[-23:-18]
        #w.dataTime=w.getDataTime(w.datetime()+datetime.timedelta(1./24*int(w.dataPath[-11:-8])))
        #w.outputPath="kongreywrf"+
        #w.imagePath=


monsoon.fix= monsoonfix
soulik.fix = soulikfix
kongrey.fix = kongreyfix
kongreywrf.fix = kongreywrffix
kongreywrf2.fix = kongreywrf2fix
march2014wrf.fix=march2014wrffix


