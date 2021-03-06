# armor.texture.analysis.py
# should work automatically
""" 
script to analyse the texture and perform segmentation, given radar data
pipeline: 
   1.   dbz radar data  -> armor.DBZ object 
   2.   (filter bank) -> feature layers
   3.   (clustering)  -> texture layers
   4. (neighbour aggregation)     -> segmentation

== USE ==

cd /media/Seagate\ Expansion\ Drive/ARMOR/python
python

from armor.texture import analysis
reload(analysis)
return_value={}

x = analysis.main(scales=[1,3,9,27,81], NumberOfOrientations = 6, memoryProblem=True)
x = analysis.main(scales=[1,2,4,8,16,32,64,128], NumberOfOrientations = 6, memoryProblem=True)

x = analysis.main(k=6, scales=[1], NumberOfOrientations = 4, memoryProblem=True) # 10minutes overall

reload(analysis); x = analysis.main(scales=[4,8,16,32], NumberOfOrientations = 6, memoryProblem=True)


#x = analysis.main(featureFolder='armor/texture/gaborFeatures1370349660/')
#x = analysis.main(a=a, scales=scales, NumberOfOrientations = NumberOfOrientations, featureFolder=featureFolder, textureFolder=textureFolder, memoryProblem=True)

###
import time

t = time.time()+3600*7

while time.time()<t:
    pass

time.sleep(3600*6); x = analysis.main(scales=[1,3,9,27,81], NumberOfOrientations = 8, memoryProblem=True)


###


"""
######################################################
#   0. imports and setups
import time
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt # just in case
from scipy.cluster.vq import kmeans2
from armor import pattern
dbz = pattern.DBZ

timestamp = int(time.time())
#timestamp = 20130604
NumberOfOrientations = 6
scales  = [1, 2, 4, 8, 16, 32, 64, 128]
k = 72
# moved to main()
#featureFolder = "armor/texture/gaborFeatures_%d/" % timestamp
#textureFolder = "armor/texture/textureLayers%d_%d/" % (k,timestamp)
featureFolder = "armor/texture/%d/gaborFeatures/" % timestamp
textureFolder = "armor/texture/%d/textureLayers%d/" % (timestamp, k)
textureThickFolder = "armor/texture/%d/textureLayers%dthick/" % (timestamp, k)

######################################################
#   1.   dbz radar data  -> armor.DBZ object 
from armor import pattern
a = pattern.a

######################################################
#   2.   (filter bank) -> feature layers
# outputs to be found in:  featureFolder
def computeFeatures(a=a,scales=scales, NumberOfOrientations = NumberOfOrientations, 
                 outputFolder=featureFolder, memoryProblem=True):
    from armor.filter import gabor
    fvf = gabor.main(a,scales=scales, NumberOfOrientations = NumberOfOrientations, 
                     outputFolder=featureFolder, memoryProblem=True)
    return fvf
######################################################
#   3.   (clustering)  -> texture layers

############
# reading the feature vector field
def load(folder=featureFolder):
    # or /media/Seagate Expansion Drive/ARMOR/python/armor/filter/gaborFeatures1369996409
    t0 = time.time()
    pydumpList = [fl for fl in os.listdir(folder) if fl[-7:]==".pydump"]
    print '\n'.join(pydumpList)
    if len(pydumpList) ==1:
        d = pickle.load(open(folder+pydumpList[0],'r'))
        data = d['content']
    else:
        # initialise
        d = pickle.load(open(folder+pydumpList[0],'r'))
        data = np.zeros((d.shape[0], d.shape[1], len(pydumpList)))
        data[:,:,0] = d
        print "array size:", (d.shape[0], d.shape[1], len(pydumpList))
        for i in range(1,len(pydumpList)):
            data[:,:,i] = pickle.load(open(folder+pydumpList[i],'r'))
    timespent = time.time()-t0; print "time spent:",timespent
    return data

############
# performing the clustering
def computeClustering(data, k=k, textureFolder=textureFolder):
    t0 = time.time()
    outputFolder=textureFolder  #self reminding alias
    height, width, depth = data.shape
    data = data.reshape(height*width, depth)
    clust = kmeans2(data=data, k=k, iter=10, thresh=1e-05,\
                     minit='random', missing='warn')
    # output to textureFolder
    try:
        os.makedirs(textureFolder)
    except: 
        """don't crash.  fail gracefully or not at all"""
        print 'folder already exists!'
        os.rename(textureFolder, textureFolder[:-1]+ 'pre'+ str(timestamp))
        os.makedirs(textureFolder)
    texturelayer= []
    for i in range(k):
        print i
        texturelayer.append( (clust[1]==i).reshape(881,921) )
        #plt.imshow(cluster[i])
        #plt.show()
        if texturelayer[i].sum()==0:
            continue
        pic = dbz(  name='texture layer'+str(i),
                  matrix= np.flipud(texturelayer[i]), vmin=-2, vmax=1,
               imagePath= textureFolder+ '/texturelayer'+ str(i) + '.png')
        #pic.show()
        pic.saveImage()

    timespent= time.time()-t0;  print "time spent:",timespent

    pickle.dump({'content':texturelayer, 'notes':"%d texture layers from 'armor/filter/gaborFilterVectorField.pydump' " %k}, open(textureFolder+'/texturelayer.pydump','w'))
    return clust, texturelayer
    
######################################################
#   4. (neighbour aggregation)     -> segmentation
#def computeSegmentation(clust, texturelayer):
def computeSegmentation(clust,outputFolder = textureThickFolder):
    k = clust[1].max()+1
    from armor.geometry import morphology as morph
    disc = morph.disc
    dilate = morph.dilate
    """
    plt.imshow(texturelayer[20])
    plt.show()
    """
    #outputFolder = textureThickFolder
    try:
        os.makedirs(outputFolder)
    except: 
        """don't crash.  fail gracefully or not at all"""
        print 'folder already exists!'
        os.rename(outputFolder, outputFolder[:-1]+ 'pre'+ timestamp)
        os.makedirs(outputFolder)
    t0=time.time()

    texturelayer_thick = []
    for i in range(k):
        thislayer = (clust[1]==i).reshape(881,921)
        print i, '\tall / interior sums:',
        print thislayer.sum(), thislayer[20:-20,20:-20].sum()
        #if thislayer[50:-50,50:-50].sum() < 40:       # only layer 53 is missing. should be ok
        #    continue
        #if thislayer.sum() < 3000:                    # an arbitrary threshold, first consider the bigger ones
        #    continue                   
        layer_thick = dilate(M=thislayer, neighbourhood = disc(3))  ## <--- dilation with disc of radius 3
        texturelayer_thick.append( layer_thick )
        #plt.imshow(cluster[i])
        #plt.show()
        # only those with values away from the border
        pic = dbz(  name='texture layer %d thicked' %i,
                  matrix= np.flipud(layer_thick), vmin=-2, vmax=1,
               imagePath= outputFolder+ '/texturelayer_thick'+ str(i) + '.png')
        #pic.show()
        pic.saveImage()
        

    print 'time spent:', time.time()-t0

    pickle.dump({'content':texturelayer_thick, 'notes':"%d texture layers from 'armor/filter/gaborFilterVectorField.pydump' " %k}, open(outputFolder+'/texturelayer_thick.pydump','w'))

    ########
    #     segment via intersections of various texture layers
    #   i. compute correlations between layers with thickened texture layers
    #   ii. grouping
    #######
    # computing the correlations of thickened textures      
    import numpy.ma as ma
    corr_matrix = ma.ones((k,k)) * (-999.)
    corr_matrix.mask = True
    corr_matrix.fill_value=-999.

    #for i in range(len(texturelayer)):
    for i in range(k):
        print '||||\n||'
        for j in range(k):
            layer1 = texturelayer_thick[i]
            layer2 = texturelayer_thick[j]
            corr_matrix[i,j] = (layer1*layer2).sum() / (layer1.sum() * layer2.sum())**.5
            print '||', i,',', j,',', corr_matrix[i,j],


    ###########
    # grouping

    matchedlayers1 =[]
    matchedlayers2 =[]
    matchedlayers3 =[]
    for i in range(k):
        for j in range(k):
            if i==j:
                continue
            if corr_matrix[i,j]>0.3:
                matchedlayers1.append((i,j))
            if corr_matrix[i,j]>0.5:
                matchedlayers2.append((i,j))
            if corr_matrix[i,j]>0.7:
                matchedlayers3.append((i,j))


    print matchedlayers1
    print matchedlayers2
    print matchedlayers3

    combinedtextureregions={}
    matchedlayers= matchedlayers1       #choosing one of the above
    """
    for L in set(v[0] for v in matchedlayers):
        L_partners = [v[1] for v in matchedlayers if v[0] == L]
        tt = texturelayer[L]
        print L, L_partners
        for j in L_partners:
            tt += texturelayer[j]
        combinedtextureregions[L] = tt
        plt.imshow(tt)
        plt.show()
    """
    return {"matchedlayers1":matchedlayers1,
            "matchedlayers2":matchedlayers2,
            "matchedlayers3":matchedlayers3,
            }
            
#####################################################
#  run it all

def main(a=a, k=k, scales=scales, NumberOfOrientations = NumberOfOrientations, featureFolder="",
           textureFolder="", textureFolderThick="", rootFolder="", memoryProblem=True):
    timeOverall =time.time()
    if featureFolder=="":
        featureFolder = "armor/texture/%d/gaborFeatures/" % timestamp
    if textureFolder=="":
        textureFolder = "armor/texture/%d/textureLayers%d/" % (timestamp, k)
    if textureFolderThick=="":
        textureThickFolder = "armor/texture/%d/textureLayers%dthick/" % (timestamp, k)
    if rootFolder =="":
        rootFolder = "armor/texture/%d/" 
    ##################################################
    # start:  save the original image for the record
    a.imagePath=rootFolder
    a.saveImage()
    try:
        pickle.dump(a, open(rootFolder+ a.name + '.pydump','w'))
    except:
        pickle.dump(a, open(rootFolder+ 'a.pydump','w'))
    #### can commented some of the following lines out in debugging
    fvf = computeFeatures(a=a, scales=scales, NumberOfOrientations = NumberOfOrientations, 
                 outputFolder=featureFolder, memoryProblem=memoryProblem)
     
    data = load(featureFolder)
    clust, texturelayer = computeClustering(data=data, k=k, textureFolder=textureFolder)
    segmentation = computeSegmentation(clust=clust, outputFolder=textureThickFolder)
    print "time spent overall:", time.time()-timeOverall
    #return_value['texturelayer']=texturelayer
    #return_value['segmentation']=segmentation
    return_value = {'texturelayer': texturelayer, 
                    'segmentation': segmentation,
                    'timestamp'   : timestamp,
                    'clust'       : clust,
                    'a'           : a,}
    pickle.dump(return_value, open(rootFolder+ 'texturelayes_and_segmentations.pydump','w'))
    return return_value
 
if __name__=='__main__':
    main()
    print 'timestamp:', timestamp
