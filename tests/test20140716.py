# test20140716.py
# constructing the objects for the report
"""
COMPREF:  march 20140311.0000
-1. COMPREF Intensity plot:Scale = 2
0.  COMPREF Intensity plot:Scale = 4
1.  COMPREF Max Intensity:Scale plot (Scale 1=0.05deg) 
    20140311.0000
2.  COMPREF Max Intensity:Intensity plot (corresp. to scale) 
3.  COMPREF:  Maximal Spectrum:(2-day average)
4.  COMPREF:  Total Spectrum:(2-day average)

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
from armor.initialise import *
#from armor import objects4 as ob
#from armor import pattern
#from armor import defaultParameters as dp
#import time, os, shutil, re
#import numpy as np
#import matplotlib.pyplot as plt
from armor.graphics import specContour
#import pickle, os

#   setups
inputFolderCOMPREF = 'C:/yau/1404716726.06COMPREF_Rainband_March_2014/'
inputFolderWRF= 'C:/yau/1404716726.08WRF_Rainband_March_2014/'

outputFolder = dp.root + 'labLogs2/july2014report/'
WRFwindow = (200,200,600,560)
sigmas  = [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128]

plt.close()
##########################################################
#   1. COMPREF
"""
COMPREF:  march 20140311.0000
-1. COMPREF Intensity plot:Scale = 2
0.  COMPREF Intensity plot:Scale = 4
1.  COMPREF Max Intensity:Scale plot (Scale 1=0.05deg) 
    20140311.0000
2.  COMPREF Max Intensity:Intensity plot (corresp. to scale) 
3.  COMPREF:  Maximal Spectrum:(2-day average)
4.  COMPREF:  Total Spectrum:(2-day average)
"""
m = ob.march2014('20140311.0000')[0]
m.load()
m.show(block=False)
m.saveImage(outputFolder+ '1.png')
m1 = m.getWindow(*WRFwindow)
m1.show(block=False)
m1.saveImage(outputFolder+'2.png')
m2 = m1.coarser().coarser()
m2.show(block=False)
m2.saveImage(outputFolder+'3.png')

x2 = m2.powerSpec(outputFolder=outputFolder, toPlotContours=True, toPlot3d=True)

resp = x2['responseImages']
resp.shape

for i in range(13):
    plt.imshow(resp[:,:,i], origin='lower')
    plt.colorbar()
    plt.title('Laplacian-of-Gaussian filter;  sigma=' + str(sigmas[i]))
    plt.savefig(outputFolder+m.name+ "_sigma" + str(sigmas[i])+ ".png")
    plt.show(block=False)

###
#   3.  COMPREF:  Maximal Spectrum(2-day average)
#   4.  COMPREF:  Total Spectrum(2-day average)

L = os.listdir(inputFolderCOMPREF)

Ltotal = [v for v in L if 'XYZ.pydump' in v]
Lmax   = [v for v in L if 'XYZmax.pydump' in v]
LtotalCOMPREF = Ltotal
LmaxCOMPREF   = Lmax

inputFolder = inputFolderCOMPREF
testName     = 'Contour_Spec_COMPREF_Rainband_March_2014'
# ----> contourPlotTest.py lines 19-56
#XYZoutsCOMPREF = XYZouts

##################

"""
WRF01-WRF14

5.  WRF01- 20140311.0300 - plot
6.  WRF01 intensity plot scale 2
7.  WRF01 intensity plot scale 4
8.  WRF01 Max Intensity Scale plot
9.  WRF01 Max intensity intensity plot
10  WRF01-14 max spec (2-day average)
11  WRF01-14 total spec(2-day average)
12. COMPREF v WRF:  Max spec
13. COMPREF v WRF:  Total spec


"""

w = marchwrf('20140311.0300')[0]
x2 = w.powerSpec(outputFolder=outputFolder, toPlotContours=True, toPlot3d=True)


resp = x2['responseImages']
resp.shape

for i in range(13):
    plt.imshow(resp[:,:,i], origin='lower')
    plt.colorbar()
    plt.title('Laplacian-of-Gaussian filter;  sigma=' + str(sigmas[i]))
    plt.savefig(outputFolder+w.name+ "_sigma" + str(sigmas[i])+ ".png")
    plt.show(block=False)

###
<<<<<<< HEAD
#   3.  COMPREF:  Maximal Spectrum:(2-day average)
#   4.  COMPREF:  Total Spectrum:(2-day average)
=======
#   3.  COMPREF:  Maximal Spectrum(2-day average)
#   4.  COMPREF:  Total Spectrum(2-day average)
>>>>>>> 671a249c7e45f5bad2458d21b544d73329551b60

#   imports
from armor.initialise import *
#from armor import pattern
#from armor import defaultParameters as dp
#import time, os, shutil, re
#import numpy as np
#import matplotlib.pyplot as plt
from armor.graphics import specContour
#import pickle, os

#   setups
inputFolderCOMPREF = 'C:/yau/1404716726.06COMPREF_Rainband_March_2014/'
inputFolderWRF= 'C:/yau/1404716726.08WRF_Rainband_March_2014/'
inputFolderCOMPREF = '/media/TOSHIBA EXT/ARMOR/labLogs2/july2014report/1404716726.06COMPREF_Rainband_March_2014/'
inputFolderWRF= 'C:/yau/1404716726.08WRF_Rainband_March_2014/'



outputFolder = dp.root + 'labLogs2/july2014report/'
WRFwindow = (200,200,600,560)
sigmas  = [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128]

inputFolder = inputFolderWRF
testName     = 'Contour_Spec_WRF_Rainband_March_2014'

L = os.listdir(inputFolder)
L = [v for v in L if 'WRF15' not in v]
L = [v for v in L if '0313.0300' not in v]
L = [v for v in L if '0313.0600' not in v]
L = [v for v in L if '0313.0900' not in v]

Ltotal = [v for v in L if 'XYZ.pydump' in v]
Lmax   = [v for v in L if 'XYZmax.pydump' in v]
Ltotal[:20]

Lmax[:20]

LtotalWRF= Ltotal
LmaxWRF  = Lmax

# ----> contourPlotTest.py lines 19-56
#XYZoutsRADAR = XYZouts

###########
#   dual plots
#   2014-07-16

def specContourWithXYZout(L, label="", vmin="", vmax=""):
    if label=="":
        label = str(time.time())
    plt.close()
    Z = np.zeros((13,8))
    for frameCount, fileName in enumerate(L):
        XYZ = pickle.load(open(inputFolder+fileName,'r'))
        #X   = XYZ['X']
        #Y   = XYZ['Y']
        Z1  = XYZ['Z']
        Z  += Z1
    XYZ['Z'] = Z/ (frameCount+1)
    #vmins = (np.log10(XYZ["Z"])* (Z>0)).min()
    #vmaxs = (np.log10(XYZ["Z"])* (Z>0)).max()
    X = XYZ['X']
    Y = XYZ['Y']
    XYZout = specContour.specContour(XYZ, display=True,  outputFolder=outputFolder, 
                                            #vmin=-1.0, vmax=3.6,
                                            vmin=vmin, vmax=vmax,
                                            fileName = testName+ label + "_average_of_" + str(frameCount+1) +'images.png')
    plt.close()
    print testName, "number of frames", frameCount+1
    return XYZout

XYZ1 = specContourWithXYZout(L=LmaxCOMPREF, label="COMPREF_max", vmin="", vmax="")
XYZ2 = specContourWithXYZout(L=LmaxWRF, label="WRF_max", vmin="", vmax="")

