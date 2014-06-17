from armor import defaultParameters as dp
from armor import objects4 as ob
monsoon = ob.monsoon
#x=a.shortTermTrajectory(DBZstream=monsoon, key1="", key2="", radius=30, hours=3, timeInterval=3, verbose=True, drawCoast=True)

a0=a.threshold(0)
b0=b.threshold(0)
x=a0.drawShiibaTrajectory(b0, k=12,L=[dp.tainan, dp.taipei,  dp.kenting, dp.hualien], searchWindowWidth=15, 
                         searchWindowHeight=5)

