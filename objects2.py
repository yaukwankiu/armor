"""

    ds2 = DBZstream(dataFolder='%sdata/SOULIK/wrf_shue/' %externalHardDriveRoot, 
                    lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
                    upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                     )

"""

import pickle


print "loading module 'objects2'"

from armor import pattern

dbz =pattern.DBZ
DBZ =pattern.DBZ
DS  = pattern.DBZstream

a = DBZ('20120612.0200')
b = DBZ('20120612.0230')
c = DBZ('20120612.0300')
d = DBZ('20120612.0210')
e = DBZ('20120612.0240')
f = DBZ('20120612.0310')

kongrey = DS(name='kongrey',
             dataFolder='/home/k/ARMOR/data/KONG-REY/OBS/')

kongreywrf  =  DS(name='kongreywrf',
                  dataFolder='/home/k/ARMOR/data/KONG-REY/WRFEPS/')

soulik  = DS(name='soulik',
             dataFolder='/home/k/ARMOR/data/SOULIK/wrf_shue/',
             lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
             upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
             )


monsoon = DS(name='monsoon',
             dataFolder='/media/KINGSTON/ARMOR/data_temp/'
             )


kongreyregridFolder = '/home/k/ARMOR/data/KONG-REY/summary/WRF[regridded]/'

kongreymodelsall = DS(name='kongreymodelsall',
                      dataFolder='/home/k/ARMOR/data/KONG-REY/WRFEPS/'
                      )
for k in kongreymodelsall:
    k.name += k.dataPath[-8:-4] #add model label

###############################################
#

from armor.dataStreamTools import kongrey as kr
def kongreyModel(M):
    return kr.constructWRFstream(folder='/home/k/ARMOR/data/KONG-REY/WRFEPS/', M=M, dumping=False)

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



def fix(dbzstream, key1='', threshold=0):
    print 'loading', dbzstream.name, 'with key', key1
    dbzstream.load(key1)
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


monsoon.fix= monsoonfix
soulik.fix = soulikfix
kongrey.fix = kongreyfix

