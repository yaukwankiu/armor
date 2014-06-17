# script to convert logitude/latitude data into grid data
# 1.  read the file
# 2.  convert the data
# 3.  save the file

import numpy as np
import itertools
####################################
#  functions from morphology.py
def squareNeighbourhood(size=3):
    """ to be used in function erode, dilate, etc.
    min size = 2 (including the centre)
    """
    return list(itertools.product(range(-size//2+1,size//2+1), range(-size//2+1,size//2+1)))

def disc(radius=5):
    square = squareNeighbourhood(size=int(radius)*2+1)
    d = []
    for i, j in square:
        if i**2+j**2 <= radius**2 :
            d.append((i,j))
    return d

#
#####################################
kwargs =    {'files'  :['100','1000','2000','3000', 'Coast'],
             'width'  : 921,
             'height' : 881,
             'lowerLeft' : (115, 18),
             'upperRight' : (126.5, 29),
             'folder' : '',
             'suffix' : ".DAT",
             }


def read(path):
    # 1.  read the file
    x = open(path, 'r').read()
    return x

def convert(x, lowerLeft, upperRight, width, height):
    # 2.  convert the data
    nx = width  / (upperRight[0] - lowerLeft[0])
    ny = height / (upperRight[1] - lowerLeft[1])
    y = x.split()
    y = np.array([float(v) for v in y])
    #lon = y[0::2]
    #lat = y[1::2]
    y[0::2] = (np.round((y[0::2] - lowerLeft[0]) * nx)).astype(int)
    y[1::2] = (np.round((y[1::2] - lowerLeft[1]) * ny)).astype(int)
    return y

def dilate(y, radius=72):
    """ to dilate the coast
    """
    d = disc(radius=radius)
    z = []
    for i in range(0, len(y),2):
        v0 = y[i]
        v1 = y[i+1]
        neigh = [(v0+w[0], v1+w[1]) for w in d]
        z.extend(neigh)
    z = sorted(list(set(z)))
    z = [[w[0],w[1]] for w in z]
    z = sum(z,[])
    return z

def save(z,path):
    # 3.  save the file
    # x, y -> i,j switch takes place here
    outputString = "# Latitude(North), Longitude(East)\n"
    for i in range(0,len(z),2):
        outputString += str(int(z[i+1])) + "    " + str(int(z[i])) + "\n"
    open(path,'w').write(outputString)
    

# run it

def main0(files, width, height, lowerLeft, upperRight, folder, suffix):
    for fileName in files:
        print fileName
        x = read(folder+fileName+suffix)
        y = convert(x, lowerLeft, upperRight, width, height)
        #z = dilate(y, 36)
        save(y, folder+'relief'+fileName+'.dat')
        print y[:10]
    


def main1(files, width, height, lowerLeft, upperRight, folder, suffix):
    for fileName in files:
        print fileName
        x = read(folder+fileName+suffix)
        y = convert(x, lowerLeft, upperRight, width, height)
        z = dilate(y, 36)
        save(z, folder+'relief'+fileName+'Extended.dat')
        print z[:10]


if __name__ == "__main__":
    main0(**kwargs)
        
