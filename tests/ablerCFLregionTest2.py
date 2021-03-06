#ablerCFLregionTest2.py
import time, os
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
dp  = pattern.dp
plt = pattern.plt
ma  = pattern.plt
from armor.geometry import transforms
from armor.geometry import transformedCorrelations as trc
outputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/ABLERCFLregion/'

arrayShape = np.array((200, 200))
m   = np.ma.zeros(arrayShape)
m.mask=False
m   = dbz(matrix=m)
m.show()
I, J = m.IJ()
dg  = trc.doubleGaussian(I, J, centroid_i=100, centroid_j=150, sigma_i=20, sigma_j=50, theta=1 )
DG  = dbz(matrix=np.ma.array(dg))
DG.vmin=0
DG.vmax=2
DG.show()
DG.saveImage(outputFolder+'DG_i100_j150_sigmai20_sigmaj50_theta1.png')

#   test case: one double gaussian
params = np.random.random(5)
params *= [200, 200, 20, 30, np.pi]
params += [0  ,   0,  5,  5,      0]
dg  = trc.doubleGaussian(I, J, *params)
DG  = dbz(matrix=np.ma.array(dg))
DG.vmin=0
DG.vmax=1
DG.name = 'Centroid = ' + str(params[0:2].round(2)) + ', sigma i,j = ' + str(params[2:4].round(2)) + ',\ntheta ' + str(params[4])
DG.show()

#   test case: 100 double gaussians
#dgs = []
#paramsList = []
#N   = 100
#for i in range(N):
#    params = np.random.random(5)
#    params *= [200, 200, 20, 30, np.pi]
#    params[2] = params[3]   #hack
#    paramsList.append(params)

dgs = []
paramsList = []
N=20
for i in range(N):                 #2014-11-04
    params = np.random.random(5)
    params *= [50, 50, 20, 15, np.pi]
    params[2] = params[3]   #hack
    params += [75, 75, 0, 0, 0]
    paramsList.append(params)

for i in range(N):
    dg  = trc.doubleGaussian(I, J, *paramsList[i])
    dgs.append(dg)

DG  = dbz(matrix = sum(dgs))
DG.setMaxMin()
DG.name='Sum of ' +str(N) + ' double gaussians'
DG.saveImage(outputFolder+'sumOf%dDoubleGaussians_'%N + str(int(time.time()))+'.jpg')
DG.show()

#   transformed - radiated from origin

def getParamsList(N= 100, maxRadius=10, minRadius=2):
    paramsList = []
    for i in range(N):
        params = np.random.random(5)
        params *= [200, 200, maxRadius-minRadius+1, maxRadius-minRadius+1, np.pi]
        params += [0,     0, minRadius, minRadius, 0]
        params[2] = params[3]   #hack
        #dg  = trc.doubleGaussian(I, J, *params)
        dgs.append(dg)
        paramsList.append(params)
    return paramsList

def affineTransform(dilation=1.0, rotation=0.0, translation=(0,0)):
    #   1. build the rotation matrix
    #   2. build the dilation matrix
    #   3. compute the transformation parameters
    #   4. transform the function
    pass
    
    
def doubleGaussianFunction(centroid_i, centroid_j, sigma_i, sigma_j, theta):
    cos = np.cos
    sin = np.sin
    def dg(I, J):
        I1  = I-centroid_i
        J1  = J-centroid_j
        I2  = cos(theta)*I1 - sin(theta)*J1
        J2  = sin(theta)*I1 + cos(theta)*J1
        I2 += centroid_i
        J2 += centroid_j

        return np.exp( - (I2-centroid_i)**2 / (2*sigma_i**2) \
                       - (J2-centroid_j)**2 / (2*sigma_j**2) )
    return dg

def doubleGaussianLandscape(paramsList):
    DGS = [doubleGaussianFunction(*v) for v in paramsList]
    def img(i,j):
        return sum([dg(i,j) for dg in DGS])
    return img

def constructImage(paramsList, display=False):
    DGS = [doubleGaussianFunction(*v) for v in paramsList]
    img = sum([dg(I,J) for dg in DGS])
    #plt.imshow(img, origin='lower') ; plt.show()
    img = np.ma.array(img)
    img.mask=False
    IMG = dbz(matrix=img)
    IMG.setMaxMin()
    if display:
        IMG.show()
    return IMG

def rotate(phi, paramsList=paramsList, centre=arrayShape/2,):
    cos = np.cos
    sin = np.sin
    def f(params):
        centroid_i, centroid_j, sigma_i, sigma_j, theta = params
        I1  = centroid_i - centre[0]
        J1  = centroid_j - centre[1]
        I2  = cos(phi)*I1 - sin(phi)*J1
        J2  = sin(phi)*I1 + cos(phi)*J1
        I2 += centre[0]
        J2 += centre[1]
        params = [I2, J2, sigma_i, sigma_j, theta+phi ]
        return params
    paramsList1 = [f(params) for params in paramsList]
    return paramsList1


def stretch(factor_i, factor_j, paramsList=paramsList, centre=arrayShape/2):
    def g(params):
        params1 = params.copy() #hack
        #print params
        params1 -= [centre[0], centre[1], 0, 0, 0]
        params1 *= [factor_i,  factor_j,  factor_i, factor_j, 1]
        params1 += [centre[0], centre[1], 0, 0, 0]
        #print params
        #time.sleep(1)
        return params1    
    paramsList1 = [g(params) for params in paramsList]
    return paramsList1

def translate(i, j, paramsList=paramsList):
    paramsList1 = [params+[i, j, 0,0,0] for params in paramsList]
    return paramsList1
    
    
def plotRsquared(p0=paramsList, transform='rotation', rlimit=0.05, step=0.002, *args, **kwargs):
    timeStamp = str(int(time.time()))
    IMG0    = constructImage(p0)
    plt.close()
    xs=np.arange(0, rlimit, step)
    ys=[]
    print '\n-----------------\n'
    print transform
    for x in xs:
        if transform=='rotation':
            p1  = rotate(phi=x, paramsList=p0, *args, **kwargs)
        elif transform=='stretching':
            p1  = stretch(1+x, 1-x, paramsList=p0, *args, **kwargs)
        IMG1 = constructImage(p1)
        IMG1.name = transform + str(x)
        IMG1.show()
        Rsquared  = IMG0.shiiba(IMG1, searchWindowWidth=9, searchWindowHeight=9)['Rsquared']
        print 'x:', x
        print 'Rsquared', Rsquared
        ys.append(Rsquared)
    plt.clf()
    plt.plot(xs, ys)
    title = transform+": Rsquared versus change" + "(radians)" * (transform=='rotation') + " relative stretching" *(transform=='stretching')
    plt.title(title)
    plt.savefig(outputFolder+ timeStamp + "_Rsquared versus change plot - " + transform + '.jpg')
    return ys


def transform_and_analyse(p0=paramsList, transform='rotation', rlimit=0.20, step=0.01, outputFolder=outputFolder, *args, **kwargs):
    timeStamp = str(int(time.time()))
    logFile = open(outputFolder+timeStamp+'_%s_logFile.txt'%transform,'a')
    logFile.write('#x, Rsquared, c1t, c2t, c4t, c5t, c1, c2, c4, c5\n')
    print 'output file:', outputFolder+timeStamp+'_%s_logFile.txt'%transform
    time.sleep(3)
    cos = np.cos
    sin = np.sin
    IMG0    = constructImage(p0)
    plt.close()
    xs=np.arange(0, rlimit, step)
    ys=[]
    print '\n-----------------\n'
    print transform
    for x in xs:
        if transform=='rotation':
            p1  = rotate(phi=x, paramsList=p0, *args, **kwargs)
            c1t = cos(x) -1         # theoretical "shiiba" C-values
            c2t = -sin(x)
            c4t = sin(x)
            c5t = cos(x) -1            

        elif transform=='stretching':
            p1  = stretch(1+x, 1-x, paramsList=p0, *args, **kwargs)
            c1t = 1+x -1            # theoretical "shiiba" C-values
            c2t = 0
            c4t = 0
            c5t = 1-x-1            

        IMG1 = constructImage(p1)
        IMG1.name = transform + str(x)
        #IMG1.show()
        res  = IMG0.shiiba(IMG1, searchWindowWidth=9, searchWindowHeight=9)
        Rsquared = res['Rsquared']
        C        = res['C']
        c1       = C[0]     # experimental "shiiba" C-values
        c2       = C[1]
        c4       = C[3]
        c5       = C[4]
        print 'x:', x
        print 'Rsquared', Rsquared
        ys.append(Rsquared)
        outputString = ', '.join([str(v) for v in [x, Rsquared, c1t, c2t, c4t, c5t, c1, c2, c4, c5]]) +'\n'
        print outputString
        logFile.write(outputString)
    plt.clf()
    plt.plot(xs, ys)
    title = transform+": Rsquared versus change" + "(radians)" * (transform=='rotation') + " relative stretching" *(transform=='stretching')
    plt.title(title)
    plt.savefig(outputFolder+ timeStamp + "_Rsquared versus change plot - " + transform + '.jpg')
    logFile.close()
    return ys


###########################################
#   tests
#   rotation
timeStamp = str(int(time.time()))
paramsList1 = rotate(np.pi/18, paramsList)
a   = constructImage(paramsList)
b   = constructImage(paramsList1)
c   = a-b
c.setMaxMin()

a.imagePath = outputFolder + timeStamp +"_a.jpg"
b.imagePath = outputFolder + timeStamp +"_b.jpg"
a.drawCross(newObject=False)
b.drawCross(newObject=False)
b.name='rotation'
a.saveImage()
b.saveImage()

#   stretch
timeStamp = str(int(time.time()))
paramsList1 = stretch(0.9, 1.1, paramsList)
a   = constructImage(paramsList)
b   = constructImage(paramsList1)
c   = a-b
c.setMaxMin()
c.show()

a.imagePath = outputFolder + timeStamp +"_a.jpg"
b.imagePath = outputFolder + timeStamp +"_b.jpg"
a.drawCross(newObject=False)
b.drawCross(newObject=False)
b.name='stretching'
a.saveImage()
b.saveImage()

#   test case ABLER
#ys1 = plotRsquared(paramsList, transform='rotation')
#ys2 = plotRsquared(paramsList, step=0.02, rlimit=0.5, transform='stretching')

#   looping
for count in range(10):
    paramsList = getParamsList(100)
    a   = constructImage(paramsList)
    #   rotation
    timeStamp = str(int(time.time()))
    paramsList1 = rotate(np.pi/18, paramsList)
    a   = constructImage(paramsList)
    b   = constructImage(paramsList1)
    a.name='original'
    b.name='rotation'
    #c   = a-b
    #c.setMaxMin()
    a.imagePath = outputFolder + timeStamp +"_a.jpg"
    b.imagePath = outputFolder + timeStamp +"_b.jpg"
    a.drawCross(newObject=False)
    b.drawCross(newObject=False)
    a.saveImage()
    b.saveImage()

    #   stretch
    timeStamp = str(int(time.time()))
    paramsList1 = stretch(0.9, 1.1, paramsList)
    a   = constructImage(paramsList)
    b   = constructImage(paramsList1)
    a.name='original'
    b.name='stretching'
    a.imagePath = outputFolder + timeStamp +"_a.jpg"
    b.imagePath = outputFolder + timeStamp +"_b.jpg"
    a.drawCross(newObject=False)
    b.drawCross(newObject=False)
    b.saveImage()
    ys1 = transform_and_analyse(paramsList, transform='rotation',  rlimit=0.20, step=0.01)
    ys1a = transform_and_analyse(paramsList, transform='rotation',  rlimit=0.05, step=0.002)
    ys2 = transform_and_analyse(paramsList, transform='stretching',  rlimit=0.20, step=0.01)
    ys2a = transform_and_analyse(paramsList, transform='stretching',  rlimit=0.05, step=0.002)

