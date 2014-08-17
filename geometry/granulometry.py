#   http://en.wikipedia.org/wiki/Granulometry_%28morphology%29
#   http://scipy-lectures.github.io/advanced/image_processing/
#   http://scipy-lectures.github.io/advanced/image_processing/auto_examples/plot_granulo.html#example-plot-granulo-py
#

from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import time
from .. import defaultParameters as dp

def disk_structure(n):
    struct = np.zeros((2 * n + 1, 2 * n + 1))
    x, y = np.indices((2 * n + 1, 2 * n + 1))
    mask = (x - n)**2 + (y - n)**2 <= n**2
    struct[mask] = 1
    return struct.astype(np.bool)


def granulometry(data, sizes=None):
    s = max(data.shape)
    if sizes == None:
        sizes = range(1, s/2, 2)
    granulo = [ndimage.binary_opening(data, \
            structure=disk_structure(n)).sum() for n in sizes]
    return granulo


def analyse(im, scales=[4,10,14,40], verbose=True,display=True, outputFolder=""):
    try:
        mask = im > im.mean()
    except:
        im = im.matrix
        mask = im > im.mean()

    #granulo = granulometry(mask, sizes=np.arange(2, 19, 4))
    granulo = granulometry(mask, sizes=scales)
    print 'granulo:', granulo

    plt.figure(figsize=(6, 2.2))
    plt.subplot(121)
    plt.imshow(mask, cmap=plt.cm.gray, origin='lower')

    openedList = [0] * len(scales)
    for i, s in enumerate(scales):
        openedList[i] = ndimage.binary_opening(mask, structure=disk_structure(s))

    if len(scales)==4:
        plt.contour(openedList[0], [0.5], colors='g', linewidths=1)
        plt.contour(openedList[1], [0.5], colors='b', linewidths=1)
        plt.contour(openedList[2], [0.5], colors='r', linewidths=1)
        plt.contour(openedList[3], [0.5], colors='k', linewidths=1)
    else:
        for i in range(len(scales)):
            plt.contour(openedList[i], [0.5], colors=dp.coloursList[i], linewidths=1)
    
    plt.axis('off')
    plt.subplot(122)
    plt.plot(scales, granulo, 'ok', ms=8)
    plt.subplots_adjust(wspace=0.02, hspace=0.15, top=0.95, bottom=0.15, left=0, right=0.95)

    #################################
    #   maximise frame window 
    #   http://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
    #   how?
    
    #
    #################################

    if outputFolder!="":
        plt.savefig(outputFolder+ str(time.time())+ str(scales)+'granulometry.png', dpi=200)
    if display:
        plt.show(block=False)
    
    return openedList


def main():
    np.random.seed(1)
    n = 10
    l = 256
    im = np.zeros((l, l))
    points = l*np.random.random((2, n**2))
    im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
    im = ndimage.gaussian_filter(im, sigma=l/(4.*n))
    analyse(im)


if __name__ == '__main__':
    main()

