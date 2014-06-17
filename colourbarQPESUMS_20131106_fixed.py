#  colour bar for QPESUMS
# https://docs.google.com/viewer?a=v&pid=gmail&attid=0.1&thid=1390f8c8674573cf&mt=application/vnd.openxmlformats-officedocument.wordprocessingml.document&url=https://mail.google.com/mail/u/0/?ui%3D2%26ik%3D4655456462%26view%3Datt%26th%3D1390f8c8674573cf%26attid%3D0.1%26disp%3Dsafe%26zw&sig=AHIEtbRyeWc8FBF0v6BP4JnTh-xWWnQQGQ



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
             5 : [156 ,156 , 156],
             0 : [115, 99 , 132],
            -5 : [ 99 , 82 , 115],
           -10 : [100, 100, 100],       # i made it up myself.
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

bounds  = range(10, 75, 5)
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
fig = pyplot.figure()
ax3 = fig.add_axes()
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
                                     #orientation='horizontal'
                                     )


cb3.set_label('Custom extension lengths, some other units')

pyplot.show()


