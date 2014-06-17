#python struct test http://www.python.org/doc//current/library/struct.html


"""
use

h:
cd armor\python
python


import armor.tests.structTest as st
reload(st) ; y = st.main()
len(y)
L = st.factorise(len(y))
print L[-1]

"""
import os
import struct

from ..defaultParameters import *
folder  = externalHardDriveRoot + 'data_fetched_20130812/'
L       = os.listdir(folder)
filePath= folder + L[0]
print filePath

def load(filePath=filePath):
    f   = open(filePath, 'rb')
    x   = f.read()
    return x
    

def unpack_one(x, n=0, fmt="f", bytes=4):
    return struct.unpack(fmt,x[n:n+bytes])


def unpack(x, fmt='f', bytes=4):
    y = []
    for i in range(0,len(x), bytes):
        y.append(unpack_one(x=x, n=i, fmt=fmt, bytes=bytes)[0])
    return y

def factorise(N):
    """
    helps me with choosing the right shape
    """
    factorPairs = []
    a = 2
    while a< N**2:
        if N % a ==0:
            factorPairs.append((a,N/a))
            print a,N/a
        a +=1
    return factorPairs
        

def main():
    x_default = load()
    print len(x_default)
    y         = unpack(x_default)
    print len(y)
    return y