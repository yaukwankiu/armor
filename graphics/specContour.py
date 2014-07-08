
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random
import os


def specContour(XYZ, XYZ2=None, **kwargs):
    x = XYZ['X'][0]
    y = np.zeros([len(XYZ['Y'])])

    for i in range(0, len(y)):
        y[i] = XYZ['Y'][i][0]

    X, Y = np.meshgrid(y, x)

    Z = np.transpose(XYZ['Z'])
    for i in range(0, len(Z)):
        for j in range(0, len(Z[i])):
            if Z[i][j] > 0:
                Z[i][j] = np.log10(Z[i][j])

    if XYZ2 is not None:
        Z2 = np.transpose(XYZ2['Z'])
        for i in range(0, len(Z2)):
            for j in range(0, len(Z2[i])):
                if Z2[i][j] > 0:
                    Z2[i][j] = np.log10(Z2[i][j])
    try:
        rand_cmap = kwargs['random_cmap']
    except(KeyError):
        rand_cmap = False

    try:
        title = kwargs['title']
    except(KeyError):
        title = ""

    try:
        name1 = kwargs['name1']
    except(KeyError):
        name1 = ""
    try:
        name2 = kwargs['name2']
    except(KeyError):
        name2 = ""


    if XYZ2 is None:
        if rand_cmap:
            maps = [m for m in plt.cm.datad if not m.endswith("_r")]
            r = random.randint(0, len(maps)-1)
            cmap = plt.get_cmap(maps[r])
        else:
            cmap = plt.cm.BuPu

        plt.xlabel('sigma, log scale base=2')
        plt.ylabel('Intensity')

        if name1:
            title = title + '\n' + name1
        plt.title(title)

        CS0 = plt.contourf(X, Y, Z, 20, cmap=cmap, origin='lower')
        #CS1 = plt.contour(CS0, levels=CS0.levels, colors='k',
        #                  origin='lower', hold='on', alpha=0.8, inline=1,
        #                  linestyles='solid')
        CS1 = plt.contour(X,Y,Z, 10, colors='k',
                          origin='lower', hold='on', alpha=0.8, inline=1,
                          linestyles='solid')



        plt.clabel(CS1, inline=1, fontsize=10, fmt='%1.1f')
        plt.semilogx(Y, basex=2, visible=False)
        
        diver = make_axes_locatable(plt.gca())
        cax = diver.append_axes("bottom", "5%", pad="8%")
        cbar = plt.colorbar(CS0, orientation='horizontal', cax=cax)
        cax.set_title('10^N', fontsize=12, y=-1.4)
        cbar.add_lines(CS1)
        plt.tight_layout(h_pad=0.5)
            
    else:
        Z3 = np.zeros([len(Z), len(Z[0])])
        for i in range(0, len(Z)):
            for j in range(0, len(Z[i])):
                Z3[i][j] = Z2[i][j] - Z[i][j]

        plt.xlabel('sigma, log scale base=2')
        plt.ylabel('Intensity')

        if name1:
            title = title + '\n' + name1
        if name2:
            title = title + '\n' + 'and ' + name2

        plt.title(title)

        CS1 = plt.contour(X, Y, Z, 20, colors='k', origin='lower', hold='on',
                          alpha=0.6, linestyles='solid', inline=1)
        CS2 = plt.contour(X, Y, Z2, 20, colors='r', origin='lower', hold='on',
                          alpha=1, linestyles='solid', inline=1)
        plt.clabel(CS1, inline=1, fontsize=10, fmt='%1.1f')
        plt.clabel(CS2, inline=1, fontsize=11, fmt='%1.1f')

        maps = ['BrBG', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu',
                'RdYlGn', 'coolwarm']
        if rand_cmap:
            r = random.randint(0, len(maps)-1)
            cmap = plt.get_cmap(maps[r])
        else:
            cmap = plt.cm.coolwarm

        CS3 = plt.contourf(X, Y, Z3, 20, cmap=cmap, origin='lower')
        #CS4 = plt.contour(CS3, levels=CS3.levels, colors='w',
        #            origin='lower', hold='on', alpha=0.6, inline=1,
        #            fontsize=10)
        CS4 = plt.contour(X, Y, Z3 ,10, colors='w',
                    origin='lower', hold='on', alpha=0.6, inline=1,
                    fontsize=10)
        plt.semilogx(Y, basex=2, visible=False)

        diver = make_axes_locatable(plt.gca())
        cax = diver.append_axes("bottom", "5%", pad="8%")
        cbar = plt.colorbar(CS3, orientation='horizontal', cax=cax)
        cax.set_title('10^N', fontsize=12, y=-1.4)
        cbar.add_lines(CS4)
        plt.tight_layout(h_pad=0.5)

    try:
        display = kwargs['display']
    except(KeyError):
        display = True

    try:
        outputFolder = kwargs['outputFolder']
    except(KeyError):
        outputFolder = os.getcwd()

    try:
        fileName = kwargs['fileName']
        plt.savefig(outputFolder +  fileName)
    except(KeyError):
        None

    if display:
        plt.show()
