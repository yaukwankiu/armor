# -*- coding: utf-8 -*-
"""
Module to convert DBZstreams into videos

GOAL:
    to make videos of COMPREF/WRF patterns combined:  upper left: COMPREF (size=4x); lower right: COMPREF (next), the rest: WRF

USE:  

cd /media/KINGSTON/ARMOR/python
python
from armor.dataStreamTools import makeVideo as mv
reload(mv); mv.main()


INPUT:
    a list DSS of lists of dataStreams 
    [   [ds1,   ds2,    ds3],
        [ds4,   ds5,    ds6]    ]
OUTPUT:
    a video with the assigned name, with datastreams arranged as in DSS


NOTE:
    Since the images could be too big - we should redraw the charts to smaller sizes (a.saveImage(dpi=40) for a = a pattern.DBZ obejct)  
                                        before plotting
    
CODECS:
    CV_FOURCC('P','I','M','1')    = MPEG-1 codec
    CV_FOURCC('M','J','P','G')    = motion-jpeg codec (does not work well)
    CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2 codec
    CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3 codec
    CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4 codec
    CV_FOURCC('U', '2', '6', '3') = H263 codec
    CV_FOURCC('I', '2', '6', '3') = H263I codec
    CV_FOURCC('F', 'L', 'V', '1') = FLV1 codec

References 
    1. http://stackoverflow.com/questions/5772831/python-library-to-create-a-video-file-from-images
    2. http://stackoverflow.com/questions/5772831/python-library-to-create-a-video-file-from-images
    3. http://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    4. http://opencv.willowgarage.com/documentation/reading_and_writing_images_and_video.html
    5. http://stackoverflow.com/questions/12290023/opencv-2-4-in-python-video-processing/12333066#12333066
            "
            #THE FOLLOWING CODES ARE FROM REFERENCE 3 ABOVE
            To create a video, you could use opencv,
            #load your frames
            frames = ...
            #create a video writer
            writer = cvCreateVideoWriter(filename, -1, fps, frame_size, is_color=1)
            #and write your frames in a loop if you want
            cvWriteFrame(writer, frames[i])
            "
"""

#################
# imports
import time
import os
import pickle
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
try:
    from scipy.misc import imread
except:
    from matplotlib import image as mpimg
    imread = mpimg.imread

import cv, cv2
from armor import pattern
dbz = pattern.DBZ
#timeStamp = str(int(time.time()))

# 'time.struct_time(tm_year=2013, tm_mon=9, tm_mday=30, tm_hour=14, tm_min=54, tm_sec=28, tm_wday=0, tm_yday=273, tm_isdst=0)'
localtime = time.localtime()    # 2013-09-30
year    = localtime.tm_year
month   = localtime.tm_mon
day     = localtime.tm_mday
hour    = localtime.tm_hour
minute  = localtime.tm_min

timeString = '-'.join([str(v) for v in [year, month, day, hour, minute]])  # 2013-09-30
timeStamp = timeString #alias

##################
# setup
from .. defaultParameters import *

defaultFrameSize    = (1600,1200)
defaultFps          = 1

defaultInput1       = hardDriveRoot + 'data/KONG-REY/summary/COMPREF/dbzstreamLoaded.pydump'
defaultInputFolder2 = hardDriveRoot + 'data/KONG-REY/summary/WRF[regridded]/'
defaultInputs2      = sorted([defaultInputFolder2+v for v in os.listdir(defaultInputFolder2) if v.endswith('.pydump')])
sandbox             = hardDriveRoot + 'data/KONG-REY/temp/' 
defaultOutputFolder = sandbox
try:
    os.makedirs(defaultOutputFolder)
except OSError:
    print defaultOutputFolder, "folder exists!"

def loadDataStreams(paths):
    if not isinstance(paths, list):
        paths = [paths]
    DSS = []
    for path in paths:
        ds = pickle.load(open(path, 'r'))
        DSS.append(ds)
    return DSS
        

def makeDBZimages(ds, flipud=True, drawCoast=True, outputFolder=sandbox, toLoad=False, dpi=200):
    if toLoad:
        ds.load()
    ds.imageFolder=outputFolder + ds.name + '/'
    ds.saveImages(drawCoast=drawCoast, flipud=flipud, dpi=dpi)


def loadImages(inputFolder=sandbox, key1="", key2="", key3='.png', key4='.jpg'):
    try:
        L = [v for v in os.listdir(inputFolder) if key1 in v and key2 in v and key3 in v and key4 in v]
        #print inputFolder
        #print L
        imageList=[""]*len(L)
        for n, fileName in enumerate(L):
            #img = Image.open(inputFolder+fileName)  # doesn't work
            #imageList[n] = cv.LoadImage(inputFolder+fileName)  #old
            try:
                imageList[n] = imread(inputFolder+fileName)     # new, converted to cv2
                print n, inputFolder, fileName
            except:
                print n, inputFolder, fileName, "loadImages print!!!!!!!!!!!!!!!!"
            #ERROR imageList[n]
        return imageList
    except:
        print "loadImages ERROR!!!!!!!!"


def makeVideo( DSS,      # [ds0, ds1, ds2, ds3, ds4, ...], a list of armor.pattern.DBZstream objects
               panel_cols = 5,              # number of colums in the panel
               panel_rows = 5,              # no need to be filled
               fourcc = cv.CV_FOURCC('F', 'L', 'V', '1'),
               fps = defaultFps,
               extension= '.avi',
               #fourcc = cv.CV_FOURCC('P', 'I', 'M', '1'),
               outputFileName ="",
               outputFolder=defaultOutputFolder,
               sandbox=sandbox,             # added 2013-09-23
               saveFrames = True,        # saving the frames as images
               frameDpi = 200,          # added 2013-09-23
               useCV2   = False,        # opencv doesn't work! switched off!!!
               useCV    = False,        # ditto
               ordering = "",           # ordering of the models
              ):    
    """
    INPUT:fo
        DSS - a list of list of DBZ objects
              unloaded to save memory - we just need the ds.imageFolder's
    OUTPUT:
        video
    """
    if outputFileName=="":
        outputFileName = timeStamp + extension
    imageFolders    = [v.imageFolder for v in DSS]
    for ds in DSS:
        ds.tempImagePaths = sorted(os.listdir(ds.imageFolder))
    if ordering =="":
        # no ordering specifieed (backward compatibility)
        # do nothing, and define the ordering to be precise
        ordering = [v for v in range(len(DSS))]  # [0, 1, 2, .., len(DSS)-1]
    else:
        # if ordering is specified, reorder DSS
        # DSS = [DSS[ordering[i]] for i in range(len(DSS))]
        pass  # do nothing here - since the ordering of the DSS could be different for each dataTime,
                # we move the reordering into the dataTime loop
    #####################################################
    #       2. initialise background, initialise writer
    try:
        os.makedirs(outputFolder)
    except OSError:
        print outputFolder, 'folder exists!'

    try:
        print DSS[1][1].imagePath
        sampleImage = imread(DSS[1][1].imagePath)
    except IndexError:
        try:
            print DSS[1][0].imagePath
            sampleImage = imread(DSS[1][0].imagePath)
        except IndexError:
            print DSS[0][0].imagePath
            sampleImage = imread(DSS[0][0].imagePath)

    height, width, depth = sampleImage.shape
    # initialise (black) currentFrame
    #currentFrame = np.ones((1200,1200,3))  #(1200x1200x3)
    sampleFrame = sampleImage        # pick ds1 rather than ds0 since ds0 (observation) may be of a different size
    sampleFrame = sampleFrame *0 +1
    sampleFrame = np.hstack([sampleFrame] * panel_cols)   #   | | | | |    
    sampleFrame = np.vstack([sampleFrame] * panel_rows)   #   =======

    #dataTimeList = sorted(list(set(sum([[v.dataTime for v in ds0] for ds0 in DSS], []))))  # doesn't seem to work 2013-09-24
    dataTimeList = set([v.dataTime for v in DSS[0]])                                        # the follow loop replaces the line above
    for ds0 in DSS[1:]:
        dataTimeList = dataTimeList.intersection([v.dataTime for v in ds0])
    dataTimeList = sorted(list(dataTimeList))
    print dataTimeList
    time.sleep(3)

    #debug
    #plt.imshow(currentFrame)
    #plt.show()
    # end debug
    if useCV2:
        """
        writer = cv2.VideoWriter(filename=outputFolder + outputFileName,
                                fourcc=fourcc,
                                fps=fps,
                                #frameSize = (1200,1200),    
                                frameSize= (width*panel_cols, height*panel_rows),
                                #frameSize = defaultFrameSize,
                                )
        """    
        writer = cv2.VideoWriter(outputFolder + outputFileName,
                                fourcc,
                                fps,
                                #frameSize = (1200,1200),    
                                (width*panel_cols, height*panel_rows),
                                #frameSize = defaultFrameSize,
                                1,  # test  http://courses.cs.washington.edu/courses/cse599j/12sp/final_projects/Dave_Lattanzi/video_writer.py
                                )
    elif useCV:
        writer=cv.CreateVideoWriter(outputFolder + outputFileName, 
                                    fourcc, 
                                    fps, 
                                    defaultFrameSize, 
                                    True)
    else:
        writer = None

    if writer is None:
        print 'writer cannot be created'
        #xxx=raw_input('press enter')
        time.sleep(3)
    else:
        print "writer created"

    print '--------------------------------------------------------'
    print "ordering:"    
    print '\n'.join([str(v) for v in ordering])
    for M, dataTime in enumerate(dataTimeList):
        currentFrame = sampleFrame *0 +1
        # debug
        #plt.imshow(currentFrame)
        #plt.show()
        print '\n.....................................................'
        print dataTime
        #for N, ds in enumerate(DSS):
        for N, ds in enumerate([DSS[ordering[M][i]] for i in range(len(DSS))]):
            if N >= panel_cols * panel_rows:        # we have room only for so many
                break
            print ds.name,
            D = ds(dataTime)     # getting the DBZ pattern of the given datastream ds corresponding to the given model at the given dataTime 
            if len(D) == 0:
                print '-XX\t',
                continue
            else:
                D = D[0]
                print ':-)\t',
                # debug
                #print D.imagePath, '...',

            #2. load paste the new image and paste it to the frame
            #  e.g. /.../CWB/charts/2013-05-17/2013-05-17_1530.MOS0.jpg
            try:
                img = imread(D.imagePath) 
                #debug
                #print D.imagePath,
                print 'READ!\t',
            except: 
                continue
            # debug
            # plt.imshow(img)
            #plt.imshow(currentFrame)
            #plt.show()
            # end debug
            hor_displ = (N % panel_cols) * width     # horizontal displacement
            vert_displ = (N//panel_cols) *height  # vertical displacement
            currentFrame[vert_displ:vert_displ+height, hor_displ:hor_displ+width, :] = img 
            # debug
            #print hor_displ, vert_displ
            # end debug
        framePath = sandbox+ 'DBZ' + dataTime +'.png'
        if saveFrames:
            #debug
            plt.imshow(currentFrame)
            # plt.show()
            plt.savefig(framePath, dpi=frameDpi)
            #cv.SaveImage( sandbox+str(int(time.time()))+'.png', currentFrame)
            plt.close()
        print 'writing...'
        # convert the image from 4-channel png to 3-channel jpg
        # http://www.comp.nus.edu.sg/~cs4243/conversion.html
        cimg = cv.LoadImage(framePath,cv.CV_LOAD_IMAGE_COLOR)        # hack
        pimg = Image.fromstring("RGB", cv.GetSize(cimg), cimg.tostring()) 
        arr  = np.array(pimg)
        #debug
        #plt.imshow(arr)
        #plt.show()
        print 'arr.shape:',arr.shape
        print 'arr.sum():', arr.sum()
        #writer.write(currentFrame)    
        if useCV2:
            writer.write(arr)
        elif useCV:
            # try this http://stackoverflow.com/questions/16897480/making-a-video-with-opencv-getting-only-1-frame
            cv.WriteFrame(writer, cimg)
        ##########################################
        # trim the loaded data to save space
        for ds in DSS:
            ds.unload(dataTime)

    print 'frameSize', (width*panel_cols, height*panel_rows)
    print "type(writer):", type(writer)
    #writer.release()

def main(toMakeImages=True, dpi=80, constructDSS=True, 
          fourcc=cv.CV_FOURCC('F', 'L', 'V', '1') ,
           extension ='.avi',
           saveFrames=True,
           useCV2=True,
        ):
    '''
    cd /media/KINGSTON/ARMOR/python
    python
    from armor.dataStreamTools import makeVideo as mv
    reload(mv) ; DSS=mv.main(toMakeImages=False, saveFrames=False, dpi=80, useCV2=False)
    '''
    inputPaths = [defaultInput1] + defaultInputs2  # paths for the pydumps for the data streams
    #print inputPaths #debug
    #DSS = loadDataStreams(inputPaths)  # this works too but may take some memory and time
    DSS = []        # our main object of interest

    ############################################################################
    #
    # either 1.    
    if constructDSS:
        for path in inputPaths:
            print '............................'
            print path
            ds = pickle.load(open(path, 'r'))
            print ds.name
            ds.setVmin(-40)
            if toMakeImages:
                makeDBZimages(ds, outputFolder=sandbox, toLoad=False, drawCoast=True, flipud=True, dpi=dpi) 
            else:
                ds.setImageFolder(sandbox + ds.name + '/')
            ds.unload()         # after plotting the images, we no longer need the data
            DSS.append(ds)
        pickle.dump(DSS, open(sandbox+'DSS.pydump','w'))
    ##############
    # or    2.
    else:
        DSS = pickle.load(open(sandbox+'DSS.pydump','r'))
    #
    ############################################################################
    # key function call
    makeVideo(DSS, fourcc=fourcc, extension=extension, useCV2=useCV2,
                saveFrames=saveFrames) # saveFrames should be true for the moment since we need the pics to 
                                                                              # create the videos
    print 'time now:' , time.asctime(), int(time.time())
    print 'timestamp', timeStamp
    print 'time spent', int(time.time())-int(timeStamp)
    return DSS

"""
CODECS:
    CV_FOURCC('P','I','M','1')    = MPEG-1 codec
    CV_FOURCC('M','J','P','G')    = motion-jpeg codec (does not work well)
    CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2 codec
    CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3 codec
    CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4 codec
    CV_FOURCC('U', '2', '6', '3') = H263 codec
    CV_FOURCC('I', '2', '6', '3') = H263I codec
    CV_FOURCC('F', 'L', 'V', '1') = FLV1 codec
"""
