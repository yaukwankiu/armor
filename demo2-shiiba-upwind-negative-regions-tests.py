"""
In this demo we
0.  get a = dbz('20120612.0200')
1.  get a rotational vector field vect
2.  transport a along vect
3.  regress a with a_rotated to get C
4.  compare the prediction a1 from (C,a) and a_rotated
5.  compare the vector field vect1 from regression from vect

6.  do the above again, now without recursion

Results - see the folder python/testing/test116/
"""

#############################################
# 1. basic case

from armor.examples import *

#  get a = dbz('20120612.0200'), 
#  setting the coordinate origin to (440, 460) to match the vector field
#
a.load()
a.coordinateOrigin = (440,460)

#  get a rotational vector field vect
vect = antiClockwiseField(magnitude = 0.002)  
vect.U *=2    # vect.V.max() = 0.88 ; vect.U.max() = 1.76

#  transport a along vect
a_rotated = a.advect(vect, scope = (11,11))

#  regress a with a_rotated to get C
x = a.shiiba(a_rotated)

#  compare the prediction a1 from (C,a) and a_rotated
#  compare the vector field vect1 from regression from vect

x.keys()
x['mn']
x['Rsquared']
x['corr']
x['C']

C       = x['C']
vect1   = x['vect']
vect2   = x['deformation']

vect1.show()
vect2.show()
(vect1-vect2).show()

a1 = x['prediction']
a2 = x['prediction6']

a1.copy().show2()
a1.corr(a_rotated)[0,1]
a2.corr(a_rotated)[0,1]


diff=  a1-a_rotated
diff.vmax = diff.matrix.max()
diff.vmin = diff.matrix.min()
diff.matrix.max()
diff.matrix.min()
diff.matrix.mean()
diff.matrix.var()
diff.copy().show2()

(abs(diff.matrix)>0).sum()
(abs(diff.matrix)>1).sum()
(abs(diff.matrix)>2).sum()
(abs(diff.matrix)>3).sum()
(abs(diff.matrix)>5).sum()
(abs(diff.matrix)>10).sum()
(abs(diff.matrix)>20).sum()




vec_diff = vect1-vect
vec_diff.U.max()
vec_diff.U.min()
vec_diff.U.mean()
vec_diff.U.var()

vec_diff.V.max()
vec_diff.V.min()
vec_diff.V.mean()
vec_diff.V.var()

vec_diff.show()

((vec_diff.U**2 + vec_diff.V **2)>0).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.001).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.01).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.1).sum()

###################################################################
# 2. do the above again, now without recursion



from armor.examples import *
a.load()
a.coordinateOrigin = (440,460)
vect = antiClockwiseField(magnitude = 0.002)  
vect.U *=2    # vect.V.max() = 0.88 ; vect.U.max() = 1.76
a_rotated = a.advect(vect, scope = (11,11))

x = a.shiiba(a_rotated, useRecursion=False)

#~ blablabla ~

x.keys()
x['mn']
x['Rsquared']
x['corr']
x['C']

C       = x['C']
vect1   = x['vect']
vect2   = x['deformation']

vect1.show()
vect2.show()
(vect1-vect2).show()

a1 = x['prediction']
a2 = x['prediction6']

a1.copy().show2()
a1.corr(a_rotated)[0,1]
a2.corr(a_rotated)[0,1]


diff=  a1-a_rotated
diff.vmax = diff.matrix.max()
diff.vmin = diff.matrix.min()
diff.matrix.max()
diff.matrix.min()
diff.matrix.mean()
diff.matrix.var()
diff.copy().show2()

(abs(diff.matrix)>0).sum()
(abs(diff.matrix)>1).sum()
(abs(diff.matrix)>2).sum()
(abs(diff.matrix)>3).sum()
(abs(diff.matrix)>5).sum()
(abs(diff.matrix)>10).sum()
(abs(diff.matrix)>20).sum()




vec_diff = vect1-vect
vec_diff.U.max()
vec_diff.U.min()
vec_diff.U.mean()
vec_diff.U.var()

vec_diff.V.max()
vec_diff.V.min()
vec_diff.V.mean()
vec_diff.V.var()

vec_diff.show()

((vec_diff.U**2 + vec_diff.V **2)>0).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.001).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.01).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.1).sum()
# ~~ blablabla ends ~~

(vect1.U>=0).sum()
(vect1.U<0).sum()
(vect1.V>=0).sum()
(vect1.V<0).sum()

(vect1.V<-0).sum()
(vect1.V<-0.1).sum()
(vect1.V<-0.2).sum()
(vect1.V<-0.3).sum()
(vect1.V<-1).sum()

diff = a1-a_rotated
diff.vmax = diff.matrix.max()
diff.vmin = diff.matrix.min()
diff.copy().show2()

abs(diff.matrix).max()

(abs(diff.matrix)>0).sum()
(abs(diff.matrix)>1).sum()
(abs(diff.matrix)>2).sum()
(abs(diff.matrix)>3).sum()
(abs(diff.matrix)>5).sum()
(abs(diff.matrix)>10).sum()
(abs(diff.matrix)>20).sum()

#############################################
# 3. this time, shiiba-regress with fixed origin, u, v>0 assumed

"""
>>> a1.corr(a_rotated)[0,1]
0.97635925959909309
>>> a2.corr(a_rotated)[0,1]
0.99747553351920326
>>> 
>>> vec_diff = vect1-vect
>>> vec_diff.U.max()
1.259356960447763
>>> vec_diff.U.min()
0.43497487359934239
>>> vec_diff.U.mean()
0.81931653367060997
>>> vec_diff.U.var()
0.034683233939640935
>>> 
>>> vec_diff.V.max()
0.59103386689824011
>>> vec_diff.V.min()
-0.41659398755264582
>>> vec_diff.V.mean()
0.037443212962887551
>>> vec_diff.V.var()
0.052663907316796078
>>> 
>>> vec_diff.show()
('==computing the length of the vector field at centre for reference:==\nr_centre=', 'r_centre')
>>> 
>>> ((vec_diff.U**2 + vec_diff.V **2)>0).sum()
148165
>>> ((vec_diff.U**2 + vec_diff.V **2)>0.001).sum()
148165
>>> ((vec_diff.U**2 + vec_diff.V **2)>0.01).sum()
148165
>>> ((vec_diff.U**2 + vec_diff.V **2)>0.1).sum()
148165
>>> # ~~ blablabla ends ~~
... 
>>> (vect1.U>=0).sum()
148165
>>> (vect1.U<0).sum()
0
>>> (vect1.V>=0).sum()
115268
>>> (vect1.V<0).sum()
32897
>>> 
>>> (vect1.V<-0).sum()
32897
>>> (vect1.V<-0.1).sum()
10955
>>> (vect1.V<-0.2).sum()
19
>>> (vect1.V<-0.3).sum()
0
>>> (vect1.V<-1).sum()
0
>>> 
>>> (abs(diff.matrix)>0).sum()
107096
>>> (abs(diff.matrix)>1).sum()
50169
>>> (abs(diff.matrix)>2).sum()
22048
>>> (abs(diff.matrix)>3).sum()
10569
>>> (abs(diff.matrix)>5).sum()
3090
>>> (abs(diff.matrix)>10).sum()
276
>>> (abs(diff.matrix)>20).sum()
2
>>> 
>>> diff.matrix.max()
21.093886493913097
>>> diff.matrix.min()
-20.483738269318422
>>> diff.matrix.var()
3.898480269202067
>>> diff.matrix.mean()
-0.0073237133916380761
>>>

"""



from armor.examples import *
#import armor.shiiba.regression2 as regression
#import armor.shiiba.regression3 as reg
import armor.shiiba.upWind as upWind

a.load()
a.coordinateOrigin = (440,460)
vect = antiClockwiseField(magnitude = 0.002)  
vect.U *=2    # vect.V.max() = 0.88 ; vect.U.max() = 1.76
a_rotated = a.advect(vect, scope = (11,11))

x = upWind.regress(a, a_rotated)


x.keys()
x['Rsquared']
x['C']

C       = x['C']
Rsquared= x['Rsquared']
 
vect1 = a.getVect(C)
C2    = C.copy()
C2[2] = 0       # deformation only
C2[5] = 0
C2[8] = 0
vect2 = a.getVect(C2)

vect1.show()
vect2.show()
(vect1-vect2).show()

#########

a1 = a.getPrediction(C)
a2 = a.getPrediction(C2)

a1.copy().show2()
a1.corr(a_rotated)[0,1]
a2.corr(a_rotated)[0,1]

#########

diff=  a1-a_rotated
diff.vmax = diff.matrix.max()
diff.vmin = diff.matrix.min()
diff.matrix.max()
diff.matrix.min()
diff.matrix.mean()
diff.matrix.var()
diff.copy().show2()

(abs(diff.matrix)>0).sum()
(abs(diff.matrix)>1).sum()
(abs(diff.matrix)>2).sum()
(abs(diff.matrix)>3).sum()
(abs(diff.matrix)>5).sum()
(abs(diff.matrix)>10).sum()
(abs(diff.matrix)>20).sum()


vec_diff = vect1-vect
vec_diff.U.max()
vec_diff.U.min()
vec_diff.U.mean()
vec_diff.U.var()

vec_diff.V.max()
vec_diff.V.min()
vec_diff.V.mean()
vec_diff.V.var()

vec_diff.show()

((vec_diff.U**2 + vec_diff.V **2)>0).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.001).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.01).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.1).sum()
# ~~ blablabla ends ~~

(vect1.U>=0).sum()
(vect1.U<0).sum()
(vect1.V>=0).sum()
(vect1.V<0).sum()

(vect1.V<-0).sum()
(vect1.V<-0.1).sum()
(vect1.V<-0.2).sum()
(vect1.V<-0.3).sum()
(vect1.V<-1).sum()

###################################
# marking out the regions where U, V are negative ...
vect1_U_negative = dbz(matrix=(1.*(vect1.U<0)), vmax = 1, vmin=-1, name = ' dbz(matrix=(vect1.V<0), vmax = 1, vmin=-1).show2()')

vect1_V_negative = dbz(matrix=(1.*(vect1.V<0)), vmax = 1, vmin=-1, name = ' dbz(matrix=(vect1.V<0), vmax = 1, vmin=-1).show2()')

vect1u = (1.*(vect1.U<0))
vect1v = (1.*(vect1.V<0))
# ... and then regress with mask

a_uneg = a.copy()
a_uneg.matrix.mask += (vect1u.view(np.ndarray) ==0)  # masking the region where u>=0
a_uneg.copy().show2()


a_vneg = a.copy()
a_vneg.matrix.mask += (vect1v.view(np.ndarray) ==0)  # masking the region where v>=0
a_vneg.copy().show2()

a_uneg.coordinateOrigin         # check
a_vneg.coordinateOrigin

from armor.shiiba import upWind
x_uneg = upWind.regress(a_uneg, a_rotated)
x_vneg = upWind.regress(a_vneg, a_rotated)

x_uneg
x_vneg

a1_uneg = a_uneg.predict( x_uneg['C'])
a1_vneg = a_vneg.predict( x_vneg['C'])

a1_uneg.copy().show2()
a1_vneg.copy().show2()

a1_uneg.corr(a_rotated)[0,1]
a1_vneg.corr(a_rotated)[0,1]

#######################################
# 4. do everything above again (shiiba-regress with fixed origin, u, v>0 assumed)
# this time with another image and its rotation:  dbz('20120612.0300')

from armor.examples import *
#import armor.shiiba.regression2 as regression
#import armor.shiiba.regression3 as reg
import armor.shiiba.upWind as upWind

import armor.shiiba.upWind as upWind
from armor.examples import *
##compare with local regression:
import numpy as np
import numpy.ma as ma
import armor.pattern as pattern
dbz= pattern.DBZ
a = dbz('20120612.0300')
a.load()
a.coordinateOrigin = (440,460)

vect = antiClockwiseField(magnitude = 0.002)  
vect.U *=2    # vect.V.max() = 0.88 ; vect.U.max() = 1.76
a_rotated = a.advect(vect, scope = (11,11))

import armor.shiiba.regressionCFLfree as cflfree
x_550= cflfree.regressLocal(a,a_rotated,550,500,100,100, searchWindowWidth=13,\
                            useRecursion=True, display=False)


                    
#x_550 = a.shiibaLocal(b=a_rotated,iRange=[550], jRange=[550])

##################################################
# 5. do as 3. (shiiba regress with fixed origin) above, 
#    and the flipped axes where appropriate and regress locally
#    and compute the correlations thereof
# 8 April 2013



from armor.examples import *
#import armor.shiiba.regression2 as regression
#import armor.shiiba.regression3 as reg
import armor.shiiba.upWind as upWind

a.load()
a.coordinateOrigin = (440,460)
vect = antiClockwiseField(magnitude = 0.002)  
vect.U *=2    # vect.V.max() = 0.88 ; vect.U.max() = 1.76
a_rotated = a.advect(vect, scope = (11,11))

x = upWind.regress(a, a_rotated)


x.keys()
x['Rsquared']
x['C']

C       = x['C']
Rsquared= x['Rsquared']
 
vect1 = a.getVect(C)
C2    = C.copy()
C2[2] = 0       # deformation only
C2[5] = 0
C2[8] = 0
vect2 = a.getVect(C2)

vect1.show()
vect2.show()
(vect1-vect2).show()

#########

a1 = a.getPrediction(C)
a2 = a.getPrediction(C2)

a1.copy().show2()
a1.corr(a_rotated)[0,1]
a2.corr(a_rotated)[0,1]

#########

diff=  a1-a_rotated
diff.vmax = diff.matrix.max()
diff.vmin = diff.matrix.min()
diff.matrix.max()
diff.matrix.min()
diff.matrix.mean()
diff.matrix.var()
diff.copy().show2()

(abs(diff.matrix)>0).sum()
(abs(diff.matrix)>1).sum()
(abs(diff.matrix)>2).sum()
(abs(diff.matrix)>3).sum()
(abs(diff.matrix)>5).sum()
(abs(diff.matrix)>10).sum()
(abs(diff.matrix)>20).sum()


vec_diff = vect1-vect
vec_diff.U.max()
vec_diff.U.min()
vec_diff.U.mean()
vec_diff.U.var()

vec_diff.V.max()
vec_diff.V.min()
vec_diff.V.mean()
vec_diff.V.var()

vec_diff.show()

((vec_diff.U**2 + vec_diff.V **2)>0).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.001).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.01).sum()
((vec_diff.U**2 + vec_diff.V **2)>0.1).sum()
# ~~ blablabla ends ~~

(vect1.U>=0).sum()
(vect1.U<0).sum()
(vect1.V>=0).sum()
(vect1.V<0).sum()

(vect1.V<-0).sum()
(vect1.V<-0.1).sum()
(vect1.V<-0.2).sum()
(vect1.V<-0.3).sum()
(vect1.V<-1).sum()

###################################
# marking out the regions where U, V are negative ...
vect1_U_negative = dbz(matrix=(1.*(vect1.U<0)), vmax = 1, vmin=-1, name = ' dbz(matrix=(vect1.V<0), vmax = 1, vmin=-1).show2()')

vect1_V_negative = dbz(matrix=(1.*(vect1.V<0)), vmax = 1, vmin=-1, name = ' dbz(matrix=(vect1.V<0), vmax = 1, vmin=-1).show2()')

# create local versions
xy = []
for i in range(881):
    for j in range(921):
        xy.append((i,j))
        
###
# window for u<0

vu = vect1_U_negative.matrix
vu0 = [p[0] for p in xy if vu[p]==1]
vu1 = [p[1] for p in xy if vu[p]==1]
bottom  = min(vu0)
top     = max(vu0)
left    = min(vu1)
right   = max(vu1)

print "top, bottom, left, right:", top, bottom, left, right
unegpic = vect1_U_negative.drawRectangle(bottom, left, top-bottom, right-left)
unegpic.name = "Region in which u<0: top=%d, bottom=%d, left=%d, right=%d" %\
                                    (top, bottom, left, right)
unegpic.show2()

a_uneg = a.getWindow(bottom, left, top-bottom, right-left)

###
# window for v<0
vv = vect1_V_negative.matrix
vv0 = [p[0] for p in xy if vv[p]==1]
vv1 = [p[1] for p in xy if vv[p]==1]
bottom  = min(vv0)
top     = max(vv0)
left    = min(vv1)
right   = max(vv1)

print "top, bottom, left, right:", top, bottom, left, right
vnegpic = vect1_V_negative.drawRectangle(bottom, left, top-bottom, right-left)
vnegpic.name = "Region in which v<0: top=%d, bottom=%d, left=%d, right=%d" %\
                                    (top, bottom, left, right)
vnegpic.show2()

a_vneg = a.getWindow(bottom, left, top-bottom, right-left)

###
# flip and regress local, cflfree, no iteration
a_uneg.show4()
a_vneg.show4()

from armor.shiiba import regressionCFLfree as cflfree

bottomu  = min(vu0)
topu     = max(vu0)
leftu    = min(vu1)
rightu   = max(vu1)


bottomv  = min(vv0)
topv     = max(vv0)
leftv    = min(vv1)
rightv   = max(vv1)

#a_uneg.matrix=np.fliplr(a_uneg.matrix)
#a_vneg.matrix=np.flipud(a_vneg.matrix)

###########
##  calling regression
#
xu = cflfree.regressLocal(a.fliplr(), a_rotated.fliplr(), 
                         bottom = 880-topu,  left   = 920-rightu, 
                         height = topu-bottomu, width = rightu-leftu,
                         searchWindowHeight=7, searchWindowWidth=15,
                         useRecursion=False)
                         
xv = cflfree.regressLocal(a.flipud(), a_rotated.flipud(), 
                         bottom = 880-topv,  left   = 920-rightv, 
                         height = topv-bottomv, width = rightv-leftv,
                         searchWindowHeight=7, searchWindowWidth=15,
                         useRecursion=False)

# control cases:
xu_control = cflfree.regressLocal(a, a_rotated, 
                         bottom = bottomu,  left   = leftu, 
                         height = topu-bottomu, width = rightu-leftu,
                         searchWindowHeight=7, searchWindowWidth=15,
                         useRecursion=False)
                         
xv_control = cflfree.regressLocal(a, a_rotated, 
                         bottom = bottomv, left=leftv ,
                         height = topv-bottomv, width = rightv-leftv,
                         searchWindowHeight=7, searchWindowWidth=15,
                         useRecursion=False)

xu[0]
xv[0]
xu_control[0]
xv_control[0]

"""
RESULTS OF THE ABOVE:

>>> 
>>> xu[0]
[(0, -1), array([  1.29718420e-04,  -5.21524644e-04,   7.57040247e-02,
         3.46731501e-03,   1.43798839e-04,   3.44152966e-01,
         9.88602713e-04,   3.05508466e-04,  -1.34620777e-01]), 0.99774731059254906]
>>> xv[0]
[(-1, 0), array([ -9.26057280e-04,  -1.95910249e-03,   4.56430082e-01,
         1.66033385e-03,   1.15658056e-05,   1.56651792e-01,
         1.37220435e-03,   1.44803815e-05,   1.08290191e-01]), 0.999408121450161]
>>> xu_control[0]
[(0, -1), array([  1.29718420e-04,  -5.21524644e-04,   7.57040247e-02,
         3.46731501e-03,   1.43798839e-04,   3.44152966e-01,
         9.88602713e-04,   3.05508466e-04,  -1.34620777e-01]), 0.99774731059254906]
>>> xv_control[0]
[(-1, 0), array([ -9.26057280e-04,  -1.95910249e-03,   4.56430082e-01,
         1.66033385e-03,   1.15658056e-05,   1.56651792e-01,
         1.37220435e-03,   1.44803815e-05,   1.08290191e-01]), 0.999408121450161]
>>> 
>>>
>>>
>>> aa= a.getWindow(bottomu,leftu, topu-bottomu, rightu-leftu)
>>> aa.show4()
>>> aa1=aa.predict(xu_control[0][1])
>>> aa1.show4()
>>> ab1 = a_rotated.getWindow(bottomu,leftu-1, topu-bottomu, rightu-leftu)
>>> ab1.show4()
>>> (aa1-ab1).show4()
>>> diff=aa1-ab1
>>> diff.vmax=diff.matrix.max()
>>> diff.show4()
>>> aa1.corr(ab1)[0,1]
0.99942123896388302
>>> 

"""
#
##
###########

