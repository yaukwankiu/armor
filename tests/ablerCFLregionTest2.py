#ablerCFLregionTest2.py
import time, os
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
dp  = pattern.dp
from armor.geometry import transforms
from armor.geometry import transformedCorrelations as trc
outputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/ABLERCFLregion/'


m   = np.ma.zeros((200,200))
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
dgs = []
paramsList = []
N   = 100
for i in range(N):
    params = np.random.random(5)
    params *= [200, 200, 20, 30, np.pi]
    params[2] = params[3]   #hack
    dg  = trc.doubleGaussian(I, J, *params)
    dgs.append(dg)
    paramsList.append(params)

DG  = dbz(matrix = sum(dgs))
DG.setMaxMin()
DG.name='Sum of ' +str(N) + ' double gaussians'
DG.saveImage(outputFolder+'sumOf%dDoubleGaussians_'%N + str(int(time.time()))+'.jpg')
DG.show()

#   transformed - radiated from origin
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

def constructImage(paramsList):
    DGS = [doubleGaussianFunction(*v) for v in paramsList]
    img = sum([dg(I,J) for dg in DGS])
    plt.imshow(img) ; plt.show()
    img = np.ma.array(img)
    img.mask=False
    IMG = dbz(matrix=img)
    IMG.setMaxMin()
    IMG.show()
    return IMG


