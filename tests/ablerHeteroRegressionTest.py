# ablerHeteroRegressionTest.py
# to test the parameters for any pair of data
#   0. imports and parameters
#   1. build the test examples
#   2. test regression
#   3. output


#   0. imports and parameters
import time
import numpy as np
import matplotlib.pyplot as plt
from armor import pattern
from armor.geometry import transforms as tr
dbz = pattern.DBZ

#X, Y = np.meshgrid(range(921), range(881))
#arr = np.exp(-(Y-400.)**2/3200-(X-400.)**2/8000)

X, Y = np.meshgrid(range(183), range(203))
arr = np.exp(-(Y-100.)**2/200-(X-100.)**2/500)

I, J = Y,X

plt.imshow(arr, origin='lower')
plt.show(block=False)
time.sleep(1)
a = dbz(matrix=np.ma.array(arr*50, mask=False, fill_value=-999.))
#a.matrix.mask = (a.matrix<1.)
a.show()
time.sleep(1)
T = np.array([[0.9,0.],[0.,1.1]])
T = tr.rotationMatrix(rad=-np.pi/18)*T
displacement = np.array([[1],[4]])
T = np.hstack([T,displacement])
print T
b = a.affineTransform(T)
#b.matrix.mask=(b.matrix<1.)
b.show()
time.sleep(1)

(b-a).show()
b.matrix.fill_value=-999.

a.matrix.mask  = (a.matrix<1.)
b.matrix.mask += (b.matrix<1.)

a.coordinateOrigin = a.getCentroid()
b.coordinateOrigin = b.getCentroid()

print "coordinateOrigins for a,b:", a.coordinateOrigin, b.coordinateOrigin
time.sleep(2)
#x=b.shiiba(a)

###################################################################################
print '\n========================\n'

a2=pattern.a.load()
b2=a2.copy()
b2= a2.affineTransform(T)
#a2.coordinateOrigin=a2.getCentroid()
print 'b2.coordinateOrigin',b2.coordinateOrigin
x2 = b2.shiiba(a2)


#   1. build the test examples
#   2. test regression
#   3. output


