import time, pickle, os, shutil
from armor import pattern
from armor import defaultParameters as dp
from armor.defaultParameters import *
from armor.misc import *

from armor import objects4 as ob

kongrey = ob.kongrey
kongreywrf = ob.kongreywrf
monsoon = ob.monsoon
may     = ob.may2014
march   = ob.march2014
maywrf19  = ob.may2014wrf19
maywrf20  = ob.may2014wrf20
maywrf21  = ob.may2014wrf21
maywrf22  = ob.may2014wrf22
maywrf23  = ob.may2014wrf23
marchwrf = ob.march2014wrf

ob.kongreywrf.fix()
ob.march2014wrf.fix()
monsoon.list = [v for v in monsoon.list if '0612' in v.dataTime]

comprefCutRegion = (200, 200, 150*4, 140*4)

w = ob.may2014wrf20[0]
w.load()

WRFwindow = (200,200,600,560)

"""
k12 =kongrey[12]
k11 =kongrey[11]
k10 =kongrey[10]
k10.load()
k11.load()
k12.load()

x = k11.shiiba(k12, searchWindowWidth=5, searchWindowHeight=17)


hualien4=  getFourCorners(hualienCounty)
k11_new =  k11.drawShiibaTrajectory(k12, L=hualien4, k=12)
k11_new.showWithCoast() 
"""
