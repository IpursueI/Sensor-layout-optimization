# import numpy as np
# import matplotlib.cm as cm
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt

# delta = 0.025
# x = y = np.arange(-3.0, 3.0, delta)
# X, Y = np.meshgrid(x, y)
# Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
# Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
# Z = Z2 - Z1  # difference of Gaussians

# print Z
# im = plt.imshow(Z, interpolation='bilinear', cmap=cm.RdYlGn,
#                 origin='lower', extent=[-3, 3, -3, 3],
#                 vmax=abs(Z).max(), vmin=-abs(Z).max())

# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np

# A = np.random.rand(5, 5)
# print A

# plt.figure(3)
# #plt.imshow(A, interpolation='bicubic')
# plt.imshow(A, interpolation='bicubic', extent=[0, 100, 0, 100])
# plt.grid(True)

# plt.show()

from pykrige.ok import OrdinaryKriging
import numpy as np
import pykrige.kriging_tools as kt

data = np.array([[0.3, 1.2, 0.47],
                 [1.9, 0.6, 0.56],
                 [1.1, 3.2, 0.74],
                 [3.3, 4.4, 1.47],
                 [4.7, 3.8, 1.74]])

gridx = np.arange(0.0, 5.5, 0.5)
gridy = np.arange(0.0, 5.5, 0.5)

# Create the ordinary kriging object. Required inputs are the X-coordinates of
# the data points, the Y-coordinates of the data points, and the Z-values of the
# data points. If no variogram model is specified, defaults to a linear variogram
# model. If no variogram model parameters are specified, then the code automatically
# calculates the parameters by fitting the variogram model to the binned 
# experimental semivariogram. The verbose kwarg controls code talk-back, and
# the enable_plotting kwarg controls the display of the semivariogram.
OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear',
                     verbose=False, enable_plotting=False)

# Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
# grid of points, on a masked rectangular grid of points, or with arbitrary points.
# (See OrdinaryKriging.__doc__ for more information.)
z, ss = OK.execute('grid', gridx, gridy)

# Writes the kriged grid to an ASCII grid file.
print z