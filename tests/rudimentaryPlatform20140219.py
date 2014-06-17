"""
To do - A rudimentary platform
Yau Kwan Kiu,   19 Feb 2014.

Synopsis
    Professor Lee requested testing of various tools but did not specify the 
    standards or criteria against which the tools are to be tested.  How much
    human input is required is not yet clear.

    Today I shall construct a quick-and-dirty but complete system of forecasting.
    Various features can be fine-tuned, optimised or sped up, but it will form the 
    basic platform to develop ideas for the standards which we want to test against.

Plan
    1.  filter and preprocessing
    2.  matching
    3.  selection of models
    4.  data fusion
    5.  forecasting 
    6.  monitoring


cd /media/TOSHIBA\ EXT/ARMOR/python/
ipython


"""
################################################################################
#    0.  imports and loading the data
from armor import pattern
from armor import objects3 as ob
import numpy as np




################################################################################
#    1.  filter and preprocessing

def filter1(dataList, sigma=5):
    """
    to filter a list of images with the gaussian filter

    input:
        list of data = image slides
        sigma - parameter

    output: 
        list of filtered data
    """
    return 0

################################################################################
#    2.  matching
    """
    to match a list of (NWP) images with a template (RADAR) image
    returning a list of scores for each
    """

################################################################################
#    3.  selection of models
    """
    based on the matching (or matchings) select the top 8 models
    """
################################################################################
#    4.  data fusion
    """
    based on the results of matching and selection, perform data fusion
    """

################################################################################
#    5.  forecasting 

    """
    based on the results of fusion and selection of models, make a forecast
    """
################################################################################
#    6.  monitoring and evaluation
    """
    to evaluate the forecast
    idea:
        1. check the resemblence of the forecast to actual data (if available)
        2. if 1 is not available, use human judgement

    """
    

################################################################################
#    7.  main




def __main__():
    results1    = filter1(data)
    results2    = match1(results1)
    results3    = select1(results2)
    results4    = fuse1(results3)
    results5    = forecast1(results4)     
    scores      = evaluate1(results5) 

    
if __name__ == "__main__":
    main()
