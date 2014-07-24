#powerSpecLocalTest.py

from armor.initialise import *
L = monsoon.list + march.list + kongrey.list + may.list 
###
outputFolder = dp.root+"labLogs2/powerSpecLocal/"
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

#plt.figure()

###

for count in range(30):
    I = int(3+np.random.random()*2)
    J = I
    N = int(np.random.random() * len(L))
    m = L[N]
    m.load()
    height, width = m.matrix.shape
    m.mask=0
    m.setThreshold(0)
    psResults={}
    maxSpecs={}
    for i in range(I):
        for j in range(J):
            m1 = m.getWindow(height*i//I, width*j//J, height//I, width//J)
            try:
                psResults[(i,j)] = m1.powerSpec(scaleSpacePower=2, outputFolder=outputFolder, 
                                                bins=[0, 0.003, 0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30.,100.],
                                                sigmas  = [1, 2, 4, 8 ,16, 32, 64, 128, 256],
                                                 responseThreshold=0.00 ,   
                                                 useOnlyPointsWithSignals=False,
                                                )
            except:
                print "Error!\n\n==============", i, j
                time.sleep(2)
    
    m.load()
    for i in range(I):
        for j in range(J):
            m.drawRectangle(height*i//I, width*j//J, height//I-1, width//J-1, newObject=False)
    
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
                
                sigmas = psResults[(i,j)]['sigmas']
                arr    = psResults[(i,j)]['maxSpec'].matrix
                hist, edges = np.histogram(arr, bins=[0]+ sigmas+[999999], )
                #plt.plot([0]+sigmas, np.log10(hist))
                plt.xlim([-1,8])
                plt.ylim([0,8])
                plt.plot([-1]+np.log2(sigmas).tolist(), np.log10(hist), "o-")
                #plt.plot([-1]+np.log2(sigmas).tolist(), hist)
            except KeyError:
                print "key error!", i, j
                plt.imshow(m.matrix, origin='lower', cmap = m.cmap, vmin=m.vmin,vmax=m.vmax)
                plt.colorbar()
                time.sleep(2)
    outputPath = outputFolder+ 'powerSpecLocal_' + m.dataTime + "_"+ str(int(time.time())) + '.jpg'
    print "saving to:, ", outputPath ,'\n\n###################################################'
    plt.savefig(outputPath, dpi=200)
    plt.show(block=False)
    m.matrix=np.ma.array([0]) #unload
    
