#powerSpecTest20140707.py

from armor.initialise import *

outputFolder = dp.root + "labLogs2/powerSpec3/"
eventsList = [march, may, marchwrf, maywrf20, kongrey, kongreywrf]

for event in eventsList:
    timeString = str(time.time())
    eventFolder = outputFolder + timeString+ event.name +"/"
    os.makedirs(eventFolder)
    for a in event:
        a.load()
        a.powerSpec(outputFolder=eventFolder, toDumpResponseImages=False)
