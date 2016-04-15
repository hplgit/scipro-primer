"""Add dimensions to vehicle0.py figure."""
from pysketcher import *

R = 1    # radius of wheel
L = 4    # distance between wheels
H = 2    # height of vehicle body
w_1 = 5  # position of front wheel

xmax = w_1 + 2*L + 3*R
drawing_tool.set_coordinate_system(xmin=0, xmax=xmax,
                                   ymin=-1, ymax=2*R + 3*H,
                                   axis=True)

drawing_tool.set_grid(True)

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

x_dim = w_1 + L + 2*R + R  # line for vertical dimensions
y_dim = 2*R + H + 1.25*H + R/2.
w_1_dim = Text_wArrow('$w_1$', (w_1+2*R, 1.5*R), (w_1, R))
wheel_dim = Distance_wText((x_dim, 0), (x_dim, R), '$R$')
under_dim = Distance_wText((x_dim, 2*R), (x_dim, 2*R+H), '$H$')
over_dim  = Distance_wText((x_dim, 2*R+H), (x_dim, 2*R+H+1.25*H),
                           r'$\frac{5}{4}{H}$')
front_dim = Distance_wText((w_1-2*R, y_dim), (w_1, y_dim), '$2R$')
L_dim     = Distance_wText((w_1, y_dim), (w_1+L, y_dim), '$L$')
back_dim  = Distance_wText((w_1+L, y_dim), (w_1+L+2*R, y_dim), '$2R$')

dims = Composition(dict(w_1_dim=w_1_dim,
                        wheel_dim=wheel_dim,
                        under_dim=under_dim,
                        over_dim=over_dim,
                        front_dim=front_dim,
                        L_dim=L_dim,
                        back_dim=back_dim))

fig = Composition({'vehicle': vehicle, 'ground': ground, 'dims': dims})
fig.draw()  # send all figures to plotting backend

drawing_tool.display()
drawing_tool.savefig('tmp1.png')
drawing_tool.savefig('tmp1.pdf')

print fig

raw_input()
