# downloadpics.py
# python script to download cwb radar patterns for today
# examples : 
# http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/2013-05-19_0015.MOS0.jpg  (with relief)
# http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/2013-05-20_0045.2MOS0.jpg (without relief)
# http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-2013-05-20-15-30.jpg (visible spectrum)
# http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-2013-05-20-15-30.jpg (colours)
# http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-2013-05-20-15-30.jpg (enhanced colours)
# http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-2013-05-20-15-30.jpg (black and white)
# http://cwb.gov.tw/V7/observe/temperature/Data/2013-05-20_1300.GTP.jpg  (temperature)
# http://cwb.gov.tw/V7/observe/rainfall/Data/hk520153.jpg               (rainfall -small grid)
# http://cwb.gov.tw/V7/observe/rainfall/Data/2013-05-20_1530.QZJ.grd2.jpg (rainfall -large gird)
# 
# 
# 

"""
USE:
0. install python (preferrably 2.7, though 2.5 probably suffices)
1. put this script in any folder (for me, it is f:\work\CWB\)
2. just run it;  the folders will be created automatically: 
                        .\charts for radar patterns with taiwan relief
                        .\charts2 for pure patterns with taiwan coastline

3. to run:  (for example, if your python.exe is in c:\python27 just like mine)

    c:\python27\python.exe downloadpics.py

4. to download a specific date:
    uncomment and edit the following line:
    url_date = "2013-05-18"   ###### <-------- UNCOMMENT THIS TO GET A SPECIFIC DATE  #########

NOTE:
    At present the Central Weather Bureau keeps every radar pattern for 48 hours.

"""


########################################################################################
# imports
import urllib
import urllib2
import zipfile
import re  
import os
import sys
from datetime import date, timedelta
import time

########################################################################################
# defining the container class
# added 2013-08-21

class Url_info:
    def __init__(self, url_root, url_suffix, outputFolder, timeStringType):
        self.url_root       = url_root
        self.url_suffix     = url_suffix
        self.outputFolder   = outputFolder
        self.timeStringType =  timeStringType
########################################################################################
# default parameters and settings - CHANGE THESE TO GET SPECIFIC RESULTS

#####
# 1. generate the current local time
# e.g. 2013,5,20 -> 2013-05-20
today           = date.today()
yesterday       = today - timedelta(1)

year, month, day= yesterday.year, yesterday.month, yesterday.day ###### <--------UNCOMMENT THIS TO GET YESTERDAY  #########
url_date_yesterday = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for yesterday
year, month, day= today.year, today.month, today.day   ###### <--------UNCOMMENT THIS TO GET TODAY  #########
url_date_today = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for today

url_date=url_date_yesterday

#url_date = "2013-05-18"   ###### <-------- UNCOMMENT THIS TO GET A SPECIFIC DATE  #########

#####
# 2. detect the current operating system and generate the folder separater
sep = os.sep        # "\\" for windows, "/" for linux
# actually, no need.  anyhow
#####
# 3. other parameters, server-end and user-end

defaultReloadMode = False
# http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/2013-05-19_0015.MOS0.jpg  (with relief)
url_root = "http://cwb.gov.tw/V7/observe/radar/Data/MOS_1024/"      
url_suffix= ".MOS0.jpg"
outputfolder = "charts"

# http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/2013-05-20_0045.2MOS0.jpg (without relief)
url_root2 = "http://cwb.gov.tw/V7/observe/radar/Data/MOS2_1024/"   
url_suffix2= ".2MOS0.jpg"
outputfolder2 = "charts2"

# http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-2013-05-20-15-30.jpg (visible spectrum)
url_root3 = "http://cwb.gov.tw/V7/observe/satellite/Data/sbo/sbo-"    
url_suffix3= ".jpg"
outputfolder3 = "satellite1"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-2013-05-20-15-30.jpg (colours)
url_root4 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3p/s3p-"    
url_suffix4= ".jpg"
outputfolder4 = "satellite2"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-2013-05-20-15-30.jpg (enhanced colours)
url_root5 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3q/s3q-"    
url_suffix5= ".jpg"
outputfolder5 = "satellite3"

# http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-2013-05-20-15-30.jpg (black and white)
url_root6 = "http://cwb.gov.tw/V7/observe/satellite/Data/s3o/s3o-"    
url_suffix6= ".jpg"
outputfolder6 = "satellite4"

# http://cwb.gov.tw/V7/observe/temperature/Data/2013-05-20_1300.GTP.jpg  (temperature)
url_root7 = "http://cwb.gov.tw/V7/observe/temperature/Data/"    
url_suffix7= ".GTP.jpg"
outputfolder7 = "temperature"

# http://cwb.gov.tw/V7/observe/rainfall/Data/hk520153.jpg               (rainfall -small grid)
url_root8 = "http://cwb.gov.tw/V7/observe/rainfall/Data/hk"    
url_suffix8= ".jpg"
outputfolder8 = "rainfall1"

# http://cwb.gov.tw/V7/observe/rainfall/Data/2013-05-20_1530.QZJ.grd2.jpg (rainfall -large gird)
url_root9 = "http://cwb.gov.tw/V7/observe/rainfall/Data/"    
url_suffix9= ".QZJ.grd2.jpg"
outputfolder9 = "rainfall2"
# 

############  ####################  ####################  ################################
# the following are added on 2013-08-21

# http://www.cwb.gov.tw/V7/observe/satellite/Sat_H_EA.htm?type=1#
# http://www.cwb.gov.tw/V7/observe/satellite/Data/HSAO/HSAO-2013-08-21-17-30.jpg  (high definition south-east asia - visible light)
url_root10 = "http://www.cwb.gov.tw/V7/observe/satellite/Data/HSAO/HSAO-"    
url_suffix10= ".jpg"
outputfolder10 = "hsao"
timeStringType10         = "satellite"
# 

url_info_list = []

# http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1O/HS1O-2013-08-21-17-30.jpg (high definition south-east asia - infra-red)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1O/HS1O-",
                              ".jpg",
                              "hs1o",
                              "satellite"))
# 

# http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1P/HS1P-2013-08-21-17-30.jpg (high definition south-east asia - coloured)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1P/HS1P-",
                              ".jpg",
                              "hs1p",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1Q/HS1Q-2013-08-21-17-30.jpg (high definition south-east asia - colour-enhanced)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/HS1Q/HS1Q-",
                              ".jpg",
                              "hs1q",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/sco/sco-2013-08-21-17-30.jpg (global - visible light)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/sco/sco-",
                              ".jpg",
                              "sco",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/s0p/s0p-2013-08-21-17-30.jpg (global - coloured)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/s0p/s0p-",
                              ".jpg",
                              "s0p",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/s0q/s0q-2013-08-21-17-30.jpg (global - colour-enhanced)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/s0q/s0q-",
                              ".jpg",
                              "s0q",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/satellite/Data/s0o/s0o-2013-08-21-17-30.jpg (global - infra-red)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/satellite/Data/s0o/s0o-",
                              ".jpg",
                              "s0o",
                              "satellite"))

# http://www.cwb.gov.tw/V7/observe/rainfall/Data/hq821190.jpg (hourly rainfall)
url_info_list.append(Url_info("http://www.cwb.gov.tw/V7/observe/rainfall/Data/hq",
                              ".jpg",
                              "hq",
                              "rainfall1"))

########################################################################################
# defining the functions
def download(url, to_filename, url_date=url_date, folder=".", reload=defaultReloadMode):
    ################
    # first, create the directory if it doesn't exist
    try: 
        os.makedirs(folder + sep + url_date)
    except OSError:
        if not os.path.isdir(folder + sep + url_date):
            raise
    ###############
    # download
    to_path = folder + sep + url_date + sep + to_filename
    # check if to_path exists first!!!
    # added  2013-08-21
    if os.path.isfile(to_path) and reload==False:
        print to_path, ' <--- already exists!!'
        if os.path.getsize(to_path) >= 6000:
            return 0.5
        else:
            print 'file broken! - removed'
    try:
        f = urllib.urlretrieve(url, to_path)
        if os.path.getsize(to_path) < 6000:
            os.remove(to_path)
            print to_path, 'not found ' + url
            returnvalue = 0
        else:
            print to_path, '- fetched!!!!!!!!!!!!!!!!!!!!!'
        returnvalue = 1
    except:
        print "Error !", url
        returnvalue = 0
    # delete if filesize < 6000 (with safety margin)
    return returnvalue

def downloadoneday(url_root=url_root, url_date=url_date, url_suffix=url_suffix, 
                 outputfolder=outputfolder, type="radar"):
    try:
        for hour in range(24):
            for minute in [0, 7, 15, 22, 30, 37, 45,52 ]:
                #if (minute == 15 or minute ==45) and \
                #    (type == "rainfall1" or type =="rainfall2" or type =="satellite"):
                #    continue                        # no data
                if type == "radar":
                    timestring = "_" + ("0"+str(hour))[-2:] + ("00"+str(minute))[-2:]
                elif type == "satellite":           # 2013-05-20-15-30
                    timestring = "-" + ("0"+str(hour))[-2:] + "-" + ("00"+str(minute))[-2:]
                elif type == "temperature":         # "2013-05-20_1300"
                    timestring = "_" + ("0"+str(hour))[-2:] + ("00"+str(minute))[-2:]
                elif type == "rainfall2":           # "2013-05-20_1530"
                    timestring = "_" + ("0"+str(hour))[-2:] + ("00"+str(minute))[-2:]
                elif type == "rainfall1":           # "520100" for 2013-05-20 10:00 - the odd man out
                    timestring = ("0"+str(hour))[-2:] + str(minute)[0]

                url = url_root + url_date + timestring + url_suffix

                if type == "rainfall1":           # "520153" for 2013-05-20 15:30, 
                                                  # "520010" for 2013-05-20 01:00, 
                                                  # "520100" for 2013-05-20 10:00 - the odd man out
                                                  # "a02090" for 2013-10-02 09:00
                    
                    m = int(url_date[5:7])
                    if m < 10:
                        monthString = str(m)
                    else:
                        monthString = chr(m+87)  # 'a' for 10, 'b' for 11, etc
                    #url = url_root + monthString + str(int(url_date[8:10])) + timestring + url_suffix   # doesn't work any more 2013-10-01
                    url = url_root + monthString + url_date[8:10] + timestring + url_suffix   # added 2013-10-01
                    #debug
                    #print url
                    #time.sleep(1)
                    #end debug
                to_filename = url_date +"_" +("0"+str(hour))[-2:] +("00"+str(minute))[-2:] +url_suffix
                download(url=url, to_filename=to_filename, url_date=url_date, folder=outputfolder)
    except:
        print "--------------------------------------------------------"
        print "Error!!!! During", type, url_root
        

def downloadoneday2(url_info, url_date=url_date):
    u = url_info
    return downloadoneday(url_root=u.url_root, url_date=url_date, url_suffix=u.url_suffix, 
                        outputfolder=u.outputFolder, type=u.timeStringType)

        
########################################################################################
# running
def main(url_date=url_date):

    """ """
    downloadoneday(url_root=url_root, url_date=url_date, url_suffix=url_suffix,
                        outputfolder=outputfolder, type="radar")
    downloadoneday(url_root=url_root2, url_date=url_date, url_suffix=url_suffix2, 
                        outputfolder=outputfolder2, type="radar")
    downloadoneday(url_root=url_root3, url_date=url_date, url_suffix=url_suffix3, 
                        outputfolder=outputfolder3, type="satellite")
    downloadoneday(url_root=url_root4, url_date=url_date, url_suffix=url_suffix4, 
                        outputfolder=outputfolder4, type="satellite")
                        
    downloadoneday(url_root=url_root5, url_date=url_date, url_suffix=url_suffix5, 
                        outputfolder=outputfolder5, type="satellite")
                        
    downloadoneday(url_root=url_root6, url_date=url_date, url_suffix=url_suffix6, 
                        outputfolder=outputfolder6, type="satellite")
    downloadoneday(url_root=url_root7, url_date=url_date, url_suffix=url_suffix7, 
                        outputfolder=outputfolder7, type="temperature")
    downloadoneday(url_root=url_root8, url_date=url_date, url_suffix=url_suffix8, 
                        outputfolder=outputfolder8, type="rainfall1")
    downloadoneday(url_root=url_root9, url_date=url_date, url_suffix=url_suffix9, 
                        outputfolder=outputfolder9, type="rainfall2")
    downloadoneday(url_root=url_root10, url_date=url_date, url_suffix=url_suffix10, 
                        outputfolder=outputfolder10, type=timeStringType10)
    for u in url_info_list:
        downloadoneday(url_root=u.url_root, url_date=url_date, url_suffix=u.url_suffix, 
                        outputfolder=u.outputFolder, type=u.timeStringType)
        


if __name__ == '__main__':
    time0= int(time.time())
    argv = sys.argv
    if len(argv) > 1:
        try:
            secs = int(argv[1])
            print 'sleeping %d seconds' % secs, 'from localtime', time.asctime()
            print 'waking up at UTC', time.asctime(time.gmtime( time.time()+ secs ))
            time.sleep(secs)
            while True:
                timeStart       = time.time()
                today           = date.today()
                yesterday       = today - timedelta(1)
                year, month, day= yesterday.year, yesterday.month, yesterday.day ###### <--------UNCOMMENT THIS TO GET YESTERDAY  #########
                #year, month, day= today.year, today.month, today.day   ###### <--------UNCOMMENT THIS TO GET TODAY  #########
                
                url_date = str(year) + "-" + ("0"+str(month))[-2:] + "-" + ("0"+str(day))[-2:]  # for today
                main(url_date=url_date)
                timeSpent   = int(time.time()) - timeStart
                print "time spent", timeSpent
                print 'sleeping', 86400-timeSpent, 'seconds, from localtime', time.asctime()
                print 'waking up at UTC', time.asctime(time.gmtime( time.time()+ 86400-timeSpent ))
                time.sleep(86400-timeSpent)
        except ValueError:
            for url_date in sys.argv[1:]:
                main(url_date)
    else:
        print "\n\nYESTERDAY:\n"
        main(url_date=url_date_yesterday)
        print "\n\nTODAY:\n"
        main(url_date=url_date_today)

    #main(url_date='2013-07-11')
    #main(url_date='2013-07-09')
    #main(url_date='2013-07-08')
    #main(url_date='2013-07-07')
    print "\nTime spent:", int(time.time()) - time0
    print "Time now:", time.asctime()

