#powerSpecTest20140707.py

from armor.initialise import *
from armor import objects4 as ob

outputFolder = dp.root + "labLogs2/powerSpec3/"
eventsList = [maywrf20, kongrey, kongreywrf, march, may, marchwrf, ]

for event in eventsList:
    timeString = str(time.time())
    eventFolder = outputFolder + timeString+ event.name
    os.makedirs(eventFolder)
    for a in event:
        a.powerSpec(outputFolder=eventFolder, toDumpResponseImages=False)
