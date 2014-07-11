#powerSpecTest20140707.py

from armor.initialise import *

outputFolder = dp.root + "labLogs2/powerSpec3/"
#eventsList = [maywrf20, kongrey, kongreywrf, march, may, marchwrf, ]
#eventsList = [ kongrey, kongreywrf, march, may,marchwrf, kongreywrf, maywrf20 ]
#eventsList = [maywrf19, maywrf20, maywrf21, maywrf22, maywrf23, ]
eventsList = [kongrey, may, monsoon, kongreywrf]


preprocessType = "averaging"  # <-- edit here

COUNT = 0

eventFolder={}

for event in eventsList:
    timeString = str(time.time())
    eventFolder[event] = outputFolder +  preprocessType + "/" + timeString+ event.name + "/" 
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
        a.saveImage(outputFolder+str(time.time())+a.name+".png")
        if a.matrix.shape == (881,921):
            a1 = a.getWindow(*comprefCutRegion)
            if preprocessType == "averaging":
                a1=a1.coarser().coarser()      # <--  choice:  averaging 
            elif preprocessType == "sampling":
                a1.matrix = a1.matrix[::4, ::4] # <--  choice:  sampling
            a.matrix = a1.matrix
            a.nameBackup = a.name
            a.name +="sampling"
            print "a.matrix.shape", a.matrix.shape
            a.saveImage(outputFolder+str(time.time())+a.name+".png")
            bins=[0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.]              
        else:
            bins=[0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.]
            #bins = [0.03, 0.1, 0.3, 1., 3., 10., 30,. 100.]
        if COUNT < 2:
            COUNT +=1
            a.show()
        a.powerSpec(outputFolder=eventFolder[event], toDumpResponseImages=False, bins=bins)
        a.name = a.nameBackup                                        
