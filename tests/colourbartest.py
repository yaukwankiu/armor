'''
Make a colorbar as a separate figure.
'''

from matplotlib import pyplot
import matplotlib as mpl

# Make a figure and axes with dimensions as desired.
fig = pyplot.figure(figsize=(8,3))
ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
ax3 = fig.add_axes([0.05, 0.15, 0.9, 0.15])

# Set the colormap and norm to correspond to the data for which
# the colorbar will be used.
cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin=5, vmax=10)

# ColorbarBase derives from ScalarMappable and puts a colorbar
# in a specified axes, so it has everything needed for a
# standalone colorbar.  There are many more kwargs, but the
# following gives a basic continuous colorbar with ticks
# and labels.
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                   norm=norm,
                                   orientation='horizontal')
cb1.set_label('Some Units')

# The second example illustrates the use of a ListedColormap, a
# BoundaryNorm, and extended ends to show the "over" and "under"
# value colors.
cmap = mpl.colors.ListedColormap(['r', 'g', 'b', 'c'])
cmap.set_over('0.25')
cmap.set_under('0.75')

# If a ListedColormap is used, the length of the bounds array must be
# one greater than the length of the color list.  The bounds must be
# monotonically increasing.
bounds = [1, 2, 4, 7, 8]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                     norm=norm,
                                     # to use 'extend', you must
                                     # specify two extra boundaries:
                                     boundaries=[0]+bounds+[13],
                                     extend='both',
                                     ticks=bounds, # optional
                                     spacing='proportional',
                                     orientation='horizontal')
cb2.set_label('Discrete intervals, some other units')

# The third example illustrates the use of custom length colorbar
# extensions, used on a colorbar with discrete intervals.

colourbar = {65 : [255 ,255,255],
            60 : [159 , 49 , 206],
            55 : [255 , 0 ,255],
            50 : [206 , 0 , 0],
            45 : [255 , 0 , 0],
            40 : [255 , 99 , 99],
            35 : [255 , 148 , 0],
            30 : [231 , 198 , 0],
            25 : [255 , 255, 0],
            20 : [ 0 , 148, 0 ],
            15 : [ 0 , 173 , 0 ],
            10 : [ 0 , 206 , 0 ],
             5 : [ 0,    0, 255], # VV i made these up: VV
             0 : [ 0,  99,  255],
            -5 : [ 0, 198,  255],
           -10 : [156 ,156 , 156],
            }
# http://stackoverflow.com/questions/3373256/set-colorbar-range-in-matplotlib            
# http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
# http://stackoverflow.com/questions/12073306/customize-colorbar-in-matplotlib
# http://stackoverflow.com/questions/7875688/how-can-i-create-a-standard-colorbar-for-a-series-of-plots-in-python
#*  http://matplotlib.org/examples/api/colorbar_only.html
#   http://stackoverflow.com/questions/4801366/convert-rgb-values-into-integer-pixel
"""
cdict   =   {   'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
                'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
                'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
            }
"""

colourbarlen    = 70 - (-10)

cdict   =   {
                'red'  :  [],
                'green':  [],
                'blue' :  [],
            }

##################################################################################

bounds  = range(-10, 75, 5)
lowers  = sorted(colourbar.keys())
cmap = mpl.colors.ListedColormap([[1.*colourbar[v][0]/255, 
                                   1.*colourbar[v][1]/255, 
                                   1.*colourbar[v][2]/255
                                  ] for v in lowers
                                 ])      # [[0., .4, 1.], [0., .8, 1.], [1., .8, 0.], [1., .4, 0.]]



cmap.set_over((1.*colourbar[65][0]/255, 
               1.*colourbar[65][1]/255, 
               1.*colourbar[65][2]/255))

cmap.set_under((1.*colourbar[-10][0]/255, 
                1.*colourbar[-10][1]/255, 
                1.*colourbar[-10][2]/255))




norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#fig = pyplot.figure()
#ax3 = fig.add_axes()
cb3 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap,
                                     norm=norm,
                                     boundaries=[-10]+bounds+[10],
                                     extend='both',
                                     # Make the length of each extension
                                     # the same as the length of the
                                     # interior colors:
                                     #extendfrac='auto',
                                     ticks=bounds,
                                     spacing='uniform',
                                     orientation='horizontal'
                                     )


cb3.set_label('Custom extension lengths, some other units')


pyplot.show()
