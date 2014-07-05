# plot3dTest.py
# reference: http://matplotlib.org/1.3.1/mpl_toolkits/mplot3d/tutorial.html#wireframe-plots

import numpy as np
sigmasWRF =	[1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256]
streamMeanWRF = [7409.220327605598, 3562.90438433474, 1422.2769389734751, 1027.9384682553884, 488.49372551120683, 333.32743684275295, 144.7859178516336, 96.65068596540995, 39.53496976443776, 25.15277040160953, 8.85970026197041, 5.151248971686913, 1.350387397474956, 0.6389661286267941, 0.11484552373963036]

X = sigmasWRF
Z = streamMeanWRF

X = [np.log2(v) for v in X]
Z = [np.log2(v) for v in Z]

X, Y = np.meshgrid(X, range(30))
Z = [Z] * 30



from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
plt.show()


"""
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()
"""
