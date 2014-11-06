# to use cv2??
import cv2
# bla

# construct the data

from armor import objects4 as ob
kongrey = ob.kongrey
wrf     = ob.kongreywrf2

k   = kongrey[20].load() # just pick one
w   = wrf[40].load()
k.show()
w.show()

k1 = k.above(20)
w1 = w.above(10)
k1.show()
w1.show()

k2 = k1.connectedComponents()
w2 = w1.connectedComponents()
k2.show()
w2.show()

M = k2.matrix.max()+1
k_sizes = [k2.levelSet(v).matrix.sum() for v in range(M)]
k_ordered = sorted(range(M), key=lambda v:k2.levelSet(v).matrix.sum(), reverse=True )
for i in k_ordered[:10]:
    k2.levelSet(i).show(block=True)
k_region_selected = k2.levelSet(k_ordered[1])   # the biggest region but the background

N = w2.matrix.max()+1
w_sizes = [w2.levelSet(v).matrix.sum() for v in range(N)]
w_ordered = sorted(range(N), key=lambda v:w2.levelSet(v).matrix.sum(), reverse=True )
for i in w_ordered[:10]:
    w2.levelSet(i).show(block=True)
w_region_selected = w2.levelSet(w_ordered[1])   # the biggest region but the background

k4=k_region_selected
w4=w_region_selected

k4.matrix= k4.matrix.astype(int)
w4.matrix= w4.matrix.astype(int)

print k4.matrix
print w4.matrix
k4.show()
w4.show()

outputFolder= './'
k4.outputPath=outputFolder+ 'k4.dat'
k4.saveMatrix()
w4.outputPath=outputFolder+ 'w4.dat'
w4.saveMatrix()
k4.saveImage(outputFolder+'k4.png')
w4.saveImage(outputFolder+'w4.png')

