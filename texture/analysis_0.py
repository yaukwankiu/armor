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
analysis.main()

"""
######################################################
#   0. imports and setups
import time
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt # just in case

timestamp = int(time.time())
NumberOfOrientations = 5
scales  = [1, 2, 4, 8, 16, 32, 64, 128]
featureFolder = "armor/texture/gaborFeatures%d/" % timestamp
k = 72
textureFolder = "armor/texture/textureLayers%d/" % k

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
def computeClustering(data, textureFolder=textureFolder):
    outputFolder=textureFolder  #self reminding alias
    height, width, depth = data.shape
    data = data.reshape(height*width, depth)
    clust = kmeans2(data=data, k=k, iter=10, thresh=1e-05,\
                     minit='random', missing='warn')
    # output to textureFolder
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
    return texturelayer
    
######################################################
#   4. (neighbour aggregation)     -> segmentation
def computeSegmentation(texturelayer):

    from armor.geometry import morphology as morph
    disc = morph.disc
    dilate = morph.dilate

    plt.imshow(texturelayer[20])
    plt.show()

    outputFolder = textureFolder + 'thick/'
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

    for i in range(len(texturelayer)):
        print '||||||\n||'
        for j in range(len(texturelayer)):
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
            if corr_matrix[i,j]>0.5:
                matchedlayers1.append((i,j))
            if corr_matrix[i,j]>0.6:
                matchedlayers2.append((i,j))
            if corr_matrix[i,j]>0.8:
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
def main(a=a, scales=scales, NumberOfOrientations = NumberOfOrientations, 
                 memoryProblem=True):
    # temporarily switching off after debugging - 2013-6-4
    #fvf = computeFeatures(a=a,scales=scales, NumberOfOrientations = NumberOfOrientations, 
    #             outputFolder=featureFolder, memoryProblem=memoryProblem)
    # 
    data = load(featureFolder)
    texturelayer = computeClustering(data=data, textureFolder=textureFolder)
    segmentation = computeSegmentation(texturelayer=texturelayer)
    return {'texturelayer':texturelayer,
            'segmentation':segmentation}

if __name__=='__main__':
    main()

