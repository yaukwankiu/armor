#   lablog-
#   version:  2014-01-27
"""
procedure:  
    1.  regress and find the vector field
    2.  cut out the specific "upstream region" templates
    3.  match with WRF outputs
    4.  document the results
"""
from armor import pattern
from armor.defaultParameters import *
from armor.misc import *
from armor import objects3 as ob
kongrey = ob.kongrey
wrf  = ob.kongreywrf2
wrf.fix()

k17 = kongrey[17]
k18 = kongrey[18]
k19 = kongrey[19]
k17.load()
k18.load()
k19.load()
print k18.dataTime
wrf.load('20130828.0300')
wrf.load('20130828.0000')
wrf.load('20130828.0600')
wrf.cutUnloaded()

x = k17.shiiba(k19, searchWindowWidth=21, searchWindowHeight=7, )
vect=x['vect']
mn = x['mn']
vect+=mn
vect.show()
vect    = (0,0)-vect


y = k18.shiiba(k19, searchWindowWidth=15, searchWindowHeight=9)
vect2=y['vect']
mn2 = y['mn']
vect2+=mn2
vect2.show()
vect2   = (0,0)-vect2

#   cut out the specific templates
taichungArea    = getFourCorners(taiChungCounty)
hualienArea     = getFourCorners(hualienCounty)
k18.drawCross(hualienArea, 20).showWithCoast()

hualienArea12   = vect2.semiLagrange(L=hualienArea, k=12)
hualienArea24   = vect2.semiLagrange(L=hualienArea, k=24)
k18.drawCross(hualienArea, 20).drawCross(hualienArea24, 10).showWithCoast()

hualienUpwindArea   = hualienArea + hualienArea12 + hualienArea24
hualienUpwindArea   = getRectangularHull(hualienUpwindArea).astype(int)

print hualienUpwindArea 

k18.drawRectangle(*hualienUpwindArea).showWithCoast()
k18.getWindow(*hualienUpwindArea).show()


#   match

#   document the results
