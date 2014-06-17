"""
2014-05-16
from modifiedMexicanHatTest11d.py

"""

#   step 1 #######################################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import interpolate
sigmasWRF       =	[1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256]
streamMeanWRF   = [7409.220327605598, 3562.90438433474, 1422.2769389734751, 1027.9384682553884, 488.49372551120683, 333.32743684275295, 144.7859178516336, 96.65068596540995, 39.53496976443776, 25.15277040160953, 8.85970026197041, 5.151248971686913, 1.350387397474956, 0.6389661286267941, 0.11484552373963036]

#   compref - gaussian-filtered with sigma=10
sigmasCOMPREF   =	[1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256]
streamMeanCOMPREFfiltered=	[1993.727995932973, 1947.3956203558316, 1760.7290006381527, 1650.8805395581173, 1312.0354638968115, 1109.907031445121, 678.8742812522369, 505.41158145517403, 251.6407023738663, 182.13265183228373, 96.87821564224363, 70.11983626699457, 31.324129624638708, 19.7656570841436, 6.320385253963474]

#   compref - unfiltered
streamMeanCOMPREF=	[65619.21969966723, 24334.797165590895, 8940.372143450608, 6363.797461877879, 3014.4268343048398, 2084.903318558238, 947.5865842225744, 647.9512143724545, 289.9740481731289, 203.02679360214267, 103.8992032500717, 74.70764698469168, 33.2929266570803, 21.071496733959307, 6.7553689548435605]


sigmasWRF       = sigmasWRF[:-4]
streamMeanWRF   = streamMeanWRF[:-4]
sigmasWRF       =	np.array(sigmasWRF )
streamMeanWRF   =	np.array(streamMeanWRF )
sigmasCOMPREF   =	np.array(sigmasCOMPREF)
streamMeanCOMPREF=	np.array(streamMeanCOMPREF)
streamMeanCOMPREFfiltered   = np.array(streamMeanCOMPREFfiltered)

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


##  with difference
#diffComprefWrf  = f1(t) - f2(t)

s1  = np.log2(streamMeanCOMPREF2adjusted3)
s2  = np.log2(streamMeanWRF)
r1  = np.log2(sigmasCOMPREF2)
r2  = np.log2(sigmasWRF*4)

t   = np.linspace(r1.min(), r1.max(), 100)
f1  = interpolate.interp1d(r1, s1, kind='cubic')
f2  = interpolate.interp1d(r2, s2, kind='cubic')

plt.plot(r1, s1)
plt.plot(r2, s2)
plt.plot(t, (f1(t) - f2(t))*10)
plt.plot(t,[0]*len(t), 'k')
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies, Adjusted by volume\n" +\
          "And their difference x 10 (red)- log-log (based 2)scale")
plt.show()

##########################################################################################
##  plot radar-radar pre-filtered with various sigmas (2,4,10, etc)
#   2014-05-19

#   compref - gaussian-filtered

sigmasCOMPREF   =	[1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256]

#sigma=2
#streamMeanCOMPREFfiltered=	[18356.666825829154, 12953.149446514077, 6385.860830628616, 4733.454540339049, 2305.6584484338737, 1594.3888811611698, 735.1828243087518, 521.4745605311966, 270.4798057385379, 204.73876213678247, 114.36544360907304, 84.30793750876904, 38.744780363520924, 24.313291621444094, 7.455997973432501]
#sigmaPreprocessing  = 2

#sigma=4
#streamMeanCOMPREFfiltered=	[7803.871591019487, 6863.567333588634, 4691.665961978126, 3819.5001037041893, 2152.9699294554343, 1554.884642611616, 748.6356443240323, 529.8167777441868, 263.8201489404912, 195.1635591925086, 107.97382404329787, 79.98478197118261, 37.24115505099149, 23.496907458433768, 7.273694825320909]
#sigmaPreprocessing  = 4

#sigma=10
#streamMeanCOMPREFfiltered=	[1993.727995932973, 1947.3956203558316, 1760.7290006381527, 1650.8805395581173, 1312.0354638968115, 1109.907031445121, 678.8742812522369, 505.41158145517403, 251.6407023738663, 182.13265183228373, 96.87821564224363, 70.11983626699457, 31.324129624638708, 19.7656570841436, 6.320385253963474]
#sigmaPreprocessing  = 10

#sigma=16
streamMeanCOMPREFfiltered=	[816.3641385870271, 814.0762423317899, 762.2820659595036, 737.2588075828543, 657.2632309641889, 601.5875883935341, 449.8857092851208, 371.32755866190297, 228.1043332402935, 178.42906551575135, 104.04611499065814, 77.92551399299033, 36.727506105698, 23.25358821662107, 7.238594257772964]
sigmaPreprocessing  = 16

#   compref - unfiltered
streamMeanCOMPREF=	[65619.21969966723, 24334.797165590895, 8940.372143450608, 6363.797461877879, 3014.4268343048398, 2084.903318558238, 947.5865842225744, 647.9512143724545, 289.9740481731289, 203.02679360214267, 103.8992032500717, 74.70764698469168, 33.2929266570803, 21.071496733959307, 6.7553689548435605]

plotTitle   = "COMPREF(blue) and COMPREF-gaussian(sigma=%d) filtered(green) numerical spectra for L-O-G filter\n"% sigmaPreprocessing +\
          "With high frequences [1,2] truncated and frequncies, Adjusted by volume\n" +\
          "And their difference x 10 (red)- log-log (based 2)scale" 

print "\n============\nfilterd!"
print "sigma=", sigmaPreprocessing

sigmasCOMPREF   =	np.array(sigmasCOMPREF)
streamMeanCOMPREF=	np.array(streamMeanCOMPREF)
streamMeanCOMPREFfiltered   = np.array(streamMeanCOMPREFfiltered)
sum7    = np.trapz(streamMeanCOMPREF, sigmasCOMPREF)
sum8    = np.trapz(streamMeanCOMPREFfiltered, sigmasCOMPREF)

streamMeanCOMPREFfiltered_adjusted  = streamMeanCOMPREFfiltered * sum7/sum8

r1  = np.log2(sigmasCOMPREF)
r2  = r1
s1  = np.log2(streamMeanCOMPREF)
s2  = np.log2(streamMeanCOMPREFfiltered_adjusted)

t   = np.linspace(r1.min(), r1.max(), 100)
f1  = interpolate.interp1d(r1, s1, kind='cubic')
f2  = interpolate.interp1d(r2, s2, kind='cubic')

plt.plot(r1, s1)
plt.plot(r2, s2)
plt.plot(t, (f1(t) - f2(t))*10)
plt.plot(t,[0]*len(t), 'k')
plt.title(plotTitle)
plt.show()




"""
##  dual axes
#   codes adapted from http://matplotlib.org/examples/api/two_scales.html

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
