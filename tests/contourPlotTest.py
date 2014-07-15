from armor.graphics import specContour
from armor.initialise import *
import pickle, os
import numpy as np
import matplotlib.pyplot as plt

# COMPREF
#inputFolder = dp.root + 'labLogs2/powerSpec3/1404707377.16COMPREF_Rainband_March_2014/'
inputFolder = "C:/yau/1404716726.06COMPREF_Rainband_March_2014/"
outputFolder = inputFolder+  'meanSpecs/'
testName     = 'Contour_Spec_COMPREF_Rainband_March_2014'

L = os.listdir(inputFolder)
Ltotal = [v for v in L if 'XYZ.pydump' in v]
Lmax   = [v for v in L if 'XYZmax.pydump' in v]
L0=L

labels =['total', 'max']
XYZs = [0,0]
count = 0
for count , L in enumerate([Ltotal, Lmax]):
    Z = np.zeros((13,8))
    for frameCount, fileName in enumerate(L):
        xyz = pickle.load(open(inputFolder+fileName,'r'))
        #X   = xyz['X']
        #Y   = xyz['Y']
        Z1  = xyz['Z']
        Z  += Z1
    xyz['Z'] = Z/ (frameCount+1)
    specContour.specContour(xyz, display=True, outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images.png')
    XYZs[count] = xyz
    plt.close()

specContour.specContour(XYZs[0], XYZs[1], outputFolder=outputFolder, fileName=testName+"total-max.png")
print testName, "number of frames", frameCount+1

#=============================================================================================

# WRf
#inputFolder = dp.root + 'labLogs2/powerSpec3/1404707377.16COMPREF_Rainband_March_2014/'
inputFolder = "C:/yau/1404716726.08WRF_Rainband_March_2014/"
outputFolder = inputFolder+  'meanSpecs/'
testName     = 'Contour_Spec_WRF_Rainband_March_2014'

L = os.listdir(inputFolder)
L = [v for v in L if not ('0313.0300' in v or '0313.0600' in v or '0313.0900' in v) ]
Ltotal = [v for v in L if 'XYZ.pydump' in v]
Lmax   = [v for v in L if 'XYZmax.pydump' in v]
L0=L

labels =['total', 'max']
XYZwrfs = [0,0]
count = 0
for count , L in enumerate([Ltotal, Lmax]):
    Z = np.zeros((13,8))
    plt.close()
    for frameCount, fileName in enumerate(L):
        xyz = pickle.load(open(inputFolder+fileName,'r'))
        #X   = xyz['X']
        #Y   = xyz['Y']
        Z1  = xyz['Z']
        Z  += Z1
    xyz['Z'] = Z/ (frameCount+1)
    specContour.specContour(xyz, display=True, outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images.png')
    XYZwrfs[count] = xyz
    plt.close()

specContour.specContour(XYZs[0], XYZs[1], outputFolder=outputFolder, fileName=testName+"total-max.png")
print testName, "number of frames", frameCount+1


######################################################################################################
#outputFolder= 'testing/'
plt.close()
specContour.specContour(XYZs[0], XYZwrfs[0], outputFolder=outputFolder, fileName="Rainband_march_2014_COMPREF-versus-WRF-total-Spec.png")
plt.close()
specContour.specContour(XYZs[1], XYZwrfs[1], outputFolder=outputFolder, fileName="Rainband_march_2014_COMPREF-versus-WRF-max-Spec.png")
plt.close()
