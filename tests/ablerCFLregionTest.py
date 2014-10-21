#ablerCFLregionTest.py
import time, os
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
dp  = pattern.dp
from armor.geometry import transforms as tr
outputFolder    = '/media/TOSHIBA EXT/ARMOR/labLogs2/'


a = pattern.a.load()
a = a.getWindow(400,400,200,200)

X, Y    = np.meshgrid(range(200), range(200))
I, J    = Y, X

X       = dbz(matrix=X)
Y       = dbz(matrix=Y)

a2  = a.affineTransform(tr.rotation(rad=np.pi/3), origin=a.coordinateOrigin)
a2.showWith(a)
#####################################
#   rotation

for N in range(0, 10):
    print N, ' degrees'
    T   = tr.rotation(rad=np.pi/180 * N)
    origin   = (100,100)
    X2  = X.affineTransform(T, origin=origin)
    Y2  = Y.affineTransform(T, origin=origin)

    diffx   = X2-X
    diffy   = Y2-Y

    diffx.setMaxMin()
    diffy.setMaxMin()
    diffx.showWith(diffy)

    diffx.matrix = (abs(diffx.matrix)<=1)
    diffx.setMaxMin()
    diffx.show()
    diffy.matrix = (abs(diffy.matrix)<=1)
    diffy.setMaxMin()
    #diffy.show()

    diffxy = diffx.copy()
    diffxy.matrix = diffx.matrix * diffy.matrix
    diffxy.cmap = 'jet'
    diffxy.name = 'CFL Region for A Rotation of '+str(N) + ' degrees'
    diffxy.show()
    diffxy.saveImage(outputFolder+'rotation_'+str(N)+'degrees.jpg')
    time.sleep(1)
###############################
#   stretching

for N in range(-4,10):
    print N, ' percents'
    T   = np.zeros((2,3))
    T[0,0] = 1+ 0.01*N
    T[1,1] = 1+ 0.01*N
    origin   = (100,100)
    X2  = X.affineTransform(T, origin=origin)
    Y2  = Y.affineTransform(T, origin=origin)

    diffx   = X2-X
    diffy   = Y2-Y

    diffx.setMaxMin()
    diffy.setMaxMin()
    diffx.showWith(diffy)

    diffx.matrix = (abs(diffx.matrix)<=1)
    diffx.setMaxMin()
    diffx.show()
    diffy.matrix = (abs(diffy.matrix)<=1)
    diffy.setMaxMin()
    #diffy.show()

    diffxy = diffx.copy()
    diffxy.matrix = diffx.matrix * diffy.matrix
    diffxy.cmap = 'jet'
    diffxy.name = 'CFL Region for stretching in both axes of '+str(N) + ' percents'
    diffxy.show()
    diffxy.saveImage(outputFolder+'stretching_'+str(N)+'percents.jpg')
    time.sleep(1)
