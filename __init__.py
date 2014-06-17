"""
I am completely rewriting this framework which was formerly known as weatherPattern. Yau Kwan Kiu, 801 CERB, NTU, 23-1-2013.

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
*   We encode the basic information associated with streams of weather patterns (e.g. COMPREF or WRF)
    with python class DBZ, DBZstreams, VectorField, etc., and define functions
    that act upon them in submodules.

== Future ideas ==
* speeding up with CUDA?
* integration with QGIS?
* incorporating tools from opencv and sympy, such as SIFT/SURF, symbolic manipulations, etc?
* multithreading ?
== Details ==

armor.  -   the main package
    BASIC CONSTRUCTIONS
        defaultParameters.py    - defining the default parameters (most of the case for COMPREF RADAR patterns from Central Weather Bureau)
        pattern.py     - module to define the main classes
            CLASSES:
                DBZ         - the basic class, to encode weather information from the Central Weather Bureau,
                              endowed with basic methods and wrappers for more complex functions
                VectorField - the class to represent vector fields
                DBZstream   - the class to represent streams/time series of DBZ patterns, endowed with basic methods
        pattern2.py     - extension to pattern
            CLASSES:
                DataStreamSet   -  a class with methods for sets of DBZstreams
        objects.py,     - defining some basic objects of interest, including the time series for kongrey and monsoon 
        objects2.py,
        objects3.py
        misc.py         - miscellaneous functions
        start.py,       - some test/demo scripts
        start2.py,
        start3.py   
        
        [... and other test scripts...]
    
    SUBMODULES:
        advection       - now defunct/under construction, module for semi-lagrangian advection
        basicio         - now defunct/under construction, supplementary functions for basio i/o's
        dataStreamTools - tools for the armor.pattern.DBZstream class
            kongrey.py      - defining the kongrey DBZstream objects (time series), for RADAR observations and WRF outputs
            makeVideo.py    - (not working) functions for creating videos from DBZstreams; uses opencv

        fft             - empty/defunct (see filter.fourier)
        filter          - filter functions
            fourier.py              - the fourier transform
            gabor.py                - the gabor filter
            laplacianOfGaussian.py  - the laplacian-of-gaussian filter
        geometry        - functions for geometric transformations and analyses
            boundaries.py
                components.py       - function to compute the connected components of a DBZ object
                edges.py            - functions for edge detecting (Sobel mask, etc)
                frames.py           - functions for putting several images("frames") together
                granulometry.py     - functions to perform granulometry
                localDeformation.py - empty
                localFeatures.py    - function to find local features with morphology and thresholding 
                moments.py          - module for computing Hu's invariant moments among other things
                morphology.py       - module for mathematical morphology
                regrid.py           - module for regridding (interpolating) 
                smoothCutoff.py     - (under construction) module to create a smooth cutoff of a given set
                transformedCorrelations.py      - module to compute the "transformed" or moment-normalised correlations
                transforms.py       - module to compute the linear/affine transformations of arrays
        hht             - empty/defunct
        hmm             - empty/defunct
        kmeans          - module for computing k-means clustering of an object
            clustering.py           - the main code
                                    - can think of more clustering tools in the future         
        patternMatching - module for pattern matching
            algorithm1.py           - plain correlation test (deprecated)
            algorithms.py           - main testing algorithms: 
                                      (works with pipeline.py below)
                                      (under active construction)
                                        1.  plain correlation, 
                                        2.  local coorelation with "nonstandard kernel" (see ARMOR RFP 2014)
                                        3.  ...
            pipeline.py             - (under active construction) filter-matching-scoring test 
                                        acts on armor.pattern2.DataStreamSet class
                                        calls algorithms.py
        shiiba          - module for ABLER-Shiiba algorithm
            regression2.py,         - modules for local/global/cfl free regression functions
            regression3.py,
            regressionCFLfree.py
            upWind.py               - as above, variant without the central difference/upwind recursion
        spectral        - module for spectral analysis
            hht.py                  - (incomplete) Hilbert-Huang transform (HHT), with only 1-d version so far
            scaleSpace.py           - module for scale space analysis
            signaltools.py          - a copy of a module from scipy with the same name
        tests           - notebook for various tests
        texture         - module for texture (gabor filter wavelet) analysis
        trec            - empty
        video           - (out of order?!) module for making videos from DBZstream's
        
You can see the above with 

import armor
help(armor)

...............Cheers, YKK 23-1-2013..............
...............updated YKK 14-03-2014

"""

__all__ = ['pattern', 'advection', 'basicio', 'fft', 'hht', 'hmm', 'kmeans', 'morphology', 'shiiba', 'wavelet']
test_attr = 'haha!'

