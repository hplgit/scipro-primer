import os
from math import *
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

font = {'size'   : 24}
font2 = {'size'   : 12}

h0 = 2277.   # Height of the top of the mountain (m)
R = 4.       # Radius of the mountain (km)
#endinitvalues

# Grid for x, y values (km)
x = y = np.linspace(-10., 10., 41)
xv, yv = np.meshgrid(x, y, indexing='ij', sparse=False)

hv = h0/(1 + (xv**2+yv**2)/(R**2))
# endinitgrid

s = np.linspace(0, 2*np.pi, 100)
curve_x = 10*(1 - s/(2*np.pi))*np.cos(s)
curve_y = 10*(1 - s/(2*np.pi))*np.sin(s)
curve_z = h0/(1 + 100*(1 - s/(2*np.pi))**2/(R**2))
# endparamcurve




# Simple plot of mountain
fig = plt.figure(1)
ax = fig.gca(projection='3d')
ax.plot_wireframe(xv, yv, hv, rstride=2, cstride=2)

# Simple plot of mountain and parametric curve
fig = plt.figure(2)
ax = fig.gca(projection='3d')
from matplotlib import cm
ax.plot_surface(xv, yv, hv, cmap=cm.coolwarm,
                rstride=1, cstride=1)

# add the parametric curve. linewidth controls the width of the curve
ax.plot(curve_x, curve_y, curve_z, linewidth=5)
# endsimpleplots



#h0 = 22.77
#R = 4.

#hv = h0/(1 + (xv**2+yv**2)/(R**2))

# Define a coarser grid for the vector field
x2 = y2 = np.linspace(-10.,10.,11)
x2v, y2v = np.meshgrid(x2, y2, indexing='ij', sparse=False)
h2v = h0/(1 + (x2v**2 + y2v**2)/(R**2)) # h on coarse grid
# endcoarsergrid

dhdx, dhdy = np.gradient(h2v) # dh/dx, dh/dy
# endgradient


# Default two-dimensional contour plot with 7 colored lines
fig = plt.figure(3)
ax = fig.gca()
ax.contour(xv, yv, hv)
plt.axis('equal')

# Default three-dimensional contour plot
fig = plt.figure(4)
ax = fig.gca(projection='3d')
ax.contour(xv, yv, hv)

# Plot of mountain and contour lines projected on the
# coordinate planes
fig = plt.figure(5)
ax = fig.gca(projection='3d')
ax.plot_surface(xv, yv, hv, cmap=cm.coolwarm,
                rstride=1, cstride=1)
# zdir is the projection axis
# offset is the offset of the projection plane
ax.contour(xv, yv, hv, zdir='z', offset=-1000, cmap=cm.coolwarm)
ax.contour(xv, yv, hv, zdir='x', offset=-10,   cmap=cm.coolwarm)
ax.contour(xv, yv, hv, zdir='y', offset=10,    cmap=cm.coolwarm)

# View the contours by displaying as an image
fig = plt.figure(6)
ax = fig.gca()
ax.imshow(hv)

# 10 contour lines (equally spaced contour levels)
fig = plt.figure(7)
ax = fig.gca()
ax.contour(xv, yv, hv, 10)
plt.axis('equal')

# 10 black ('k') contour lines
fig = plt.figure(8)
ax = fig.gca()
ax.contour(xv, yv, hv, 10, colors='k')
plt.axis('equal')

# Specify the contour levels explicitly as a list
fig = plt.figure(9)
ax = fig.gca()
levels = [500., 1000., 1500., 2000.]
ax.contour(xv, yv, hv, levels=levels)
plt.axis('equal')

# Add labels with the contour level for each contour line
fig = plt.figure(10)
ax = fig.gca()
cs = ax.contour(xv, yv, hv)
plt.clabel(cs)
plt.axis('equal')
#end contourplots

# Draw contours and gradient field of h
fig = plt.figure(11)
ax = fig.gca()
ax.quiver(x2v, y2v, dhdx, dhdy, color='r',
          angles='xy', scale_units='xy')
ax.contour(xv, yv, hv)
plt.axis('equal')
# end draw contours and gradient field of h


plt.rc('font', **font)

plt.figure(1)
plt.savefig('images/simple_plot_matplotlib.pdf')
plt.savefig('images/simple_plot_matplotlib.png')

plt.figure(2)
plt.savefig('images/simple_plot_colours_matplotlib.pdf')
plt.savefig('images/simple_plot_colours_matplotlib.png')

# Save contour plots

plt.figure(3)
plt.savefig('images/default_contour_matplotlib.pdf')
plt.savefig('images/default_contour_matplotlib.png')

plt.figure(4)
plt.savefig('images/default_contour3_matplotlib.pdf')
plt.savefig('images/default_contour3_matplotlib.png')

plt.figure(5)
plt.savefig('images/contour3_dims_matplotlib.png')
plt.savefig('images/contour3_dims_matplotlib.pdf')

plt.figure(6)
plt.savefig('images/contour_imshow_matplotlib.pdf')
plt.savefig('images/contour_imshow_matplotlib.png')

plt.figure(7)
plt.savefig('images/contour_10levels_matplotlib.pdf')
plt.savefig('images/contour_10levels_matplotlib.png')

plt.figure(8)
plt.savefig('images/contour_10levels_black_matplotlib.pdf')
plt.savefig('images/contour_10levels_black_matplotlib.png')

plt.figure(9)
plt.savefig('images/contour_speclevels_matplotlib.pdf')
plt.savefig('images/contour_speclevels_matplotlib.png')

plt.figure(10)
plt.savefig('images/contour_clabel_matplotlib.pdf')
plt.savefig('images/contour_clabel_matplotlib.png')


# Save vector field plots

plt.rc('font', **font2)

plt.figure(11)
plt.savefig('images/quiver_matplotlib_advanced.pdf')
plt.savefig('images/quiver_matplotlib_advanced.png')
