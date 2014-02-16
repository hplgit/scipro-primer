"""
As movie1_mpl1.py, but avoiding line.set_ydata in favor of
just using plain, repeated plot commands.
"""
import numpy as np
import matplotlib.pyplot as mpl
import time, glob, os

# Clean up old frames
for name in glob.glob('tmp_*.eps'):
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

# Make a first plot
mpl.ion()
fig = mpl.figure()

# Show the movie, and make hardcopies of frames simulatenously
counter = 0
for s in s_values:
    mpl.delaxes()  # delete plot, replot everything this s
    mpl.axis([x[0], x[-1], -0.1, max_f])
    y = f(x, m, s)
    mpl.plot(x, y)
    mpl.xlabel('x')
    mpl.ylabel('f')
    mpl.legend(['s=%4.2f' % s])
    mpl.draw()
    mpl.savefig('tmp_%04d.png' % counter)
    counter += 1
raw_input('Type Return key: ')



