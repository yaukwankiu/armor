#   entropyTest2.py
#   framing the regions with high entropy
import pickle

folder  = '/media/TOSHIBA EXT/ARMOR/labLogs2/entropy/COMPREF_Rainband_March_2014/'
fileName = '1405249186Entropy_Map_COMPREF_Rainband_March_201420140312.1600.pydump'

x = pickle.load(open(folder+fileName,'r'))
m = x.matrix
m1 = (m>1.5)

x1=x.copy()
x1.matrix=m1
x2 = x1.connectedComponents()


for i in range(9):
    reg = (x2.getRegionForValue(i))
    x2 = x2.drawRectangle(*reg)
    x2.show()
    print reg
    a=a.drawRectangle(*reg)
    a.show()

