# -*- coding: utf-8 -*-
# defining the basic object we will be working with
# adapted from :
#	/media/KINGSTON/ARMOR/ARMOR/python/weatherPattern.py ,
#	/media/KINGSTON/ARMOR/ARMOR/python/clustering.py ,  
#       /media/KINGSTON/ARMOR/2013/pythonJan2013/basics.py
# Yau Kwan Kiu, Room 801, 23-1-2013

##############################################################################################
#
#==== imports ================================================================================
# some of the stuff were moved to defaultParameters.py
import copy
import time, datetime
import pickle
import struct
import os
import re
import numpy
import numpy as np
import numpy.ma as ma
#import matplotlib
import matplotlib.pyplot as plt
#import scipy.misc.pilutil as smp
#import numpy.fft as fft
#import shutil
#import sys
from copy import deepcopy
try:
    from scipy import signal
    from scipy import interpolate
except ImportError:
    #print "Scipy not installed"
    pass

#==== setting up the global parameters========================================================

import defaultParameters as dp      # to keep a link    2014-03-12
import misc                         # to keep a link    2014-03-12
from defaultParameters import *     # bad habit but all these variables are prefixed with "default"
                                    # or at least i try to make them to
from misc import *                  # same - default functions
import colourbarQPESUMS                  # the colourbars for the Central Weather Bureau
import colourbarQPESUMSwhiteBackground   # the same as above, with white backgrounds


#==== defining the classes ===================================================================
class DBZ(object):      #python 2.7 (?) new style class, subclassing object
    """module predecessors:  basics.py;  weatherPattern.py
    NOTE: a DBZ object can be loaded from data or generated in run time (e.g. by translation, or
        other operations.)  There is flexibility in this.  In particular, the object is instantiated before
        its values loaded (either from file or from other computations).

    attributes (some to be defined at __init__, some afterwards):
        DBZ.name        - a string, the name of the instance, default = something like "DBZ20120612.0200"
        DBZ.matrix      - a numpy.ma.core.MaskedArray object
        DBZ.datatime    - a string like "20120612.0200" 
        DBZ.dataPath   - a string like "../data/dbz20120612.0200.dat"
                            can be relative (preferred) or absolute
        DBZ.outputPath  - a string like "../data/dbz20120612.0200.dat"
                            can be relative (preferred) or absolute

        DBZ.inputType   - a string to record the type of input file, most common is "txt",
                            which should be 2-dim arrays in text, separated by " " and "\n",
                            readable by numpy or matlab
                        - convention:  first row of data = bottom row of pixels
        DBZ.image       - I am not going to define this yet, since matplotlib.pyplot is pretty fast
        DBZ.imagePath   - a string like "../data/dbz20120612.0200.png"
                            can be relative (preferred) or absolute
                            default = "" (undefined)
        DBZ.dt          - time interval from the previous image  (default=1; how about 10mins = 1/6 hour??)
        DBZ.dy          - grid size, latitudinal, in km  (default =1; how about 0.0125 degree = how many kms?)
        DBZ.dx          - grid size, longitudinal, in km  (same as above)
        DBZ.timeStamp   - time stamp when the object was created
        DBZ.verbose     - whether print out a lot of stuff when we work with this object
        #################################################################
        # DBZ.inputFolder             - a string, self evident          #  <-- not used yet,
        # DBZ.outputFolder            - ditto                           #       perhaps not here
        # DBZ.outputFolderForImages   - ditto                           # 
        #################################################################
        DBZ.database                - a string, pointing to the database, somehow, for future
    methods:
        DBZ.load            - load into DBZ.matrix
        DBZ.save
        DBZ.saveImage
        DBZ.printToScreen

    use:
    >>> from armor import pattern
    >>> a = pattern.DBZ(dataTime="20120612.0200",name="", dt=1, dx=1, dy=1, dataPath="", imagePath="")
    >>> a.load()
    >>> a.printToScreen()

>>> import numpy as np
>>> import armor
>>> import armor.pattern as pattern
>>> dbz=pattern.DBZ
>>> a = dbz('20120612.0300')
DBZ20120612.0300initialised.  Use the command '___.load()' to load your data, and '__.printToScreen()' to print it to screen.
>>> b = dbz('20120612.0330')
DBZ20120612.0330initialised.  Use the command '___.load()' to load your data, and '__.printToScreen()' to print it to screen.
>>> a.load()
>>> b.load()# -*- coding: utf-8 -*-
>>> c=a-b
DBZ20120612.0300_minus_DBZ20120612.0330initialised.  Use the command '___.load()' to load your data, and '__.printToScreen()' to print it to screen.
>>> c.show()
>>> d=a*b
DBZ20120612.0300_times_DBZ20120612.0330initialised.  Use the command '___.load()' to load your data, and '__.printToScreen()' to print it to screen.
>>> d.show()
>>> 




    """
    def __init__(self, dataTime="NoneGiven", matrix=-999, name="", dt=1, dx=1, dy=1,\
                 dataPath="",outputPath ="",imagePath="",\
                  cmap=defaultCmap, vmin=-20, vmax=100, coordinateOrigin="default",\
                  coastDataPath="", relief100DataPath='', relief1000DataPath='',\
                  relief2000DataPath='', relief3000DataPath='',\
                  lowerLeftCornerLatitudeLongitude ='',\
                  upperRightCornerLatitudeLongitude ='',\
                  database="", 
                  allocateMemory=True,
                  imageTopDown="",
                  missingDataThreshold="",      #added 2014-02-20
                  verbose=False):
        self.timeStamp = str(int(time.time()))

        """
        Notes: 
        1.  cmap = colourbar of the dbz plot, need to find out how to plot it with
                CWB's colour scheme as specified in the modules colourbarQPESUMS
                and colourbarQPESUMSwhiteBackground
        2. coordinateOrigin:  normally either place at the centre of the picture 
                              or at Taichung Park
                                (24.145056°N 120.683329°E)
                              which translates to
                                (492, 455) in our 881x921 grid
                    reference: 
                    http://zh.wikipedia.org/wiki/%E8%87%BA%E4%B8%AD%E5%85%AC%E5%9C%92
                    /media/KINGSTON/ARMOR/2013/python/testing/test104/test104.py
                
        """

        ########
        #
        if name == "":
            name = "DBZ" + dataTime
        if type(matrix)==type(-999):                                # if matrix not given,
            # the following line is replaced 2013-09-07 due to memory waste
            #matrix     = ma.zeros((defaultHeight, defaultWidth))   # initialise with zeros
            matrix      = ma.zeros((1,1))
            matrix.mask = False
            matrix.fill_value = -999                               # -999 for missing values always
        if isinstance(matrix, ma.MaskedArray):
            matrix.fill_value = -999
        if missingDataThreshold=="":
            missingDataThreshold = defaultMissingDataThreshold  #added 2014-02-20
        if isinstance(matrix, np.ndarray) and not isinstance(matrix, ma.MaskedArray):
            matrix     = matrix.view(ma.MaskedArray)
            matrix.mask = (matrix<missingDataThreshold )
            matrix.fill_value = -999
        if dataPath =="":
            dataPath = defaultInputFolder + "COMPREF." + dataTime +".dat"
        if outputPath =="":
            outputPath = defaultOutputFolder + name + '_'+ self.timeStamp + ".dat"
        if imagePath =="":
            imagePath = defaultOutputFolderForImages + name + '_'+self.timeStamp + ".png"
        if coastDataPath == "":
            coastDataPath = defaultInputFolder + "taiwanCoast.dat"
        if relief100DataPath == "":
            relief100DataPath = defaultInputFolder + "relief100.dat"
        if relief1000DataPath == "":
            relief1000DataPath = defaultInputFolder + "relief1000.dat"
        if relief2000DataPath == "":
            relief2000DataPath = defaultInputFolder + "relief2000.dat"
        if relief3000DataPath == "":
            relief3000DataPath = defaultInputFolder + "relief3000.dat"
        if lowerLeftCornerLatitudeLongitude =="":
            lowerLeftCornerLatitudeLongitude = defaultLowerLeftCornerLatitudeLongitude
        if upperRightCornerLatitudeLongitude=="":
            upperRightCornerLatitudeLongitude = defaultUpperRightCornerLatitudeLongitude
        if imageTopDown=="":
            imageTopDown = defaultImageTopDown
        if database =="":                   # an extra parameter not yet used
            database = defaultDatabase
        
        ###############################################################################
        # if matrix shape = (881, 921) then by default the origin at Taichung Park
        #                                   (24.145056°N 120.683329°E)
        #                                or   (492, 455) in our grid
        # else the centre is the origin by default
        ###############################################################################
        if coordinateOrigin == "default":  #default
            if matrix.shape == (881, 921) or matrix.size<10:  # hack
                coordinateOrigin = (492, 455)
            else:
                coordinateOrigin = (matrix.shape[0]//2, matrix.shape[1]//2)
        elif coordinateOrigin == "centre" or coordinateOrigin=="center":
            coordinateOrigin = (matrix.shape[0]//2, matrix.shape[1]//2)
        elif (coordinateOrigin == 'Taichung' or \
             coordinateOrigin == 'Taichung Park' or\
             coordinateOrigin == 'taichungpark') and matrix.shape==(881,921):
            coordinateOrigin = (492,455)

        #coordinateOrigin = (0,0)       # switch it off - will implement coordinate Origin later
             
        if verbose:
            print "------------------------------------------------------------------"
            print "armor.pattern.DBZ:\nname, dt, dx, dy, dataPath, imagePath ="
            print                      name, dt, dx, dy, dataPath, imagePath
        #
        ########
        self.matrix     = matrix
        self.dataTime   = dataTime
        self.name       = name
        self.dt         = dt                #retrospective
        self.dx         = dx                #grid size
        self.dy         = dy
        self.outputFolder= defaultOutputFolder
        self.dataPath   = dataPath
        self.outputPath = outputPath
        self.imagePath  = imagePath
        self.coastDataPath      = coastDataPath
        self.relief100DataPath  = relief100DataPath
        self.relief1000DataPath = relief1000DataPath
        self.relief2000DataPath = relief2000DataPath
        self.relief3000DataPath = relief3000DataPath
        self.lowerLeftCornerLatitudeLongitude = lowerLeftCornerLatitudeLongitude
        self.upperRightCornerLatitudeLongitude = upperRightCornerLatitudeLongitude
        self.database   = database
        self.cmap       = cmap
        self.vmin       = vmin              # min and max for makeImage()
        self.vmax       = vmax
        self.coordinateOrigin = coordinateOrigin
        self.O          = self.coordinateOrigin  #alise, no guarentee
        self.imageTopDown       = imageTopDown
        self.missingDataThreshold = missingDataThreshold
        self.verbose    = verbose
        #self.matrix_backups = []            # for storage
        #if verbose:
        #    print(self.name + "initialised.  Use the command '___.load()' to load your data, " +\
        #                  "and '__.printToScreen()' to print it to screen.")

#################################################################################
# basic operator overloads

    def __call__(self, i=-999, j=-999, display=False):
        if i ==-999 and j ==-999:
            height, width = self.matrix.shape
            h = int(height**.5 /2)
            w = int(width**.5 /2)
            print self.matrix.filled().astype(int)[height//2-h:height//2+h,\
                                                    width//2-w: width//2+w]
            return self.matrix.filled().astype(int)
        else:
            """
            returns interpolated value
            """
            arr= self.matrix
            i0 = int(i)
            j0 = int(j)
            i1 = i0 + 1
            j1 = j0 + 1
            i_frac = i % 1
            j_frac = j % 1
            f00 = arr[i0,j0]
            f01 = arr[i0,j1]
            f10 = arr[i1,j0]
            f11 = arr[i1,j1]
            interpolated_value = (1-i_frac)*(1-j_frac) * f00 + \
                                 (1-i_frac)*(  j_frac) * f01 + \
                                 (  i_frac)*(1-j_frac) * f10 + \
                                 (  i_frac)*(  j_frac) * f11 

            if display:
                print i_frac, j_frac, f00, f01, f10, f11
            return interpolated_value


    def __add__(self, DBZ2):
        """defining the addition of two pattern.DBZ objects
        c.f. http://docs.python.org/release/2.5.2/ref/numeric-types.html
        can move to CUDA in the future
        """
        return  DBZ(dataTime=self.dataTime, matrix=self.matrix+DBZ2.matrix,\
                    name=self.name+"_plus_"+DBZ2.name, \
                    dt=self.dt, dx=self.dx, dy=self.dy,\
                    dataPath  =self.outputPath+"_plus_"+DBZ2.name+".dat",\
                    outputPath=self.outputPath+"_plus_"+DBZ2.name+".dat",\
                    imagePath =self.imagePath +"_plus_"+DBZ2.name+".png",\
                    database  =self.database,\
                    cmap=self.cmap, verbose=self.verbose)

    def __sub__(self, DBZ2):
        """defining the subtraction of two pattern.DBZ objects
        c.f. http://docs.python.org/release/2.5.2/ref/numeric-types.html
        can move to CUDA in the future
        """
        return  DBZ(dataTime=self.dataTime, matrix=self.matrix-DBZ2.matrix,\
                    name=self.name+"_minus_"+DBZ2.name, \
                    dt=self.dt, dx=self.dx, dy=self.dy,\
                    dataPath  =self.outputPath+"_minus_"+DBZ2.name+".dat",\
                    outputPath=self.outputPath+"_minus_"+DBZ2.name+".dat",\
                    imagePath =self.imagePath +"_minus_"+DBZ2.name+".png",\
                    database  =self.database,\
                    cmap=self.cmap, verbose=self.verbose)
        
    def __mul__(self, M):
        """ defining multiplication
        c.f. http://docs.python.org/release/2.5.2/ref/numeric-types.html
        can move to CUDA in the future
        """
        if type(M)==type(1) or type(M)==type(1.1) or type(M)==type(self.matrix) :
            matrix = self.matrix * M
            name=self.name+"_times_"+ str(M)
        if type(M)==type(self):
            matrix = self.matrix * M.matrix
            name=self.name+"_times_"+ M.name
        return  DBZ(dataTime=self.dataTime, matrix=matrix,\
                    dt=self.dt, dx=self.dx, dy=self.dy,\
                    name      =name,
                    dataPath  =self.outputPath+"_times_"+str(M)+".dat",\
                    outputPath=self.outputPath+"_times_"+str(M)+".dat",\
                    imagePath =self.imagePath +"_times_"+str(M)+".png",\
                    database  =self.database,\
                    cmap=self.cmap, verbose=self.verbose)

    def __rmul__(self, M):
        """ defining multiplication on the right
        c.f. http://docs.python.org/release/2.5.2/ref/numeric-types.html
        can move to CUDA in the future
        """
        if type(M)==type(1) or type(M)==type(1.1) or type(M)==type(self.matrix) : 
            matrix = self.matrix * M
            name=self.name+"_times_"+ str(M)
        if type(M)==type(self):
            matrix = self.matrix * M.matrix
            name=self.name+"_times_"+ M.name
        return  DBZ(dataTime=self.dataTime, matrix=matrix,\
                    dt=self.dt, dx=self.dx, dy=self.dy,\
                    name      =name,
                    dataPath  =self.outputPath+"_times_"+str(M)+".dat",\
                    outputPath=self.outputPath+"_times_"+str(M)+".dat",\
                    imagePath =self.imagePath +"_times_"+str(M)+".png",\
                    database  =self.database,\
                    cmap=self.cmap, verbose=self.verbose)

#  end basic operator overloads
##################################

############################################################
# basic i/o's
    def load(self, toInferPositionFromShape=True, **kwargs):
        """
        DBZ.load            - load into DBZ.matrix
        adapted from basics.readToArray(path)
        """
        try:    #if it's text
            m           = np.loadtxt(self.dataPath)
        except ValueError:  # try to load with the binary option
            m           = self.loadBinary(**kwargs)            
        self.matrix = ma.array(m)
        # setting the mask
        self.matrix.fill_value  = -999                               # -999 for missing values
        # self.matrix.fill_value  = -20.1                               # -20 for missing values
        self.matrix.mask        = (m < self.missingDataThreshold)      # smaller than -20 considered no echo
                                                    # 1 March 2013
                                                 # converted to -40, 12 september 2013
                                                 # converted to missingDataThreshold, 16 september 2013
                                                 # anything below " missingDataThreshold is marked as "masked"
                                                 # changed to (m < self.missingDataThreshold) , 20 feb 2014

        if toInferPositionFromShape:            # 26 March 2014
            #   determining the type/position of the grid by the size of the grid (heuristics)
            if self.matrix.shape == (150,140):
                self.lowerLeftCornerLatitudeLongitude   = defaultWRFLowerLeftCornerLatitudeLongitude
                self.upperRightCornerLatitudeLongitude  = defaultWRFUpperRightCornerLatitudeLongitude 
        ##
        # THE FOLLOWING IS SKIPPED TO SAVE MEMORY
        # loading coastal data
        #try:
        #    self.coastData = np.loadtxt(self.coastDataPath)
        #except:
        #    print "Cannot load coast data from the path:  ", self.coastDataPath
        return self

    def loadBinary(self, height=201, width=183):
        """
        codes from Dr. C. Y. Feng, 19 May 2014
        e.g. self.dataPath  )
        a   = pattern.DBZ(dataPath= "/media/TOSHIBA EXT/ARMOR/data/1may2014/RADARCV/COMPREF.20140501.1200.0p03.bin"
        """
        dataFile=open(self.dataPath,'rb')
        data   = []
        for i in range(height):
            dataV = struct.unpack("!%df" % width, dataFile.read(4*width))
            data.append(list(dataV))
        dataFile.close()
        self.matrix = ma.array(data)
        return self.matrix

    def loadCoast(self):
        try:
            self.coastData = np.loadtxt(self.coastDataPath)
        except:             
            self.coastData = np.loadtxt(defaultTaiwanReliefDataFolder + 'taiwanCoast.dat')  #fallback
    def load100(self):
        self.coastData = np.loadtxt(self.relief100DataPath)

    def load1000(self):
        self.coastData = np.loadtxt(self.relief1000DataPath)

    def load2000(self):
        self.coastData = np.loadtxt(self.relief2000DataPath)

    def load3000(self):
        self.coastData = np.loadtxt(self.relief3000DataPath)

    def toArray(self):
        """convert return a normal array filled with -999 for missing values for other uses
        """
        return ma.filled(self.matrix)

    def save(self):
        """
        * We convert the masked array into a standard array with masked data filled by -999
        * adapted from basics.writeArrayToTxtFile(arr, path, as_integer=False):
            if as_integer:
                np.savetxt(path, arr, fmt='%.0f')       # 0 decimal place
            else:
                np.savetxt(path, arr, fmt='%.2f')       # two decimal places as default
        """
        np.savetxt(self.outputPath, self.toArray())

    def constructFromFunction(self, func, funcParameters={},  
                                origin="", height="", width="", newName="",
                               takeRealPart=False, takeImagPart=False, resetVmaxmin=True):
        """
        to construct a matrix from a function
        added 2014-04-09
        """
        #   setting the coordinate origin
        if origin == "":
            origin = self.coordinateOrigin
        else:
            self.coordinateOrigin = origin
        i0, j0  = origin

        #   setting an empty matrix
        if hasattr(self, "matrix"):
            self.matrix *= 0
            height, width = self.matrix.shape
        else:
            if height == "":
                height = dp.defaultHeight
            if width == "":
                width  = dp.defaultWidth
            self.matrix = np.zeros((height, width))
        #   computing
        X, Y    = np.meshgrid(range(width), range(height))
        I, J    = Y, X
        Z       = func(I-i0, J-j0, **funcParameters)
        if takeRealPart:
            self.fullMatrix = Z
            Z = np.real(Z)
        if takeImagPart:
            self.fullMatrix = Z
            Z = np.imag(Z)

        self.matrix = Z
        if newName != "":
            self.name   = newName
        if resetVmaxmin:
            self.vmax = Z.max()
            self.vmin = Z.min()
        #del self.dataPath
        return Z                

    def saveMatrix(self):
        """ alias for self.save()
        """
        self.save()

    def makeImage(self, matrix="", vmin=99999, vmax=-99999, cmap="", title="",\
                  showColourbar=True, closeAll=True,
                  *args, **kwargs):
        """
        requires: matplotlib
        to make the plot before you save/print it to screen
        *adapted from basics.printToScreen(m,cmap='gray'):
            which was in turn adapted from stackoverflow:  
                http://stackoverflow.com/questions/7875688/how-can-i-create-a-standard-colorbar-for-a-series-of-plots-in-python
        def printToScreen(m,cmap='gray'):
            fig, axes = plt.subplots(nrows=1, ncols=1)
            # The vmin and vmax arguments specify the color limits
            im = axes.imshow(m, vmin=-20, vmax=100, cmap=cmap)
            cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
            fig.colorbar(im, cax=cax)
            plt.show()

        !!! TO DO: FIX THE AXES !!!
        """
        if isinstance(matrix, str):
            matrix = self.matrix
        if title =="":
            title = self.name
        if cmap == "":
            cmap = self.cmap
        if vmin == 99999:
            vmin    = self.vmin
        if vmax == -99999:
            vmax    = self.vmax
        # clear the canvass
        if closeAll:
            #plt.clf()
            plt.close()
        # make the image
        fig, axes = plt.subplots(nrows=1, ncols=1)
        if not self.imageTopDown:
            #matrix = np.flipud(matrix)
            imshowOrigin = 'lower'
        else:
            imshowOrigin = 'upper'
        im = axes.imshow(matrix,                       # or np.flipud(self.matrix)?
                         vmin=vmin, vmax=vmax, cmap=cmap,   # The vmin and vmax arguments specify the color limits
                         origin=imshowOrigin,               # 2013-10-15
                         )
        plt.title(title)
        if showColourbar :
            cax = fig.add_axes([0.9, 0.1, 0.01, 0.8])
            fig.colorbar(im,cax=cax)
        #plt.show()                                          # wait, don't show!

    def saveImage(self, imagePath="", matrix="",  dpi=200, **kwargs):
        if matrix=="":
            matrix = self.matrix
        if imagePath == "":
            imagePath = self.imagePath
        self.makeImage(matrix, **kwargs)
        if dpi =="default":
            plt.savefig(imagePath)
        else:
            plt.savefig(imagePath, dpi=dpi)  

    #def printToScreen(self, matrix="", cmap=""):
    def printToScreen(self,  block=False, *args, **kwargs):   #2013-12-06
        #self.makeImage(matrix=matrix, cmap=cmap)
        self.makeImage(*args, **kwargs)
        plt.show(block=block)        
        
    #def show(self, matrix="", cmap=""):
    def show(self, *args, **kwargs):  #2013-12-06
        """alias to printToScreen()
        """
        #self.printToScreen(matrix=matrix, cmap=cmap)
        self.printToScreen(*args, **kwargs)
    def showWithFlip(self, cmap=""):
        """flip it upside down and show it
        """
        self.matrix = np.flipud(self.matrix)
        self.printToScreen(cmap=cmap)

    def showWithCoast(self, matrix="", cmap='', intensity=9999):
        if matrix=="":
            matrix=self.matrix
        try:
            if self.showingWithCoast:       # if already showing coast:  do nothing 
                self.show(matrix=matrix)
                return None                 # just show and go
        except AttributeError:              # if it didn't happen before: default = False
            self.showingWithCoast = False     # just do something
        self.showingWithCoast = True
        #self.matrix_backup = self.matrix.copy()
        self.backupMatrix()                 #2014-05-22
        if cmap != '':
            self.cmap_backup = self.cmap
            self.cmap        = cmap
        else:
            self.cmap_backup = self.cmap
        try:
            if self.coastData == "" : print "haha"      #test for existence
        except AttributeError:
            self.loadCoast()
            print "\n... coast data loaded from ", self.coastDataPath, "for ", self.name
        for v in self.coastData:
            self.matrix[v[0], v[1]] = intensity
            try:
                self.matrix.mask[v[0], v[1]].mask = 0    
            except AttributeError:  # AttributeError: 'numpy.float64' object has no attribute 'mask'
                pass
            matrix=self.matrix
        self.show(matrix=matrix)
        #self.show()
        
    def show2(self, cmap='', intensity=99999):
        """ adding the coastline and then flip it
        """
        try:
            if self.showingWithCoast:       # if already showing coast:  do nothing 
                self.show()
                return None                 # just show and go
        except AttributeError:              # if it didn't happen before: default = False
            self.showingWithCoast = False     # just do something

        self.showingWithCoast = True
        self.matrix_backup = self.matrix.copy()

        if cmap != '':
            self.cmap_backup = self.cmap.copy()
            self.cmap        = cmap
        else:
            self.cmap_backup = self.cmap

        try:
            if self.coastData == "" : print "haha"      #test for existence
        except AttributeError:
            self.loadCoast()
            print "\n... coast data loaded from ", self.coastDataPath, "for ", self.name
        for v in self.coastData:
            self.matrix[v[0], v[1]] = intensity
        self.matrix = np.flipud(self.matrix)
        self.printToScreen(cmap=cmap)
               
    def showWithoutCoast(self):
        """resetting
        """
        self.showingWithCoast = False
        self.cmap = self.cmap_backup
        self.matrix = self.matrix_backup
        self.show()

    def show3(self):            
        """alias
        """
        self.showWithoutCoast()

    def showInverted(self):
        self.matrix = np.flipud(self.matrix)
        self.printToScreen()
        self.matrix = np.flipud(self.matrix)   
    def show0(self):
        """alias
        """
        self.showInverted()

    def show4(self):
        """alias
        """
        self.showInverted()

    def backupMatrix(self, name=""):
        """backing up self.matrix for analysis
            paired with self.restoreMatrix()
        """
        try:
            self.backupCount += 1
            if name =="":
                name = self.backupCount
            self.matrix_backups[name] = self.matrix.copy()
        except AttributeError: 
            self.backupCount = 0
            self.matrix_backups = {}
            if name =="":
                name = self.backupCount
            self.matrix_backups[name] = self.matrix.copy()

    def restoreMatrix(self, name =""):
        """see self.backupMatrix() for comments
        """
        if name =="":
            name = self.backupCount
        self.matrix = self.matrix_backups[name].copy()
        
    # end basic i/o's
    ############################################################

    #############################################################
    # new objects from old
    def copy(self):
        """returning a copy of itself
        9 March 2013
        """
        return DBZ(dataTime =self.dataTime,
                   matrix   =self.matrix.copy(),
                   name     =self.name,
                   dt       =self.dt,
                   dx       =self.dx,
                   dy       =self.dy,
                   dataPath =self.dataPath,
                  outputPath=self.outputPath[:-4]+ '[copy]' + self.outputPath[-4:],
                   imagePath=self.imagePath[:-4] + '[copy]' + self.imagePath[-4:],
               coastDataPath=self.coastDataPath,
           relief100DataPath=self.relief100DataPath,
           relief1000DataPath=self.relief1000DataPath,
           relief2000DataPath=self.relief2000DataPath,
           relief3000DataPath=self.relief3000DataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax, 
               coordinateOrigin= self.coordinateOrigin,
 lowerLeftCornerLatitudeLongitude = self.lowerLeftCornerLatitudeLongitude, 
 upperRightCornerLatitudeLongitude =self.upperRightCornerLatitudeLongitude,
                   verbose  =self.verbose)

    def setMaxMin(self, vmax="", vmin=""):
        if vmax=="":
            self.vmax = self.matrix.max()
        if vmin=="":
            self.vmin = self.matrix.min()

    def drawCross(self, i="", j="", radius=5, intensity=9999):
        """to draw a cross (+) at the marked point
        """
        #   to draw a list of crosses - added 2014-01-23
        
        if isinstance(i, list):
            a2  = self.copy()
            if j!="":
                radius = j
            for p, q in i:  # i = list of points
                a2 = a2.drawCross(i=p, j=q, radius=radius, intensity=intensity)
            return a2
            
        #   codes before 2014-01-23
        if i=="" or j=="":
            i=self.coordinateOrigin[0]
            j=self.coordinateOrigin[1]
        matrix=self.matrix.copy()
        matrix[i-radius:i+radius+1, j                  ]  = intensity
        matrix[i                  , j-radius:j+radius+1]  = intensity
        return DBZ(dataTime =self.dataTime,
                   matrix   =     matrix,
                   name     =self.name + \
                           ", cross at x,y=(%d,%d), radius=%d" %\
                                                  (j, i, radius),
                   dt       =self.dt,
                   dx       =self.dx,
                   dy       =self.dy,
                   dataPath =self.dataPath,
                  outputPath=self.outputPath[:-4]+ '_with_cross' + self.outputPath[-4:],
                   imagePath=self.imagePath[:-4]+ '_with_cross' + self.imagePath[-4:],
               coastDataPath=self.coastDataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax, 
                   coordinateOrigin= self.coordinateOrigin, 
 lowerLeftCornerLatitudeLongitude = self.lowerLeftCornerLatitudeLongitude, 
 upperRightCornerLatitudeLongitude =self.upperRightCornerLatitudeLongitude,
                   verbose  =self.verbose)

    def drawFrame(self, intensity=9999, newCopy=False):
        """
        2013-11-08
        """
        if newCopy:
            a = self.copy()  # no need for this i guess!!!
        else:
            a = self
        a.matrix[ 0,:] = intensity
        a.matrix[-1,:] = intensity
        a.matrix[ :, 0] = intensity
        a.matrix[ :,-1] = intensity
        a.matrix.mask[ 0,:] = 0
        a.matrix.mask[-1,:] = 0
        a.matrix.mask[ :, 0] = 0
        a.matrix.mask[ :,-1] = 0

        return a 
       

    def drawCoast(self, intensity=9999, matrix="", newCopy=False):
        """
        adapted from DBZ.show2()
        """
        if newCopy:
            a = self.copy()  # no need for this i guess!!!
        else:
            a = self
        if matrix =="":
            matrix = a.matrix
        try:
            if a.coastData == "" : print "haha"      #test for existence
        except AttributeError:
            a.loadCoast()
            print "\n... coast data loaded from ", a.coastDataPath, "for ", a.name
        for v in a.coastData:
            matrix[v[0], v[1]] = intensity
            matrix.mask[v[0], v[1]] = 0

        return a 

    def recentreTaichungPark(self):
        """
        2013-08-27
        use:  
            a = pattern.a
            a.showTaichungPark()        
        takes as input 
            attributes:
                lowerLeftCornerLatitudeLongitude
                upperRightCornerLatitudeLongitude
            constants:
                taichung park coordinates (24.145056°N 120.683329°E)       
        changes:
            self.coordinateOrigin
            self.O
        returns:
            grid square for taichung park
                    
        """
        #global taichungParkLatitude, taichungParkLongitude
        height, width = self.matrix.shape
        i0      = taichungParkLatitude        #defined in defaultParameters.py
        j0      = taichungParkLongitude
        # the above two lines dont work, here's a hack fix
        #import defaultParameters
        #j0      = defaultParameters.taichungParkLongitude
        #i0      = defaultParameters.taichungParkLatitude
        i1, j1  = self.lowerLeftCornerLatitudeLongitude
        i2, j2  = self.upperRightCornerLatitudeLongitude
        i3      = 1.*(i0-i1)*height/(i2-i1)  # (latitudeTCP-latLowerleft) * grid per latitude
        j3      = 1.*(j0-j1)*width/(j2-j1)  # ditto for longitude
        self.coordinateOrigin = (i3,j3)
        self.O                = (i3,j3)
        return i3, j3
        
    def recentre(self):
        """alias for recentreTaichungPark(self)       
        """
        return self.recentreTaichungPark()

    def recenter(self):
        """alias for recentreTaichungPark(self)       
        """
        return self.recentreTaichungPark()


    def drawRectangle(self, bottom=0, left=0, height=100, width=100, intensity=9999, newObject=True):
        """ return a copy with a rectangle on the image
        """
        vmax    = self.vmax
        matrix  = self.matrix.copy()
        for i in range(bottom, bottom+height):
            matrix[i        , left:left+2]  = intensity
            matrix[i        , left+width]   = intensity

        for j in range(left, left+width):
            matrix[bottom:bottom+2, j]      = intensity
            matrix[bottom+height, j]        = intensity
            
        if newObject:
            return DBZ(dataTime =self.dataTime,
                       matrix   =     matrix,
                       name     =self.name + \
                               ", rectangle at x,y=(%d,%d), width=%d, height=%d" %\
                                                      (left, bottom, width, height),
                       dt       =self.dt,
                       dx       =self.dx,
                       dy       =self.dy,
                       dataPath =self.dataPath,
                      outputPath=self.outputPath,
                       imagePath=self.imagePath,
                   coastDataPath=self.coastDataPath,
                       database =self.database,
                       cmap     =self.cmap,
                       vmin     =self.vmin, 
                       vmax     =self.vmax, 
                       coordinateOrigin= self.coordinateOrigin, 
                       verbose  =self.verbose)
        else:
            self.matrix = matrix
            return self

    def drawRectangleForValue(self, N=20, N2="", **kwargs):
        """ to draw a rectanglular hull for all points with the given value range
        """
        if N2 =="":
            N2=N
        indexMatrix = (self.matrix>=N) * (self.matrix<=N2)
        locations = np.argwhere(indexMatrix)
        if locations == []:
            return self
        else:
            iMax = max([v[0] for v in locations])
            iMin = min([v[0] for v in locations])
            jMax = max([v[1] for v in locations])
            jMin = min([v[1] for v in locations])
            return self.drawRectangle(iMin, jMin, iMax-iMin, jMax-jMin)

    def getRegionForValue(self, N=20, N2="", **kwargs):
        """ to draw a rectanglular hull for all points with the given value range
        """
        if N2 =="":
            N2=N
        indexMatrix = (self.matrix>=N) * (self.matrix<=N2)
        locations = np.argwhere(indexMatrix)
        if locations.tolist() == []:
            return (-1,-1,0,0)
        else:
            iMax = max([v[0] for v in locations])
            iMin = min([v[0] for v in locations])
            jMax = max([v[1] for v in locations])
            jMin = min([v[1] for v in locations])
            return (iMin, jMin, iMax-iMin, jMax-jMin)



    def getWindow(self, bottom=0, left=0, height=100, width=100):
        """return a dbz object, a window view of itself

        """
        name    = self.name +'_windowed' + '_bottom' + str(bottom) +\
                  '_left' + str(left) + '_height' + str(height) + '_width' + str(width)
        matrix  = self.matrix.copy()
        matrix  = matrix[bottom:bottom+height, left:left+width]
        return DBZ(dataTime =self.dataTime,
                   matrix   =     matrix,
                   name     =     name,
                   dt       =self.dt,
                   dx       =self.dx,
                   dy       =self.dy,
                   dataPath =self.dataPath,
                  outputPath=self.outputPath,
                   imagePath=self.imagePath,
               coastDataPath=self.coastDataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax,
               coordinateOrigin = (height//2, width//2) ,  #hack
                   verbose  =self.verbose)

    def getRectangle(self, *args, **kwargs):
        """
        alias
        """
        return self.getWindow(*args, **kwargs)

    def getRectangularHull(self, points):
        """2014-03-13"""
        iMax            = max(v[0] for v in points) 
        iMin            = min(v[0] for v in points) 
        jMax            = max(v[1] for v in points) 
        jMin            = min(v[1] for v in points) 
        height  = iMax-iMin
        width   = jMax-jMin
        return (iMin, jMin, height, width)

    def drawRectangularHull(self, points, newObject=False, **kwargs):
        """2014-03-13"""
        rec = self.getRectangularHull(points)
        self.drawRectangle(*rec, newObject=newObject, **kwargs)
        
    def shiftMatrix(self,i,j):
        """shifting the array/dbz pattern; masking the edge
        codes migrated from shiiba.py (now armor.shiiba.regression) to here
        i = shift in axis-0 = going up
        j = shift in axis-1 = going right
        """
        #1. copy the matrix
        matrix = self.matrix.copy()

        #2. shift the matrix
        matrix   = np.roll(matrix, i,axis=0)
        matrix   = np.roll(matrix, j,axis=1)

        #3. mask the edges
        if i>0:  # up
            matrix.mask[ :i, : ]   = 1     #mask the first (=bottom) i rows
        if i<0:  # down
            matrix.mask[i: , : ]   = 1     #mask the last (=top) rows; i<0
        if j>0:  # right
            matrix.mask[ : , :j]   = 1      #mask the first (=left) columns
        if j<0:  # left
            matrix.mask[ : ,j: ]   = 1      #mask the last (=right) columns

        #4. return an armor.pattern.DBZ object
        self_shifted_by_ij =DBZ(dataTime=self.dataTime, matrix=matrix,\
                            name=self.name+"shifted"+str((i,j)),\
                            dt=self.dt, dx=self.dx, dy=self.dy, \
                            dataPath    =self.outputPath+"shifted"+str((i,j))+".dat",\
                            outputPath  =self.outputPath+"shifted"+str((i,j))+".dat",\
                            imagePath   =self.imagePath +"shifted"+str((i,j))+".png",\
                            database    =self.database,\
                            cmap=self.cmap, 
                            coordinateOrigin = (self.coordinateOrigin,\
                                                self.coordinateOrigin),
                            verbose=self.verbose) 
        return self_shifted_by_ij

    def shift(self, i, j):
        """alias for shiftMatrix()
        """
        return self.shiftMatrix(i,j)

    def smooth(self, ker=""):
        """
        ################################
        # smoothing the image by convolution with a kernal
        #   uses SciPY
        # return : a DBZ object, smoothed 
        # 8 March 2013
        #################################
        """
        if ker=="":
            ker = 1./237. * np.array(  [[1, 4, 7, 4, 1],        # default kernel
                                        [4,16,26,16, 4],
                                        [7,26,41,26, 7],
                                        [4,16,26,16, 4],
                                        [1, 4, 7, 4, 1]])
        phi0 = self.matrix.copy()
        phi0.fill_value = -999999999
        phi0 = signal.convolve(phi0.filled(),ker)
        phi0 = ma.array(phi0, fill_value=-999, mask=(phi0<-80))
        #  cutting it down to size (881,921)
        return DBZ(name=self.name+'smoothed', matrix =phi0[2:-2, 2:-2],
                    dt=self.dt, dx=self.dx, dy=self.dy,
                    dataPath  =self.dataPath  +'smoothed.dat',
                    outputPath=self.outputPath+'smoothed.dat',
                    imagePath =self.imagePath +'smoothed.dat',
                    coastDataPath=self.coastDataPath,
                    database=self.database,
                    cmap=self.cmap, vmin=self.vmin, vmax=self.vmax,
                    coordinateOrigin = self.coordinateOrigin,
                    verbose=self.verbose)

    def coarser(self, scale=2):
        """
        ################################
        # returning a coarser image by averaging 4 nearby points
        # 
        # return : a DBZ object
        # parameter "scale" not used yet
        # 8 March 2013
        # parameter "scale" implementation started on 12 march 2013
        #################################
        """
        phi = self.matrix.copy()
        # trim if dimensions not even
        height, width   = phi.shape
        horizontal      = width//scale
        vertical        = height//scale
        phi = phi[0:vertical*scale, 0:horizontal*scale]  # trimming
        
        # getting the shifted copies
        #  0 1
        #  2 3
        phi.fill_value = -999999999
        phiList = []    #work to be continued here (parameter "scale" implementation)
        phi0    = phi[ ::scale, ::scale].flatten()
        phi1    = phi[ ::scale,1::scale].flatten()
        phi2    = phi[1::scale, ::scale].flatten()
        phi3    = phi[1::scale,1::scale].flatten()  # unfinished re: scale/averaging
        phi_mean= ma.vstack([phi0, phi1, phi2, phi3])
        phi_mean= ma.mean(phi_mean, axis=0)
        phi_mean= phi_mean.reshape(vertical, horizontal)

        #  cutting it down to size (881,921)
        return DBZ(name=self.name+'_coarser', matrix =phi_mean,
                    dt=self.dt, dx=self.dx, dy=self.dy,
                    dataPath  =self.dataPath[:-4]  +'_coarser' + self.dataPath[-4:],
                    outputPath=self.outputPath[:-4]+'_coarser' + self.outputPath[-4:],
                    imagePath =self.imagePath[:-4] +'_coarser' + self.imagePath[-4:],
                    #coastDataPath=self.coastDataPath,
                    database=self.database,
                    cmap=self.cmap, vmin=self.vmin, vmax=self.vmax,
                    coordinateOrigin = (self.coordinateOrigin[0] //scale,\
                                        self.coordinateOrigin[1] //scale ) ,
                    verbose=self.verbose)

    def coarser2(self):
        """ like coarser() but returning a matrix of the same size, not smaller
        do it later when i have time
        algorithm:
            to multiply self.matrix with a "diagonal" of matrix [[.5, .5],[.5,.5]] 
            on both left and right.

        """                  
        height, width = self.matrix.shape
        pass


    def coarser3(self, scale=2):
        """
        ################################
        # returning a coarser image by picking one out of 2x2 points
        # 
        # return : a DBZ object
        # parameter "scale" not used yet
        # adapted from function "coarser", 25 Feb 2014
        #################################
        """
        phi = self.matrix.copy()
        # trim if dimensions not even
        height, width   = phi.shape
        horizontal      = width//scale
        vertical        = height//scale
        phi = phi[0:vertical*scale, 0:horizontal*scale]  # trimming
        
        # getting the shifted copies
        #  0 1
        #  2 3
        phi.fill_value = -999999999
        phiList = []    #work to be continued here (parameter "scale" implementation)
        phi0    = phi[ ::scale, ::scale]

        #  cutting it down to size (881,921)
        return DBZ(name=self.name+'coarser', matrix =phi0,
                    dt=self.dt, dx=self.dx, dy=self.dy,
                    dataPath  =self.dataPath[:-4]  +'_coarser' + self.dataPath[-4:],
                    outputPath=self.outputPath[:-4]+'_coarser' + self.outputPath[-4:],
                    imagePath =self.imagePath[:-4] +'_coarser' + self.imagePath[-4:],
                    coastDataPath=self.coastDataPath,
                    database=self.database,
                    cmap=self.cmap, vmin=self.vmin, vmax=self.vmax,
                    coordinateOrigin = (self.coordinateOrigin[0] //scale,\
                                        self.coordinateOrigin[1] //scale ) ,
                    verbose=self.verbose)



    def getPrediction(self, C):
        """wrapping armor.shiiba.regression2.getPrediction
        """
        from armor.shiiba import regression2
        return regression2.getPrediction(C, self)

    def predict(self, *args, **kwargs):
        """wrapping self.getPrediction for the moment
        """
        return self.getPrediction(*args, **kwargs)    
        
    def advect(self, *args, **kwargs):
        """wrapping advection.semiLagrangian.interploate2 for the moment
        """
        from armor.advection import semiLagrangian as sl
        return sl.interpolate2(self, *args, **kwargs)    

    def flipud(self):
        """wrapping the function np.flipud
        """
        a_flipud = self.copy()
        a_flipud.matrix = np.flipud(a_flipud.matrix)
        return a_flipud

    def fliplr(self):
        a_fliplr = self.copy()
        a_fliplr.matrix = np.fliplr(a_fliplr.matrix)
        return a_fliplr

    def threshold(self, threshold=0, type='lower'):
        """getting a threshold image of itself with mask
        """
        matrix= self.matrix.copy()
        name  = self.name + " thresholded (" + str(type) + ")at " + str(threshold)
        oldMask = matrix.mask.copy()
        if type=='lower':
            matrix.mask += (matrix < threshold)
        else:
            matrix.mask += (matrix > threshold)
        a_thres  = DBZ(dataTime =self.dataTime,
                   matrix   =matrix,
                   name     =name,  
                   dt       =self.dt,
                   dx       =self.dx,
                   dy       =self.dy,
                   dataPath =self.dataPath,
                  outputPath=self.outputPath[:-4] + "_thresholded_" + str(threshold) + self.imagePath[-4:],
                   imagePath=self.imagePath[:-4]  + "_thresholded_" + str(threshold) + self.imagePath[-4:],
               coastDataPath=self.coastDataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax, 
                   coordinateOrigin= self.coordinateOrigin, 
                   verbose  =self.verbose)
        a_thres.oldMask     = oldMask
        return a_thres

    def above(self, threshold=10):
        """
        getting all the points above threshold
        """
        a = self
        a1 = a.copy()
        a1.name = a.name + '_points_above_' + str(threshold)
        a1.vmin = -.5
        a1.vmax = 2
        a1.matrix = (a.matrix >threshold)
        return a1

    def entropyGlobal(self, threshold=-999, 
                      strata = [0, 10, 20, 25, 20, 35, 40, 45, 50, 55, 60, 65, 70, 75, 999],
                      display=False):
        """
        http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy.stats.entropy.html
        scipy:  from probability/frequency distribution to entropy
        """
        from scipy.stats import entropy
        if threshold != -999:
            a = self.threshold(0)
            arr = a.matrix
        else:
            a=self
            arr = self.matrix
        freqList =[]
        N   = len(strata)
        for i in range(N-1):
            m = (arr>=strata[i]) * (arr<strata[i+1])
            freqList.append(m.sum())
        freqList = np.array(freqList)
        freqTotal = freqList.sum()
        probArray   = 1.* freqList / freqTotal
        if display:
            a.show(block=False)
        return entropy(probArray)

    def entropyLocal(self,
                    *args, **kwargs):
        from . import analysis
        return analysis.entropyLocal(a=self, *args, **kwargs)

    def entropy(self, *args, **kwargs):
        return self.entropyGlobal(*args, **kwargs)    

    def affineTransform(self, T=np.matrix([[1,0,0],[0,1,0]]), origin=""):
        """2013-10-17
        """
        if origin =="":
            origin = self.getCentroid()
        a2 = self.copy()
        a2.name += '_affineTransformed'
        from .geometry import transforms as tr
        I, J = tr.IJ (a2.matrix)
        I, J = tr.affine(I, J, T=T, origin=origin)
        a2.matrix = tr.interpolation(a2.matrix, I, J)
        a2.matrix = ma.array(a2.matrix, mask=(a2.matrix < self.missingDataThreshold))
        #a2.setThreshold(0)
        return a2
        
    def momentNormalise(self, b, 
                        useShiiba=False,
                        centre=(0,0),       # shiiba parameter: the search window centre
                        searchWindowHeight=9, searchWindowWidth=9,
                        extraAngle = 0   # set it to np.pi if we want to add 180 degrees or pi to the rotation angle
                         ):        
        """2013-10-17
        """
        from .geometry import transforms as tr
        a = self
        a.getCentroid()
        a.getEigens()
        b.getCentroid()
        b.getEigens()
        Mlin = tr.rotationMatrix( b.momentAngle+ extraAngle) * \
               np.diag(b.eigenvalues / a.eigenvalues) **.5 * \
               tr.rotationMatrix(-a.momentAngle )

        if useShiiba:
            x       = a.shiiba(b, centre=centre,
                               searchWindowHeight=searchWindowHeight,
                               searchWindowWidth=   searchWindowWidth,
                                )
            shift   = x['C'][2:6:3]+x['mn']
        else:
            shift   = b.centroid-a.centroid
        origin  = a.centroid + shift
        Maffine = np.hstack([Mlin, np.matrix(shift).T])
        a2  = a.affineTransform(T=Maffine, origin=origin)
        a2.name = a.name + '_normalised_to_' + b.name
        if useShiiba:
            a2.name+='_with_shiiba'
            a2.shiibaResult = x
        #################################
        #   storing the results
        a2.Maffine = Maffine    
        try:
            a.relativeAngle[b.name] = b.momentAngle + extraAngle - a.momentAngle
        except:
            a.relativeAngle = {b.name : b.momentAngle + extraAngle - a.momentAngle}
        try:
            a.momentRatios[b.name]  = np.diag(b.eigenvalues / a.eigenvalues) **.5
        except:
            a.momentRatios  = {b.name : np.diag(b.eigenvalues / a.eigenvalues) **.5}
        #################################
        #   return value
        return a2

    def shiibaNormalise(self, b):
        """2013-10-17
        """
        pass
        
    def truncate(self, threshold=0, mode='below', newObject=True):
        """2013-10-20
        truncate the image above/below the threshold
        """
        if newObject:
            a1 = self.copy()
        else:
            a1 = self
        if mode == 'below':
            a1.matrix = a1.matrix * (a1.matrix >=threshold )
        elif mode == 'above':
            a1.matrix = a1.matrix * (a1.matrix <= threshold )
        return a1
        
    def levelSet(self, value):
        """
        DBZ object at the given value
        """
        a1 = self.copy()
        a1.name = self.name + '_level_set_' + str(value)
        a1.matrix = (a1.matrix==value)
        a1.vmax = 1
        a1.vmin = -0.5
        return a1
    
    def laplacianOfGaussian(self, sigma=20):
        """
        returns a dbz object
        """
        from scipy import ndimage
        a1  = self.copy()
        a1.matrix   = ndimage.filters.gaussian_laplace(self.matrix, sigma)
        a1.matrix   = ma.array(a1.matrix, fill_value=-999.)
        a1.name = self.name + "laplacian-of-gaussian-sigma" + str(sigma)
        a1.imagePath    = self.imagePath[:-4]  + "laplacian-of-gaussian-sigma" + str(sigma) +  self.imagePath[-4:]  #hack
        a1.outputPath   = self.outputPath[:-4] + "laplacian-of-gaussian-sigma" + str(sigma) + self.outputPath[-4:]  #hack
        mx = a1.matrix.max()
        mn = a1.matrix.min()
        a1.vmax = mx + (mx-mn)*0.2  # to avoid red top
        a1.vmin = mn
        return a1

        #    def laplacianOfGaussianMask(self, sigma=100):
        #        """
        #        returns a function from the domain to the interval [0, 1] in Real Numbers
        #        2013-11-07
        #        """
        #        a1 = self.laplacianOfGaussian(sigma=sigma)
        #        m  = a1.matrix
        
    def gaussianFilter(self, sigma=20):
        """
        returns a dbz object
        """
        from scipy import ndimage
        a1  = self.copy()
        a1.matrix   = ndimage.filters.gaussian_filter(self.matrix, sigma)
        a1.matrix   = ma.array(a1.matrix, fill_value=-999.)
        a1.matrix.mask = np.zeros(a1.matrix.shape)
        a1.name = self.name + "gaussian-sigma" + str(sigma)
        a1.imagePath    = self.imagePath[:-4]  + "gaussian-sigma" + str(sigma) +  self.imagePath[-4:]  #hack
        a1.outputPath   = self.outputPath[:-4] + "gaussian-sigma" + str(sigma) + self.outputPath[-4:]  #hack
        mx = a1.matrix.max()
        mn = a1.matrix.min()
        #a1.vmax = mx + (mx-mn)*0.2  # to avoid red top     # replaced by lines below 2014-02-20
        #a1.vmin = mn
        a1.matrix.mask = (a1.matrix< self.missingDataThreshold)
        a1.vmax = self.vmax
        a1.vmin = self.vmin
        return a1

    def gaussianMask(self, sigma=20, fraction=0.8):
        """
        returns an array - a smooth mask valued from 0 to 1 built from the gaussian filter
                         - sigma = sigma
                         - fraction = fraction retained extending from a1.matrix.max() to a1.matrix.min()
        """
        a1 = self.gaussianFilter(sigma=sigma)
        a1max = a1.matrix.max()
        a1min = a1.matrix.min() 
        a1min = a1min + (a1max-a1min)*(1-fraction)
        a_mask  = (a1.matrix - a1min) / (a1max-a1min)
        a_mask *= (a_mask > 0)
        self.mask = a_mask
        return a_mask
        
    def gaborFilter(self, sigma=20, phi=1./5, theta=0, **kwargs):
        """
        wrapping armor.filter.gabor.gaborFilter
        """
        from armor.filter import gabor
        a2 = gabor.gaborFilter(self, sigma, phi, theta, **kwargs) 
        return a2        # a pair

    def shortTermTrajectory(self, DBZstream="", key1="", key2="", radius=30, hours=6, timeInterval=3, verbose=True, drawCoast=True):
        """
        plot the twelve-hourly-trajectory (+-6) within the DBZstream
        with the DBZ object having the keywords key1 and key2
        """
        a1 = self.copy()    # dirty copy for computation
        a2 = self.copy()    # clean copy for display
        try:
            a2.load()   #get a clean copy for display
            #a2.show()   #debug
        except:
            pass
        if DBZstream =="":
            DBZstream = self.DBZstream
        a1.name = self.name + '\nshort term trajectory: +- ' + str(hours) + 'hours'
        a2.name = self.name + '\nshort term trajectory: +- ' + str(hours) + 'hours'
        ds = DBZstream  # alias
        a1.setThreshold(a1.matrix.min())
        a1.getCentroid()
        a2.matrix = a2.drawCross(a1.centroid[0], a1.centroid[1], radius=radius+5, intensity= 9999).matrix
        for h in range(-hours, hours+1, timeInterval):
            if h == 0:
                continue    # skip this 
            dataTime = self.timeDiff(hours=h)
            D   = [v for v in ds(dataTime) if key1 in v.name and key2 in v.name]
            if verbose:
                print 'time:', dataTime
            if len(D) == 0:
                continue    # do nothing if none found
            else:
                r = max(radius - 2.5 *abs(h), 5)
                #print 'radius:', rs #debug
                #print '\n\n\n'
                D = D[0]    # choose the first one if there's any ambiguity
                if verbose:
                    print 'DBZ object name:', D.name
                D.load()
                D.setThreshold(self.matrix.min())  #usually =0
                D.getCentroid()
                if verbose:
                    print D.name, "centroid:", D.centroid
                #   plot the centroid of D onto a1 with crosses of decreasing size, min=5
                if h <= 0:
                    a2.matrix = a2.drawCross(D.centroid[0], D.centroid[1], r, intensity= 9999).matrix
                else:
                    a2.matrix = a2.drawCross(D.centroid[0], D.centroid[1], r, intensity= 90).matrix
        if drawCoast:
            a2.drawCoast
        if verbose:
            a2.show()
        return a2        

    def drawShiibaTrajectory(self, a2, L, 
                        k=12,       #default - 12 steps (or 2 hours if successive slides are 10 minutes apart) 
                        *args, **kwargs   
                        ):

        """wrapper"""
        from armor import analysis
        a1_new = analysis.drawShiibaTrajectory(a1=self, a2=a2, L=L, 
                        k=k, *args, **kwargs)
        return a1_new

    def fft(self):
        """2014-02-24
        wrapping armor.filter.fourier
        """
        from armor.filter import fourier
        return fourier.fft(self)
    def ifft(self):
        """2014-02-24
        wrapping armor.filter.fourier
        """
        from armor.filter import fourier
        return fourier.ifft(self)

    def sigmoid(self, L=""):
        """2014-02-24
        supplementary function to smooth out the extremities of the fourier transforms
        wrapping armor.misc.sigmoid"""
        from armor import misc

        if L=="":
            L = self.vmax - self.vmin
        self.matrix = misc.sigmoid(self.matrix, L=L)
        self.vmax = 1.
        self.vmin = 0.

    def powerSpec(self, *args, **kwargs):
        """
        moved to armor/analysis.py 2014-07-04
        updated 2014-07-03 
            including the new 3dplotting function from lin yen ting
            armor.graphics.spectrum3d
        new pipeline:
            WRF/RADAR  ->   response layers for various sigmas -> 1. max spec map
                                                          2. max internsity map
                                                          3. sigma ranges

                                                       -> 1.    3D max spec chart
                                                          2.    3D total spec chart
                                                      
        
        """
        from armor import analysis
        return analysis.powerSpec(self, *args, **kwargs)

    def powerSpecTest0709(self ,*args, **kwargs):
        from armor import analysis
        return analysis.powerSpecTest0709(self, *args, **kwargs)
    

    #   end new objects from old
    #############################################################

    ############################################################
    # functions on object

    def datetime(self, T="", dh=0):
        """
        2013-11-28
        get the datetime object
        dH - diff in number of hours
        """
        import datetime
        if T =="":
            T = self.dataTime   # '20120612.0100'
        dt   = datetime.timedelta(1./24 * dh)
        dd   = re.findall(r'\d\d', T)
        year    = int(dd[0]+dd[1])
        month   = int(dd[2])
        day     = int(dd[3])
        hour    = int(dd[4])
        minute  = int(dd[5])
        return datetime.datetime(year, month, day, hour, minute) + dt

    def getDataTime(self, T):
        """
        input:
            T  - a datetime.datetime object
        output:
            a dataTime string in the pattern.DBZ format
        effect:
            none
        """
        dataTime = str(T.year) + ("0"+str(T.month))[-2:] + ("0"+str(T.day))[-2:] + "." + \
                  ("0"+str(T.hour))[-2:] + ("0"+str(T.minute))[-2:] 
        return dataTime
            
    def setDataTime(self, T):
        """
        input:
            T  - a datetime.datetime object
        output:
            none
        effect:
            resetting self.dataTime to T
        """
        dataTime = str(T.year) + ("0"+str(T.month))[-2:] + ("0"+str(T.day))[-2:] + "." + \
                  ("0"+str(T.hour))[-2:] + ("0"+str(T.minute))[-2:] 
        self.dataTime = dataTime

    def volume(self, threshold=-999):
        """    return the volume above the threshold
        """
        m   = self.matrix.copy()
        m  *= (m >= threshold)
        vol = m.sum()
        return vol
        
    def count(self, threshold=-999):
        """    return the number of points above the threshold
        """
        m   = self.matrix
        c = (m >= threshold).sum()
        return c

    def getCentroid(self):
        """
        2013-10-17
        """
        from .geometry import transforms as tr
        self.centroid = tr.getCentroid(self.matrix)
        return self.centroid
        
    def getEigens(self):
        """2013-10-17
        get the momentMatrix, eigenvalues and eigenvectors, momentAngle 
            store them as attributes
        and return the eigenvalues and eigenvectors
        
        small eigenvalue goes first (small eigenvalue-> i(=y)-axis)
    
        """
        self.getCentroid()
        from .geometry import transforms as tr
        self.momentMatrix = tr.getMomentMatrix(self.matrix)
        self.eigenvalues, self.eigenvectors = tr.getAxes(self.momentMatrix)
        v0 = self.eigenvectors[:,0]
        v1 = self.eigenvectors[:,1]
        self.momentAngle = np.arctan(1.*v0[1]/v0[0]) 

        return self.eigenvalues, self.eigenvectors                                           
     

    def cov(self, dbz2):
        """wrapping the ma.cov function:  covariance between two images
        """
        phi0 = self.matrix.flatten()
        phi1 = dbz2.matrix.flatten()
        cov  = ma.cov(phi0, phi1)
        return cov
    def corr(self, dbz2):
        """wrappig the ma.corrcoef function:  correlation between two images
        """
        phi0 = self.matrix.flatten()
        phi1 = dbz2.matrix.flatten()
        corr = ma.corrcoef(phi0, phi1)
        if (not isinstance(corr, float)) and (not isinstance(corr,int)):
            corr = corr[0,1]                        # return a number
        return corr

    def localCov(self, dbz2, windowSize=7):
        """plotting the local covariance of two dbz patterns
        a slow version of the function
        >>> test.tic() ; x=a.localCov(b) ; test.toc()
        *************************
        time spent: 4091.93978906
        >>> x
        >>> xm=x.matrix
        >>> xm.min()
        -1.0000000000000002
        >>> xm.max()
        1.0000000000000002
        >>> xm.mean()
        0.21721107449067339
        >>> x.name = 'local correlation: dbz20120612.0200 - 0210'
        >>> x.outputPath='testing/test112/localCorrelationMatrix.dat'
        >>> x.save()
        >>> x.matrix=np.flipud(x.matrix)
        >>> x.imagePath='testing/test112/localCorrelationMatrix.png'
        >>> x.saveImage()
        >>> 
        """
        height, width  = self.matrix.shape
        E = (windowSize-1)/2        #shorthand
        # initialise
        localcovar = ma.zeros((height,width))
        localcovar.mask = True
        for i in range(height):
            for j in range(width):
                window1 = self.matrix[max(0,i-E):min(i+E+1, height),max(0,j-E):min(j+E+1,width)]
                window2 = dbz2.matrix[max(0,i-E):min(i+E+1, height),max(0,j-E):min(j+E+1,width)]
                localcovar[i,j] = ma.corrcoef(window1.flatten(), window2.flatten())[0,1]
        return localcovar


    def shiiba(self,b,centre=(0,0),searchWindowHeight=9, searchWindowWidth=9, *args, **kwargs):
        """wrapping armor.analysis.shiiba
        """
        from armor import analysis
        
        self.shiibaResult = analysis.shiiba(self, b, centre=centre, 
                                            searchWindowHeight=searchWindowHeight, 
                                            searchWindowWidth=searchWindowWidth,
                                            *args, **kwargs)
        return self.shiibaResult 

    def shiibaLocal(self, b, *args, **kwargs):
        """wrapping armor.analyais.shiibaLocal
        """
        from armor import analysis
        self.shiibaLocalResult = analysis.shiibaLocal(self,b, *args, **kwargs)
        self.shiibaLocalResult 

    def shiibaFree(self,b, *args, **kwargs):
        """wrapping armor.shiiba.regressionCFLfree
        """
        from armor.shiiba import regressionCFLfree as cflfree
        self.shiibaFreeResult =  cflfree.regressGlobal(self,b, *args, **kwargs)
        return self.shiibaFreeResult 

    def getVect(self, C):
        """wrapping armor.shiiba.regression2.convert
        """
        from armor.shiiba import regression2
        return regression2.convert(C, self)

    def getKmeans(self, *args, **kwargs):
        """wrapping armor.kmeans.clustering.getKmeans()
        8 April 2013
        """
        import armor.kmeans.clustering as clust
        x = clust.getKmeans(self, *args, **kwargs)
        return x

    def invariantMoments(self, takeRoots=True, **kwargs):
        """wrappng armor.geometry.moments.HuMoments
        normalise with respect to the degree
        """
        from armor.geometry import moments
        x = moments.HuMoments(self.matrix, **kwargs)
        if takeRoots:
            x[0] = np.sign(x[0])*abs(x[0])**(.5)
            x[1] = np.sign(x[1])*abs(x[1])**(.25)
            x[2] = np.sign(x[2])*abs(x[2])**(1./6)
            x[3] = np.sign(x[3])*abs(x[3])**(1./6)
            x[4] = np.sign(x[4])*abs(x[4])**(1./12)
            x[5] = np.sign(x[5])*abs(x[5])**(1./8)
            x[6] = np.sign(x[6])*abs(x[6])**(1./12)
        self.invMom = x     #storing it for the future
        return x

    def spline(self):
        """
        wrapping the scipy interpolate module
        http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html#scipy.interpolate.RectBivariateSpline
        """
        height, width = self.matrix.shape
        return interpolate.RectBivariateSpline(range(height), range(width), self.matrix)
        

    def granulometry(self, scales=[4,10,14,40]):
        from .geometry import granulometry as gr
        granulo = gr.analyse(self, scales=scales)
        self.granulo = granulo
        granulo_objects = [DBZ(matrix=granulo[i], name=self.name+'_granulo_'+str(scales[i]),
                                vmax=1, vmin=-0.5,) for i in range(len(scales))]
        return granulo_objects

    def binaryOpening(self, scale=10, threshold=20):
        """
        2013-12-06
        """
        try:
            from scipy import ndimage
            from .geometry import granulometry as gr
            structure = gr.disk_structure(scale)
            opened = ndimage.binary_opening(self.matrix>threshold, structure=structure)
            return opened

        except ImportError:
            print 'Cannot import scipy module "ndimage".  Check your scipy package or (re)install it.'


    def binaryClosing(self, scale=10, threshold=20):
        """
        2013-12-10
        """
        try:
            from scipy import ndimage
            from .geometry import granulometry as gr
            structure = gr.disk_structure(scale)
            closed = ndimage.binary_closing(self.matrix>threshold, structure=structure)
            return closed

        except ImportError:
            print 'Cannot import scipy module "ndimage".  Check your scipy package or (re)install it.'


    def IJ(self):
        height, width = self.matrix.shape
        X, Y    = np.meshgrid(range(width), range(height))
        I, J    = Y, X
        return I, J
        
    def doubleGaussian(self, verbose=True):
        """
        defining a double gaussian covering the blob
        """
        from .geometry import transformedCorrelations as tr
        self.getEigens()  # compute the relevant stats
        self.getCentroid()
        I, J = self.IJ()
        g = tr.doubleGaussian(I, J, self.centroid[0], self.centroid[1], 
                             2* self.eigenvalues[0]**.5, 2* self.eigenvalues[1]**.5, 
                             -self.momentAngle)
        if verbose:
            plt.imshow(g, origin='lower')
            plt.show()
        return g

    def connectedComponents(self, N=-999):
        """
        connected components labelling
        http://scipy-lectures.github.io/advanced/image_processing/
        sorted in descending order
        0 = largest component
        N = max. number of labels

        """
        from scipy import ndimage
        labels, number_of_components = ndimage.label(self.matrix)

        if N ==-999:
            N = number_of_components
        else:
            N = min(number_of_components, N)
            labelsCounts = [(i, (labels==i).sum()) for i in range(number_of_components)]
            labelsCounts.sort(key=lambda v: v[1], reverse=True)
            labels2 = np.ones(labels.shape) *-999
            for i in range(N):
                # reset the labels
                labels2+= (labels==labelsCounts[i][0])*(999+i)
            labels = labels2

        components_object = DBZ(matrix=labels, name=self.name + '_connected_components',
                                vmin=-2, vmax= N )
        self.components = labels
        return components_object
                
    def timeDiff(self, days=0, hours=0, minutes=0):
        """
        return a string "yyyymmdd.hhmm" computed from self.dataTime and the input
        """
        T           = self.dataTime
        from datetime import datetime, timedelta
        timeDiff    = timedelta(days=days, microseconds=hours*3600*1000000+minutes*60*1000000)    # positive or negative
        timeIn      = datetime(int(T[0:4]), int(T[4:6]), int(T[6:8]), int(T[9:11]), int(T[11:13]))
        timeOut     = timeIn + timeDiff
        timeOutString   =   str(timeOut.year) + ('0'+str(timeOut.month))[-2:] + ('0'+str(timeOut.day))[-2:] + \
                          '.' + ('0'+str(timeOut.hour))[-2:] + ('0'+str(timeOut.minute))[-2:]
        return timeOutString

    def getScaleSpace(self, order=0, gamma=1, scales=[1,2,5,10,20,40,100]):
        """
        wraps armor.spectral.scaleSpace
        see the reference there
        scales = sigma
        """
        from armor.spectral import scaleSpace as ss
        scaleSpace = []
        for scale in scales:
            L_scale = ss.L_normalised(image=self.matrix, sigma=scale, order=order, gamma=gamma)
            scaleSpace.append(L_scale)

        self.scaleSpace = scaleSpace
        self.scales     = scales
        return scaleSpace  

    def getScaleMap(self):
        try:
            scaleSpace = self.scaleSpace
        except AttributeError:
            scaleSpace = self.getScaleSpace()
        height, width = self.matrix.shape
        scaleMax = scaleSpace[0]
        for i in range(1, len(scaleSpace)):        
            scaleMax = np.maximum(scaleMax, scaleSpace[i])

        scaleMapMatrix = np.zeros((height,width))
        for i in range(height):
            for j in range(width):
                scaleMapMatrix[i,j] = min([k for k in range(len(scaleSpace)) if scaleSpace[k][i,j] == scaleMax[i,j] ])   # pick the "min" scale that sits on the optimal

        scaleMap = self.copy()
        scaleMap.matrix = scaleMapMatrix
        scaleMap.name = self.name + "scale_map;\nscales=" + str(self.scales)
        scaleMap.outputPath = self.outputPath[:-4] + 'scales' + self.outputPath[-4:]
        scaleMap.imagePath  = self.imagePath[:-4]  + 'scales' + self.imagePath[-4:]
        scaleMap.vmin = -5
        scaleMap.vmax = scaleMap.matrix.max() + 2
        scaleMap.cmap = 'hsv'
        self.scaleMap = scaleMap
        return scaleMap

    def gaussianCorr(self, wrf, sigma=20, thres=15, showImage=True, saveImage=True, outputFolder=''):
        """
        wrapping analysis module
        """
        from armor import analysis
        return analysis.gaussianSmooothNormalisedCorrelation(self, wrf, sigma, thres, 
                                                               showImage,saveImage, outputFolder)

    def histogram(self, bins=20, matrix="", outputPath="", display=True, **kwargs):
        """
        wrapping numpy.histogram
        http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html
        """
        if matrix == "":
            matrix = self.matrix
        plt.close()
        hist, edges = np.histogram(matrix, bins=bins, **kwargs)
        plt.plot(edges[:-1], hist)        
        if outputPath != "":
            plt.savefig(outputPath)
        if display:
            plt.show()

    # end function on object
    ############################################################


    ############################################################
    # functions altering (attributes) of object
    def findEdges(self, threshold=-9999):
        from armor.geometry import edges
        m = a.matrix.copy()
        if threshold !=-9999:
            m.mask += (m<threshold)
            m_edges = edges.find(DBZ(matrix=m))
        else:
            m_edges = edges.find(DBZ(matrix=m))
            self.edges = m_edges
        return m_edges
    
    def setThreshold(self, threshold=-9999):
        mask = self.matrix.mask.copy()
        self.matrix.mask = 0
        self.matrix = self.matrix + (self.matrix<threshold) * (threshold-self.matrix) #setting the threshold to 0
        self.matrix.mask = mask
        
    # end functions altering (attributes) of object
    ############################################################

    ########################################################
    #   supplementary functions
    def constructTaiwanReliefData(self, inputFolder=defaultTaiwanReliefDataFolder, outputFolder="",
                                 dilation=0):
        """
        construct taiwan relief info to the current grid
        and save it to the dataFolder
        """
        from armor.taiwanReliefData import convertToGrid
        if outputFolder=="":
            outputFolder = os.path.dirname(self.dataPath) + '/'  #folder name of the dataPath
        height, width = self.matrix.shape
        LL_lat, LL_long = self.lowerLeftCornerLatitudeLongitude
        UR_lat, UR_long = self.upperRightCornerLatitudeLongitude
        kwargs =    {'files'  :['100','1000','2000','3000', 'Coast'],
                     'width'  : width,
                     'height' : height,
                     'lowerLeft' : (LL_long, LL_lat),
                     'upperRight' : (UR_long, UR_lat),
                     'folder' : inputFolder,
                     'outputFolder':    outputFolder,
                     'suffix' : ".DAT",
                     'dilation' : dilation,
                     }
        convertToGrid.main(**kwargs)


    def coordinatesToGrid(self, x, verbose=False):
        """
        20 jan 2014

        taken from armor.taiwanReliefData.convertTogrid
        convention:
            x = (lat, long, lat long...)
        """
        height, width = self.matrix.shape
        i1, j1  = self.lowerLeftCornerLatitudeLongitude
        i2, j2  = self.upperRightCornerLatitudeLongitude        
        nx = 1. * width  / (j2-j1)
        ny = 1. * height / (i2-i1)
        x = np.array(x)
        y = np.zeros(len(x))
        y[0::2] = (np.round((x[0::2] - i1) * ny)).astype(int)
        y[1::2] = (np.round((x[1::2] - j1) * nx)).astype(int)
        if verbose:
            print x, '-->', y
        return y

###########

    #   end supplementary functions
    ########################################################

################################################################################
                    
#####################################################

class VectorField(object):
    """wraps two masked arrays sharing the same mask (how can i make them share a mask?)

    example:
    >>> from armor import pattern
    >>> a = pattern.DBZ(dataTime="20120612.0200")
    >>> a.load()
    >>> a.show()
    >>> b = pattern.VectorField(a.matrix, -a.matrix)
    >>> b.plot()
    >>> b.show()
    """
    def __init__(self, U, V, mask=False, name='vectorfield', dataPath="", outputPath="", imagePath="", \
                 key='vector field', title='title', gridSize=25):

        """ U = first = i-component;   V=second=j-component
        """
        U  = U.view(ma.MaskedArray)
        V  = V.view(ma.MaskedArray)
        mask = U.mask + V.mask + mask
        U.mask = mask.copy()
        V.mask = mask.copy()
        self.U = U
        self.V = V
        self.mask=mask
        #################################################
        # i don't know how to make this work; comment out
        #if not isinstance(mask, type(False)):         # if mask explicitly given, initialise with it
        #    self.U.mask = mask
        #    self.V.mask = mask
        #################################################
        self.name   = name
        self.dataPath   = dataPath
        self.outputPath = outputPath    # for the future
        self.imagePath  = imagePath
        self.key    = key
        self.title  = title
        self.gridSize= gridSize


    ######################################################################
    #   start basic operator overloads

    def __sub__(self, vect2):
        """defining the subtraction of two vector fields
        """
        if isinstance(vect2, tuple) or isinstance(vect2,list):
            name = self.name + "_minus_" + str(vect2)
            #U = self.U - vect2[0]       # before 2014-1-23  we used (x,y) for external interface, not i,j
            #V = self.V - vect2[1]       # this feature was rarely used so ...
            U = self.U - vect2[1]       # 2014-1-23 - i changed my mind - because we need something like mn+vect
            V = self.V - vect2[0]       # hope this doesn't break anything - fingers crossed?! 
            mask = self.mask.copy()
            key        = self.key + " minus " + str(vect2)
            title      = self.title+" minus " + str(vect2)
            gridSize   = self.gridSize
        else:
            name = self.name + "_minus_" + vect2.name
            U = self.U - vect2.U
            V = self.V - vect2.V
            mask = self.mask + vect2.mask.copy()
            key        = self.key + " minus " + vect2.key
            title      = self.title+" minus " + vect2.title
            gridSize   = min(self.gridSize, vect2.gridSize)
        outputPath = self.outputPath + name + ".dat"
        dataPath   = outputPath
        imagePath  = self.imagePath  + name + ".png"
        return VectorField(U, V, mask=mask, name=name, dataPath=dataPath, outputPath=outputPath,\
                           imagePath=imagePath, key=key, title=title, gridSize=gridSize)

    def __rsub__(self, vect1):
        """
        2014-01-24
        adapted from __sub__()
        focus on the case "A-B" where A is a pair (tuple) or list
        """
        if isinstance(vect1, tuple) or isinstance(vect1,list):
            name = str(vect1) + "_minus_" + self.name 
            U = vect1[1] - self.U       # convention:  (i,j) = (y,x)
            V = vect1[0] - self.V       # hope this doesn't break anything - fingers crossed?! 
            mask = self.mask.copy()
            key        = str(vect1) + " minus " + self.key
            title      = str(vect1) + " minus " + self.title
            gridSize   = self.gridSize
        else:
            name = vect1.name + "_minus_" + self.name
            U = vect1.U - self.U
            V = vect1.V - self.V 
            mask = self.mask + vect1.mask.copy()
            key        = vect1.key  + " minus " + self.key
            title      = vect1.title +" minus " + self.title 
            gridSize   = min(self.gridSize, vect1.gridSize)
        outputPath = self.outputPath + name + ".dat"
        dataPath   = outputPath
        imagePath  = self.imagePath  + name + ".png"
        return VectorField(U, V, mask=mask, name=name, dataPath=dataPath, outputPath=outputPath,\
                           imagePath=imagePath, key=key, title=title, gridSize=gridSize)


        

    def __add__(self, vect2):
        """defining the addition of two vector fields
        """
        if isinstance(vect2, tuple) or isinstance(vect2,list):
            name = self.name + "_plus_" + str(vect2)
            #U = self.U + vect2[0]       # before 2014-1-23 we used (x,y) for external interface, not i,j
            #V = self.V + vect2[1]       # this feature was rarely used so ...
            U = self.U + vect2[1]       # 2014-1-23 - i changed my mind - because we need something like mn+vect
            V = self.V + vect2[0]       # hope this doesn't break anything - fingers crossed?! 
            mask = self.mask.copy()
            key        = self.key + " plus " + str(vect2)
            title      = self.title+" plus " + str(vect2)
            gridSize   = self.gridSize
        else:
            name = self.name + "_plus_" + vect2.name
            U = self.U + vect2.U
            V = self.V + vect2.V
            mask = self.mask + vect2.mask.copy()
            key        = self.key + " plus " + vect2.key
            title      = self.title+" plus " + vect2.title
            gridSize   = min(self.gridSize, vect2.gridSize)
        outputPath = self.outputPath + name + ".dat"
        dataPath   = outputPath
        imagePath  = self.imagePath  + name + ".png"
        return VectorField(U, V, mask=mask, name=name, dataPath=dataPath, outputPath=outputPath,\
                           imagePath=imagePath, key=key, title=title, gridSize=gridSize)

    def __radd__(self, vect2):
        """defining right-addition;  wrapping __add__"""
        return self+vect2

    def __mul__(self, s):
        """scalar for now, will extend later
        """
        if isinstance(s, tuple) or isinstance(s,list):
            U = self.U * s[0]
            V = self.V * s[1]
        else:        
            U = self.U * s
            V = self.V * s
        mask=self.mask.copy()
        name=self.name + "__times__" + str(s)
        dataPath=''
        outputPath=self.outputPath + "__times__" + str(s)
        imagePath =self.imagePath + "__times__" + str(s)
        key=self.key + "__times__" + str(s)
        title=self.title + "__times__" + str(s)
        gridSize = self.gridSize
        return VectorField(U=U, V=V, mask=mask, name=name, dataPath=dataPath, \
                            outputPath=outputPath, imagePath=imagePath, \
                            key=key, title=title, gridSize=gridSize)

    def __rmul__(self,s):
        """wrapping __mul__
        2014-01-23
        """
        return self * s

    def __call__(self, i=-999, j=-999, verbose=False):
        """
        22 jan 2014
        adapted from DBZ.__call__
        """
        if i ==-999 and j ==-999:
            height, width = self.U.shape
            h = int(height**.5 /2)
            w = int(width**.5 /2)
            return (self.U.filled().astype(int),
                    self.V.filled().astype(int) )

        else:
            """
            returns interpolated value
            NOTE TO SELF:  can get a better and more efficient interpolation (e.g. spline) later
            """
            arr= self.U
            i0 = int(i)
            j0 = int(j)
            i1 = i0 + 1
            j1 = j0 + 1
            i_frac = i % 1
            j_frac = j % 1
            f00 = arr[i0,j0]
            f01 = arr[i0,j1]
            f10 = arr[i1,j0]
            f11 = arr[i1,j1]
            interpolated_value_U    =    (1-i_frac)*(1-j_frac) * f00 + \
                                         (1-i_frac)*(  j_frac) * f01 + \
                                         (  i_frac)*(1-j_frac) * f10 + \
                                         (  i_frac)*(  j_frac) * f11 
            if verbose:
                print "U:", i_frac, j_frac, f00, f01, f10, f11
            #   now compute the V-component
            arr= self.V
            i0 = int(i)
            j0 = int(j)
            i1 = i0 + 1
            j1 = j0 + 1
            i_frac = i % 1
            j_frac = j % 1
            f00 = arr[i0,j0]
            f01 = arr[i0,j1]
            f10 = arr[i1,j0]
            f11 = arr[i1,j1]
            interpolated_value_V    =    (1-i_frac)*(1-j_frac) * f00 + \
                                         (1-i_frac)*(  j_frac) * f01 + \
                                         (  i_frac)*(1-j_frac) * f10 + \
                                         (  i_frac)*(  j_frac) * f11 
            if verbose:
                print "V:", i_frac, j_frac, f00, f01, f10, f11
            return np.array([interpolated_value_V, interpolated_value_U])


    #   end basic operator overloads
    ######################################################################

    def plot(self, key="", title="", gridSize=0, X=-1, Y=-1, closeAll=True, lowerLeftKey=False,
             vmin="", vmax="",):
        """
        make the plot without showing it
        adapted from 
            basics.plotVectorField(U, V, X=-1, Y=-1, gridSize=25, key="vector field",\
                                   title="title", saveFileName="", outputToScreen=False):
        """

        # clear the canvass
        #plt.clf()
        if closeAll:
            plt.close()

        U = self.U.copy()
        V = self.V.copy()
        if key =="":
            key = self.key
        if title =="":
            title = self.title
        if gridSize == 0:
            gridSize = self.gridSize
        width  = U.shape[1]
        height = U.shape[0]
        if type(X)==type(-1) or type(Y)==type(-1):
            X, Y = np.meshgrid(np.arange(0,width), np.arange(0,height))
        left   = X[ 0, 0]
        bottom = Y[ 0, 0]
        #computing the length of the vector field at centre for reference
        r_centre = (U[height//2, width//2]**2 +  V[height//2, width//2]**2) **(0.5)
        print "==computing the length of the vector field at centre for reference:==\nr_centre=",\
              "r_centre"

        if lowerLeftKey:
            # making a grid of standardardised vector in the lower-left corner 
            # for scale reference
            U[1:gridSize+1, 1:gridSize+1] = 1
            V[1:gridSize+1, 1:gridSize+1] = 0

        Q = plt.quiver( X[::gridSize, ::gridSize], Y[::gridSize, ::gridSize],\
                        U[::gridSize, ::gridSize], V[::gridSize, ::gridSize],\
                        color='r', units='x', linewidths=(2,), edgecolors=('k'),\
                         headaxislength=5 )
        qk = plt.quiverkey(Q, 0.7, 0.0, 1, 'length='+str(round(r_centre,5))+' at centre',\
                           fontproperties={'weight': 'bold'})
        if lowerLeftKey:
            qk = plt.quiverkey(Q, 0.3, 0.0, 1,\
                            key+',\nlength of the standard arrow in the lower-left corner=1',\
                           fontproperties={'weight': 'bold'})

        plt.axis([left, left+width-1, bottom, bottom+height-1])
        plt.title(title)

    def showPlot(self, block=False, **kwargs):
        self.plot(**kwargs)
        plt.show(block=block)

    def show(self,**kwargs):  #alias
        self.showPlot(**kwargs)

    def savePlot(self, imagePath=""):
        if imagePath != "":
            self.imagePath = imagePath
        self.plot()
        if self.imagePath =="":
            self.imagePath = raw_input("Please enter imagePath:")
        plt.savefig(self.imagePath, dpi=200)
            
    def saveImage(self, *args, **kwargs):
        """alias for savePlot
        """
        self.savePlot(*args, **kwargs)

    def toArray(self):
        """return normal arrays filled with -999 for missing values for other uses
        """
        return ma.filled(self.U), ma.filled(self.V)

    def saveMatrix(self):
        """
        * We convert and save the masked arrays into standard arrays with masked data filled by -999
        """
        U, V = self.toArray()
        np.savetxt(self.outputPath+"U.dat", U, '%.4f')
        np.savetxt(self.outputPath+"V.dat", V, '%.4f')
 
    def pickle(self):
        pickle.dump(self)

    #####################################################
    # functions from vector fields to values
    def corr(self, vect2, region1="", region2=""):
        """adapted from DBZ.corr():
        """
        height, width = self.U.shape
        if region1=="":
            region1 = (0, 0, height, width)
        if region2=="":
            region2 = region1
            
        u1 =  self.U[region1[0]:region1[0]+region1[2], \
                     region1[1]:region1[1]+region1[3]].flatten()
        u2 = vect2.U[region2[0]:region2[0]+region2[2], \
                     region2[1]:region2[1]+region2[3]].flatten()
        ucorr = ma.corrcoef(u1, u2)

        v1 =  self.V[region1[0]:region1[0]+region1[2], \
                     region1[1]:region1[1]+region1[3]].flatten()
        v2 = vect2.V[region2[0]:region2[0]+region2[2], \
                     region2[1]:region2[1]+region2[3]].flatten()
        vcorr = ma.corrcoef(v1, v2)

        return {'ucorr': ucorr, 'vcorr': vcorr}


    ########################################################
    #   functions from vector fields to DBZ objects
    #   2014-01-21
    
    def semiLagrange(self, L, k=6, direction=+1, verbose=True):
        """
        22 jan 2014
        semi lagrangian advection of a set via self
        input:
            L = list of points[(i, j), ...] = [(y, x), ...]
            k = steps, default = 6 steps 
                               = 1 hour if the time-interval between successive COMPREF charts is 10 mins
        output:
            results - a list of np.array pairs [ (i,j) coordinates ]
        """
        if verbose:
            print "semiLagrangian advection of", L, "via", self.name
        results = copy.deepcopy(L)   #  output holder
        for n, pt in enumerate(L):    # point
            for stp in range(k):    # step
                i, j        = results[n]
                di, dj      = self(i, j)
                results[n]  = np.array([i+ direction*di, j+ direction*dj])
            if verbose:
                print pt, "-->", results[n]

        return results

    #   end functions from vector fields to DBZ objects
    ########################################################


    ########################################################
    #   supplementary functions
    
    #   end supplementary functions
    ########################################################

################################################################################
################################################################################
#   streams of DBZ objects, with basic operations, comparisons, etc

class DBZstream:
    """
    a stream of DBZ objects, with basic i/o facilities
    migrating some codes from armor.basicio.dataStream
    WE DO ASSUME THAT there are no two sets of data with the same dataTime
    or else we would need some extra logic to check for redundancies.
    """

    ###########################################################
    #
    #   basic construction

    def __init__(self, dataFolder='../data_temp/', 
                 #name="COMPREF.DBZ", 
                 name="",
                 lowerLeftCornerLatitudeLongitude=defaultLowerLeftCornerLatitudeLongitude, 
                 upperRightCornerLatitudeLongitude=defaultUpperRightCornerLatitudeLongitude,
                 outputFolder="",
                 imageFolder="",
                 taiwanReliefFolder ="",
                 key1="",               # keywords to pick out specific files
                 key2="",               # used only once in the __init__
                 key3="",
                 preload=False,
                 imageExtension = '.png',     #added 2013-09-27
                 dataExtension  = '.txt',
                 vmin           = -40.,          #added 2013-10-28
                 vmax           = 100.,
                 coastDataPath  = "",           #2014-06-25
                 ):
        """
        construct the objects without loading them
        input:  path of folder "/../../" 
        process: parse the folder for files
        output:  sequence of armor.pattern.DBZ objects
                DBZ(name, dataPath, dataTime) 
    
        # parse the filename and look for clues

        """
        if outputFolder =="":
            outputFolder = defaultOutputFolder
        if not outputFolder.endswith('/'):
            outputFolder += '/'
        if imageFolder =="":
            imageFolder = defaultImageFolder
        if taiwanReliefFolder =="":
            taiwanReliefFolder = dataFolder
        if coastDataPath =="":
            coastDataPath = taiwanReliefFolder + "taiwanCoast.dat"
        self.dataFolder = dataFolder            
        self.taiwanReliefFolder = taiwanReliefFolder
        self.lowerLeftCornerLatitudeLongitude   = lowerLeftCornerLatitudeLongitude
        self.upperRightCornerLatitudeLongitude  = upperRightCornerLatitudeLongitude
        self.outputFolder = outputFolder
        self.imageFolder = imageFolder
        self.imageExtension = imageExtension
        self.dataExtension  = dataExtension
        self.vmin           = vmin
        self.vmax           = vmax
        self.coastDataPath  = coastDataPath
        dbzList     = []
        dataFolder      = re.sub(r'\\', '/' , dataFolder)  # standardise:  g:\\ARMOR .. --> g:/ARMOR
        dataSource  = '-'.join(dataFolder.split('/')[-2:]) + '-'
        if name != "":
            self.name = name
        else:
            self.name = dataSource            
        
        L = os.listdir(dataFolder)
        L = [v for v in L if (v.lower().endswith('.txt') or v.lower().endswith('.dat'))\
                              and (key1 in v) and (key2 in v) and (key3 in v)]  # fetch the data files
        L.sort()
        for fileName in L:
            dataTime    = re.findall(r'\d{4}', fileName)
            if len(dataTime)<3:         # NOT DATED DBZ FILE, REJECT
                continue
            if len(dataTime)>3:             # 2014-05-06 hack - assuming the date-time would be at the end of the filename
                dataTime = dataTime[-3:]
            dataTime    = dataTime[0] + dataTime[1] + '.' + dataTime[2]
            dbzName     = name + dataTime
            dataPath    = dataFolder + fileName
            a = DBZ(dataTime=dataTime, 
                    name=dbzName, 
                    dataPath=dataPath,
                    outputPath=outputFolder+dbzName+self.dataExtension,
                    imagePath=imageFolder+dbzName+self.imageExtension,
                    lowerLeftCornerLatitudeLongitude=lowerLeftCornerLatitudeLongitude,
                    upperRightCornerLatitudeLongitude=upperRightCornerLatitudeLongitude,
                    vmin    = self.vmin,
                    vmax    = self.vmax,
                    coastDataPath = coastDataPath  , #2014-06-25
                    relief100DataPath = taiwanReliefFolder + "relief100.dat",
                    relief1000DataPath = taiwanReliefFolder + "relief1000.dat",
                    relief2000DataPath = taiwanReliefFolder + "relief2000.dat",
                    relief3000DataPath = taiwanReliefFolder + "relief3000.dat",
                    )
            if preload:
                a.load()
            dbzList.append(a)
            a.DBZstream = self
        ## there you go! ######
        #
        self.list = dbzList
        #
        #######################

    def __call__(self, N=-999, key2=""):
        """
        if N is an integer then return the N-th DBZ pattern in the stream
        else if N is a string then return those whose names or dataTimes contains N
        """
        if N == -999:
            return self.list
        elif isinstance(N, int):
            return self.list[N]
        elif isinstance(N, str):
            return [v for v in self.list if (N in v.name or N in v.dataTime) and (key2 in v.name or key2 in v.dataTime) ]

    def __getitem__(self, N=-999):
        """alias for self.list[] """
        return self.list[N]

    def __len__(self, dataTime=""):
        return len([v for v in self.list if dataTime in v.dataTime])

    ###########################################################
    #
    #   stream operations
    def append(self, filePath):
        """
        to append a new member to the DBZstream list or a DBZstream to another
        """
        pass

    def recentreTaichungPark(self):
        for D in self.list:
            D.recentreTaichungPark()

    def recentre(self):
        """alias"""
        self.recentreTaichungPark()


    def regrid(self, b):
        """
        wrapping armor.geometry.regrid.regrid()
        b is another DBZ object representing the grid pattern to be transformed to
        """
        from armor.geometry import regrid
        for i in range(len(self.list)):
            a_temp = regrid.regrid(self.list[i], b)
            self.list[i].matrix = a_temp.matrix
            self.list[i].name  += '[regridded]'

    def cutUnloaded(self):
        """
        cut the unloaded objects 
        """
        i=0
        while i < len(self.list):
            dbzObject = self.list[i]
            if (dbzObject.matrix**2).sum()==0:
                del(self.list[i])
            else:
                i+=1
        return i  # length of the stream in the end

    def intersect(self, ds2, cut_first=False, cut_second=False, verbose=False):
        """
        find the intersection of ds1 and ds2 w.r.t. dataTime
        and cut ds1 accordingly
        we assume each dataTime (e.g. '20120612.0200') appears only once in any dataStream
        this burden is on data management, not here
        """
        ds1 = self  #alias
        #   1. get the list of common dataTimes
        dataTimeList1 = [v.dataTime for v in ds1.list]
        dataTimeList2 = [v.dataTime for v in ds2.list]
        common_dataTimeList = sorted(list(set(dataTimeList1).intersection(set(dataTimeList2))))
        if verbose:
            print dataTimeList
        #   2. cut ds1, ds2
        ds1_new_list = [v for v in ds1 if v.dataTime in common_dataTimeList]
        ds2_new_list = [v for v in ds2 if v.dataTime in common_dataTimeList]
        if cut_first:
            ds1.list = ds1_new
        if cut_second:
            ds2.list = ds2_new
        return ds1_new_list, ds2_new_list


    def setThreshold(self, threshold):
        """
        set the threshold for each member of the stream
        """
        for dbzpattern in self:
            dbzpattern.setThreshold(threshold)

    def backupMatrices(self):
        for dbzpattern in self:
            dbzpattern.backupMatrix()

    def restoreMatrices(self):
        for dbzpattern in self:
            dbzpattern.restoreMatrix()

    ###########################################################
    #
    #   basic I/O
    #def load(self, N=-999, name="",  verbose=False):
    def load(self, N=-999, key2="", toInferPositionFromShape=True, verbose=False):
        """
        N - index of object to be loaded, if N==-999 : load all
        if N is a string, look through the list of dbz objects 
                            and load those whose dataTime string contain N
                                              and whose name contains name
        """
        if N==-999:
            for img in self.list:
                if verbose:
                    print img.name, '|',
                img.load(toInferPositionFromShape=toInferPositionFromShape)
        elif isinstance(N, int):
            self.list[N].load(toInferPositionFromShape=toInferPositionFromShape)
        elif isinstance(N, str):
            for img in self.list:
                if (N in img.dataTime or N in img.name) and (key2 in img.name or key2 in img.dataTime):
                    img.load(toInferPositionFromShape=toInferPositionFromShape)
                    if verbose:
                        print img.name, '|',

    def unload(self, key=""):
        """
        unload/delete the loaded DBZ data to save memory
        """
        for D in self:
            if key in D.name or key in D.dataTime:
                D.matrix = np.zeros((1,1))

    def setImageFolder(self, folder=""):
        # deprecated per the saveImages() function
        if folder != "":
            self.imageFolder=folder
        for dbzPattern in self.list:
            dbzPattern.imageFolder = folder
            #dbzPattern.imagePath   = folder +  dbzPattern.name + '_'+dbzPattern.dataTime + ".png"
            try:
                dbzPattern.imagePath   = folder + self.name + dbzPattern.dataTime + self.imageExtension
            except AttributeError:      # hack added 2013-09-27
                self.imageExtension = defaultImageExtension
                dbzPattern.imagePath   = folder + self.name + dbzPattern.dataTime + self.imageExtension

    def setImagePaths(self, *args, **kwargs):
        """ alias"""
        return self.setImageFolder(*args, **kwargs)

    def setOutputFolder(self, folder):
        """
        set image folders and paths without saving
        """
        if not os.path.isdir(folder):       # added 2014-03-06
            os.makedirs(folder)             # added 2014-03-06
        self.outputFolder=folder
        for dbzPattern in self.list:
            dbzPattern.outputFolder = folder
            #dbzPattern.outputPath   = folder +  dbzPattern.name + '_'+dbzPattern.dataTime + ".dat"
            dbzPattern.outputPath   = folder + dbzPattern.dataTime + self.dataExtension  

    def setTaiwanReliefFolder(self, folder=''):
        if folder =="":
            folder = self.taiwanReliefFolder
        else:
            self.taiwanReliefFolder = folder
        for dbzpattern in self:
            dbzpattern.coastDataPath =  folder + "taiwanCoast.dat"
            dbzpattern.relief100DataPath =  folder + "relief100.dat"
            dbzpattern.relief1000DataPath =  folder + "relief1000.dat"
            dbzpattern.relief2000DataPath =   folder + "relief2000.dat"
            dbzpattern.relief3000DataPath =  folder + "relief3000.dat"    

    def setVmin(self, vmin=""):        # DBZ.vmin and DBZ.vmax are colour parameters for image output
        if vmin == "":
            vmin = self.vmin
        else:
            self.vmin = vmin
        for dbzPattern in self:         # telling the plotting function the min and max value in each chart
            dbzPattern.vmin = vmin

    def setVmax(self, vmax=""):
        if vmax == "":
            vmax = self.vmax
        else:
            self.vmax = vmax
        for dbzPattern in self:
            dbzPattern.vmax = vmax


    def saveImages(self, flipud=False, drawCoast=False, verbose=False, dpi=200):
        """ 
        note:  here we set the imagePath's first (imageFolder+dataTime+ .png) 
              and then save the images to it
        """
        ds1 = self  # just a reminder self= a dbz data stream
        try:            # make it in case the folder does not exist yet
            os.makedirs(ds1.imageFolder)
        except OSError:  # except if it's already there
            pass
        for dbzPattern in ds1.list:
            dbzPattern.imagePath = ds1.imageFolder + ds1.name + dbzPattern.dataTime + '.png'
            if drawCoast:
                dbzPattern.drawCoast()
            if flipud==True:
                dbzPattern.matrix = np.flipud(dbzPattern.matrix)
            if verbose:
                print dbzPattern.imagePath
                xxx = raw_input('press enter to continue:')
            dbzPattern.saveImage(dpi=dpi)


    
    def saveMatrices(self, verbose=False):
        """
        note:  here we set the imagePath's first (imageFolder+dataTime+ .png) 
              and then save the images to it
        """
        ds1 = self  # just a reminder self= a dbz data stream
        try:            # make it in case the folder does not exist yet
            os.makedirs(ds1.outputFolder)
        except OSError:  # except if it's already there
            pass
        for dbzPattern in ds1.list:
            dbzPattern.outputPath = ds1.outputFolder + ds1.name + dbzPattern.dataTime + '.dat'
            if verbose:
                print dbzPattern.imagePath
                xxx = raw_input('press enter to continue:')
            dbzPattern.saveMatrix()


    ###########################################################
    #
    #   functions on streams

    def listLoaded(self):
        """
        return the list of loaded DBZ objects in the stream
        essentially computing those with matrix!=0
        """
        L = [v for v in self if (v.matrix**2).sum()!=0]
        return L

    def countLoaded(self):
        """
        return the number of loaded DBZ objects in the stream
        essentially computing those with matrix!=0
        """
        return len([v for v in self if (v.matrix**2).sum()!=0])

    def setMasks(self, lowerThreshold):
        """
        reset the masks, masking those values lower than the new lowerThreshold
        True=masked
        2013-09-27
        """
        for dbzpattern in self.list:
            m = dbzpattern.matrix
            m.mask = False
            m.mask = (m < lowerThreshold)

    def setFloor(self, lower):
        """
        cut of those that are below lower and replace them as lower
        """
        for d in self.list:
            m = d.matrix
            d.matrix = m + (m<lower)* (lower-m)

    def setCommonMask(self, key=""):
        """
        set the mask to the union of all (biggest mask, showing the general common (smallest) region)
        """
        m = self.list[0].matrix.mask
        try:
            for d in self(key):
                m += d.matrix.mask

            for d in self(key):
                d.matrix.mask = m
        except:
            print 'cannot construct common mask!'
     
    def fix(dbzstream, key1='', threshold=0):       #standard fix, codes from armor.objects2
        print 'loading', dbzstream.name, 'with key', key1
        dbzstream.load(key1)
        print 'cutting the excess'
        dbzstream.cutUnloaded()
        print 'setting threshold', threshold
        dbzstream.setThreshold(threshold)
        dbzstream.setTaiwanReliefFolder()
        dbzstream.setVmin()
        dbzstream.setVmax()

    def timeShift(self, days=0, secs=0, verbose=False):
        """
        just change the dataTimes and names ; nothing else.  the dataPaths aren't changed
        2014-03-05
        """
        for d in self:
            T   = d.datetime()
            dt  = datetime.timedelta(days + 1.*secs/86400)
            T  += dt
            d.setDataTime(T)
            d.name  += "_timeShift_%ddays_%dsecs" % (days, secs)
            if verbose:
                print d.name, d.dataTime

    ###########################################################
    #
    #   Tests and comparisons
    def corr(self, ds2, verbose=False):
        """
        returns a list of correlation of the streams
                  [(dataTime <str>, corr <float>),...]
        """
        ds1 = self      # alias
        #   1. get the list of common dataTimes
        dataTimeList1 = [v.dataTime for v in ds1.list]
        dataTimeList2 = [v.dataTime for v in ds2.list]
        dataTimeList = sorted(list(set(dataTimeList1).intersection(set(dataTimeList2))))
        if verbose:
            print dataTimeList

        #   2. compute the correlations with the built in DBZ.corr() method
        L = []
        for T in dataTimeList:
            a = ds1(T)[0]
            b = ds2(T)[0]
            L.append((T, a.corr(b)))
        return L

    def invariantMomentsCorr(self, ds2, comparison='distance', verbose=False):
        '''
        comparison = 'dot', 'correlation', 'distance' (euclidean distance)
        '''
        ds1 = self
        from geometry import moments
        #   1. get the list of common dataTimes
        dataTimeList1 = [v.dataTime for v in ds1.list]
        dataTimeList2 = [v.dataTime for v in ds2.list]
        dataTimeList = sorted(list(set(dataTimeList1).intersection(set(dataTimeList2))))
        if verbose:
            print dataTimeList

        #   2. compute the moments and compare them
        L = []
        for T in dataTimeList:
            a = ds1(T)[0]
            b = ds2(T)[0]
            #a.invMom = a.invariantMoments()
            #b.invMom = b.invariantMoments()
            a.invariantMoments()
            b.invariantMoments()
            #debug
            print '====== a.invMom, b.invMom: ======='
            print a.invMom
            print b.invMom
            # end debug
            if comparison == 'corr':
                invarcorr    = np.corrcoef(a.invMom, b.invMom)[0,1]            
                                        # correlation is not always good.  use the vector dot product instead (?!)
                                        # see the next line
                print 'their correlation:', invarcorr
            elif comparison == 'dot':
                invarcorr = np.dot(a.invMom,b.invMom)/ (np.dot(a.invMom,a.invMom)*np.dot(b.invMom,b.invMom))**.5  #added 2013-09-28
                print "their dot product:", invarcorr                 
            else:
                invarcorr = np.linalg.norm( np.array(a.invMom) - np.array(b.invMom))
                print 'their euclidean distance:', invarcorr
            L.append((T, invarcorr))
        return L


    def regionalAndGlobalInvariantMomentsCorr(self, ds2, N=4, verbose=False):
        """
        analogous to Chen Sin Gam's averaging method From CWB
        returns a list of scores of the given stream ds2 w.r.t. ds1=self
                  [(dataTime <str>, score <float>),...]
        """
        import itertools
        import math
        ds1 = self
        height, width = ds1[0].matrix.shape
        h1       = height//N
        w1       = width //N
        i_splits = range(0, height, h1)
        j_splits = range(0, width,  w1)
        splits   = itertools.product(i_splits, j_splits)
        #debug
        #print 'splits - ', [v for v in splits]
        #ds2 = ds2.intersect(ds1)
        #ds1 = ds1.intersect(ds2)
        dataTimes1 = sorted([v.dataTime for v in ds1])
        dataTimes  = sorted([v.dataTime for v in ds2 if v.dataTime in dataTimes1])
        regionalMomentAverages = []
        for T in dataTimes:
            invarcorr = 0.
            observation = ds1(T)[0]      # one way or other; just for convenience
            wrf         = ds2(T)[0]        # reminder to self: there should be/we assume there is only one in the list, so [0] works
            # global moments corr
            a = observation
            b = wrf
            a.invariantMoments()
            b.invariantMoments()
            #invarcorr    = ma.corrcoef(a.invMom, b.invMom)[0,1] 

                                    # correlation is not always good.  use the vector dot product instead (?!)
                                    # see the next line
            invarcorr = ma.dot(a.invMom,b.invMom)/ (ma.dot(a.invMom,a.invMom)/ma.dot(b.invMom,b.invMom))**.5  #added 2013-09-28

            #if not isinstance(invarcorr, float):
            #if (invarcorr==np.nan):
            #if not (invarcorr>999 or invarcorr<=999):   # if invarcorr!=nan
            if math.isnan(invarcorr):
                invarcorr = 0.
                Count = 0
            else:
                Count = N
            # local moments corr
            #debug
            print 'invarcorr:', invarcorr, '/',
            for i,j in splits:
                a1 = a.getWindow(i, j, h1, w1)
                b1 = a.getWindow(i, j, h1, w1)
                a1.invariantMoments()
                b1.invariantMoments()
                invarcorr_regional = ma.corrcoef(a1.invMom, b1.invMom)[0,1]
                # debug
                print invarcorr_regional,
                #if not (invarcorr_regional==np.nan):
                #if (invarcorr_regional>999 or invarcorr_regional<=999):   # if invarcorr_regional==nan
                if not math.isnan(invarcorr_regional):
                    invarcorr += invarcorr_regional
                    Count +=1
                #debug
                print invarcorr, ':', Count, '/',
            invarcorr = 1. * invarcorr / Count  #   weighed average
            print ':', invarcorr, '||',
            regionalMomentAverages.append((T, invarcorr))      
        return regionalMomentAverages
        
    def gaborFeaturesTest(self, ds2, verbose=False):
        """
        use gabor filter to extract local scale and orientation features
        """
        

        pass
    
    def clusteringTest(self, ds2, verbose=False):
        """
        comparison via clustering
        """
        pass
        

    def LeesTransformation(self, ds2, verbose=False):
        """
        Professor Tim-Hau Lee's Idea - perform a normalising transformation
                                 according to the first two moments
                                 before comparisons
        """
        ds1 = self
        pass
    
################################################################################

DS  = DBZstream

########################
# demo

a = DBZ('20120612.0200')
b = DBZ('20120612.0230')
c = DBZ('20120612.0300')
d = DBZ('20120612.0210')
e = DBZ('20120612.0240')
f = DBZ('20120612.0310')


#a.load()
#b.load()
#c.load()
#d.load()
#e.load()
#f.load()

#a.setThreshold(0)
#b.setThreshold(0)
#c.setThreshold(0)
#d.setThreshold(0)
#e.setThreshold(0)
#f.setThreshold(0)



ds1 = DBZstream(name="COMPREF",
                imageFolder  = '../labReports/20130827/COMPREF/',
                outputFolder = '../labReports/20130827/COMPREF/')

"""
exit()
python
from armor import pattern

"""

try:
    print externalHardDriveRoot
    ds2 = DBZstream(dataFolder='%sdata/SOULIK/wrf_shue/' %externalHardDriveRoot, 
                    lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
                    upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                     )
except:
    print 'EXTERNAL HARD DRIVE %sdata/SOULIK/wrf_shue/' %externalHardDriveRoot, "NOT FOUND"
    try:
        ds2 = DBZstream(dataFolder='%sdata/SOULIK/wrf_shue/' %hardDriveRoot, 
                        lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
                        upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                        )
        print 'HARD DRIVE  %sdata/SOULIK/wrf_shue/' %hardDriveRoot, "\nFOUND!!"
    except: 
        print 'HARD DRIVE  %sdata/SOULIK/wrf_shue/' %hardDriveRoot, "NOT FOUND"
        try:
            print externalHardDriveRoot2
            ds2 = DBZstream(dataFolder='%sdata/SOULIK/wrf_shue/' %externalHardDriveRoot2, 
                            lowerLeftCornerLatitudeLongitude=(17.7094,113.3272),
                            upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                            )
            print 'EXTERNAL HARD DRIVE  %sdata/SOULIK/wrf_shue/' %externalHardDriveRoot2, "\nFOUND!!"
        except:
            print 'EXTERNAL HARD DRIVE %sdata/SOULIK/wrf_shue/' %externalHardDriveRoot2, "NOT FOUND"

try:
    ds3 = DBZstream(dataFolder='../data_simulation/20120611_12/', name="WRF", 
                     lowerLeftCornerLatitudeLongitude=(17.7094,113.3272), 
                     upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                     outputFolder = '../labReports/20130827/WRF/',
                     imageFolder = '../labReports/20130827/WRF/',
                     preload=False)
except:
    print '../data_simulation/20120611_12/  - NOT FOUND'
    
"""
The following are constructed from data from mr. shue : https://mail.google.com/mail/u/0/?shva=1#search/azteque%40manysplendid.com/14070bb7d7aef48c
wd3
282x342
    MaxLatF                   = 28.62909
    MinLatF                   = 17.7094
    MaxLonF                   = 127.6353
    MinLonF                   = 113.3272

"""
try:
    cx = DBZ(name='WRF20120612.0200', dataTime='20120612.0200', 
        dataPath= usbRoot + '/data_simulation/20120611_12/out_201206120200.txt',
        lowerLeftCornerLatitudeLongitude= (17.7094, 113.3272),
        upperRightCornerLatitudeLongitude= (28.62909,127.6353) ,
        )


    dx = DBZ(name='WRF20120612.0210', dataTime='20120612.0210',
        dataPath= usbRoot + '/data_simulation/20120611_12/out_201206120210.txt',
            lowerLeftCornerLatitudeLongitude= (17.7094, 113.3272),
        upperRightCornerLatitudeLongitude= (28.62909,127.6353) ,
      )
except:
    print 'data not found!  construction of cx and dx skipped'


