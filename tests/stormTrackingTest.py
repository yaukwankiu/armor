from armor import pattern
from armor import objects4 as ob
from armor.geometry import morphology as morph
from armor.kmeans import stormTracking as st
dbz = pattern.DBZ

a = ob.may2014('0519.1830')[0]
a.load().show()

x=a.stormTracking(upperThreshold=40, lowerThreshold=15)

x.keys()
x['regionsToTrack']

