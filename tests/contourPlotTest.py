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
vmins = [0,0]
vmaxs = [0,0]
labels =['total', 'max']
XYZs = [0,0]
count = 0
for count , L in enumerate([Ltotal, Lmax]):
    plt.close()
    Z = np.zeros((13,8))
    for frameCount, fileName in enumerate(L):
        XYZ = pickle.load(open(inputFolder+fileName,'r'))
        #X   = XYZ['X']
        #Y   = XYZ['Y']
        Z1  = XYZ['Z']
        Z  += Z1
    XYZ['Z'] = Z/ (frameCount+1)
    #vmins[count] = (np.log10(XYZ["Z"])* (Z>0)).min()
    #vmaxs[count] = (np.log10(XYZ["Z"])* (Z>0)).max()
    X = XYZ['X']
    Y = XYZ['Y']
    XYZout = specContour.specContour(XYZ, display=True,  outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images.png')
    plt.close()
    XYZs[count] = {'X': X.copy(), 'Y': Y.copy(), 'Z': Z.copy()}

specContour.specContour(XYZs[0], XYZs[1], outputFolder=outputFolder, fileName=testName+"total-max.png", vmin=-.8, vmax=3.17)
print testName, "number of frames", frameCount+1


##   set the "setMin/setMax"  - edit here
#vmax = max(vmaxs)
#vmin = min(vmins)
vmax = 3.17
vmin = -0.944
print vmin, vmax

for count , L in enumerate([Ltotal, Lmax]):
    plt.close()
    XYZ['Z'] = XYZs[count]['Z']
    #specContour.specContour(XYZ, display=True,  outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images.png')
    specContour.specContour(XYZ, display=True, vmin = vmin, vmax=vmax,
                            outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images_colourbars_matched_.png')



"""

#=============================================================================================

# WRFs all together
#inputFolder = dp.root + 'labLogs2/powerSpec3/1404707377.16COMPREF_Rainband_March_2014/'
inputFolder = "C:/yau/1404716726.08WRF_Rainband_March_2014/"
testName     = 'Contour_Spec_WRF_Rainband_March_2014'
outputFolder = inputFolder+  'meanSpecs/'

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
        XYZ = pickle.load(open(inputFolder+fileName,'r'))
        #X   = XYZ['X']
        #Y   = XYZ['Y']
        Z1  = XYZ['Z']
        Z  += Z1
    XYZ['Z'] = Z/ (frameCount+1)
    specContour.specContour(XYZ, display=True, outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images.png')
    XYZwrfs[count] = XYZ
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

"""
#############################################################################################################################################
#   individual WRFs

wrfLabels = [ 'WRF' + ("00"+str(v))[-2:] for v in range(1,21)]

inputFolder = "C:/yau/1404716726.08WRF_Rainband_March_2014/"

logFile = open (inputFolder + 'meanSpecs/' + str(time.time()) + 'log.txt','w')
logFile.write('Contour_Spec_WRF_Rainband_March_2014\n')
logFile.write('InputFolder:\t' + inputFolder + '\n')
logFile.write('WRF, Number of Frames, Diff in TotalSpec, Diff in MaxSpec\n')


for i in range(20):
    #try:

        testName     = 'Contour_Spec_WRF_Rainband_March_2014_' + wrfLabels[i]
        outputFolder = inputFolder+  'meanSpecs/' + wrfLabels[i] + '/'
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        L = os.listdir(inputFolder)
        L = [v for v in L if not ('0313.0300' in v or '0313.0600' in v or '0313.0900' in v) ]
        L = [v for v in L if wrfLabels[i] in v]     # pick out the outputs with from the WRF specified
        Ltotal = [v for v in L if 'XYZ.pydump' in v]
        Lmax   = [v for v in L if 'XYZmax.pydump' in v]
        L0=L
        print '\n'.join([str(v) for v in Ltotal])
        print "<-- Ltotal\n\n"
        time.sleep(2)
        print '\n'.join([str(v) for v in Lmax])
        print "<-- Lmax\n\n"
        time.sleep(3)
        
        labels =['total', 'max']
        XYZwrfs = [0,0]
        count = 0
        for count , L in enumerate([Ltotal, Lmax]):
            Z = np.zeros((13,8))
            plt.close()
            for frameCount, fileName in enumerate(L):
                XYZ = pickle.load(open(inputFolder+fileName,'r'))
                #X   = XYZ['X']
                #Y   = XYZ['Y']
                Z1  = XYZ['Z']
                Z  += Z1
            XYZ['Z'] = Z/ (frameCount+1)
            XYZout = specContour.specContour(XYZ, display=True, outputFolder=outputFolder, fileName = testName+ labels[count] + "_average_of_" + str(frameCount+1) +'images.png')
            XYZwrfs[count] = XYZ
    
            plt.close()
        
        XYZout, XYZwrfout = specContour.specContour(XYZs[0], XYZwrfs[0], outputFolder=outputFolder, fileName= "Total_Spec_COMPREF-versus-" + wrfLabels[i] +".png")
        plt.close()
        XYZout2, XYZwrfout2=specContour.specContour(XYZs[1], XYZwrfs[1], outputFolder=outputFolder, fileName= "Max_Spec_COMPREF-versus-" + wrfLabels[i] +".png")
        plt.close()
        print testName, "number of frames", frameCount+1
        logString = wrfLabels[i] + '\t' + str(frameCount+1) + '\t' + str(((XYZout['Z']-XYZwrfout['Z'])**2).sum()) + '\t' + str(((XYZout2['Z']-XYZwrfout2['Z'])**2).sum())
        logString +='\n'
        logFile.write(logString)
        logFile.flush()
    #except:
    #    print "Error!!!", wrfLabels[i], "count", count

logFile.close()

