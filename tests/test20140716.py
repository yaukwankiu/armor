# test20140716.py
# constructing the objects for the report
"""
COMPREF:  march 20140311.0000
-1. COMPREF Intensity plotScale = 2
0.  COMPREF Intensity plotScale = 4
1.  COMPREF Max IntensityScale plot (Scale 1=0.05deg) 
    20140311.0000
2.  COMPREF Max IntensityIntensity plot (corresp. to scale) 
3.  COMPREF:  Maximal Spectrum(2-day average)
4.  COMPREF:  Total Spectrum(2-day average)

WRF01-WRF20

5.  WRF01- 20140311.0300 - plot
6.  WRF01 intensity plot scale 2
7.  WRF01 intensity plot scale 4
8.  WRF01 Max Intensity Scale plot
9.  WRF01 Max intensity intensity plot
10  WRF01-14 max spec (2-day average)
11  WRF01-14 total spec(2-day average)
12. COMPREF v WRF:  Max spec
13. COMPREF v WRF:  Total spec

WRF14 
14. WRF14
15. WRF14 intensity plot scale2
16  ...     scale 4
17. ...     max intensity scale plot
18. ...     max intensity intensity plot
19. ...     max spec (2-day average)
20. ...     total spec(2-day average)
21. COMPREF v WRF14 max spec
22. COMPREF v WRF14 total spec

"""
#   imports
from armor import objects4 as ob
from armor import pattern
from armor import defaultParameters as dp
import time, os, shutil, re
import numpy as np
import matplotlib.pyplot as plt
from armor.graphics import specContour
import pickle, os

#   setups
inputFolderCOMPREF = 'C:/yau/1404716726.06COMPREF_Rainband_March_2014/'
inputFolderWRF= 'C:/yau/1404716726.08WRF_Rainband_March_2014/'

outputFolder = dp.root + 'labLogs2/july2014report/'
WRFwindow = (200,200,600,560)
sigmas  = [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128]
##########################################################
#   1. COMPREF
"""
COMPREF:  march 20140311.0000
-1. COMPREF Intensity plotScale = 2
0.  COMPREF Intensity plotScale = 4
1.  COMPREF Max IntensityScale plot (Scale 1=0.05deg) 
    20140311.0000
2.  COMPREF Max IntensityIntensity plot (corresp. to scale) 
3.  COMPREF:  Maximal Spectrum(2-day average)
4.  COMPREF:  Total Spectrum(2-day average)
"""
m = ob.march2014('20140311.0000')[0]
m.load()
m.show()
m.saveImage(outputFolder+ '1.png')
m1 = m.getWindow(*WRFwindow)
m1.show()
m1.saveImage(outputFolder+'2.png')
m2 = m1.coarser().coarser()
m2.show()
m2.saveImage(outputFolder+'3.png')

x2 = m2.powerSpec(outputFolder=outputFolder, toPlotContours=True, toPlot3d=True)

resp = x2['responseImages']
resp.shape

for i in range(13):
    plt.imshow(resp[:,:,i], origin='lower')
    plt.colorbar()
    plt.title('Laplacian-of-Gaussian filter;  sigma=' + str(sigmas[i]))
    plt.savefig(outputFolder+m.name+ "_sigma" + str(sigmas[i])+ ".png")
    plt.show()

###
#   3.  COMPREF:  Maximal Spectrum(2-day average)
#   4.  COMPREF:  Total Spectrum(2-day average)

L = os.listdir(inputFolderCOMPREF)

Ltotal = [v for v in L if 'XYZ.pydump' in v]
Lmax   = [v for v in L if 'XYZmax.pydump' in v]

inputFolder = inputFolderCOMPREF
# ----> contourPlotTest.py










