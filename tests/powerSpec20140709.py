from armor.initialise import *
from armor.filter import filters
#WRFwindow = (200,200,600,560)

def powerSpecTest09(a, 
                    filter=filters.gaussianFilter, 
                    filterArgs={'sigma': 20, 'newCopy':True}
                    ):
    # ported to armor.analysis.powerSpecTest0709()
    #a = march('0312.1200')[0]

       
    a.load()
    a.show()
    
    a.drawRectangle(*WRFwindow).saveImage()
    a.load()
    a1= a.getWindow(*WRFwindow)
    if filter != "":
        a1 = filter(a1, **filterArgs)
        
    a1.saveImage()
    a2 = a1.coarser().coarser()
    a2.name = a1.name
    a2.saveImage()
    a2.threshold(0).show()
    a2.threshold(0).saveImage()
    a2.powerSpec()

candidates = may('0520.05') + march('0312.11') + kongrey('0829.2150') + kongrey('0828.0200')
candidates2 = maywrf20('0600') + marchwrf('0312.1200') + kongreywrf('0829.2100') + kongreywrf('0828.0300')

candidates = kongrey('0829.2150') + kongrey('0828.0200') + march('0312.1110') + may('0520.0510')

for a in candidates:
    a.powerSpecTest0709
    for sigma in [5, 10, 20]:
        a.powerSpecTest0709(filter=filters.gaussianFilter, filterArgs={'sigma':sigma}, 
                             outputFolder=dp.root+"labLogs2/powerSpec_filtered/sigma0_5_10_20/")
    
#for a in candidates2:
#    a.powerSpecTest0709()
 
   

##########################
#from armor.initialise import *
#from armor.filter import filters
#candidates  = kongrey('0828.0200')+ kongrey('0829.2150') + kongreywrf('0828.0900', "WRF01") +\
#                march('0312.1110')+ marchwrf('0312.0300','WRF01') + may('0520.0510') + maywrf20('0520.0300', 'WRF14') +\
#                [DBZ('20120601.0000')] + may('0520.0520' ) + [DBZ('20120612.0200')] + march('0312.1140')

#for a in candidates:
#    a.powerSpecTest0709()

