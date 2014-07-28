#powerSpecLocalTest.py
thisScript = 'powerSpecLocalTest.py'

import shutil, os, time
from armor.initialise import *
##########################################################################
#   setting
#L = monsoon.list + march.list + kongrey.list + may.list 
L = pattern.DBZstream(dataFolder='/media/TOSHIBA EXT/CWB/hs1p/2014-07-22/',
                        forceAll=True) # 2014-07-26

for a in L:
    a.name= ('hs1p' + a.dataPath[-20:]).replace("/", "_")
    a.matrix*=100

bins=[0, 0.003, 0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.]
#sigmas  = [1, 2, 4, 8 ,16, 32, 64, 128, 256]
sigmas  = [8 ,16, 32, 64, 128, 256]
#
###########################################################################
outputFolder = dp.root+"labLogs2/powerSpecLocal/"
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

shutil.copyfile(dp.root+ 'python/armor/tests/'+  thisScript, outputFolder+str(time.time())+thisScript)

#plt.figure()

###

for count in range(30):
    I = int(3+np.random.random()*2)
    J = I
    N = int(np.random.random() * len(L))
    m = L[N]
    m.load()
    m.show()    #debug
    height, width = m.matrix.shape
    m.mask=0
    m.setThreshold(0)
    psResults={}
    maxSpecs={}
    for i in range(I):
        for j in range(J):
            m1 = m.getWindow(height*i//I, width*j//J, height//I, width//J)
            try:
                #########################################################################
                #   key line for computation
                psResults[(i,j)] = m1.powerSpec(scaleSpacePower=1.5, outputFolder=outputFolder, 
                                                bins=bins,
                                                sigmas  =sigmas,
                                                 responseThreshold=0.0 ,   
                                                 useOnlyPointsWithSignals=True,
                                                )
                #
                #######################################################################
            except:
                print "Error!\n\n==============", i, j
                time.sleep(2)
    
    m.load()
    for i in range(I):
        for j in range(J):
            m.drawRectangle(height*i//I, width*j//J, height//I-1, width//J-1, thickness=2,newObject=False)
    
    plt.figure()
    for i in range(I):
        for j in range(J):
            try:
    
                plt.subplot(I, J, 1+j+ J*(I-i-1))
                if 1+j+ J*(I-i-1)==2:
                    plt.title( m.name)
                if j==0 and i==0:
                    plt.xlabel('log2(sigma)')
                    plt.ylabel('log10(frequency)')
                
                """
                ####################################################################
                #   the key lines for plotting
                #
                sigmas = psResults[(i,j)]['sigmas']
                arr    = psResults[(i,j)]['maxSpec'].matrix
                hist, edges = np.histogram(arr, bins=[0]+ sigmas+[999999], )
                #plt.plot([0]+sigmas, np.log10(hist))
                plt.xlim([-1,8])
                plt.ylim([0,8])
                plt.plot([-1]+np.log2(sigmas).tolist(), np.log10(hist), "o-")
                #plt.plot([-1]+np.log2(sigmas).tolist(), hist)
                #
                #
                ####################################################################
                """

                ####################################################################
                #   the key lines for plotting
                #
                sigmas = psResults[(i,j)]['sigmas']
                responses    = psResults[(i,j)]['responseImages']
                hist         = responses.sum(axis=0).sum(axis=0).tolist()    #keeping the last axis = sigmas
                #plt.plot([0]+sigmas, np.log10(hist))
                logHist = np.log10(hist)
                plt.xlim([-1,8])
                plt.ylim([0,12])
                plt.plot(np.log2(sigmas).tolist(), logHist, "o-")
                #plt.plot([-1]+np.log2(sigmas).tolist(), hist)
                #
                #
                ####################################################################


            except KeyError:
                print "key error!", i, j
                plt.imshow(m.matrix, origin='lower', cmap = m.cmap, vmin=m.vmin,vmax=m.vmax)
                #plt.colorbar()
                plt.axis('off')
                time.sleep(2)
            except AttributeError:
                print "Attribute error!", i, j
                plt.imshow(m.matrix, origin='lower', cmap = m.cmap, vmin=m.vmin,vmax=m.vmax)
                #plt.colorbar()
                plt.axis('off')
                time.sleep(2)
            
    outputPath = outputFolder+ 'powerSpecLocal_' + m.dataTime + "_"+ str(int(time.time())) + '.jpg'
    print "saving to:, ", outputPath ,'\n\n###################################################'
    plt.savefig(outputPath, dpi=200)
    plt.show(block=False)
    m.matrix=np.ma.array([0]) #unload
    
