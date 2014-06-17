from armor import pattern
a=pattern.a 
a.load()

from armor import misc as m

reload(m)

Scales =[1,2,4,8,16,32,64,128]
L=[]

import time
print "time:", time.asctime()
t0  = time.time()

for scale in Scales:
    a.load()
    a1 = m.morlet2dFilter(a, scale=scale)
    L.append({  'scale' : scale,
                'sum'   : a1.matrix.sum(),
                'a1'    : a1,
             })
    print "scale:", scale
    print "sum:" , a1.matrix.sum()
    print "time spent so far (seconds):", int(time.time()-t0)
import matplotlib.pyplot as plt

plt.plot(scales, [v['sum'] for v in L])
plt.title(a.name+", morlet filter,\n" + str(Scales))
plt.show()


