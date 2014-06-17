# -*- coding: utf-8 -*-
'''
makeVideo2.py
version of makeVideo.py with different panel content settings

copy of /media/KINGSTON/ARMOR/python/armor/video/makeVideo.py


USE:
python makeVideo2.py 2013-08-18
'''

"""
Module to convert videos from jpgs or pdfs
USE:  

cd /media/KINGSTON/ARMOR/python
python
from armor.video import makeVideo as mv
reload(mv); mv.main()
mv.main(inputDate='2013-07-12', inputType='satellite1')
mv.main(inputDate='2013-07-12', inputType='satellite4')
import time
t0=time.time()
reload(mv); mv.makeVideoAll(inputType='rainfall1')
reload(mv); mv.makeVideoAll(inputType='satellite2')
reload(mv); mv.makeVideoAll(inputType='charts')
print '\n\ntime spent all in all:', time.time()-t0, '\n\n\n'
time.sleep(10)
t0=time.time()
reload(mv); mv.makeVideoAll(inputType='temperature')
reload(mv); mv.makeVideoAll(inputType='charts2')
reload(mv); mv.makeVideoAll(inputType='rainfall2')
#reload(mv); mv.makeVideoAll(inputType='satellite1')
reload(mv); mv.makeVideoAll(inputType='satellite3')
#reload(mv); mv.makeVideoAll(inputType='satellite4')
print 'time spent all in all:', time.time()-t0

import time
t0=time.time()
reload(mv); mv.makeVideoAll(inputType='rainfall1') ; mv.makeVideoAll(inputType = 'satellite2') ; mv.makeVideoAll(inputType='charts')
print 'time spent all in all:', time.time()-t0

    and check /media/Seagate\ Expansion\ Drive/ARMOR/sandbox 
    or something like that

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
import numpy as np
from matplotlib import pyplot as plt
#from PIL import Image
try:
    from scipy.misc import imread
except:
    from matplotlib import image as mpimg
    imread = mpimg.imread

import cv, cv2
#from armor import pattern  # armor module switched off
#dbz = pattern.DBZ

##################
# setup
#from .. defaultParameters import *
#dataRoot    = externalHardDriveRoot + '../Work/CWB/'
dataRoot = './'
defaultDate = '2013-07-12'
defaultType = 'charts'
defaultInputFolder  = dataRoot + defaultType + '/' + defaultDate +'/'
#defaultOutputFolder = externalHardDriveRoot + 'sandbox/'
defaultOutputFolder = './videos/'

defaultFrameSize    = (1600,1600)  # opencv convention - (x,y)
defaultFps          = 12
defaultFourcc       = cv.CV_FOURCC('F', 'L', 'V', '1')
defaultExtension    = '.avi'
defaultInputTypes  =    ['hq'  , 'charts', 'satellite2',
                        'hs1q' , 'hs1p']
defaultPanelPositions  = [(0,0), (0,400), (0,1000),
                          (600,0), (600,800)        ]  # my convention - (i,j)=(y,x)


def getList(folder, extensions=['.txt','.dat']):
    try:
        L = os.listdir(folder)
        L = [v for v in L if v[-4:].lower() in extensions]
        #print L
        L.sort()
        return L   
    except:
        print 'getList ERROR!!!!!!'
"""
armor module switched off
def makeDBZimages(inputFolder=defaultInputFolder, 
                 outputFolder=defaultOutputFolder, extensions=['.txt', '.dat']):
    L = getList(folder=inputFolder, extensions=extensions)
    for fileName in L:
        a = dbz(name=fileName, dataPath=inputFolder+fileName, 
                imagePath=defaultOutputFolder+fileName)
        a.load()
        a.saveImage()
"""
def loadImages(inputFolder=defaultOutputFolder, extensions=['.png', '.jpg']):
    """yes that's right
         inputFolder=defaultOutputFolder
       because we expect the pics to be in the sandbox (i.e. default output folder)
    """
    try:
        L = getList(folder=inputFolder, extensions=extensions)
        #print inputFolder
        #print L
        #print extensions
        imageList=[""]*len(L)
        #print L
        for n, fileName in enumerate(L):
            #img = Image.open(inputFolder+fileName)  # doesn't work
            #imageList[n] = cv.LoadImage(inputFolder+fileName)  #old
            try:
                imageList[n] = imread(inputFolder+fileName)     # new, converted to cv2
                print n, inputFolder, fileName
            except:
                print n, inputFolder, fileName, "loadImages ERROR!!!!!!!!!!!!!!!!"
            #print imageList[n]
        return imageList
    except:
        print "loadImages ERROR!!!!!!!!"

def makeVideo(imageList, 
              outputPath= defaultOutputFolder+ str(int(time.time()))+defaultExtension,
              fourcc=defaultFourcc,
              fps = defaultFps,
              frameSize=defaultFrameSize):
    #print imageList
    # create a video writer
    # c.f. http://opencv.willowgarage.com/documentation/python/reading_and_writing_images_and_video.html
    #fourcc=cv.FOURCC('P','I','M','1'), doesn't work?
    #writer = cv.CreateVideoWriter(filename=outputFolder+inputDate+'_'+inputType+'.avi', 
    #                                fourcc=cv.FOURCC('F', 'L', 'V', '1'),
    #                                fps=1, frame_size=(600,600), is_color=1)
        #and write your frames in a loop if you want
    # the above don't work.  replace by the following.
    # http://stackoverflow.com/questions/12290023/opencv-2-4-in-python-video-processing/12333066#12333066    
    time0 = time.time()
    writer = cv2.VideoWriter(filename=outputPath, 
                            fourcc=fourcc,
                            fps=fps,
                            frameSize=frameSize)
    for frame in imageList:
        #print frame
        #cv.ShowImage(str(frame), frame)
        #cv.WaitKey()
        #cv.WriteFrame(writer, frame) #old writer replaced
        writer.write(frame)
        

def makeVideoAll(inputType   = defaultType,
                 inputFolder = "",
                 extensions  = ['.png', '.jpg'],
                outputFolder = "",
                      fourcc = defaultFourcc,
                         fps = defaultFps,
                    frameSize=defaultFrameSize):
    """
    cd /media/KINGSTON/ARMOR/python/
    python
    from armor.video import makeVideo as mv
    reload(mv) ; mv.makeVideoAll(inputType="charts2")
    """
    time0 = time.time()
    if inputFolder == "":
        inputFolder = "%s%s/" % (dataRoot, inputType)
    if outputFolder =="":
        outputFolder = defaultOutputFolder + inputType + '_' + str(int(time.time())) +'/'
    #debug
    print inputFolder
    os.makedirs(outputFolder)
    LL = os.listdir(inputFolder)
    LL.sort()
    for folder in LL:
       imageList = loadImages(inputFolder=inputFolder+folder+'/', extensions=extensions)
       try:
            print folder
            makeVideo(imageList, 
                  outputPath= outputFolder + folder + '_' + inputType + defaultExtension,
                  fourcc=fourcc,
                  fps  = len(imageList),
                  #fps = len(imageList)/10.  ,            
                  frameSize=frameSize)        # frames per sec = len(imageList)/10.
                                               #    - so that each day lasts  10 seconds
                                                #        no matter how many frames there are
                                                                                  
       except:
            print folder, "makeVideo ERROR!!!!!!!!!!!"  # don't care if it doesn't work
            time.sleep(3)
    print time.time()-time0


def main(inputDate=defaultDate, inputType=defaultType, inputFolder="", 
         outputFolder=defaultOutputFolder, extensions=['.png','.jpg'], 
         fps = '',
         frameSize=defaultFrameSize):
    """
    USE: 
        main(inputDate=defaultDate, inputType=DefaultType, inputFolder="", outputFolder="")
    WHERE:
        defaultDate = '2013-07-12'
        defaultType = 'charts'
    OUTPUT:
        out

    """
    time0 = time.time()
    if inputFolder == "":
        inputFolder = "%s%s/%s/" % (dataRoot, inputType, inputDate)

    #print inputFolder
    imageList = loadImages(inputFolder=inputFolder, extensions=extensions)
    if fps =='':
        fps = len(imageList)/10.      # frames per sec = len(imageList)/10.
                                       #    - so that each day lasts 10 seconds
                                        #        no matter how many frames there are
    makeVideo(imageList=imageList,
              outputPath=outputFolder+inputDate+'_'+inputType+defaultExtension, 
              fourcc=defaultFourcc,
              fps=fps,
              frameSize=frameSize)  
    print outputFolder+inputDate+'_'+inputType
    print time.time()-time0
    
"""
CV_FOURCC('P','I','M','1')    = MPEG-1 codec

CV_FOURCC('M','J','P','G')    = motion-jpeg codec (does not work well)

CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2 codec

CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3 codec

CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4 codec

CV_FOURCC('U', '2', '6', '3') = H263 codec

CV_FOURCC('I', '2', '6', '3') = H263I codec

CV_FOURCC('F', 'L', 'V', '1') = FLV1 codec

"""

def makeVideoFourInOne(inputTypes = defaultInputTypes,
                       outputFolder = "",
                           fourcc = defaultFourcc,
                           fps = defaultFps,
                           extension= defaultExtension,
                           #fourcc = cv.CV_FOURCC('P', 'I', 'M', '1'),
                           #extension= '.mpg',
                           #   fps = defaultFps,
                        frameSize = defaultFrameSize,
                        panelPositions = defaultPanelPositions,
                        startingFromDate=""):
    

    # sizes- rainfall1: 400x400;  charts:  600x600 ; temperature: 400x400 ; satellite2: 430,400
    # == USE ==
    # cd /media/KINGSTON/ARMOR/python
    # python
    # from armor.video import makeVideo as mv
    # reload(mv) ; mv.makeVideoFourInOne()
    # reload(mv) ; mv.makeVideoFourInOne(startingFromDate='2013-08-15')

    # plan: 1. get four lists of file paths [(datetime, type) -> path]
    #       2. initialise background
    #       3. for each datetime do 
    #           1.look for relevant path, return blank if not found
    #           2. load paste the new image and paste it to the frame, do nothing if not found
    #           3. write the frame to the video
    ######################################################################
    #
    # 1. get four lists of file paths [(datetime, type) -> path]
    #
    if outputFolder =="":
        outputFolder = defaultOutputFolder + '_'.join(inputTypes) + '_' + str(int(time.time())) + '/'
    fileNameDict = {}
    for inputType in inputTypes:
        LL = os.listdir(dataRoot+inputType)
        for inputDate in LL:
            if not os.path.isdir(dataRoot+inputType+'/'+inputDate) :     # not valid data
                continue
            L = os.listdir(dataRoot+inputType+'/'+inputDate)
            if L == []:                                         # empty folder
                continue
            for fileName in L:
                # ('charts', '2013-05-17_1530') -> 2013-05-17_1530.MOS0.jpg
                fileNameDict[(inputType, fileName[:15])] = fileName
    #####################################################
    #       2. initialise background, initialise writer
    os.makedirs(outputFolder)
    #currentFrame = np.ones((1200,1200,3))  #(1200x1200x3)
    currentFrame = imread(dataRoot+defaultType+ '/2013-05-17/2013-05-17_1230.MOS0.jpg')
    currentFrame = np.hstack([currentFrame, currentFrame])    
    currentFrame = np.vstack([currentFrame, currentFrame])
    currentFrame = currentFrame *0 +1
    #debug
    #plt.imshow(currentFrame)
    #plt.show()
    # end debug
    dateTimeList = sorted([   v[1] for v in fileNameDict.keys() \
                           if v[1]>startingFromDate])  
                           # e.g. '2013-05-17_1530' > '2013-05-16'
    # DEBUG
    #print dateTimeList, startingFromDate
    #x=raw_input('press enter:')
    ## END DEBUG
    inputDateList = sorted(list(set([v[:10] for v in dateTimeList])))
    for inputDate in inputDateList:
        print inputDate
        #split the video into dates
        dateTimeListShort = [v for v in dateTimeList if inputDate in v]
        #debug
        #print outputFolder +inputDate +extension
        #print fourcc
        #print fps
        #print frameSize
        # end debug
        # initialise video writer
        writer = cv2.VideoWriter(filename=outputFolder +inputDate +extension, 
                                fourcc=fourcc,
                                fps=fps,
                                frameSize=frameSize)
        # initialise (black) currentFrame for each day
        # added 2013-08-16
        currentFrame = imread(dataRoot+defaultType + \
                              '/2013-05-17/2013-05-17_1230.MOS0.jpg')
        currentFrame = np.hstack([currentFrame, currentFrame, currentFrame])    
        currentFrame = np.vstack([currentFrame, currentFrame, currentFrame])
        currentFrame = currentFrame *0 +1
        currentFrame = currentFrame[:1600,:1600,:] # trim
        #####################################################
        #       3. for each datetime do 
        #           1.look for relevant path, return blank if not found
        #           2. load paste the new image and paste it to the frame, do nothing if not found
        #           3. write the frame to the video

        for dateTime in dateTimeListShort:        # e.g. '2013-05-17_1530'
            print "\n*****", dateTime, "******"
            # can add some logics here to pick out specific dates and times
            # too lazy to do it here
            for N, inputType in enumerate(inputTypes):     # e.g. 'charts'
                print inputType, 
                if (inputType, dateTime) not in fileNameDict.keys():
                    print '-X',
                    continue
                #2. load paste the new image and paste it to the frame
                #  e.g. /.../CWB/charts/2013-05-17/2013-05-17_1530.MOS0.jpg
                fileName = fileNameDict[(inputType, dateTime)]
                filePath = dataRoot +inputType +'/' + dateTime[:10] +'/' + fileName
                if os.path.getsize(filePath) < 3000:    #invalid file
                    continue
                img = 0  
                try:
                    img = imread(dataRoot +inputType +'/' + dateTime[:10] +'/' + fileName) 
                except: 
                    print fileName, '- cannot be included'
                    continue

                # debug
                print dataRoot +inputType +'/' + dateTime[:10] +'/' + fileName
                #plt.imshow(currentFrame)
                #plt.show()
                # end debug
                try:
                    height, width, depth = img.shape
                    hor_displ = panelPositions[N][1]  # horizontal displacement: 1,2,3 ; 4,5
                    vert_displ =panelPositions[N][0] # vertical displacement:  1,2,3 ; 4,5
                    currentFrame[vert_displ:vert_displ+height, hor_displ:hor_displ+width, :] = img 
                except ValueError:
                    print 'ValueError!!'
                    continue
                # debug
                #print hor_displ, vert_displ
                # end debug

            writer.write(currentFrame)
                
if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args)>=1:
        makeVideoFourInOne(startingFromDate=args[0])
    else:
        x = raw_input('do you really want to remake all videos from the beginning? ctrl-break out if not.')
        makeVideoFourInOne()
        
        
