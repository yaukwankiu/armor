#ablerCFLregionTest.py
import time, os
from armor import pattern
dbz = pattern.DBZ
np  = pattern.np
dp  = pattern.dp
from armor.geometry import transforms as tr

a = pattern.a.load()
a = a.getWindow(400,400,200,200)

X, Y    = np.meshgrid(range(200), range(200))
I, J    = Y, X

X       = dbz(matrix=X)
Y       = dbz(matrix=Y)

a2  = a.affineTransform(tr.rotation(rad=np.pi/3), origin=a2.coordinateOrigin)
a2.showWith(a)

T   = tr.rotation(rad=np.pi/180 * 1)
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
diffxy.show()

