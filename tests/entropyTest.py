#entropyTest.py
#2014-07-13

from armor.initialise import *
import numpy as np
outputFolderBase = dp.root + 'labLogs2/entropy/'
eventsList = wrfsList + radarsList

for event in eventsList:
    event.setOutputFolder(outputFolderBase+event.name+'/')
    if not os.path.exists(event.outputFolder):
        os.makerdirs(event.outputFolder)

loops = 100

#   shuffle!!
N = int(np.random.random()*len(eventsList))

eventsList  = eventsList[N:] + eventsList[:N]

for N in range(loops):     
    for event in eventsList:
        timeString_a = str(int(time.time()))
        a = event[ int(np.random.random()*len(event))]
        a.load()
        print "\n--------------------------------------"
        print event.name
        print a.name
        a.show()
        a.saveImage(event.outputFolder+timeString_a+a.name+'.png')
        an = a.entropyLocal(stepSize=(a.matrix.shape[0]//200)+1, 
                            outputFolder=event.outputFolder)
        an.outputPath = event.outputFolder+ timeString_a + "Entropy_Map_" + a.name + '.dat'
        an.imagePath = event.outputFolder+ timeString_a + "Entropy_Map_" + a.name + '.png'
        #an.saveMatrix()
        pickle.dump(an, open(event.outputFolder+ timeString_a + "Entropy_Map_" + a.name + '.pydump','w'))
        an.saveImage()
        plt.close()
