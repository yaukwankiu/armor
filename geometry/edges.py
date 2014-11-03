# armor.geometry.edges
# module for edge detecting and stuff

import copy
import numpy as np
import numpy.ma as ma
from scipy.signal import fftconvolve
#from armor import pattern

def find(a):
    """
    use straightforward summing of mask criteria
    """
    m1 = ma.zeros(a.matrix.shape)
    m2 = ma.zeros(a.matrix.shape)
    # look around it's neighbourhood
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            m1 += (a.shiftMatrix(i,j).matrix.mask==False)   # finding a point not masked
            m2 += (a.shiftMatrix(i,j).matrix.mask==True )   # finding a point masked
    return m1*m2


def complexity(a, windowSize=20):
    """
    local complexity map of a based on the proportion of edge elements in the region
    """
    height, width = a.matrix.shape
    complexityMap = ma.zeros(a.matrix.shape)
    try:
        a.edges+1
        aEdges = a.edges
    except AttributeError:
        aEdges = find(a)
    nonEdge = (aEdges==0)
    for i in range(0, height, windowSize):
        for j in range(0, width, windowSize):
            complexityMap[i:i+windowSize, j:j+windowSize] = \
           ((aEdges[i:i+windowSize, j:j+windowSize]>0).sum()+1.0) / windowSize**2
             
    a.complexityMap = complexityMap
    return complexityMap            
            
def sobel(a):
    """
    sobel operator for edge detection
    (ref:  <<image processing, analysis and machine vision>>,
                          the big black book, p.95)

    """
    h1 = np.array( [[ 1, 2, 1],
                    [ 0, 0, 0],
                    [-1,-2,-1]])

    h2 = np.array( [[ 0, 1, 2],
                    [-1, 0, 1],
                    [-2,-1, 0]])

    h3 = np.array( [[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

    ah1 = fftconvolve(a.matrix, h1)
    ah2 = fftconvolve(a.matrix, h2)
    ah3 = fftconvolve(a.matrix, h3)
    return ah1, ah2, ah3

def distance(p1=(1,1), p2=(2,2)):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ) **.5

def neighbours(points=[(1,1), (2,2), (3,3), (4,4), (5,5)], gap=5, toBeSorted=True):
    # greedy algorithm, one direction
    if toBeSorted:
        neighbours = [sorted([u for u in points if distance(u,v)<=gap], key=lambda u:distance(u,v), reverse=False) for v in points]
    else:
        neighbours = [[u for u in points if distance(u,v)<=gap] for v in points]
    neighbours = dict([(points[i], neighbours[i]) for i in range(len(points))])
    return neighbours
    
def connectTheDots(points=[(1,1), (2,2), (3,3), (4,4), (5,5)], gap=5, toBeSorted=True):
    nh = neighbours(points, gap, toBeSorted)
    unmarkedPoints = copy.deepcopy(points)
    point0      = unmarkedPoints.pop()
    point1      = point0
    pointsSequence = []
    while len(unmarkedPoints)>0:
        pointsSequence.append(point1)
        neighs = nh[point1]
        neighs = [v for v in neighs if v in unmarkedPoints] #remove marked points
        point2 = neighs[0]
        unmarkedPoints  = [v for v in unmarkedPoints if v!=point2]  #marking point2
        point1 = point2
    return pointsSequence

if __name__ == '__main__':
    time0=time.time()
    import matplotlib.pyplot as plt
    X, Y = np.meshgrid(range(-50,50), range(-50,50))
    X    = X.flatten()
    Y    = Y.flatten()
    N    = len(X)
    allPoints = np.vstack([X,Y])
    allPoints2 = [(allPoints[0,i], allPoints[1,i]) for i in range(N)]
    circle     = [v for v in allPoints2 if distance(v, (0,0))>47 and distance(v, (0,0))<=48]
    circle2    = connectTheDots(circle)
    print 'Time spent:', time.time()-time0
    x           = [v[1] for v in circle2]
    y           = [v[0] for v in circle2]
    plt.plot(x,y, '.')
    plt.title('dots')
    plt.savefig('../pictures/circle-dots.png')
    plt.show(block=True)
    plt.plot(x,y)
    plt.title('dots connected')
    plt.savefig('../pictures/circle-dots-connected.png')
    plt.show(block=True)

