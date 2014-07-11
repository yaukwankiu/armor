# powerSpecTest20140708.py
# to compute mean specs  
from armor.initialise import *
from armor import objects4 as ob
from armor.graphics import spectrum3d


testNamesList = ['sampling/1404810469.8monsoon/', 'sampling/1404810469.8COMPREF_Rainband_May_2014/', 'sampling/1404810469.69kongrey/',
                 'averaging/1404805135.42kongrey/', 'averaging/1404805135.46COMPREF_Rainband_May_2014/', 'averaging/1404805135.46monsoon/',
                 'averaging/1404805399.89COMPREF_Rainband_May_2014/',  'averaging/1404805399.89kongrey/', 'averaging/1404805399.89monsoon/',
                 ]

#testNamesList = ['sampling/1404810469.8COMPREF_Rainband_May_2014/','averaging/1404805135.46COMPREF_Rainband_May_2014/','averaging/1404805399.89COMPREF_Rainband_May_2014/'
#                ]

testNamesList = ['averaging/1404805399.89monsoon/']
testNamesList = ['1404803356.97COMPREF_Rainband_March_2014/']

inputFolderBase = dp.root + "labLogs2/powerSpec3/" 
#inputFolderBase = "c:/yau/"
#testNamesList = os.listdir(inputFolderBase)
#testNamesList = [v +"/" for v in testNamesList if os.path.isdir(inputFolderBase+v)]

for testName in testNamesList:
    try:
        #testName = "sampling/1404810469.82kongreywrf/"
        inputFolder = inputFolderBase + testName 
        
        outputFolder= inputFolder +  "meanSpecs/"
        #outputFolder = dp.root + 'python/testing/'
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        
        L   = os.listdir(inputFolder)
        maxList      = [v for v in L if "XYZmax.pydump" in v]
        totalList    = [v for v in L if "XYZ.pydump" in v]
        
        for L in [maxList, totalList]:
            print '\n'.join(L)
            time.sleep(2)
            
        ##############################################################
        Zmax = 0
        CountMax = 0
        N       =0
        for fileName in maxList:
            N   +=1
            xyz = pickle.load(open(inputFolder+ fileName))
            Zmax        += xyz['Z']
            CountMax    += Zmax.sum()
            print "N, Zmax.sum(), CountMax", N, '\t', Zmax.sum(), '\t', CountMax
        
        #Zmax /=CountMax
        print Zmax
        XYZ = xyz
        XYZ['Z'] = Zmax
        spectrum3d.spectrum3d(XYZ, title = "Max Spec " + testName + "\nwith total count="+ str(CountMax), display=False, outputFolder=outputFolder, fileName = "Max_Spec_" + "_".join(testName.split('/')) + ".png")
        print 'saved to' , outputFolder
        
        #################################################################
        Ztotal=0
        CountTotal=0
        N=0
        for fileName in totalList:
            N   +=1
            xyz = pickle.load(open(inputFolder+ fileName))
            Ztotal       += xyz['Z']
            CountTotal    += Ztotal.sum()
            print "N, Ztotal.sum(), CountTotal", N, '\t',  Ztotal.sum(), '\t', CountTotal
        
        
        print Ztotal
        XYZ['Z'] = Ztotal
        spectrum3d.spectrum3d(XYZ, title = "Total Spec " + testName + "\nwith total count="+ str(CountMax), display=False, outputFolder=outputFolder, 
                            fileName = str(time.time()) + "Total_Spec_" + "_".join(testName.split('/')) + ".png")
        
        print 'saved to' , outputFolder
    except:
        print "error! -- ", testName
