"""

from armor.shiiba import regressionCFLfree as cflfree
reload(cflfree)
from armor import analysis
reload(analysis)
from armor import pattern
reload(pattern)
from armor import objects
reload(objects)
from armor.objects import *

d1 = d.momentNormalise(e, centre=(3, 18), searchWindowWidth=13, useShiiba=True)


"""

print "loading module 'objects'"

from armor import pattern

dbz=pattern.DBZ
DBZ=pattern.DBZ

a = DBZ('20120612.0200')
b = DBZ('20120612.0230')
c = DBZ('20120612.0300')
d = DBZ('20120612.0210')
e = DBZ('20120612.0240')
f = DBZ('20120612.0310')

a.load()
b.load()
c.load()
d.load()
e.load()
f.load()

a.setThreshold(0)
b.setThreshold(0)
c.setThreshold(0)
d.setThreshold(0)
e.setThreshold(0)
f.setThreshold(0)


