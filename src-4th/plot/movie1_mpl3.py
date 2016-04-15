"""
As movie1_mpl1.py, but avoiding line.set_ydata in favor of
just using plain, repeated plot commands.
This variant applies plotting through an Axis (ax) object
instead of the matplotlib.pyplot functions.
"""

import numpy as np
import matplotlib.pyplot as plt
import time, glob, os

# Clean up old frames
for name in glob.glob('tmp_*.pdf'):
    os.remove(name)

def f(x, m, s):
    return (1.0/(np.sqrt(2*np.pi)*s))*np.exp(-0.5*((x-m)/s)**2)

m = 0
s_max = 2
s_min = 0.2
x = np.linspace(m -3*s_max, m + 3*s_max, 1000)
s_values = np.linspace(s_max, s_min, 30)
# f is max for x=m; smaller s gives larger max value
max_f = f(m, m, s_min)

plt.ion()
fig = plt.figure()

# Show the movie, and make hardcopies of frames simulatenously
counter = 0
for s in s_values:
    # delete plot, replot everything for this s
    fig.clf() # or plt.delaxes()
    ax = fig.gca()
    ax.axis([x[0], x[-1], -0.1, max_f])
    y = f(x, m, s)
    ax.plot(x, y)
    ax.set_xlabel('x')
    ax.set_ylabel('f')
    ax.legend(['s=%4.2f' % s])
    plt.draw()
    fig.savefig('tmp_%04d.png' % counter)
    counter += 1
raw_input('Type Return key: ')



