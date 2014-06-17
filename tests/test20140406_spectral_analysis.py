#   test20140406_spectral_analysis.py
#   need to find the normalisation of various scales - c.f. 
#       http://dsp.stackexchange.com/questions/10647/normalized-laplacian-of-gaussian

"""
PURPOSE:
    to conduct spectral analysis as described in section 2.2(2) in the RFP of ARMOR, year 2014

USE:
    cd /media/TOSHIBA\ EXT/ARMOR/python/
    python
    import defaultParameters as dp
    dataFolder      = dp.root + 'data/march2014/QPESUMS/'
    outputFolder    = dp.root + 'labReports/armor-report-1april2014-8april2014/' 
    import tests.test20140406_spectral_analysis as test    
    test.main(dataFolder, outputFolder)

"""
#   imports

from armor import defaultParameters as dp
from armor import misc
from armor import pattern
from scipy import ndimage


#   setups

dataFolder      =  dp.root + 'data/march2014/QPESUMS/'
outputFolder    =  dp.root + 'labReports/armor-report-1april2014-8april2014/'   


#   defining the functions
#   run

def main(inputFolder, outputFolder):
    pass

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) > 1:
        dataFolder  = argv[1]
    if len(argv) > 2:
        outputFolder= argv[2]
    res = main(inputFolder, outputFolder)    
    return res
