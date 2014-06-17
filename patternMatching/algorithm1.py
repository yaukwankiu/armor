# plain vanilla correlation comparison

#import numpy as np
import numpy.ma as ma
import time

def match(dbz1, dbz2):
    """
    input:  two armor.pattern.DBZ objects
    output: just their correlation
    **** PROBLEM:  need to resolve the grid problem with e.g. interpolation

    """
    size = dbz1.matrix.size
    return ma.corrcoef(dbz1.matrix.reshape(size), dbz2.matrix.reshape(size))[0,1]
    
    
def selfTest(dbz1, dbz2):
    """ testing itself
    use:  
        from armor.patternMatching import algorithm1
        x = algorithm1.selfTest()
    
    """
    r = match(dbz1, dbz2)
    print "the correlation of %s and %s is %f" % (dbz1.name, dbz2.name, r)
    return r

def main(verbose=True):
    t0 = time.time()
    from armor import pattern
    if verbose:
        print 'comparing:', pattern.a.name, 'and', pattern.b.name
    r = selfTest(pattern.a, pattern.b)
    if verbose:
        print 'time spent:', time.time()-t0
    return r
    