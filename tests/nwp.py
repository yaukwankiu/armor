# nwp.py
# comparing nwp model with real data
# tools:  k-means, texture analsis / segmentation, correlation, moments, detection of the upwind region
# note - this is just a test of the methods.  we don't expect good results from data which are obviously different

"""
information on nwp data:
grid size:  height=282, width=342

max latitude:  28.62909
min latitude:  17.7094
max longitude: 127.6453
min longitude:  113.3272

"""
##
# to do:  construct taiwan coast data and implement it
# for real / nwp data do these things separately:
#	segmentation
# 	calculate taiwan upwind region
#  	compute regional moments
# 	plot


# for real data do these things:
# 	compute valid region

# between results from real/nwp data do these:
#	compare, estimate likeness.

#######
# setup
#import numpy as np

from armor import pattern
dbz = pattern.DBZ

rootFolder = '../data_simulation/20120611_12/'
coastDataPath = rootFolder+"taiwanCoast.dat"
relief100DataPath = rootFolder+  "relief100.dat"
relief1000DataPath= rootFolder+ "relief1000Extended.dat"
relief2000DataPath= rootFolder+ "relief2000Extended.dat"
relief3000DataPath= rootFolder+ "relief3000Extended.dat"
 
#######
# loading the nwp


def loadNWP(dataTime = '201206120200', prefix=rootFolder+'out_', suffix='.txt', **kwargs ):

    if isinstance(dataTime, int):   # dataTime=201206120200
        dataTime = str(dataTime)
    if isinstance(dataTime, float): # dataTime=20120612.0200
        dataTime = str(int(dataTime*10000))
    a = dbz(name="NWP"+dataTime, dataPath=prefix+dataTime+suffix,  coordinateOrigin=(141,171),
           **kwargs)
    a.load()
    return a

def constructCoastlines():
    """do this once only, and put the results back in with other datafiles afterwards"""
    #max latitude:  28.62909
    #min latitude:  17.7094
    #max longitude: 127.6453
    #min longitude:  113.3272
    kwargs =    {'files'  :['100','1000','2000','3000', 'Coast'],
                 'width'  : 342,
                 'height' : 282,
                 'lowerLeft' : (113.3272, 17.7094),
                 'upperRight' : (127.6453, 28.62909),
                 'folder' : '../data_simulation/taiwanReliefData/',
                 'suffix' : ".DAT",
                 }

    from armor.taiwanReliefData import convertToGrid
    convertToGrid.main(**kwargs)

def test():
    pass
    
def main():
    a = loadNWP(dataTime=201206120200)
    b = loadNWP(dataTime=201206120210)

    #a.show4()
    #b.show4()
    #(b-a).show4()
    return a,b

if __name__=='__main__':
    main()

