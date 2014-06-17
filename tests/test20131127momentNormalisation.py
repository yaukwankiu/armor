"""
cd /media/KINGSTON/ARMOR/python
python

"""


from armor import objects3 as ob
from armor import pattern

obs = ob.kongrey
wrf = ob.kongreywrf2

k   = obs('0828.0900')[0]
k.load()
k.setThreshold(0)

correlations=[]

for w in wrf:
    #try:
        w.load()
        w.setThreshold(0)
        corr = k.gaussianCorr(w, sigma=20, thres=15, saveImage=True, outputFolder='/home/k/ARMOR/python/testing/20131127-gaussiancorr/')
        correlations.append({
                                'k' : k,
                                'w' : w,
                                'corr'  : corr,
                            })
    #except:
    #    print 'ERROR!!', k.name, ',', w.name



