from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import random
import os


def spectrum3d(XYZ, **kwargs):
    x = XYZ['X'][0]
    y = np.zeros(len(XYZ['Y']))
    for i in range(0, len(XYZ['Y'])):
        y[i] = np.log2(XYZ['Y'][i][0])

    X, Y = np.meshgrid(x, y)
    Z = np.zeros([len(XYZ['Z']), len(XYZ['Z'][0])])
    for i in range(0, len(Z)):
        for j in range(0, len(Z[0])):
            if XYZ['Z'][i][j] != 0:
                Z[i][j] = np.log10(XYZ['Z'][i][j])

    try:
        Zmax = kwargs['setMax']
    except(KeyError):
        Zmax = Z.max()
    try:
        Zmin = kwargs['setMin']
    except(KeyError):
        Zmin = Z.min()

    figure = plt.figure()
    ax = figure.gca(projection='3d')
    randcolor = False
    try:
        randcolor = kwargs['randcolor']
    except:
        color = 'b'
    if randcolor:
        color = [random.uniform(0, 1), random.uniform(0, 1),
                 random.uniform(0, 1)]

    try:
        alpha = kwargs['alpha']
    except(KeyError):
        alpha = 0.3

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color=color, alpha=alpha)
    ax.set_zlim(Zmin, Zmax)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    try:
        elev_set = kwargs['ver_rotate']
    except(KeyError):
        elev_set = 33
    try:
        azim_set = kwargs['hor_roate']
    except(KeyError):
        azim_set = -24

    ax.view_init(elev=elev_set, azim=azim_set)

    try:
        title = kwargs['title']
    except(KeyError):
        title = ""

    plt.title(title)
    plt.ylabel(r'$\sigma$=2$^x$', fontsize=18)
    plt.xlabel(r'Intensity class(0.1$\times$10$^{0.5y}$)', fontsize=16)
    ax.set_zlabel(r'log$_{10}$(N)')

    try:
        outputFolder = kwargs['outputFolder']
    except(KeyError):
        outputFolder = os.getcwd()

    try:
        fileName = kwargs['fileName']
        figure.savefig( outputFolder + "/" + fileName)
        print "Save figure with name and path %s" % outputFolder + "\\" \
                + fileName
    except(KeyError):
        print "figure not saved."

    try:
        show = kwargs['display']
    except(KeyError):
        show = False

    if show:
        plt.show()
    else:
        plt.close()
