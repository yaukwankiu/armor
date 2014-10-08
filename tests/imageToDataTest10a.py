#imageToDataTest10a.py
import os
from armor import pattern
dp = pattern.dp
dbz= pattern.DBZ
inputFolder = dp.root+'labLogs2/charts2_classification_global/'
outputFolder = inputFolder
dataFileName= 'log_imageToDataTest9.txt'

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

x = open(inputFolder+dataFileName,'r').read()
L = x.split('\n')
L = [v for v in L if '[' in v]
L1 = [v.split(',') for v in L]
L2 = [v[:13] for v in L]
L3 = [v[17:-1] for v in L]
L4 = [[int(w) for w in v.split(',') ] for v in L3]

N = len(L)
for i in range(N):
    a = dbz(dataTime=L2[i], name=L2[i]+'\n'+str(L4[i]))
    a.loadImage()
    a.imagePath = outputFolder + str(L4[i]) + '.jpg'
    a.saveImage()