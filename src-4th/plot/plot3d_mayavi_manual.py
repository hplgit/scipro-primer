import mayavi.mlab as plt
import os
from math import *
import numpy as np

h0 = 2277.
R = 4.

x = y = np.linspace(-10.,10.,41)
xv, yv = np.meshgrid(x, y, indexing='ij', sparse=False)
hv = h0/(1 + (xv**2+yv**2)/(R**2))

# Define a coarser grid for the vector field
x2 = y2 = np.linspace(-10.,10.,11)
x2v, y2v = np.meshgrid(x2, y2, indexing='ij', sparse=False)
h2v = h0/(1 + (x2v**2 + y2v**2)/(R**2)) # Surface on coarse grid
# endcoarsergrid

dhdx, dhdy = np.gradient(h2v)

# Draw contours and gradient field of h
plt.figure(11, fgcolor=(.0, .0, .0), bgcolor=(1.0, 1.0, 1.0))
plt.contour_surf(xv, yv, hv, contours=20, warp_scale=0.01)

# mode controls the style how vectors are drawn
# color controls the colors of the vectors
# scale_mode='none' ensures that vectors are drawn with the same length
plt.quiver3d(x2v, y2v, 0.01*h2v, dhdx, dhdy, np.zeros_like(dhdx),
             mode='arrow', color=(1,0,0), scale_mode='none')
# end draw contours and gradient field of h
raw_input('Press any key to continue')