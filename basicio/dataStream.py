# script for handling streams of images
import os
import re
from armor import pattern
dbz = pattern.DBZ

if os.name == "nt":
    operatingSystem = "windows"
    armorDrive = "h:/"
    dataDrive  = "g:/"
    dataDrive2 = "d:/"
else:
    operationSystem = os.name
    armorDrive = "/media/KINGSTON/"
    dataDrive  = "/media/Seagate Expansion Drive/"
    dataDrive2 = "/host/" 

def load(folder):
    """
    input:  path of folder "/../../" 
    process: parse the folder for files
    output:  sequence of armor.pattern.DBZ objects
            DBZ(name, dataPath, dataTime) 

    # parse the filename and look for clues
    """
    dbzStream   = []
    folder      = re.sub(r'\\', '/' , folder)  # standardise:  g:\\ARMOR .. --> g:/ARMOR
    dataSource  = '-'.join(folder.split('/')[-3:]) + '-'
    L = os.listdir(folder)
    L = [v for v in L if v.lower().endswith('.txt') or v.lower().endswith('.dat')]  # fetch the data files
    for fileName in L:
        dataTime    = re.findall(r'\d{4}', fileName)
        dataTime    = dataTime[0] + dataTime[1] + '.' + dataTime[2]
        name        = dataSource + fileName
        dataPath    = folder + fileName
        a = dbz(dataTime=dataTime, name=name, dataPath=dataPath)
        a.load()
        dbzStream.append(a)
    return dbzStream



## sample data

dataFolder1 = dataDrive + 'ARMOR/data/SOULIK/temp/'
dataFolder2 = dataDrive2+ 'ARMOR/data/SOULIK/temp/'
def test(folder=dataFolder1):
    return load(folder)