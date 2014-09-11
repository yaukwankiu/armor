dataFolder = 'f:/ARMOR/data/Data0827/RADARCV/'
import os
from armor import pattern
dbz = pattern.DBZ

L = os.listdir(dataFolder)

for path in L:
    a = dbz(dataPath=dataFolder+path, name=path[:21])
    a.imagePath = a.name+'.png'
    a.load()
    #a.show(block=True)
    a.saveImage()
