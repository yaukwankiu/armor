#   modifiedMexicanHatTest19_contourPlots.py
#   two 3d charts in one

thisScript  = 'modifiedMexicanHatTest19_contourPlots.py'
#outputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs/2014-05-27-modifiedMexicanHatTest18_dual_3d_charts/'


outputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs/2014-6-9-' + 'modifiedMexicanHatTest19_contourPlots' + '/'
choice = 16
diffExaggeration    = 1



"""
1.  load xyz1   for compref(radar)
2.  load xyz2   for wrf
3.  fix xyz2
4.  charting 2 in one
"""
import shutil, time, os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import axes3d
#from armor import defaultParameters as dp

timeString = str(int(time.time()))
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
###########################################################################


inputFolder='/media/TOSHIBA EXT/ARMOR/labLogs/2014-5-26-modifiedMexicanHatTest17_Numerical_Spectrum_for_Typhoon_Kong-Rey_RADAR/'
dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_RADAR"
i=121


xyz  = pickle.load(open(inputFolder+'XYZ.pydump','r'))
X   = xyz['X']
Y   = xyz['Y']
Z   = xyz['Z']

#plt.close()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_wireframe(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
#plt.title(dataSource+ " " + str(i) + "DBZ images\n"+\
#          "x-axis:  response intensity(from 0 to 20)\n"+\
#          "y-axis:  log_2(sigma)\n"+\
#          "z-axis:  log_2(count)\n")
#plt.xlabel('response intensity')
#plt.ylabel('log2(sigma)')
#fig.show()

CS = plt.contour(X, np.log2(Y), np.log2(Z))
plt.clabel(CS, inline=1, fontsize=10)
plt.show()


xyz1    = xyz
dataSource1 = dataSource
i1=i
#################################################################################

if choice   == 2:
    i    = 56
    inputFolder  = '/media/TOSHIBA EXT/ARMOR/labLogs/2014-5-28-modifiedMexicanHatTest17_Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing2/'
    dataSource   = 'Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing2'
elif choice ==4:
    i    = 68
    inputFolder  = "/media/TOSHIBA EXT/ARMOR/labLogs/2014-5-28-modifiedMexicanHatTest17_Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing4/"
    dataSource   = "Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing4"
elif choice ==10:
    i    = 123
    inputFolder   = "/media/TOSHIBA EXT/ARMOR/labLogs/2014-5-28-modifiedMexicanHatTest17_Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing10/"
    dataSource   = "Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing10"
elif choice ==16:
    i    = 75
    inputFolder   = "/media/TOSHIBA EXT/ARMOR/labLogs/2014-5-28-modifiedMexicanHatTest17_Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing16/"
    dataSource   = "Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing16"
elif choice == 'WRF' or choice=='wrf':
    i    = 399
    inputFolder  = '/media/TOSHIBA EXT/ARMOR/labLogs/2014-6-6-modifiedMexicanHatTest17_Numerical_Spectrum_for_Typhoon_Kong-Rey_WRF/'
    dataSource   = 'Numerical_Spectrum_for_Typhoon_Kong-Rey_WRF'

xyz  = pickle.load(open(inputFolder+'XYZ.pydump','r'))
X   = xyz['X']
Y   = xyz['Y']
Z   = xyz['Z']

plt.close()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_wireframe(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
#plt.title(dataSource+ " " + str(i) + "DBZ images\n"+\
#          "x-axis:  response intensity(from 0 to 20)\n"+\
#          "y-axis:  log_2(sigma)\n"+\
#          "z-axis:  log_2(count)\n")
#plt.xlabel('response intensity')
#plt.ylabel('log2(sigma)')
#fig.show()

CS = plt.contour(X, np.log2(Y), np.log2(Z))
plt.clabel(CS, inline=1, fontsize=10)
plt.show()



xyz2=xyz
dataSource2 = dataSource
i2=i
##############################################################################

xyz2['X']  +=2  #in log2 scale
xyz2['Z']  +=2

plt.close()
fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
X   = xyz1['X']
Y   = xyz1['Y']
Z   = xyz1['Z'] *1./i1
Z1  = Z
#ax.plot_surface(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1, cmap='jet')  #key line
X   = xyz2['X']
Y   = xyz2['Y']
Z   = xyz2['Z'] *1./i2
Z2  = Z
#ax.plot_surface(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1, cmap='gray')  #key line

#ax.plot_wireframe(X, np.log2(Y), (np.log2(Z1)-np.log2(Z2))* diffExaggeration, rstride=1, cstride=1, colors="red")  #key line

#ax.plot_wireframe(X, np.log2(Y), np.zeros(X.shape), colors="green")
#plt.title("Blue: Averaged "+dataSource1+ " " + str(i1) + "DBZ images\n"+\
#          "Gray: Averaged "+dataSource2+ " " + str(i2) + "DBZ images\n"+\
#          "Red wireframe: " + str(diffExaggeration) + "x Difference of Blue and Gray"
#          "y-axis:  log_2(sigma)\n"+\
#          "z-axis:  log_2(count)\n")
#plt.xlabel('response intensity')
#plt.ylabel('log2(sigma)')
#for ang in range(270, 360+270, 10):
#    ax.azim = ang
#    fig.savefig(outputFolder+ dataSource1+"_" +dataSource2+ str(ax.azim) + '.png')
#   fig.show()

levelsMin   = int(max(np.log2(Z1).min(), np.log2(Z2).min()))
levelsMax   = int(max(np.log2(Z1).max(), np.log2(Z2).max()))+1
levels      = range(levelsMin, levelsMax,3)

#CS = plt.contour(X, np.log2(Y),  np.log2(Z1), levels=levels, cmap=cm.jet)
CS = plt.contour(X, np.log2(Y),  np.log2(Z1), levels=levels, colors="b")
plt.clabel(CS, inline=1, fontsize=10)
#CS = plt.contour(X, np.log2(Y), np.log2(Z2), levels=levels, cmap=cm.jet)
CS = plt.contour(X, np.log2(Y), np.log2(Z2), levels=levels, colors="g")
plt.clabel(CS, inline=1, fontsize=10)

CS = plt.contour(X, np.log2(Y), np.log2(Z1) - np.log2(Z2), levels=levels, colors="r")
plt.clabel(CS, inline=1, fontsize=10)

plt.colorbar()
plt.title("Blue. Averaged "+dataSource1+ " " + str(i1) + "DBZ images\n"+\
          "Green. Averaged "+dataSource2+ " " + str(i2) + "DBZ images\n"+\
          "Red. The Difference Above") 
plt.savefig(outputFolder+dataSource1+"_" +dataSource2+'.png')
plt.show()




#####

shutil.copyfile('/media/TOSHIBA EXT/ARMOR/python/armor/tests/' +thisScript, outputFolder + timeString+ thisScript)


