from matplotlib import pyplot
import matplotlib as mpl
colourbar     = {
                    65 : [255 ,255,255],
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
bounds  = range(-10, 75, 5)
lowers  = sorted(colourbar.keys())
cmap = mpl.colors.ListedColormap([[
                                   1.*colourbar[v][0]/255, 
                                   1.*colourbar[v][1]/255, 
                                   1.*colourbar[v][2]/255
                                  ] for v in lowers
                                 ])      # [[0., .4, 1.], [0., .8, 1.], [1., .8, 0.], [1., .4, 0.]]


"""
cmap.set_over((1.*colourbar[65][0]/255, 
               1.*colourbar[65][1]/255, 
               1.*colourbar[65][2]/255))
"""
cmap.set_over((0,0,0)) #black!!


cmap.set_under((1.*colourbar[-10][0]/255, 
                1.*colourbar[-10][1]/255, 
                1.*colourbar[-10][2]/255))


"""

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

"""
