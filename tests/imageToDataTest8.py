import time
import os
import pickle
import numpy as np
from armor import pattern
dbz = pattern.DBZ
classificationResultsFileName = 'D:/ARMOR/labLogs2/charts2_classification_local/log_1411055155.log.txt'


def display(resultString):
    """chart:20140525.0400 / region index:6"""
    rs = resultString
    dataTime = rs[6:19]
    regionNumber = int(rs.split(":")[-1])
    a = dbz(dataTime)
    b = a.copy()
    a.loadImage(rawImage=True)
    b.loadImage(rawimage=False)
    b1 = b.connectedComponents().levelSet(regionNumber)
    region = b1.getRegionForValue(1)
    b = b.drawRectangle(*region)
    a.showWith(b)


display('chart:20140525.0400 / region index:6')
