from pysketcher import *

R = 1    # radius of wheel
L = 4    # distance between wheels
H = 2    # height of vehicle body
w_1 = 5  # position of front wheel

xmax = w_1 + 2*L + 3*R
drawing_tool.set_coordinate_system(xmin=0, xmax=xmax,
                                   ymin=-1, ymax=2*R + 3*H,
                                   axis=False)

wheel1 = Circle(center=(w_1, R), radius=R)
wheel2 = wheel1.copy()
wheel2.translate((L,0))

under = Rectangle(lower_left_corner=(w_1-2*R, 2*R),
                  width=2*R + L + 2*R, height=H)
over  = Rectangle(lower_left_corner=(w_1, 2*R + H),
                  width=2.5*R, height=1.25*H)

wheels = Composition({'wheel1': wheel1, 'wheel2': wheel2})
body = Composition({'under': under, 'over': over})

vehicle = Composition({'wheels': wheels, 'body': body})
ground = Wall(x=[R, xmax], y=[0, 0], thickness=-0.3*R)

fig = Composition({'vehicle': vehicle, 'ground': ground})
fig.draw()  # send all figures to plotting backend

drawing_tool.display()
drawing_tool.savefig('tmp1.png')
drawing_tool.savefig('tmp1.pdf')

fig['vehicle']['wheels'].set_filled_curves('blue')
fig['vehicle']['wheels'].set_linewidth(6)
fig['vehicle']['wheels'].set_linecolor('black')
fig['vehicle']['body']['under'].set_filled_curves('red')
fig['vehicle']['body']['over'].set_filled_curves(pattern='/')
fig['vehicle']['body']['over'].set_linewidth(14)

drawing_tool.erase()  # avoid drawing old and new fig on top of each other
fig.draw()
drawing_tool.display()
drawing_tool.savefig('tmp2.png')
drawing_tool.savefig('tmp2.pdf')

print fig
fig.recurse('fig')
fig.graphviz_dot('fig', False)

import time
time.sleep(1)

# Animate motion
fig['vehicle'].translate((L,0))  # move to start point for "driving"

def v(t):
    return -8*R*t*(1 - t/(2*R))

import numpy
tp = numpy.linspace(0, 2*R, 25)
dt = tp[1] - tp[0]  # time step

def move(t, fig):
    x_displacement = dt*v(t)
    fig['vehicle'].translate((x_displacement, 0))

files = animate(fig, tp, move, moviefiles=True,
                pause_per_frame=0)

files_wildcard = files.split('%')[0] + '*.png'
os.system('convert -delay 20 %s* vehicle0.gif' % (files_wildcard))
os.system('avconv -r 12 -i %s -c:v flv vehicle0.flv' % files)
os.system('avconv -r 12 -i %s -c:v libvpx vehicle0.webm' % files)
os.system('avconv -r 12 -i %s -c:v libtheora vehicle0.ogg' % files)
os.system('avconv -r 12 -i %s -c:v libx264 -s:v 1000x520 vehicle0.mp4' % files)

try:
    from scitools.std import movie
except ImportError:
    raise ImportError(
        'scitools must be installed for running the "movie" function.\n'
        'scitools is installed by sudo apt-get install python-scitools\n'
        'on Ubuntu or by sudo python setup.py install if the code is\n'
        'downloaded from http://code.google.com/p/scitools.')
# HTML page showing individual frames
movie(files_wildcard, encoder='html', fps=4, output_file='vehicle0.html')

raw_input()
