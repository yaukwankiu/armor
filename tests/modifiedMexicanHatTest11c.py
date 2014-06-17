# -*- coding: utf-8 -*-
"""
2014-05-08
step 1:
    若將我們的 Kong-Rey颱風的觀測（COMPREF）與模式（WRF）資料取Laplacian-of-Gaussian Numercial Spectra（畫圖時注意調整 sigma：WRF 的網格寬度為COMPREF 4倍），兩者垂直方向取對數scale
step 2:
    下一步：在COMPREF 除去high frequency spectral points [1,2] 之後，
    rescale 其point counts使之與WRF 之numerical spectrum相應以供比較
step 3:
    numerical integration to determine the actual areas under the curves
"""

#   step 1 #######################################################################
import numpy as np
import matplotlib.pyplot as plt

sigmasWRF       =	np.array(	[ 1,  2,  4,  5,  8 ,10, 16, 20, 32, 40, 64])
streamMeanWRF   =	np.array([12460.94006034629, 5905.22934055693, 2191.16766821571, 1552.5056166445515, 724.6954614149886, 495.5761803703676, 215.34047309551795, 143.68386315115586, 59.89102850781521, 38.51173570919996, 13.763560816523642])

sigmasCOMPREF   =		np.array([1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256])
streamMeanCOMPREF=	np.array([151227.20108002605, 53748.08786620686, 19251.82068970174, 13650.695913983964, 6510.785040990516, 4564.1056552763, 2182.380586834554, 1561.623532828618, 808.6806356928005, 600.1991351931141, 325.4054604756984, 243.53593974733363, 120.91569968680385, 79.64840385239307, 26.69538205745742])


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

##  log-log scale   2014-05-14

s1  = np.log(streamMeanCOMPREF2adjusted3)
s2  = np.log(streamMeanWRF)
plt.plot(np.log(sigmasCOMPREF2), s1)
plt.plot(np.log(sigmasWRF*4), s2)
plt.title("COMPREF(blue) and WRF(green) numerical spectra for L-O-G filter\n" +\
          "With high frequences [1,2] truncated and frequncies, Adjusted by volume\n" +\
          "- logarithmic-logarithmic scale")
plt.show()



