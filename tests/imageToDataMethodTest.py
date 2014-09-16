# still some work to do:  cleaning up the somewhat messy 35+ dbz regions.
from armor import pattern
dbz = pattern.DBZ
plt = pattern.plt
#
a = dbz('20140520.1700')
a.loadImage(type='charts2', rawImage=False) # i am showing the default arguments for clarity
#
b=a.copy()
b.load(type='charts2', rawImage=True)
#
a.show(block=True)
b.show(block=True)
#
if a.imageTopDown:
    origin = 'upper'
else:
    origin = 'lower'
plt.subplot(121)
plt.imshow(b.matrix, origin=origin)
plt.subplot(122)
plt.imshow(a.matrix, origin=origin)
plt.show()
