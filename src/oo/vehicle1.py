from pysketcher import *

R = 1    # radius of wheel
L = 4    # distance between wheels
H = 2    # height of vehicle body
w_1 = 5  # position of front wheel

xmax = w_1 + 2*L + 3*R
drawing_tool.set_coordinate_system(xmin=0, xmax=xmax,
                                   ymin=-1, ymax=2*R + 3*H,
                                   axis=False)

wheel1 = Composition({
    'wheel': Circle(center=(w_1, R), radius=R),
    'cross': Composition({'cross1': Line((w_1,0),   (w_1,2*R)),
                          'cross2': Line((w_1-R,R), (w_1+R,R))})})
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

print fig

import time
time.sleep(1)
from math import degrees

# Animate motion
w_1 += L                         # start position
fig['vehicle'].translate((L,0))  # move whole figure to start position

def v(t):
    return -8*R*t*(1 - t/(2*R))

import numpy
tp = numpy.linspace(0, 2*R, 25)
dt = tp[1] - tp[0]  # time step

def move(t, fig):
    x_displacement = dt*v(t)
    fig['vehicle'].translate((x_displacement, 0))

    # Rotate wheels
    global w_1
    w_1 += x_displacement
    # R*angle = -x_displacement
    angle = - x_displacement/R
    w1 = fig['vehicle']['wheels']['wheel1']
    w1.rotate(degrees(angle), center=(w_1, R))
    w2 = fig['vehicle']['wheels']['wheel2']
    w2.rotate(degrees(angle), center=(w_1 + L, R))

files = animate(fig, tp, move, moviefiles=True,
                pause_per_frame=0)

files_wildcard = files.split('%')[0] + '*.png'
os.system('convert -delay 20 %s* vehicle1.gif' % (files_wildcard))
os.system('avconv -r 12 -i %s -c:v flv vehicle1.flv' % files)
os.system('avconv -r 12 -i %s -c:v libvpx vehicle1.webm' % files)
os.system('avconv -r 12 -i %s -c:v libtheora vehicle1.ogg' % files)
os.system('avconv -r 12 -i %s -c:v flv vehicle1.flv' % files)
os.system('avconv -r 12 -i %s -c:v libx264 -s:v 1000x520 vehicle1.mp4' % files)
from scitools.std import movie
movie(files_wildcard, encoder='html', output_file='vehicle1')

raw_input()
