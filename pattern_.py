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
# some of the stuff are to be moved to a submodule
import copy
import time
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
import pickle
from copy import deepcopy
try:
    from scipy import signal
    from scipy import interpolate
except ImportError:
    #print "Scipy not installed"
    pass


#==== setting up the global parameters========================================================

from defaultParameters import *     #bad habits but all these variables are prefixed with "default"
                                    # or at least i try to make them to
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
                  cmap='hsv', vmin=-20, vmax=100, coordinateOrigin="default",\
                  coastDataPath="", relief100DataPath='', relief1000DataPath='',\
                  relief2000DataPath='', relief3000DataPath='',\
                  lowerLeftCornerLatitudeLongitude ='',\
                  upperRightCornerLatitudeLongitude ='',\
                  database="", verbose=False):
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
            matrix     = ma.zeros((defaultHeight, defaultWidth))   # initialise with zeros
            matrix.fill_value = -999                               # -999 for missing values always
        if isinstance(matrix, ma.MaskedArray):
            matrix.fill_value = -999
        if isinstance(matrix, np.ndarray) and not isinstance(matrix, ma.MaskedArray):
            matrix     = matrix.view(ma.MaskedArray)
            matrix.mask = None
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
            relief1000DataPath = defaultInputFolder + "relief1000Extended.dat"
        if relief2000DataPath == "":
            relief2000DataPath = defaultInputFolder + "relief2000Extended.dat"
        if relief3000DataPath == "":
            relief3000DataPath = defaultInputFolder + "relief3000Extended.dat"
        if lowerLeftCornerLatitudeLongitude =="":
            lowerLeftCornerLatitudeLongitude = defaultLowerLeftCornerLatitudeLongitude
        if upperRightCornerLatitudeLongitude=="":
            upperRightCornerLatitudeLongitude = defaultUpperRightCornerLatitudeLongitude

        if database =="":
            database = defaultDatabase
        ###############################################################################
        # if matrix shape = (881, 921) then by default the origin at Taichung Park
        #                                   (24.145056°N 120.683329°E)
        #                                or   (492, 455) in our grid
        # else the centre is the origin by default
        ###############################################################################
        if coordinateOrigin == "default":  #default
            if matrix.shape == (881, 921):
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
    def load(self):
        """
        DBZ.load            - load into DBZ.matrix
        adapted from basics.readToArray(path)
        """
        m           = np.loadtxt(self.dataPath)
        self.matrix = ma.array(m)
        # setting the mask
        self.matrix.fill_value  = -999                               # -999 for missing values
        # self.matrix.fill_value  = -20.1                               # -20 for missing values
        self.matrix.mask        = (m < -20)      # smaller than -20 considered no echo
                                                    # 1 March 2013
        ##
        # THE FOLLOWING IS SKIPPED TO SAVE MEMORY
        # loading coastal data
        #try:
        #    self.coastData = np.loadtxt(self.coastDataPath)
        #except:
        #    print "Cannot load coast data from the path:  ", self.coastDataPath

    def loadCoast(self):
        self.coastData = np.loadtxt(self.coastDataPath)

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

    def saveMatrix(self):
        """ alias for self.save()
        """
        self.save()

    def makeImage(self, matrix="", vmin=99999, vmax=-99999, cmap="", title="",\
                  showColourbar=True, closeAll=True):
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
        im = axes.imshow(matrix,                       # or np.flipud(self.matrix)?
                         vmin=vmin, vmax=vmax, cmap=cmap)   # The vmin and vmax arguments 
                                                             # specify the color limits
        plt.title(title)
        if showColourbar :
            cax = fig.add_axes([0.9, 0.1, 0.01, 0.8])
            fig.colorbar(im,cax=cax)
        #plt.show()                                          # wait, don't show!

    def saveImage(self):
        self.makeImage()
        plt.savefig(self.imagePath, dpi=200)  

    def printToScreen(self, matrix="", cmap=""):
        self.makeImage(matrix=matrix, cmap=cmap)
        plt.show()        
        
    def show(self, matrix="", cmap=""):
        """alias to printToScreen()
        """
        self.printToScreen(matrix=matrix, cmap=cmap)
        
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
        self.matrix_backup = self.matrix.copy()
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
            self.matrix[v[0], v[1]] += intensity
        self.show(matrix=matrix)
        
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
                  outputPath=self.outputPath,
                   imagePath=self.imagePath,
               coastDataPath=self.coastDataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax, 
               coordinateOrigin= self.coordinateOrigin,
 lowerLeftCornerLatitudeLongitude = self.lowerLeftCornerLatitudeLongitude, 
 upperRightCornerLatitudeLongitude =self.upperRightCornerLatitudeLongitude,
                   verbose  =self.verbose)

    def drawCross(self, i="", j="", radius=5, intensity=9999):
        """to draw a cross (+) at the marked point
        """
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
                  outputPath=self.outputPath,
                   imagePath=self.imagePath,
               coastDataPath=self.coastDataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax, 
                   coordinateOrigin= self.coordinateOrigin, 
 lowerLeftCornerLatitudeLongitude = self.lowerLeftCornerLatitudeLongitude, 
 upperRightCornerLatitudeLongitude =self.upperRightCornerLatitudeLongitude,
                   verbose  =self.verbose)

    def drawCoast(self, intensity=9999, newCopy=False):
        """
        adapted from DBZ.show2()
        """
        if newCopy:
            a = self.copy()  # no need for this i guess!!!
        else:
            a = self
        try:
            if a.coastData == "" : print "haha"      #test for existence
        except AttributeError:
            a.loadCoast()
            print "\n... coast data loaded from ", a.coastDataPath, "for ", a.name
        for v in a.coastData:
            a.matrix[v[0], v[1]] = intensity
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


    def drawRectangle(self, bottom=0, left=0, height=100, width=100, intensity=9999):
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
        phi0    = phi[ ::2, ::2].flatten()
        phi1    = phi[ ::2,1::2].flatten()
        phi2    = phi[1::2, ::2].flatten()
        phi3    = phi[1::2,1::2].flatten()
        phi_mean= ma.vstack([phi0, phi1, phi2, phi3])
        phi_mean= ma.mean(phi_mean, axis=0)
        phi_mean= phi_mean.reshape(vertical, horizontal)

        #  cutting it down to size (881,921)
        return DBZ(name=self.name+'coarser', matrix =phi_mean,
                    dt=self.dt, dx=self.dx, dy=self.dy,
                    dataPath  =self.dataPath  +'coarser.dat',
                    outputPath=self.outputPath+'coarser.dat',
                    imagePath =self.imagePath +'coarser.dat',
                    coastDataPath=self.coastDataPath,
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

    def threshold(self, threshold=0):
        """getting a threshold image of itself with mask
        """
        matrix= self.matrix.copy()
        name  = self.name + " thresholded at " + str(threshold)
        oldMask = matrix.mask.copy()
        matrix.mask += (matrix < threshold)
        a_thres  = DBZ(dataTime =self.dataTime,
                   matrix   =matrix,
                   name     =name,  
                   dt       =self.dt,
                   dx       =self.dx,
                   dy       =self.dy,
                   dataPath =self.dataPath,
                  outputPath=self.outputPath + "_thresholded_" + str(threshold),
                   imagePath=self.imagePath  + "_thresholded_" + str(threshold),
               coastDataPath=self.coastDataPath,
                   database =self.database,
                   cmap     =self.cmap,
                   vmin     =self.vmin, 
                   vmax     =self.vmax, 
                   coordinateOrigin= self.coordinateOrigin, 
                   verbose  =self.verbose)
        a_thres.oldMask     = oldMask
        return a_thres
        
    # end new objects from old
    #############################################################

    ############################################################
    # functions on object


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


    def shiiba(self,b, *args, **kwargs):
        """wrapping armor.analysis.shiiba
        """
        from armor import analysis
        
        self.shiibaResult = analysis.shiiba(self, b, *args, **kwargs)
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

    def invariantMoments(self,**kwargs):
        """wrappng armor.geometry.moments.HuMoments
        normalise with respect to the degree
        """
        from armor.geometry import moments
        x = moments.HuMoments(self.matrix, **kwargs)
        x[0] = np.sign(x[0])*abs(x[0])**(.5)
        x[1] = np.sign(x[1])*abs(x[1])**(.25)
        x[2] = np.sign(x[2])*abs(x[2])**(1./6)
        x[3] = np.sign(x[3])*abs(x[3])**(1./6)
        x[4] = np.sign(x[4])*abs(x[4])**(1./12)
        x[5] = np.sign(x[5])*abs(x[5])**(1./8)
        x[6] = np.sign(x[6])*abs(x[6])**(1./12)
        self.invMom = x
        return x

    def spline(self):
        """
        wrapping the scipy interpolate module
        http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html#scipy.interpolate.RectBivariateSpline
        """
        height, width = self.matrix.shape
        return interpolate.RectBivariateSpline(range(height), range(width), self.matrix)
        

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
    
# end functions altering (attributes) of object
############################################################
                    
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


    def __sub__(self, vect2):
        """defining the subtraction of two vector fields
        """
        if isinstance(vect2, tuple) or isinstance(vect2,list):
            name = self.name + "_minus_" + str(vect2)
            U = self.U - vect2[0]       # we use (x,y) for external interface, not i,j
            V = self.V - vect2[1]
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

    def __add__(self, vect2):
        """defining the addition of two vector fields
        """
        if isinstance(vect2, tuple) or isinstance(vect2,list):
            name = self.name + "_plus_" + str(vect2)
            U = self.U + vect2[0]       # we use (x,y) for external interface, not i,j
            V = self.V + vect2[1]
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



    def plot(self, key="", title="", gridSize=0, X=-1, Y=-1, closeAll=True, lowerLeftKey=False):
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

    def showPlot(self,**kwargs):
        self.plot(**kwargs)
        plt.show()

    def show(self,**kwargs):  #alias
        self.showPlot(**kwargs)

    def savePlot(self):
        self.plot()
        if self.imagePath =="":
            self.imagePath = raw_input("Please enter imagePath:")
        plt.savefig(self.imagePath, dpi=200)
            
    def saveImage(self):
        """alias for savePlot
        """
        self.savePlot()

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


##############################################################################
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

    def __init__(self, dataFolder='../data_temp/', name="COMPREF.DBZ", 
                 lowerLeftCornerLatitudeLongitude=defaultLowerLeftCornerLatitudeLongitude, 
                 upperRightCornerLatitudeLongitude=defaultUpperRightCornerLatitudeLongitude,
                 outputFolder="",
                 imageFolder="",
                 preload=False):
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
        if imageFolder =="":
            imageFolder = defaultImageFolder
        self.dataFolder = dataFolder
        self.lowerLeftCornerLatitudeLongitude   = lowerLeftCornerLatitudeLongitude
        self.upperRightCornerLatitudeLongitude  = upperRightCornerLatitudeLongitude
        self.outputFolder = outputFolder
        self.imageFolder = imageFolder
        dbzList     = []
        dataFolder      = re.sub(r'\\', '/' , dataFolder)  # standardise:  g:\\ARMOR .. --> g:/ARMOR
        dataSource  = '-'.join(dataFolder.split('/')[-2:]) + '-'
        if name != "":
            self.name = name
        else:
            self.name = dataSource            

        L = os.listdir(dataFolder)
        L = [v for v in L if v.lower().endswith('.txt') or v.lower().endswith('.dat')]  # fetch the data files
        for fileName in L:
            dataTime    = re.findall(r'\d{4}', fileName)
            if len(dataTime)<3:         # NOT DATED DBZ FILE, REJECT
                continue
            dataTime    = dataTime[0] + dataTime[1] + '.' + dataTime[2]
            name        = dataSource + fileName
            dataPath    = dataFolder + fileName
            a = DBZ(dataTime=dataTime, 
                    name=name, 
                    dataPath=dataPath,
                    lowerLeftCornerLatitudeLongitude=lowerLeftCornerLatitudeLongitude,
                    upperRightCornerLatitudeLongitude=upperRightCornerLatitudeLongitude,
                    )
            if preload:
                a.load()
            dbzList.append(a)
        ## there you go! ######
        #
        self.list = dbzList
        #
        #######################

    def __call__(self, N=-999):
        """
        if N is an integer then return the N-th DBZ pattern in the stream
        else if N is a string then return those whose names or dataTimes contains N
        """
        if N == -999:
            return self.list
        elif isinstance(N, int):
            return self.list[N]
        elif isinstance(N, str):
            return [v for v in self.list if N in v.name or N in v.dataTime]

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
        to append a new member to the DBZstream list
        """
        pass

    def regrid(self, b):
        """
        wrapping armor.geometry.regrid.regrid()
        b is another DBZ object representing the grid pattern to be transformed to
        """
        from armor.geometry import regrid
        for i in range(len(self.list)):
            self.list[i] = regrid.regrid(self.list[i], b)

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

    ###########################################################
    #
    #   basic I/O
    def load(self, N=-999, name="", verbose=False):
        """
        N - index of object to be loaded, if N==-999 : load all
        if N is a string, look through the list of dbz objects 
                            and load those whose dataTime string contain N
                                              and whose name contains name
        """
        if N==-999:
            for img in self.list:
                img.load()
        elif isinstance(N, int):
            self.list[N].load()
        elif isinstance(N, str):
            for img in self.list:
                if N in img.dataTime or N in img.name:
                    img.load()
                    if verbose:
                        print img.name, '|',

    def setImageFolder(self, folder):
        for dbzPattern in self.list:
            dbzPattern.imageFolder = folder
            #dbzPattern.imagePath   = folder +  dbzPattern.name + '_'+dbzPattern.dataTime + ".png"
            dbzPattern.imagePath   = folder + dbzPattern.dataTime + ".png"

    def setOutputFolder(self, folder):
        for dbzPattern in self.list:
            dbzPattern.outputFolder = folder
            #dbzPattern.outputPath   = folder +  dbzPattern.name + '_'+dbzPattern.dataTime + ".dat"
            dbzPattern.outputPath   = folder + dbzPattern.dataTime + ".dat"

    ###########################################################
    #
    #   functions on streams, comparisons, etc

    def countLoaded(self):
        """
        return the number of loaded DBZ objects in the stream
        essentially computing those with matrix!=0
        """
        return len([v for v in self if (v.matrix**2).sum()!=0])

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

########################
# demo

a = DBZ('20120612.0200')
b = DBZ('20120612.0210')
ds1 = DBZstream()

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
    ds3 = DBZstream(dataFolder='../data_simulation/20120611_12/', name="WRFoutput", 
                     lowerLeftCornerLatitudeLongitude=(17.7094,113.3272), 
                     upperRightCornerLatitudeLongitude=(28.62909, 127.6353), 
                     preload=False)
except:
    print '../data_simulation/20120611_12/  - NOT FOUND'
    
#a.load()
#b.load()

"""
The following are constructed from data from mr. shue : https://mail.google.com/mail/u/0/?shva=1#search/azteque%40manysplendid.com/14070bb7d7aef48c
wd3
282x342
    MaxLatF                   = 28.62909
    MinLatF                   = 17.7094
    MaxLonF                   = 127.6353
    MinLonF                   = 113.3272

"""

c = DBZ(name='WRF20120612.0200', dataTime='20120612.0200', 
    dataPath= usbRoot + '/data_simulation/20120611_12/out_201206120200.txt',
    lowerLeftCornerLatitudeLongitude= (17.7094, 113.3272),
    upperRightCornerLatitudeLongitude= (28.62909,127.6353) ,
    )

d = DBZ(name='WRF20120612.0210', dataTime='20120612.0210',
    dataPath= usbRoot + '/data_simulation/20120611_12/out_201206120210.txt',
        lowerLeftCornerLatitudeLongitude= (17.7094, 113.3272),
    upperRightCornerLatitudeLongitude= (28.62909,127.6353) ,
  )

