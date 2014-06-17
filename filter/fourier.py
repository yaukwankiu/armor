"""defining the fourier transform

c.f.
http://docs.scipy.org/doc/numpy/reference/routines.fft.html
"""

import numpy as np

def fft(a):
    """
    wrapping numpy.fft.fft2
    input:
        a   - a pattern.DBZ object
    output:
        a1, a2  - a pattern.DBZ object - real/imaginary parts of its transform
    """
    a1              = a.copy()
    a1.name         = a.name + "_fft_real"
    a1.outputPath   = a.outputPath[:-4] + "_fft_real" + a.outputPath[-4:]
    a1.imagePath    = a.imagePath[ :-4] + "_fft_real" + a.imagePath[ -4:]

    a2              = a.copy()
    a2.name         = a.name + "_fft_imag"
    a2.outputPath   = a.outputPath[:-4] + "_fft_imag" + a.outputPath[-4:]
    a2.imagePath    = a.imagePath[ :-4] + "_fft_imag" + a.imagePath[ -4:]

    a1.matrix       = np.fft.fft2(a.matrix)
    a2.matrix       = a1.matrix.imag
    a1.matrix       = a1.matrix.real
    return a1, a2


def ifft(a):
    """
    wrapping numpy.fft.ifft2
    input:
        a   - a pattern.DBZ object
    output:
        a1,a2  -  pattern.DBZ objects - real/imaginary parts of its inverse transform


    """
    a1              = a.copy()
    a1.name         = a.name + "_ifft_real"
    a1.outputPath   = a.outputPath[:-4] + "_ifft_real" + a.outputPath[-4:]
    a1.imagePath    = a.imagePath[ :-4] + "_ifft_real" + a.imagePath[ -4:]

    a2              = a.copy()
    a2.name         = a.name + "_fft_imag"
    a2.outputPath   = a.outputPath[:-4] + "_ifft_imag" + a.outputPath[-4:]
    a2.imagePath    = a.imagePath[ :-4] + "_ifft_imag" + a.imagePath[ -4:]

    a1.matrix       = np.fft.ifft2(a.matrix)
    a2.matrix       = a1.matrix.imag
    a1.matrix       = a1.matrix.real
    return a1, a2

    
    
