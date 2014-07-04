
import pickle
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time

def writeTxt(file_path, data):
    try:
        f = open(file_path, 'w')
        for i in range(0, len(data)):
            line = ""
            if type(data[i]) != list and type(data[i]) != np.ndarray:
                line = str(data[i])
            else:
                for j in range(0, len(data[i])):
                    line = line + str(data[i][j]) + " "
            line = line + '\n'
            f.write(line)
    except(IOError):
        print "Can't read file %s, please check file and folder existence or\
 file status." % file_path


def main(file_name):
    xyz = pickle.load(open(file_name, 'r'))
    data = list()
    row_length = len(xyz['X'])
    col_length = len(xyz['X'][0])

    X_chart = xyz['X']
    Y_chart = xyz['Y']
    Z_chart = xyz['Z']

    for i in range(0, row_length):
        for j in range(0, col_length):
            data.append([X_chart[i][j], Y_chart[i][j], Z_chart[i][j]])

    data.insert(0, "x y z")

    writeTxt('WRF.txt', data)

    data.pop(0)

    return data


def dataMapping(data, row_num):

    mapped_dat = list()
    counter = 0
    row = list()
    y = list()
    for i in range(0, len(data)):
        if not data[i][2] == 0:
            row.append(np.log(data[i][2]))
        else:
            row.append(0.0)
        counter += 1
        if counter == row_num:
            y.append(data[i][1])
            mapped_dat.append(row)
            row = list()
            counter = 0

    return [mapped_dat, y]


def plotContour(data, data_2, outputFolder="", display=False):

    [data, y] = dataMapping(data, 20)
    [data_2, y] = dataMapping(data_2, 20)

    x = np.linspace(0, 19, 20)

    X, Y = np.meshgrid(x, y)

    CS0 = plt.contourf(X, Y, data_2, 20, cmap=plt.cm.bone, origin='lower')
    CS3 = plt.contour(CS0, levels=CS0.levels[::2], colors='b', origin='lower',
                      hold='on', alpha=0.2, inline=1, fontsize=10)
    CS = plt.contourf(X, Y, data, 20, cmap=plt.cm.BuPu, origin='lower', alpha=0.7)
    CS2 = plt.contour(CS, levels=CS.levels[::2], colors='r', origin='lower',
                      hold='on')
    plt.clabel(CS3, inline=1, fontsize=10)
    plt.clabel(CS2, inline=1, fontsize=10)
    plt.semilogy(Y, basey=2)

    diver = make_axes_locatable(plt.gca())

    cax = diver.append_axes("bottom", "5%", pad="8%")
    cax2 = diver.append_axes("bottom", "5%", pad="8%")
    cbar2 = plt.colorbar(CS0, orientation='horizontal', cax=cax)
    cax.set_title('COMPREF Power Spectrum, Log Scale', fontsize=9)
    cbar2.add_lines(CS3)
    cbar = plt.colorbar(CS, orientation='horizontal', cax=cax2)
    cax2.set_title('WRF Power Spectrum, Log Scale', fontsize=9)
    cbar.add_lines(CS2)
    plt.tight_layout(h_pad=0.5)
    plt.savefig(str(time.time())+"powerSpecContourPlot.png")
    if display:
        plt.show()


if __name__ == '__main__':

    dat_in = main('XYZ(1).pydump')
    dat_in_2 = main('XYZ.pydump')
    plotContour(dat_in, dat_in_2)
