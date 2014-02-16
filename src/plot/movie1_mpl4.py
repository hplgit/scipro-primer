"""
As movie1_mpl1.py, but using the newer FuncAnimation
set-up for animations.
"""
import numpy as np
import matplotlib.pyplot as mpl
import matplotlib.animation as animation
import time, glob, os

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
fig = mpl.figure()
mpl.axis([x[0], x[-1], -0.1, max_f])
lines = mpl.plot([], [])
mpl.xlabel('x')
mpl.ylabel('f')

# Function to return the background plot in the animation
def init():
    lines[0].set_data([], [])  # empty plot
    return lines

# Function to return a frame in the movie
all_args = [(frame_no, s, x, lines)
            for frame_no, s in enumerate(s_values)]

def frame(args):
    frame_no, s, x, lines = args
    y = f(x, m, s)
    print s, y[len(y)/2]
    lines[0].set_data(x, y)
    # Does not work: mpl.legend(['s=%4.2f' % s])
    # Does not work: mpl.savefig('tmp_%04d.png' % frame_no)
    return lines

anim = animation.FuncAnimation(fig, frame, all_args, interval=150,
                               init_func=init, blit=True)
anim.save('movie1.mp4', fps=5)
mpl.show()

