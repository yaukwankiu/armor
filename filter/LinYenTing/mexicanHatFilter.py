
from math import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import os,sys

def mexiHat(sigma, t, parameter = 0.770212):
# One-dimensional mexican hat curve.    
    
    prob = 2.0/sqrt(3*sigma)/pow(pi, 0.25)*(1 - parameter*pow(t,2)/pow(sigma, 2))*\
           exp( -pow(t,2)/2/pow(sigma,2))

    return prob           

def filterGen(sigma, grid_size, parameter=0.770212):
# Generate two-dimensional filter grid. can be done with function "filterByC".

    mexfilter = list()
    
    print "Generate Modified MexicanHat filter at Sigma *3: "
    print "Filter Sigma: %f; Grid length: %f" %(sigma, grid_size)

    MatColumns = int(ceil(3*sigma/grid_size))
    MatRows =  int(ceil(3*sigma/grid_size))

    for i in range(0, MatRows+1):
        row = list()

        for j in range(0, MatColumns+1):
            prob_grid = 0
            vertex = list()
            for r in range(1, 51):
                width = grid_size/50.0
                xp = (3.0*sigma - grid_size*i) + 0.5*grid_size - width*(r-1)
                xm = (3.0*sigma - grid_size*i) + 0.5*grid_size - width*r
                for k in range(1, 51):
                    yp = (3.0*sigma - grid_size*j) + 0.5*grid_size - width*(k-1)
                    ym = (3.0*sigma - grid_size*j) + 0.5*grid_size - width*k

                    V1 = mexiHat(sigma, sqrt(pow(xp,2) + pow(yp,2)), parameter)
                    if V1 < 0: V1 = - pow(V1,2)
                    else: V1 = pow(V1,2)
                    V2 = mexiHat(sigma, sqrt(pow(xm,2)+pow(ym,2)), parameter)
                    if V2 < 0: V2 = -pow(V2,2)
                    else: V2 = pow(V2,2)
                    V3 = mexiHat(sigma, sqrt(pow(xm,2)+pow(yp,2)), parameter)
                    if V3 < 0: V3 = -pow(V3,2)
                    else: V3 = pow(V3,2)
                    V4 = mexiHat(sigma, sqrt(pow(xp,2)+pow(ym,2)), parameter)
                    if V4 < 0: V4 = -pow(V4,2)
                    else: V4 = pow(V4,2)

                    vertex.append(abs(V1))
                    vertex.append(abs(V2))
                    vertex.append(abs(V3))
                    vertex.append(abs(V4))

                    vertex.sort()

                    if V1 < 0: p_UL = -vertex[0]
                    else: p_UL = vertex[0]
                    if V2 < 0: p_LR = -vertex[1]
                    else: p_LR = vertex[1]
                    if V3 < 0: p_UR = -vertex[2]
                    else: p_UR = vertex[2]
                    if V4 < 0: p_LL = -vertex[3]
                    else: p_LL = vertex[3]

                    volume = pow(width, 2)*p_UL
                    volume_top = (((p_LL - p_UL) + (p_LR - p_UL))*0.5*width + (p_UR - p_UL)*0.5*width)*\
                                 width*0.5

                    volume = volume + volume_top

                    if ((V1 < 0) and (V2 < 0) and (V3 < 0) and (V4 < 0)) or \
                        ((V1 > 0) and (V2 > 0) and (V3 > 0) and (V4 > 0)):
                        prob_grid = prob_grid + volume
                    else: prob_grid = prob_grid + volume/2.0

            row.append(prob_grid)
        mexfilter.append(row)

    print len(mexfilter)    

    try:
        for i in range(0, MatRows+1):
           for j in range(MatColumns-1, -1, -1):
               mexfilter[i].append(mexfilter[i][j])
    except(IndexError):
        print i,j

    for i in range(MatRows-1, -1, -1):
        mexfilter.append(mexfilter[i])

    filter_sum = 0
    for i in range(0, len(mexfilter)):
        for j in range(0, len(mexfilter[i])):
            filter_sum += mexfilter[i][j]

    rowCenter = int(ceil(3*sigma/grid_size))+1
    wingwidth = int(ceil(3*sigma/grid_size))

    print "Mexican Hat Filter Sum = %f" %filter_sum
    print "Filter Rows: %d " %len(mexfilter)
    print "Filter Columns: %d " %len(mexfilter[0])
    print " Row Center at %d" %rowCenter
    print " Single Wing width : %d " %wingwidth

    return mexfilter

def textRead(textPath):

    try:
        f = open(textPath, 'r')
        data = list()
        for line in f:
            data.append(line.split())
        
        f.close()
        return data
    except(IOError):
        print "Can't locate file or file corruption, please \
            check folder or file existence."

def textWrite(file_path, data):
    try:
        f = open(file_path, 'w')
        
        for i in range(0, len(data)):
            line = ""
            for j in range(0, len(data[i])):
                line = line + str(data[i][j]) + " "
            line += "\n"                
            f.write(line)                

        f.close()
    except(IOError):
        print "Can't open file on assigned path, please check folder\
            , or writing authorization."

def filterPlot(sigma, grid_size, mexfilter, graphName = "filter_grf.jpg"):
# Plot 3-dimensional graph of generated filter. Filter must be a two-dimensional list, 
    
    figure = plt.figure()
    ax = figure.gca(projection = '3d')

    Xmin = -ceil(3*sigma/grid_size)*grid_size
    Ymin = -ceil(3*sigma/grid_size)*grid_size

    Xmax = floor(3*sigma/grid_size)*grid_size
    Ymax = floor(3*sigma/grid_size)*grid_size

    X = np.arange(Xmin, Xmax + grid_size, grid_size)
    Y = np.arange(Ymin, Ymax + grid_size, grid_size)

    X, Y = np.meshgrid(X, Y)

    for i in range(0,len(mexfilter)):
        for j in range(0,len(mexfilter[i])):
            mexfilter[i][j] = float(mexfilter[i][j])
    
    Z = mexfilter            
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,\
            linewidth=0, antialiased=False)
    
    ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    figure.colorbar(surf, shrink=0.5, aspect=5)

    figure.savefig(graphName)

    plt.show()

def filterByC(sigma, grid_size, parameter = 0.770212):

# Generate filter grid by C program, filter generated is stored by "filter.txt".
# Function textRead can read "filter.txt" into 2 dimensional string list.

    sigma = float(sigma)
    grid_size = float(grid_size)
    paramater = float(parameter)

    osString = "./mexiFilter " + "-sigma " + str(sigma) + " -grd " + str(grid_size) + \
                " -p " + str(parameter)
    os.system(osString)

def main(sigma, grid_size, parameter):

    filterByC(sigma, grid_size, parameter)
    mexfilter = textRead("filter.txt")
    filterPlot(sigma, grid_size, mexfilter)

def compileC():
    os.system("g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF 'mexiFilter.d' -MT \
            'mexiFilter.d' -o 'mexiFilter.o' 'mexiFilter.cpp'")
    os.system("g++  -o 'mexiFilter'  ./mexiFilter.o   ")

def stringToFloat(mexifilter):
    for i in range(0,len(mexifilter)):
        for j in range(0,len(mexifilter[i])):
            mexifilter[i][j] = float(mexifilter[i][j])
    return mexifilter            


if __name__ == '__main__':

    sigma = 5.0       # sigma of mexican hat curve
    grid_size = 1.0    # width of the rectangular grid.
    parameter = 0.770212  # preset parameter of mexican hat curve, make adjustment to this
                          # value to make sum of all the filter grids close to 0.
    main(sigma, grid_size, parameter)

