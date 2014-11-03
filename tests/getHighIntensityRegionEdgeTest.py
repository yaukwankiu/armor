import itertools
from armor import pattern
from armor import objects4 as ob

outputFolder = '/media/TOSHIBA EXT/ARMOR/labLogs2/charts2_local_features_distribution/misc/'


def getXY(a, name='', thres=thres):
    a1 = a.levelSet(thres)
    a1.show()
    I, J = np.where(a.matrix==thres)
    I = I.compressed()
    J = J.compressed()
    X, Y = J, I
    coords = [(X[i], Y[i]) for i in range(len(X))]  
    coordsString  = '\n'.join([ str(X[i]) + "  " + str(Y[i]) for i in range(len(X))])
    fileName = 'coords' + str(thres) + name + "_"+ str(int(time.time()))+'.dat'
    open(outputFolder+ fileName, 'w').write(coordsString)
    print "changes written to ", fileName
    return {'X': X, "Y": Y}



thres = 35
a= pattern.a
a.load()
getXY(a, a.name, thres)

thres = 20
wrf  = ob.kongreywrf2
wrf.fix()
#k = wrf[212].load()
ks = [v for v in wrf if v.dataTime =='20130829.1200']
k  = ks[13]
k.above(thres-0.1).connectedComponents().show()
k1  = k.above(thres-0.1).connectedComponents()
k1.levelSet(2).show()
k2 = k1.levelSet(2) * k.levelSet(20)
k2.setMaxMin()
k2.show()

k3 = k1.levelSet(2)

k_   = k*-1
k_   = k_.above(-thres-0.1)
k4   = k_ * k3
k4.setMaxMin()
k4.show()
k4.matrix.sum()
d = getXY(k4, k.name + "threshold20_", 2)
