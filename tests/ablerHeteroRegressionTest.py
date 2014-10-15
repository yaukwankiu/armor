# ablerHeteroRegressionTest.py
# to test the parameters for any pair of data
#   0. imports and parameters
#   1. build the test examples
#   2. test regression
#   3. output


#   0. imports and parameters
import pickle
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from armor import pattern
from armor import defaultParameters as dp
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
T = np.array([[0.95,0.],[0.,1.05]])
T = tr.rotationMatrix(rad=-np.pi/360)*T
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
#x=a.shiiba(b)

###################################################################################
#intensityFactor = 1.00     #   <-- edit here
#axis1factor     = 0.995
#axis2factor     = 1.005
a=pattern.a.load()
a2 = a.getRectangle(400,400,200,200)
b=pattern.b.load()
b2 = b.getRectangle(400,400,200,200)
b3 = b.getRectangle(500,600,200,200)
c  = dbz('20120612.0800').load()
c2 = c.getRectangle(300,400,200,200)
c3 = c.getRectangle(200,200,200,200)
c4 = c.getRectangle(400,600,200,200)
d  = dbz('20120612.0900').load()
d2 = d.getRectangle(400,400,200,200)
d3 = d.getRectangle(500,500,200,200)

dbzs = [d2, d3, c4, b2,a2, b3, c2, c3, ]
for a in dbzs:
    a.backupMatrix(0)
angles =[0.1, 0.2, 0.5, 1.,]
#axis1factors = [0.8, 0.9, 0.95, 0.99, 0.995, 1., 1.005, 1.01, 1.05, 1.1, 1.2]
#axis2factors = [0.8, 0.9, 0.95, 0.99, 0.995, 1., 1.005, 1.01, 1.05, 1.1, 1.2]
#intensityFactors = [0.9, 0.95, 0.99, 0.995, 1., 1.005, 1.01, 1.05, 1.1]
axis1factors = [0.9, 0.95, 0.99, 0.995, 1.,  1.01,]
axis2factors = [0.8, 0.9, 0.95, 0.99, 0.995, 1., 1.1, ]
intensityFactors = [0.95, 1., 1.01,]

import itertools
testCases = itertools.product(dbzs, angles, axis1factors, axis2factors, intensityFactors)


testGoal = 'Axes Transformation, Translation and Rotation and intensity adjustment by intensity '
#a2.coordinateOrigin= (100,100)
print '\n========================\n'
a2.backupMatrix(0)
outputFolder= dp.root+'labLogs2/ABLERselectionIndex/'
outputString = "\n====================================\n"
outputString += time.asctime() +'\n'
outputString += "Test Goal: " + testGoal
outputString += "\na2.name"
outputString += "\tangle"
outputString += "\taxis1factor"
outputString += "\taxis2factor"
outputString += "\tintensityFactor"
outputString +="\tR-squared" 
outputString +="\tdisplacement" 
outputString +="\tT" 
outputString +="\t(m,n)" 
outputString += "\tC"
outputString +='\n'
open(outputFolder+'log.txt', 'a').write(outputString)

testCases = itertools.product(dbzs, angles, axis1factors, axis2factors, intensityFactors)
for a2, angle, axis1factor, axis2factor, intensityFactor in testCases:
    T = np.array([[axis1factor,0.],[0.,axis2factor]])
    T = tr.rotationMatrix(rad=-np.pi*angle/360)*T
    displacement = np.array([[1],[4]])
    T = np.hstack([T,displacement])

    a2.restoreMatrix(0)
    b2=a2.copy()
    b2= a2.affineTransform(T)
    b2.matrix *= intensityFactor
    
    print '----------'
    print 'angle:', angle*np.pi/180
    print 'T:'
    print T
    a2.saveImage(imagePath=outputFolder+'%d_a.png' % int(time.time()))
    b2.saveImage(imagePath=outputFolder+'%d_b.png' % int(time.time()))
    #a2.coordinateOrigin=a2.getCentroid()
    print 'b2.coordinateOrigin',b2.coordinateOrigin
    x2 = a2.shiiba(b2, searchWindowHeight=9, searchWindowWidth=13)# <-- key line
    vect = x2['vect'] + x2['mn']
    vect.imagePath = outputFolder+'%d_vect.png' % int(time.time())
    vect.saveImage()

    pickle.dump(x2, open(outputFolder+'%d_x.pydump' % int(time.time()),'w'))

    outputString = str(a2.name)
    outputString += '\t,' + str(angle)
    outputString += "\t," + str(axis1factor)
    outputString += "\t," + str(axis2factor)
    outputString += "\t," + str(intensityFactor)

    outputString += "\t,"+str(x2['Rsquared'])
    outputString += "\t,"+str(displacement.flatten())
    outputString +=  "\t," + ' '.join([str(v) for v in np.array(T).reshape(T.size)])
    outputString +=  "\t,"+str(x2['mn'])
    #outputString +=  "\t," + str(x2['C'].round(3).flatten()) #doesn't work
    outputString += "\t," + ' '.join([str(v) for v in np.array(x2['C'].round(3))])
    outputString += '\n'
    #open(outputFolder+'log.txt','a').write(outputString)
    # for excel
    outputString = outputString.replace('[','')
    outputString = outputString.replace(']','')
    outputString = outputString.replace(',','')
    outputString = outputString.replace('(','')
    outputString = outputString.replace(')','')
    open(outputFolder+'log.txt','a').write(outputString)

outputString += '\n=========================================================\n'
    
#   1. build the test examples
#   2. test regression
#   3. output


