#   http://en.wikipedia.org/wiki/Granulometry_%28morphology%29
#   http://scipy-lectures.github.io/advanced/image_processing/
#   http://scipy-lectures.github.io/advanced/image_processing/auto_examples/plot_granulo.html#example-plot-granulo-py
#

from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np

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


def analyse(im, scales=[4,10,14,40], verbose=True):
    try:
        mask = im > im.mean()
    except:
        im = im.matrix
        mask = im > im.mean()

    granulo = granulometry(mask, sizes=np.arange(2, 19, 4))
    print 'granulo:', granulo

    plt.figure(figsize=(6, 2.2))
    plt.subplot(121)
    plt.imshow(mask, cmap=plt.cm.gray, origin='lower')
    opened_less = ndimage.binary_opening(mask, structure=disk_structure(scales[0]))
    opened = ndimage.binary_opening(mask, structure=disk_structure(scales[1]))
    opened_more = ndimage.binary_opening(mask, structure=disk_structure(scales[2]))
    opened_even_more = ndimage.binary_opening(mask, structure=disk_structure(scales[3]))
    plt.contour(opened_less, [0.5], colors='g', linewidths=2)
    plt.contour(opened, [0.5], colors='b', linewidths=2)
    plt.contour(opened_more, [0.5], colors='r', linewidths=2)
    plt.contour(opened_even_more, [0.5], colors='k', linewidths=2)

    plt.axis('off')
    plt.subplot(122)
    plt.plot(np.arange(2, 19, 4), granulo, 'ok', ms=8)
    plt.subplots_adjust(wspace=0.02, hspace=0.15, top=0.95, bottom=0.15, left=0, right=0.95)
    if verbose:
        plt.show()
    
    return opened_less, opened, opened_more, opened_even_more


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

