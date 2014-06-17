from armor import pattern
from armor import objects3 as ob
import time
import pylab
pylab.ion()
pylab.draw()
kongrey = ob.kongrey

for k in kongrey:
    k.load()
    k.makeImage(closeAll=True)
    pylab.draw()
    pylab.pause(1)
    
    
"""
ion()


x = arange(0,2*pi,0.01)            # x-array
line, = plot(x,sin(x))
for i in arange(1,200):
    line.set_ydata(sin(x+i/10.0))  # update the data
    draw()                         # redraw the canvas

print 'FPS:' , 200/(time.time()-tstart)
"""
