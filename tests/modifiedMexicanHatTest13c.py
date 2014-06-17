"""
2014-05-14
from modifiedMexicanHatTest11c.py

"""

#   step 1 #######################################################################
import numpy as np
import matplotlib.pyplot as plt

sigmasWRF       =	[1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256]
streamMeanWRF   =	[7409.220327605598, 3562.90438433474, 1422.2769389734751, 1027.9384682553884, 488.49372551120683, 333.32743684275295, 144.7859178516336, 96.65068596540995, 39.53496976443776, 25.15277040160953, 8.85970026197041, 5.151248971686913, 1.350387397474956, 0.6389661286267941, 0.11484552373963036]
sigmasCOMPREF   =	[1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256]
streamMeanCOMPREF=	[65619.21969966723, 24334.797165590895, 8940.372143450608, 6363.797461877879, 3014.4268343048398, 2084.903318558238, 947.5865842225744, 647.9512143724545, 289.9740481731289, 203.02679360214267, 103.8992032500717, 74.70764698469168, 33.2929266570803, 21.071496733959307, 6.7553689548435605]

sigmasWRF       = sigmasWRF[:-4]
streamMeanWRF   = streamMeanWRF[:-4]
sigmasWRF       =	np.array(sigmasWRF )
streamMeanWRF   =	np.array(streamMeanWRF )
sigmasCOMPREF   =	np.array(sigmasCOMPREF)
streamMeanCOMPREF=	np.array(streamMeanCOMPREF)

factor           = 1.*881*921/140/150/16
streamMeanWRF   *= factor


s1  = np.log(streamMeanCOMPREF)
s2  = np.log(streamMeanWRF)

plt.plot(sigmasCOMPREF, s1)
plt.plot(sigmasWRF*4, s2)
plt.title("COMPREF and WRF numerical spectra for L-O-G filter\n- logarithmic scale")
plt.show()

#   step 2 #################################################3

streamMeanCOMPREF1      = streamMeanCOMPREF[:2]
streamMeanCOMPREF2      = streamMeanCOMPREF[2:]
sigmasCOMPREF2          = sigmasCOMPREF[2:]
sum1                    = streamMeanCOMPREF1.sum()
sum2                    = streamMeanCOMPREF2.sum()
highFreqPercentage      = sum1 / (sum1+sum2)

streamMeanCOMPREF2adjusted  = streamMeanCOMPREF[2:] / (1-highFreqPercentage)

##test
sum3        = streamMeanWRF.sum()
sum4        = streamMeanCOMPREF2.sum()
streamMeanCOMPREF2adjusted2  = streamMeanCOMPREF2 * sum3/sum4 * 13./11.

print "sum3, sum4", sum3, sum4, 
print "streamMeanCOMPREF2adjusted", streamMeanCOMPREF2adjusted2
print "streamMeanWRF", streamMeanWRF

plt.plot(sigmasCOMPREF2, streamMeanCOMPREF2adjusted)
plt.plot(sigmasWRF*4, streamMeanWRF)
plt.title("COMPREF and WRF numerical spectra for L-O-G filter")
plt.show()


s1  = np.log(streamMeanCOMPREF2adjusted)
s2  = np.log(streamMeanWRF)
plt.plot(sigmasCOMPREF2, s1)
plt.plot(sigmasWRF*4, s2)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies Adjusted\n" +\
          "- logarithmic scale")
plt.show()

s1  = np.log(streamMeanCOMPREF2adjusted2)
s2  = np.log(streamMeanWRF)
plt.plot(sigmasCOMPREF2, s1)
plt.plot(sigmasWRF*4, s2)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies Adjusted\n" +\
          "- logarithmic scale")
plt.show()




plt.plot(sigmasCOMPREF2, streamMeanCOMPREF2adjusted2)
plt.plot(sigmasWRF*4, streamMeanWRF)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies Adjusted\n" +\
          "- natural scale")
plt.show()


#   step 3  ################################################################

sum5    = np.trapz(streamMeanWRF, sigmasWRF*4)
sum6    = np.trapz(streamMeanCOMPREF2, sigmasCOMPREF2)
streamMeanCOMPREF2adjusted3  = streamMeanCOMPREF2 * sum5/sum6
print "sum5, sum6 =", sum5, sum6

##  log scale
s1  = np.log(streamMeanCOMPREF2adjusted3)
s2  = np.log(streamMeanWRF)
plt.plot(sigmasCOMPREF2, s1)
plt.plot(sigmasWRF*4, s2)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies, Adjusted by volume\n" +\
          "- logarithmic scale")
plt.show()

##  natural scale
plt.plot(sigmasCOMPREF2, streamMeanCOMPREF2adjusted3)
plt.plot(sigmasWRF*4, streamMeanWRF)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies Adjusted by volume\n" +\
          "- natural scale")
plt.show()

##  log-log scale

s1  = np.log(streamMeanCOMPREF2adjusted3)
s2  = np.log(streamMeanWRF)
r1  = np.log(sigmasCOMPREF2)
r2  = np.log(sigmasWRF*4)
plt.plot(r1, s1)
plt.plot(r2, s2)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies, Adjusted by volume\n" +\
          "- log-log scale")
plt.show()


##  dual axes
#   codes adapted from http://matplotlib.org/examples/api/two_scales.html


#diffComprefWrf  = f1(t) - f2(t)

s1  = np.log2(streamMeanCOMPREF2adjusted3)
s2  = np.log2(streamMeanWRF)
r1  = np.log2(sigmasCOMPREF2)
r2  = np.log2(sigmasWRF*4)

t   = np.linspace(r1.min(), r1.max(), 100)
f1  = interp1d(r1, s1, kind='cubic')
f2  = interp1d(r2, s2, kind='cubic')

plt.plot(r1, s1)
plt.plot(r2, s2)
plt.plot(t, (f1(t) - f2(t))*10)
plt.plot(t,[0]*len(t), 'k')
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies, Adjusted by volume\n" +\
          "And their difference x 10 (red)- log-log (based 2)scale")
plt.show()

"""
fig, ax1 = plt.subplots()
ax1.plot(t, s1, 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('exp', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')


ax2 = ax1.twinx()
s2 = np.sin(2*np.pi*t)
ax2.plot(t, s2, 'r.')
ax2.set_ylabel('sin', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()
"""
