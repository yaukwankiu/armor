"""
I am completely rewriting this framework which was formerly known as weatherPattern. Yau Kwan Kiu, 802 CERB, NTU, 23-1-2013.

== Requirements ==
* python 2.7 or similar (python 2.5 will probably be okay, no python 3 please)
* numpy and scipy
* no sympy needed yet
* no opencv yet

== What's this? ==

ARMOR = Adjustment of Rainfall from MOdels using Radar, from WEather DEcision Technologies Inc, USA, based on the papers of [DuFran et al 2009], which builds on MAPLE (McGill Algorithm for Prediction by Lagrangian Extrapolation) based on [German, Zawadzki and Turner, 2001-2005] - see our 2012 Annual report to the Central Weather Bureau Taiwan for reference and details

This is our integrated ARMOR testing platform written in python.  We shall develop and test our algorithms together here.

== Philosophy ==
* python as a glue, C or CUDA as the sword if need be
* keep it simple in design and use
* cross platform  - at least running on pc and linux

== Design ==
* data structure:  
** new style class (for future flexibility) armor.pattern.DBZ, (and other patterns for the future!), wrapping numpy.ma.MaskArray [ http://docs.scipy.org/doc/numpy/reference/maskedarray.baseclass.html#the-maskedarray-class ], with identifying parameters (name, time, etc), parameters for I/O (path for input/output, params for screen display, etc), as well as simple I/O and standard methods for data processing and analysis
** module package operations acting on armor.Pattern: armor.advection, armor.shiiba, armor.wavelet, armor.hht, armor.kmeans, armor.hmm, armor.morphology

** try to be as python3 friendly as possible

== Roadmap ==
* speeding up with CUDA
* integration with QGIS
* incorporating tools from opencv and sympy, such as SIFT/SURF, symbolic manipulations, etc

You can see the above with 

import armor
help(armor)

...............Cheers, YKK 23-1-2013..............

"""

__all__ = ['pattern', 'advection', 'basicio', 'fft', 'hht', 'hmm', 'kmeans', 'morphology', 'shiiba', 'wavelet']
test_attr = 'haha!'

