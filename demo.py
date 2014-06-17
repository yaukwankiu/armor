from armor.examples import *

a.copy().show2()
vect.U *=0.4
vect.V *=0.2
vect.show()





#####################
# useRecursion=True by default in armor.analysis
"""
>>> print x['README']
Results for shiiba global regression.  "mn" = shift, where the first coordinate is i=y, the second is j=x, "vect" =  total vector field, "deformation" = deformation vector field, "corr" = correlation between prediction and ground truth,  "prediction6"= prediction with 6 shiiba coeffs (instead of 9), "results" = list of (m,n), C, Rsquared in descending order of Rsquared
>>> xvect = x['vect']
>>> C = x['C']
>>> print C
[ -1.70539092e-04   1.80476099e-03   4.18378805e-03  -3.67649033e-03
   1.10427001e-04   5.23271952e-06   3.06938125e-05  -5.86734368e-06
  -2.27873478e-03]
>>> (xvect-vect).show()
('==computing the length of the vector field at centre for reference:==\nr_centre=', 'r_centre')
>>> diff = xvect-vect
>>> diff.U.max()
0.30550887034717777
>>> diff.V.max()
0.11895286896818602
>>> diff.V.var()
0.0023736533951793349
>>> diff.U.var()
0.002480375190512701
>>> diff.U.mean()
0.20739985637255659
>>> diff.V.mean()
0.0080580391030654046
>>> vect.U.max()
1.7600000000000002
>>> vect.V.max()
0.92000000000000015
>>> 
"""

a2 = a.advect(vect, scope= (9,9))
a2.show()
x = a.shiiba(a2)
print x.keys()
print x['README']
C = x['C']
xvect = x['vect']
print C
xvect.show()

#############################################
# this time:  useRecursion = False, scope = (9,9) by default
# doesn't look very good
"""
>>> C = x['C']
>>> xvect = x['vect']
>>> print C
[  4.22679027e-05   7.23340393e-04   8.50832813e-02  -2.25272575e-03
   1.15251370e-05   7.56251443e-01  -1.37582351e-04   2.06126764e-04
  -1.41492311e-02]
>>> xvect.show()
('==computing the length of the vector field at centre for reference:==\nr_centre=', 'r_centre')
>>> 
>>> x['mn']
(0, -1)


"""
x = a.shiiba(a2, useRecursion=False)
print x.keys()
print x['README']
C = x['C']
xvect = x['vect']
print C
xvect.show()

###################################################
# this time: fixed origin at (440,460) shiiba without recursion

"""
>>> C, Rsquared = x
>>> a1 = a.getPrediction(C)
>>> vect1 = regression.convert(C, a)
>>> vect1.show()
('==computing the length of the vector field at centre for reference:==\nr_centre=', 'r_centre')
>>> a1.copy().show2()

... coast data loaded from  ../data_temp/taiwanCoast.dat for  shiiba prediction for DBZ20120612.0200
>>> diff = vect1-vect
>>> diff.U.max()
0.30550887034717777
>>> diff.U.min()
0.10688081807710559
>>> diff.U.mean()
0.20739985637255659
>>> diff.U.var()
0.002480375190512701
>>> 
>>> diff.V.max()
0.11895286896818602
>>> diff.V.min()
-0.075060251183684423
>>> diff.V.mean()
0.0080580391030654046
>>> diff.V.var()
0.0023736533951793349
>>> diff.show()
('==computing the length of the vector field at centre for reference:==\nr_centre=', 'r_centre')
>>> a_cent.coordinateOrigin
(440, 460)
>>> C
array([ -1.70539092e-04,   1.80476099e-03,   4.18378805e-03,
        -3.67649033e-03,   1.10427001e-04,   5.23271952e-06,
         3.06938125e-05,  -5.86734368e-06,  -2.27873478e-03])
>>> 

"""

import armor.pattern as pattern
import armor.examples as examples
from armor.shiiba import regression3 as reg
from armor.shiiba import regression2 as regression

a = pattern.a.copy()
vect = examples.antiClockwiseField()
vect.U *=0.4
vect.V *=0.2
a2 = a.advect(vect, scope=(9,11))

a_cent = a.copy()
a_cent.coordinateOrigin = (440,460)

x = reg.regress(a_cent, a2)

print x

C, Rsquared = x

a1 = a.getPrediction(C)
vect1 = regression.convert(C, a)

vect1.show()
a1.copy().show2()
a1.corr(a2)


vdiff = vect1-vect
vdiff.U.max()
vdiff.U.min()
vdiff.U.mean()
vdiff.U.var()

vdiff.V.max()
vdiff.V.min()
vdiff.V.mean()
vdiff.V.var()

vdiff.show()

diff=  a1-a2
diff.vmax = diff.matrix.max()
diff.vmin = diff.matrix.min()
diff.matrix.max()
diff.matrix.min()
diff.matrix.mean()
diff.matrix.var()
diff.copy().show2()


