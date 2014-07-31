#start_image.py

bins = [0, 0.001, 0.003, 0.01, 0.3, 1., 3., 10., 30., 100.]
sigmas=[1, 2, 4, 8 , 16, 32, 64, 128, 256]

from armor import pattern
dbz = pattern.DBZ

a=dbz(dataTime='20140722.1300')
a.loadImage()
a.setMaxMin()

#a.powerSpec()

a1 = a.laplacianOfGaussian(sigma=1.5)
a1 = a1.copy()
a1.matrix= (abs(a1.matrix>1))
a1.setMaxMin()
a1.cmap ='jet'
a1.show()
###################################

from armor import pattern
dbz = pattern.DBZ

a=dbz(dataTime='20140722.1300')
a.loadImage()
a.setMaxMin()

from armor.geometry import fractal
reload(fractal)
res = fractal.hausdorffDimLocal(a, epsilon=1)


