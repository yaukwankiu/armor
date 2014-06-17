# normalised correlation test after gaussian smoothing
# gaussian radii: 40 and 60
# thresholds: dBZ = 15, 25, 35
# 

import copy
from armor import pattern
from armor import objects3 as ob
from armor.tests.roughwork20131106 import construct3by3
#from armor.geomtery import frames as fr
import numpy as np
import numpy.ma as ma
import pylab
pylab.ion()
#pylab.draw()
    
    

kongrey = ob.kongrey
wrf     = ob.kongreywrf2
wrf.fix()

dataTime    = '20130828.1500'
outputFolder = pattern.a.outputFolder

k   = kongrey(dataTime)[0]
#k.load()
#k.setThreshold(0)
#k.getCentroid()



dataTimeStart   = k.timeDiff(hours=-6)
dataTimeEnd     = k.timeDiff(hours= 6)
dataTimes       = [w.dataTime for w in wrf]
dataTimes       = [w for w in dataTimes if w >= dataTimeStart and w <= dataTimeEnd]
dataTimes       = sorted(list(set(dataTimes)))      # '20130828.0900' to '20130828.2100'


#for T in dataTimes:
#    wrf.load(T)
#wrf.cutUnloaded()
#wrf.setThreshold(0)

wrf.list = [w for w in wrf if w.dataTime in dataTimes]

outputString = ''
correlationsAll=[]
makeImages = True
saveImages = False

count   = -1
for thres in [15, 25, 30]:
    wrf.listTemp = copy.copy(wrf.list)
    for sigma in [60, 40, 20]:
        outputString = ''
        count +=1
        #if count <1:
        #    continue
        # LOAD k, smooth by gaussian , and get threshold
        k.load()
        k.setThreshold(0)
        k.matrix0 = k.matrix.copy()
        k.getCentroid()
        k.matrix = k.gaussianFilter(sigma).matrix
        k.matrix = 100.* (k.matrix>=thres) 
        k.matrix.mask = np.zeros(k.matrix.shape)
        #k.vmax=2
        #k.vmin=-2
        #k.makeImage(closeAll=True)
        #pylab.draw()
        correlations = []
        for w in wrf.listTemp:
            #try:
                # LOAD w, smooth by gaussian , and get threshold
                w.load()
                w.setThreshold(0)
                w.getCentroid()
                w1 = w.gaussianFilter(sigma)
                topRowName = w.name + ', gaussian(' + str(sigma) + ') and ' + k.name
                topRow = ma.hstack([w.matrix, w1.matrix, k.matrix0])
                #k.load()
                #k.setThreshold(0)
                #topRow = ma.hstack([w.matrix, w1.matrix, k.matrix])
                w1.matrix = 100.*(w1.matrix>=thres)
                w1.matrix.mask = np.zeros(w1.matrix.shape)
                #w1.vmax = 2
                #w1.vmin =-2
                #w.makeImage(closeAll=True)
                #pylab.draw()
                #print "w.matrix.shape, w.matrix.mask.shape", w.matrix.shape, w.matrix.mask.shape
                try:
                    ############################################
                    #   punchlines
                    w2 = w1.momentNormalise(k)
                    corr = w2.corr(k)
                    #w2.vmax = 2
                    #w2.vmin =-2
                    w2.matrix = ma.hstack([w1.matrix, w2.matrix, k.matrix])
                    w2.name   = w.name + ', normalised, and ' + k.name + '\nnormalised correlation:  ' + str(corr)
                    w2.matrix = ma.vstack([w2.matrix, topRow])
                    w2.name  = topRowName + '\n' + "bottom row:" + w2.name
                    w2.imagePath = '/home/k/ARMOR/python/testing/' + w.name + '_' + k.name + '_sigma' + str(sigma) + '_thres' + str(thres) + '.png'
                    w2.vmin= -20.
                    w2.vmax = 100.
                    if saveImages:
                        w2.saveImage()
                    if makeImages:
                        w2.makeImage(closeAll=True)
                        pylab.draw()

                    #
                    ############################################
                #except IndexError:
                except SyntaxError:
                    corr = -999
                correlations.append({
                                         'sigma': sigma,
                                         'thres': thres,
                                         'k'    : k.name,
                                         'w'    : w.name,
                                         'corr' : corr,
                                         })
                print k.name, w.name, 'sigma:', sigma, 'thres:', thres, 'corr:', corr
                w.matrix = 0        # unload!!
            #except:   
            #    print "Error!! - "
            #    print "k.name, w.name, sigma, thres"
            #    print k.name, w.name, sigma, thres
        # sort, get the best matches
        correlations.sort(key=lambda v: v['corr'], reverse=True)
        # output
        outputString += '\n\n................................................\n'
        outputString += 'Top Matches for\n'
        outputString += '    sigma, thres: ' + str(sigma) + ', ' + str(thres) + '\n'
        for entry in correlations[:20]:
            outputString += '        k, w, corr: ' + '\t' + str(entry['k']) + \
                                                     '\t' + str(entry['w']) + \
                                                     '\t' + str(entry['corr']) + '\n'
        print outputString
        open('gaussianSmoothNormalisedCorrelationTest.log.txt', 'a').write(outputString)
        correlationsAll.append(correlations)

        candidates  = correlations[: len(correlations)//2]  # taking the top half going down the scale
        candidates  = [entry['w'] for entry in candidates]  # taking the w.name only
        wrf.listTemp = [v for v in wrf.listTemp if v.name in candidates]                      # trim the list

open('gaussianSmoothNormalisedCorrelationTest.log.txt', 'a').write('\n\n\n====\nAll Correlations'+\
                                                                    str(correlationsAll))



