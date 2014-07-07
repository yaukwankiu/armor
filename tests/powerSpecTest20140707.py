#powerSpecTest20140707.py

from armor.initialise import *
from armor import objects4 as ob

outputFolder = dp.root + "labLogs2/powerSpec3/"
#eventsList = [maywrf20, kongrey, kongreywrf, march, may, marchwrf, ]
eventsList = [ kongrey, kongreywrf, march, may,marchwrf, kongreywrf, maywrf20 ]

COUNT = 0

eventFolder={}

for event in eventsList:
    timeString = str(time.time())
    eventFolder[event] = outputFolder + timeString+ event.name + "/"
    os.makedirs(eventFolder[event])


maxLen = max([len(ev) for ev in eventsList])

for N in range(maxLen):
    
    for event in eventsList:
        try: 
            a = event[N]
        except IndexError:
            continue
        print "-----------"
        print event.name, a.name
        a.load()
        if a.matrix.shape == (881,921):
            a1 = a.getWindow(*comprefCutRegion)
            a1=a1.coarser().coarser()
            a.matrix = a1.matrix
            print "a.matrix.shape", a.matrix.shape
            bins=[0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.]  
            
        else:
            bins=[0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.]
            #bins = [0.03, 0.1, 0.3, 1., 3., 10., 30,. 100.]
        if COUNT < 2:
            COUNT +=1
            a.show()
        a.powerSpec(outputFolder=eventFolder[event], toDumpResponseImages=False)
