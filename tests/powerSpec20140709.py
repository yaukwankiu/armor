from armor.initialise import *
#WRFwindow = (200,200,600,560)

def powerSpecTest09(a):
    # ported to armor.analysis.powerSpecTest0709()
    #a = march('0312.1200')[0]
    a.load()
    a.show()
    
    a.drawRectangle(*WRFwindow).saveImage()
    a.load()
    
    a1= a.getWindow(*WRFwindow)
    a1.saveImage()
    
    a2 = a1.coarser().coarser()
    a2.name = a1.name
    a2.saveImage()
    
    a2.threshold(0).show()
    a2.threshold(0).saveImage()
    
    a2.powerSpec()

candidates = may('0520.05') + march('0312.11') + kongrey('0829.2150') + kongrey('0828.0200')
candidates2 = maywrf20('0600') + marchwrf('0312.1200') + kongreywrf('0829.2100') + kongreywrf('0828.0300')

for a in candidates:
    a.powerSpecTest0709()
    
for a in candidates2:
    a.powerSpecTest0709()
    



