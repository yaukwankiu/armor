# -*- coding: utf-8 -*-
####################################
#   imports 
import time, datetime
import platform


####################################
# computer settings

computer = 'asus-laptop'
if platform.node() == 'k-Aspire-E1-571G':
    computer = 'acer-laptop'
elif platform.node() == 'k-801':
    computer = 'k-801'  # 801-desktop
elif platform.node() == 'k-acer':
    computer = 'k-acer'  # ubuntu 12.04/Win7 acer laptop
elif platform.node() == 'zxc-Aspire-E1-571G':
    computer = 'k-acer'  # ubuntu 12.04/Win7 acer laptop
elif platform.node()== 'Qoo-PC':
    computer = 'Qoo-PC'


#computer = 'i5-desktop'

print "computer: ", computer

defaultInputFolder              = "../data_temp/"
defaultOutputFolder             = "testing/"
defaultOutputFolderForImages    = defaultOutputFolder
defaultImageFolder              = defaultOutputFolderForImages  #alias
defaultDatabase                 = ""        #not used yet
defaultImageExtension           = '.png'    # added 2013-09-27
defaultImageTopDown             = False


if computer == 'acer-laptop':
    #usbDriveName    = 'k/KINGSTON'
    #externalHardDriveName = 'k/Seagate Expansion Drive'
    #externalHardDriveName2= 'k/A4ECB939ECB90718'
    #hardDriveName   = 'DATA'
    usbDriveName    = 'TOSHIBA EXT'
    externalHardDriveName = 'TOSHIBA EXT'
    externalHardDriveName2= 'TOSHIBA EXT'
    hardDriveName   = 'DATA'
elif computer == 'k-801':
    usbDriveName    = 'k/KINGSTON'
    externalHardDriveName = 'k/FreeAgent Drive' #?!
    externalHardDriveName2= 'k/A4ECB939ECB90718'
    hardDriveName   = '../home/k'

elif computer == 'k-acer':      #acer- ubuntu - main platform 2014-02-19
    #usbDriveName    = 'KINGSTON'
    #externalHardDriveName = 'FreeAgent Drive' #?!
    #externalHardDriveName2= 'A4ECB939ECB90718'
    #hardDriveName    = 'home/k'
    #hardDriveName2   = 'data'
    usbDriveName    = 'TOSHIBA EXT'
    externalHardDriveName = 'TOSHIBA EXT'
    externalHardDriveName2= 'TOSHIBA EXT'
    #hardDriveName   = '051798CD6AAE5EEF'
    hardDriveName   = 'media/TOSHIBA EXT'

else:
    usbDriveName    = 'KINGSTON'
    externalHardDriveName = 'Seagate Expansion Drive'
    externalHardDriveName2= 'A4ECB939ECB90718'
    hardDriveName   = 'host'



if computer == 'acer-laptop':
    usbDriveLetter ='H'
    externalHardDriveLetter = 'G'
    hardDriveLetter = 'D'
elif computer == 'i5-desktop':
    usbDriveLetter ='G'
    externalHardDriveLetter = 'D'
    hardDriveLetter = 'C'
elif computer == 'asus-laptop':
    usbDriveLetter ='I'     #forgot
    externalHardDriveLetter = 'G'  #forgot
    hardDriveLetter = 'D'    
elif computer == 'k-801':
    usbDriveLetter ='I'     #forgot
    externalHardDriveLetter = 'G'  #forgot
    hardDriveLetter = 'D'    #FORGOT
elif computer == 'k-acer':
    usbDriveLetter ='I'     #don't know yet
    externalHardDriveLetter = 'G'  #don't know yet
    hardDriveLetter = 'D'    #don't know yet
elif computer =='Qoo-PC':
    usbDriveLetter ='D'     
    externalHardDriveLetter = 'D'  
    hardDriveLetter = 'D'    
    hardDriveLetter2 = 'D'    
    

################################
# need to check the following
#elif computer == 'k-801':
#    usbDriveLetter ='I'     #forgot
#    externalHardDriveLetter = 'G'  #forgot
#    hardDriveLetter = 'D'    

import os
if os.sep == "/":
    usbRoot = '/media/%s/ARMOR/' % usbDriveName
    externalHardDriveRoot = '/media/%s/ARMOR/' % externalHardDriveName
    externalHardDriveRoot2 = '/media/%s/ARMOR/' % externalHardDriveName2
    hardDriveRoot = '/%s/ARMOR/' % hardDriveName
else:
    usbRoot = '%s:/ARMOR/' % usbDriveLetter
    externalHardDriveRoot = '%s:/ARMOR/' % externalHardDriveLetter
    externalHardDriveRoot2 = '%s:/ARMOR/' % hardDriveLetter2 # don't know this yet
    hardDriveRoot = '%s:/ARMOR/' % hardDriveLetter

defaultRootFolder   = usbRoot    # can choose (= .../ARMOR/)
defaultRoot         = defaultRootFolder     #alias
root                = defaultRootFolder     #alias
rootFolder          = defaultRootFolder     #alias

defaultLabReportsFolder = defaultRootFolder + 'labReports/'
defaultLabReportFolder  = defaultLabReportsFolder   #alias

defaultLabLogsFolder    = 'labLogs/'
defaultLabLogFolder    = defaultLabLogsFolder   #alias

################################################################
# geography

# taichung park coordinates (24.145056°N 120.683329°E)

#defaultTaiwanReliefDataFolder = defaultRootFolder+'armor/taiwanReliefData/'
defaultTaiwanReliefDataFolder = defaultRootFolder+'data/taiwanRelief881/'    #2014-06-12
defaultTaiwanReliefDataFolder881 = defaultRootFolder+'data/taiwanRelief881/'    #2014-06-12
defaultTaiwanReliefDataFolder150 = defaultRootFolder+'data/taiwanRelief150/'    #2014-06-12

taichungParkLatitude = 24.145056
taichungParkLongitude= 120.683329

#   2014-01-19
taipeiLatitude  = 25.0333   # google
taipeiLongitude = 121.6333
taipei          = (taipeiLatitude, taipeiLongitude)

tainanLatitude  = 22.9833
tainanLongitude = 120.1833
tainan          = ( tainanLatitude, tainanLongitude)

kentingLatitude     = 21.9800
kentingLongitude    = 120.7970
kenting             = (kentingLatitude, kentingLongitude )

hualienLatitude     = 23.9722
hualienLongitude    = 121.6064
hualien             = (hualienLatitude ,hualienLongitude  )

taitungLatitude     = 22.7583
taitungLongitude    = 121.1444
taitung             = ( taitungLatitude,taitungLongitude  )

#   from armor.tests.projectProposal20140119
taipeiCounty    = (530, 500, 60, 60)
taichungCounty  = (475, 435, 40, 80)
tainanCounty    = (390, 400, 40, 50)
kaohsiungCounty = (360, 410, 70, 70)
yilanCounty     = (500, 500, 50, 50)
hualienCounty   = (410, 480, 100, 60)
taitungCounty   = (335, 460, 100, 60)
kenting         = (319, 464)
sector7         = (464, 504, 96, 60)
sector2         = (428, 396, 96, 108)
sector1         = (500, 432, 96, 120)
allReg          = (300, 100, 500, 600)


##############################################################
# input image info
#   ..........................................................
#   COMPREF
defaultHeight                   = 881
defaultWidth                    = 921
defaultLowerLeftCornerLatitudeLongitude = (18., 115.)   # p.25, https://docs.google.com/file/d/0B84wEiWytQMwemhzX3JkQ1dSaTA/edit 
defaultUpperRightCornerLatitudeLongitude = (29., 126.5)   # p.25, https://docs.google.com/file/d/0B84wEiWytQMwemhzX3JkQ1dSaTA/edit 
#missingDataThreshold            = -150. # anything below " missingDataThreshold is marked as "masked"
defaultMissingDataThreshold            = -150. # anything below " missingDataThreshold is marked as "masked"    # this line replaces the line above 2014-02-20
missingDataThreshold = defaultMissingDataThreshold  # this line is for backward compatibility if any
#defaultThreshold                = missingDataThreshold
#   ..........................................................
#   WRF
"""
defaultHeight                   = 881
defaultWidth                    = 921
defaultLowerLeftCornerLatitudeLongitude = (18., 115.)   # p.25, https://docs.google.com/file/d/0B84wEiWytQMwemhzX3JkQ1dSaTA/edit 
defaultUpperRightCornerLatitudeLongitude = (29., 126.5)   # p.25, https://docs.google.com/file/d/0B84wEiWytQMwemhzX3JkQ1dSaTA/edit 
#missingDataThreshold            = -150. # anything below " missingDataThreshold is marked as "masked"
defaultMissingDataThreshold            = -150. # anything below " missingDataThreshold is marked as "masked"    # this line replaces the line above 2014-02-20
missingDataThreshold = defaultMissingDataThreshold  # this line is for backward compatibility if any
#defaultThreshold                = missingDataThreshold
"""
defaultWRFHeight    = 150
defaultWRFWidth     = 140
defaultWRFLowerLeftCornerLatitudeLongitude      = (20., 117.5)
#defaultWRFUpperRightCornerLatitudeLongitude     = (28., 124.5)
defaultWRFUpperRightCornerLatitudeLongitude     = (27.-0.05, 124.5-0.05)  #2014-06-13

LL  = defaultWRFLowerLeftCornerLatitudeLongitude  #alias    #2014-06-02
UR  = defaultWRFUpperRightCornerLatitudeLongitude  #alias

################################################################
#   plotting
from . import colourbar
defaultCmap = colourbar.cmap

################################################################
#   filenames
defaultImageSuffix = ".png"
#defaultDataSuffix1 = ".txt"
#defaultDataSuffix2 = ".dat"

################################################################
#   misc

defaultTimeString   = str(int(time.time()))

localtime   = time.localtime()
year        = localtime.tm_year
month       = localtime.tm_mon
day         = localtime.tm_mday
hour        = localtime.tm_hour
minute      = localtime.tm_min
second      = localtime.tm_sec





