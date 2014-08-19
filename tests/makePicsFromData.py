import time
import os
from armor import objects4 as ob

comprefsList = [ob.monsoon,  ob.may2014,ob.soulik,ob.march2014,  ob.kongrey, ]

for ds in comprefsList:
    outputFolder=ds.dataFolder+'.pics/'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    ds.setImageFolder(outputFolder)
    
    ds.saveImages(dpi=200, verbose=True, toLoad=True, drawCoast=True)