#   preliminary tests for project proposal 2014

"""
Process
    1.  Apply ABLER to COMPREF to obtain the advection field
    2.  apply semi-Lagrangian extrapolation to compute the upwind regions
        for each river basin
    3.  divide the COMPREF and WRF outputs into upwind regions according to the
        results of point 2 above.        
    4.  filter each region with suitable filters (we need to test for the best combination)
        and use one of the methods we have developed for pattern matching (plain correlation,
        normalised/adjusted correlation, or invariant moment features)
    5.  combine the various features into an index and pick out the best WRF matches for the COMPREF
    6.  method validation with human eyes.

cd /media/KINGSTON/ARMOR/python
ipython

"""

from armor.defaultParameters import *
from armor import pattern
from armor import objects3 as ob

kongrey = ob.kongrey
k10     = kongrey[10]
k11     = kongrey[11]
k10.load()
k11.load()

x   = k10.shiiba(k11, searchWindowHeight=9, searchWindowWidth=13)
print "k10.shiibaResult['mn']", k10.shiibaResult['mn']
print "Rsquared", k10.shiibaResult['Rsquared']
print "vector field", x['vect'].show()

###

taipeiCounty    = (530, 500, 60, 60)
taichungCounty  = (475, 435, 40, 80)
tainanCounty    = (390, 400, 40, 50)
kaohsiungCounty = (360, 410, 70, 70)
yilanCounty     = (500, 500, 50, 50)
hualienCounty   = (410, 480, 100, 60)
kenting         = (319, 464)

#print   pattern.kentingLongitude, pattern.kentingLatitude
#k11.coordinatesToGrid(kenting)
#k11.drawCross(*kenting, radius=20).showWithCoast()

def getFourCorners(reg):
    i, j, height, width = reg
    return [(i,j), (i+height, j), (i, j+width), (i+height, j+width)]


def drawCrosses(a, L, radius=20):
    a1  = a.drawCross(*L[0], radius=radius)
    for i, j in L[1:]:
        a1=a1.drawCross(i,j, radius=radius)
    a1.showWithCoast()
    return a1        

vect    = x['vect']
mn      = x['mn']
vect.V  += mn[0]
vect.U  += mn[1]

vect.show()

vect.V  = -vect.V
vect.U  = -vect.U

H4      = getFourCorners(hualienCounty)
H4_6     = vect.semiLagrange(H4, k=6 )   #1 hours
H4_12    = vect.semiLagrange(H4, k=12)   #2 hours
H4_18    = vect.semiLagrange(H4, k=18)   #three hours
H4_24    = vect.semiLagrange(H4, k=24)   #Four hours
kenting_6   = vect.semiLagrange([kenting], k=6 )
kenting_12  = vect.semiLagrange([kenting], k=12)
kenting_18  = vect.semiLagrange([kenting], k=18)
kenting_24  = vect.semiLagrange([kenting], k=24)

k11_a   = drawCrosses(k11, H4, radius=20)
k11_a   = drawCrosses(k11_a, H4_6,  radius=10)
k11_a   = drawCrosses(k11_a, H4_12, radius=10)
k11_a   = drawCrosses(k11_a, H4_18, radius=10)
k11_a   = drawCrosses(k11_a, H4_24, radius=10)

k11_a   = drawCrosses(k11_a, [kenting] , radius=20)
k11_a   = drawCrosses(k11_a, kenting_6 , radius=10)
k11_a   = drawCrosses(k11_a, kenting_12, radius=10)
k11_a   = drawCrosses(k11_a, kenting_18, radius=10)
k11_a   = drawCrosses(k11_a, kenting_24, radius=10)

dbz = pattern.DBZ
a   = pattern.a
b   = dbz('20120612.0210')
c   = dbz('20120612.0220')
d   = dbz('20120612.0230')
e   = dbz('20120612.0240')
f   = dbz('20120612.0250')

a.load()
b.load()

b.shiiba(a, searchWindowHeight=5, searchWindowWidth=15)
vect2   = b.shiibaResult['vect']
mn2     = b.shiibaResult['mn']
vect2.V += mn2[0]
vect2.U += mn2[1]

H5       = H4[:2] + [kenting]    # five points
H5_6     = vect2.semiLagrange(H5, k=6 )   #1 hours
H5_12    = vect2.semiLagrange(H5, k=12)   #2 hours
H5_18    = vect2.semiLagrange(H5, k=18)   #three hours
H5_24    = vect2.semiLagrange(H5, k=24)   #Four hours

a0200   = a
a0200_a   = drawCrosses(a, H5, radius=20)
a0200_a   = drawCrosses(a0200_a, H5_6,  radius=10)
a0200_a   = drawCrosses(a0200_a, H5_12, radius=10)
a0200_a   = drawCrosses(a0200_a, H5_18, radius=10)
a0200_a   = drawCrosses(a0200_a, H5_24, radius=10)






