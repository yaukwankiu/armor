from armor.initialise import *
#WRFwindow = (200,200,600,560)

def powerSpecTest09(a):
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

candidates = [may