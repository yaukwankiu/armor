import time, os, shutil, pickle
import numpy as np
import matplotlib.pyplot as plt

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
maywrf20  = ob.may2014wrf20
marchwrf = ob.march2014wrf

ob.kongreywrf.fix()
ob.march2014wrf.fix()

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
