thisScript  = "roughwork20140523.py"

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
#   1
#dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_WRF"
#inputFolder = root + "labLogs/2014-5-26-modifiedMexicanHatTest17_kongreywrf/"

#   2
#dataSource  = "Numerical_Spectrum_for_Typhoon_Kong-Rey_RADAR"
#inputFolder = root + "labLogs/2014-5-26-modifiedMexicanHatTest17_kongreycompref/"

#   3
dataSource  =  "Numerical_Spectrum_for_Kong-Rey_COMPREF-sigmaPower2"
inputFolder = root + "labLogs/2014-5-26-modifiedMexicanHatTest10/"


#
############################################################################

outputFolder    = root+"labLogs/%d-%d-%d-modifiedMexicanHatTest17_%s/" % (dp.year, dp.month, dp.day, dataSource)
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
        
    print "sleeping 2 seconds"
    time.sleep(2)

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
    #   making the chart
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
    plt.title(dataSource+ " " + str(i) + "DBZ images\n"+\
              "x-axis:  response intensity(from 0 to 20)\n"+\
              "y-axis:  log_2(sigma)\n"+\
              "z-axis:  log_2(count)\n")
    plt.xlabel('response intensity')
    plt.ylabel('log2(sigma)')
    #   saving
    fig.savefig(outputFolder+ "3d_numspec_plot_log2scale.png", dpi=200)
    pickle.dump({"X": X, "Y":Y, "Z":Z}, open(outputFolder+'XYZ.pydump','w'))
    #pickle.dump(fig,open(outputFolder+"fig.pydump","w"))   #doesn't work

    logFile = open(timeString+"logs.txt",'w')
    logFile.write("i    = " + str(i)
    logFile.write("\noutputFile   = " + str(outputFile)
    logFile.write("\ndataSource   = " + str(dataSource)
    logFile.close()


fig.show()

open(outputFolder+thisScript,'a').write('\n\n   outputFolder\n   '+outputFolder)
"""
to see the final fig, go to the output folder, enter python interactive mode, and:

inputFolder=""  #<-- fix it yourself
dataSource=""   # ditto
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
ax.plot_wireframe(X, np.log2(Y), np.log2(Z), rstride=1, cstride=1)  #key line
plt.title(dataSource+ " " + str(i) + "DBZ images\n"+\
          "x-axis:  response intensity(from 0 to 20)\n"+\
          "y-axis:  log_2(sigma)\n"+\
          "z-axis:  log_2(count)\n")
plt.xlabel('response intensity')
plt.ylabel('log2(sigma)')
fig.show()



"""
print "outputFolder:", outputFolder
