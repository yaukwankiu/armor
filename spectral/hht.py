# python codes for empirical hilbert-huang transform

from matplotlib import *
from numpy import *
#from scipy.interpolate import interp1d
from matplotlib import pyplot
from scipy import interpolate, arange
from scipy.signal import signaltools    # including convoluation and hilbert transform
import cmath

#extremaDetection([1,2,3,3,2,1,1,2,3,4,5,6,7,2,3,4,4,3,2,4,5,6,7,9,0])
def extremaDetection(data=[1,2,3,4,5], x=[0,1,2,3,4]):
    start = min(x)
    step = x[1] - x[0]
    upperEnvelop = [(start,data[0])]	#initialisation
    lowerEnvelop = [(start,data[0])]
    j = data[0]
    print (start,data[0]),
    newDirection = 0
    oldDirection = sign(data[1]-data[0])# =1 when the data is going up, 0 when flat
    cache = []       	# to store data for the case when there is a stationary point
    xcount = start
    for i in data[1:]:
        xcount+= step
        print (xcount,i),
        
        newDirection = sign(i-j)
        if newDirection == 0: 
           cache.append((xcount,i))
           j=i
           continue			# got a flat section, keep it in cache
        if (oldDirection == 1) and (newDirection == -1):	#got a max
            upperEnvelop += cache 
            cache = [(xcount,i)]
            oldDirection = newDirection
            print '!'
        if (oldDirection ==-1) and( newDirection == 1 ):	#got a min
            lowerEnvelop += cache
            cache = [(xcount,i)]
            oldDirection = newDirection
            print 'v'
        if oldDirection * newDirection == 1:		#equal but nonzero : clear cache
            cache = [(xcount,i)]
        j = i						#keep old datapoint
    upperEnvelop.append((xcount,data[-1]))
    lowerEnvelop.append((xcount,data[-1]))
    print upperEnvelop, lowerEnvelop
    return upperEnvelop, lowerEnvelop

## to construct the cubic spline

def cubicSpline(x, y):
    return interpolate.splrep(x,y)   

## to display the spline

def displaySpline(f, x, y):
    a = min(x)
    b = max(x)
    xnew = arange(a,b, (a-b)/50.0)
    ynew = interpolate.splev(xnew, f, der=0)
    pyplot.plot(xnew, ynew, '.', x, y, 'o')
    pyplot.title('displaySpline')
    pyplot.legend(['interpolation','data'])

## stoppage criterion:
def stoppage(y1,y2):
    y2=single(y2)
    SD = sum((y1-y2)**2 / y1**2)
    if SD < 0.2:
        return True
    else:
        return False
    
##getting the next mode

def getNextMode(y=[1,2,3,2,1], x=[0,1,2,3,4]):  # also called 'sifting' -
                                 #input:  a function;  output: the next mode y1
                                 #                       and the residue m=y-y1
    
    upper,lower = extremaDetection(y, x)
    Fu = cubicSpline([v[0] for v in upper], [v[1] for v in upper])
    Fl = cubicSpline([v[0] for v in lower], [v[1] for v in lower])
    xnew = arange( min(x), max(x), 0.1)
    ynew = interpolate.splev(xnew, F)
    ynew_u = interpolate.splev(xnew, Fu)
    ynew_l = interpolate.splev(xnew, Fl)
    ynew_m = (ynew_u + ynew_l) /2
    y1 = (ynew - ynew_m)   #first mode=original data interpolated - average trend
    return y1, ynew_m
 

#empirical mode decomposition (EMP)
def emp(y=[1,2,3,4,5]):       #input: a function;  output: a list of functions
    
    stoppage = False
    while stoppage == False:
        #########
        #  main loop
        #  F = cubicSpline(x,y) - already done before the function call
        stoppage = True
    return data


##############



##marginal spectrum
def marginalSpectrum(x):
    return x

def main():
      
  y = array([1,2,3,3,2,1,1,2,3,4,5,6,7,2,3,4,4,3,2,4,5,6,7,9,0])
  x = array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])

  y = array([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])
  x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13])


  y = array([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1])
  x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13])

  y = [1, 2, 1, 2, 1, 2, 1, 3, 0, 2, 1, 2, 2, 1, 2]
  x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14]

  y = [4, 3, 4, 2, 5, 1, 6, 3, 9, 0,10, 1,11, 4,13]
  x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14]

  y = [0, -0.1, 1, 1, 2, 2.1, 2, 3, 3, 2, 2, 0, 0, 5, 5, 2, 2, 6, 6]
  x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18]

  print 'x-y:',
  print len(x)-len(y)
  
  F = cubicSpline(x,y)
  upper,lower = extremaDetection(y)
  #Fu = cubicSpline([v[0] for v in upper], [v[1] for v in upper])
  #Fl = cubicSpline([v[0] for v in lower], [v[1] for v in lower])
  #xnew = arange( min(x), max(x), 0.1)
  #ynew = interpolate.splev(xnew, F)
  #ynew_u = interpolate.splev(xnew, Fu)
  #ynew_l = interpolate.splev(xnew, Fl)
  #ynew_m = (ynew_u + ynew_l) /2

  #y1 = (ynew - ynew_m)   #first mode=original data interpolated - average trend
  y1, ynew_m = getNextMode(ynew, xnew)
  
  pyplot.plot(x,y,'.', xnew,ynew,'-', xnew, ynew_u, '--', xnew, ynew_l, '--',
              xnew, ynew_m,'--', xnew, y1, '-', xnew, [0]*len(xnew), '-' )
  pyplot.legend(['data', 'interpolation', 'upper', 'lower', '"mean"','first mode'], loc='best')
  pyplot.show()

  #computing the analytic signal (x + i.hilbertTransformOf(x) )
  Hy1 = signaltools.hilbert(y1)
  #print Hy1

  #extracting the phase
  phase1 = [cmath.phase(i) for i in Hy1]
  pyplot.plot(xnew, phase1, '.')
  pyplot.title('phase plot for the first mode y1, from the analytic signal')
  pyplot.show()
  #plotting the instantaneous frequency omega = dtheta/dt
  omega1=[]
  for i in range(len(phase1)-1):
      om = (phase1[i+1]-phase1[i])
      if om > 3.15:
          om = om- 2*pi
      if om < -3.15:
          om += 2*pi
      
      om = om/(xnew[i+1]-xnew[i])
      omega1.append(om)
      
  pyplot.plot(xnew[10:-11], omega1[10:-10],'.')
  pyplot.title('instantanenous frequency omega1 for the first mode')
  pyplot.show()
  #print omega1
  #print xnew

  



if __name__ == "__main__":
    main()


