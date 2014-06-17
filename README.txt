see the doc string in __init__.py.  I won't be updating this any more. YKK, 23-1-2013.

I am completely rewriting this framework which was formerly known as weatherPattern.

Yau Kwan Kiu, 23-1-2013
[slightly updated 23-12-2013]

== Requirements ==
* python 2.7 or similar (python 2.5 will probably be okay, no python 3 please)
* numpy and scipy
* no sympy needed yet
* no opencv yet

== Philosophy ==
* python as a glue, [C or CUDA as the sword if need be]
* keep it simple in design and use
* cross platform  - at least running on pc and linux

== Design ==
* data structure:  
** class Pattern, wrapping numpy.ma.MaskArray [ http://docs.scipy.org/doc/numpy/reference/maskedarray.baseclass.html#the-maskedarray-class ], with identifying parameters (name, time, etc), parameters for I/O (path for input/output, params for screen display, etc), as well as simple I/O and standard methods for data processing and analysis
** module package operations acting on dbz.Pattern: dbz.advection, dbz.shiiba, dbz.wavelet, dbz.hht, dbz.kmeans, dbz.hmm

== Possible future direction ==
* speeding up with CUDA [not done]
* integration with QGIS [not done]

== Description ==
pattern.py  - defining the classes of objects
                pattern.DBZ - weather patterns with a rich class of methods to extract information from objects
                                and for objects to interact with each other
                pattern.VectorField - vector field objects, often obtained from DBZ objects
                pattern.DBZstream   - a stream of DBZ objects with I/O methods and other operations to make life easier
objects3.py - a class of sample objects

== How to use it ==
[on my computer, for example]
cd /media/KINGSTON/ARMOR/python   # cd into the ARMOR/python/ folder
python                           # enter the python interactive mode

>>> from armor import pattern
>>> a = pattern.a
>>> a.load()
>>> a.show()
>>> b = pattern.DBZ('20120612.0210')
>>> b.load()
>>> b.show()
>>> c = b-a
>>> c.show()
 
Note:   Most of the paramaters, folder and path settings as well as the default
        logitudinal and grid size settings are in defaultParameters.py


