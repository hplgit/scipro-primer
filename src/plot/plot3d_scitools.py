from math import *
import numpy as np

import scitools.easyviz as plt
#from scitools.easyviz.gnuplot_ import *


h0 = 2277.  # Height of the top of the mountain (m)
R = 4.     # The radius of the mountain (km)

x = y = np.linspace(-10., 10., 41)
xv, yv = plt.ndgrid(x, y)             # Grid for x, y values (km)
hv = h0/(1+(xv**2+yv**2)/(R**2)) # Compute height (m)

x = y = np.linspace(-10.,10.,11)
x2v, y2v = plt.ndgrid(x, y)      # Define a coarser grid for the vector field
h2v = h0/(1+(x2v**2+y2v**2)/(R**2)) # Compute height for new grid
dhdx, dhdy = np.gradient(h2v)         # Compute the gradient vector (dh/dx,dh/dy)

# Draw contours and gradient field of h
plt.figure(9)
plt.quiver(x2v, y2v, dhdx, dhdy, 0, 'r')
plt.hold('on')
plt.contour(xv, yv, hv)
plt.axis('equal')
# end draw contours and gradient field of h

x = y = np.linspace(-5, 5, 11)
xv, yv = plt.ndgrid(x, y)
u = xv**2 + 2*yv - .5*xv*yv
v = -3*yv

# Draw 2D-field
plt.figure(10)
plt.quiver(xv, yv, u, v, 200, 'b')
plt.axis('equal')
# end draw 2D-field





plt.figure(9)
plt.savefig('images/quiver_scitools_advanced.pdf')
plt.savefig('images/quiver_scitools_advanced.png')

plt.figure(10)
plt.savefig('images/quiver_scitools_simple.pdf')
plt.savefig('images/quiver_scitools_simple.png')