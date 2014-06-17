thisScript  = "powerSpec1_3d.py"

import pickle, os, shutil, time
from armor import pattern
from armor import defaultParameters as dp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
root = dp.rootFolder
timeString  = str(int(time.time()))
######################################################################
#
#   1
#dataSource = "Numerical_Spectrum_for_March2014_Rainband_WRF"
#inputFolder = root+ "labLogs/2014-5-14-modifiedMexicanHatTest13_2/"

#   2
#dataSource = "Numerical_Spectrum_for_March2014_Rainband"
#inputFolder = root+ "labLogs/2014-5-13-modifiedMexicanHatTest13/"

#   3
#dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey"
#inputFolder = root+ "labLogs/2014-5-7-modifiedMexicanHatTest10/"

#   4
#dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_WRF"
#inputFolder = root+ "labLogs/2014-5-7-modifiedMexicanHatTest9/"

############
#   2014-05-26

choice=1.2
if choice==1:
    #   1
    dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_RADAR"
    inputFolder = root + "labLogs/powerSpec1/1402639538/"
    colors      = 'blue'

elif choice == 1.2:
    #   1.2   RADAR - really taking 4x4 average rather than sampling
    dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_RADAR_4x4_average"
    inputFolder = root + "labLogs/powerSpec1/1402655563/"
    colors     = 'blue'
 

elif choice==2:
    #   2
    dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_WRF"
    inputFolder = root + "labLogs/powerSpec1/1402645004/"
    colors     = 'green'

elif choice==3:
    #   3
    dataSource  = "Numerical_Spectrum_for_Rainband_March2014_RADAR"
    inputFolder = root + "labLogs/powerSpec1/1402648758RADAR/"
    colors     = 'blue'

elif choice==4:
    #   4
    dataSource  = "Numerical_Spectrum_for_Rainband_March2014_WRF"
    inputFolder = root + "labLogs/powerSpec1/1402649322WRF/"
    colors     = 'green'



#dataSource  =  "Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing10"
#inputFolder = root + "labLogs/2014-5-16-modifiedMexicanHatTest15_march2014/"

#inputFolder = root+ "labLogs/2014-5-19-modifiedMexicanHatTest15_march2014_sigmaPreprocessing2/"

#inputFolder = root+ "labLogs/2014-5-19-modifiedMexicanHatTest15_march2014_sigmaPreprocessing4/"

#dataSource  =  "Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPreprocessing16"
#inputFolder = root+ "labLogs/2014-5-19-modifiedMexicanHatTest15_march2014_sigmaPreprocessing16/"
#
############################################################################

outputFolder    = root+"labLogs/powerSpec1/" + timeString + "_3dplots/"
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

shutil.copyfile(root+"python/armor/tests/"+thisScript, outputFolder+thisScript)
open(outputFolder+thisScript,'a').write('\n#   outputFolder:\n#   ' + outputFolder)

L   = os.listdir(inputFolder)
L   = [v for v in L if ".pydump" in v and "responseImagesList" in v]
L   = [inputFolder+v for v in L]

print len(L)
N   = len(L)
##  test/parameter setup
sigmas = []
for i in range(3):

    responseImages   = pickle.load(open(L[i],'r'))
    M       = responseImages[0]['matrix']
    sigma   = responseImages[0]['sigma']

    height, width   = M.shape
    for j in range(len(responseImages)):
        M       = responseImages[j]['matrix']
        M       = M*(M>0)
        sigma   = responseImages[j]['sigma']
        sigmas.append(sigma)
        print j, sigma, '\t', M.min(), '\t', M.max()
        
    print "sleeping .02 seconds"
    time.sleep(.02)

sigmas  = sorted(list(set(sigmas)))
### end test/parameter setup

#   makeing the 3d plot
X, Y    = np.meshgrid(range(20), sigmas)
I, J    = Y, X
Z       = np.zeros(X.shape)

for i in range(len(L)):

    responseImages   = pickle.load(open(L[i],'r'))
    M       = responseImages[0]['matrix']
    sigma   = responseImages[0]['sigma']
    z   = np.zeros(X.shape)
    for j in range(len(responseImages)):
        M       = responseImages[j]['matrix']
        M       = M*(M>0)
        sigma   = responseImages[j]['sigma']
        print j, sigma, '\t', M.min(), '\t', M.max()
        h   = np.histogram(M, bins=20, range=(0,20))
        z[j,:] = h[0]
    Z   += z
    #   making the charts

    #   3dplot
    #Z   /= len(L)   #2014-06-13
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
    ax.plot_surface(X, np.log2(Y), np.log2(Z/(i+1)), rstride=1, cstride=1)  #key line #2014-06-13
    plt.title(dataSource+ " " + str(i) + "DBZ images\n"+\
              "x-axis:  response intensity(from 0 to 20)\n"+\
              "y-axis:  log_2(sigma)\n"+\
              "z-axis:  log_2(count)\n")
    plt.xlabel('response intensity')
    plt.ylabel('log2(sigma)')
    fig.savefig(outputFolder+ "3d_numspec_plot_log2scale_transparent.png", dpi=200, transparent=True)
    fig.savefig(outputFolder+ "3d_numspec_plot_log2scale.png", dpi=200, transparent=False)

    #   contour plot
    plt.close()
    CS = plt.contour(X, np.log2(Y), np.log2(Z/(i+1)), colors=colors)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title(dataSource+' averaged over %d samples' %(i+1))
    plt.savefig(outputFolder+ "contourplot_transparent.png", dpi=200,transparent=True)
    plt.savefig(outputFolder+ "contourplot.png", dpi=200,transparent=False)

    pickle.dump({"X": X, "Y":Y, "Z":Z}, open(outputFolder+'XYZ.pydump','w'))
    pickle.dump({"X": X, "Y":Y, "Z":Z/(i+1)}, open(outputFolder+'XYZ.pydump','w')) #2014-06-13
    #pickle.dump(fig,open(outputFolder+"fig.pydump","w"))   #doesn't work

    logFile = open(outputFolder+timeString+"logs.txt",'w')
    logFile.write("i    = " + str(i+1))
    logFile.write("\noutputFolder  = '" + str(outputFolder) + "'")
    logFile.write("\ndataSource   = '" + str(dataSource) + "'")
    logFile.close()

print "time spent: ", time.time() - int(timeString)
fig.show()

open(outputFolder+thisScript,'a').write('\n\n   outputFolder\n   '+outputFolder)
"""
to see the final fig, go to the output folder, enter python interactive mode, and:

dataSource=""   #<-- fix it yourself

inputFolder=outputFolder  #<-- fix it yourself
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

xyz  = pickle.load(open(inputFolder+'XYZ.pydump','r'))
X   = xyz['X']
Y   = xyz['Y']
Z   = xyz['Z']

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
plt.title(dataSource+ " " + str(i) + "DBZ images\n"+\
          "x-axis:  response intensity(from 0 to 20)\n"+\
          "y-axis:  log_2(sigma)\n"+\
          "z-axis:  log_2(count)\n")
plt.xlabel('response intensity')
plt.ylabel('log2(sigma)')
fig.show()



"""
print "outputFolder:", outputFolder
