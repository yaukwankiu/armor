from armor.graphics import specContour
from armor.initialise import *
import pickle, os
import numpy as np
import matplotlib.pyplot as plt

inputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs2/powerSpec3/1404707377.16COMPREF_Rainband_March_2014/'
outputFolder = 'testing/'
testName     = 'COMPREF_Rainband_11_March_2014'

L = os.listdir(inputFolder)
Ltotal = [v for v in L if 'XYZ.pydump' in v]
Lmax   = [v for v in L if 'XYZmax.pydump' in v]
L0=L

labels =['total', 'max']
XYZs = [0,0]
count = 0
for L in [Ltotal, Lmax]:    
    Z = np.zeros((13,8))
    for fileName in L:
        xyz = pickle.load(open(inputFolder+fileName,'r'))
        #X   = xyz['X']
        #Y   = xyz['Y']
        Z1  = xyz['Z']
        Z  += Z1
    xyz['Z'] = Z
    specContour.specContour(xyz, outputFolder=outputFolder, fileName = testName+ labels[count]+'.png')
    XYZs[count] = xyz
    plt.close()
    count+=1

specContour.specContour(XYZs[0], XYZs[1], outputFolder=outputFolder, fileName=testName+"total-max.png")

