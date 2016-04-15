from pysketcher import *

def draw_vehicle(
    R=1,    # radius of wheel
    L=4,    # distance between wheels
    H=2,    # height of vehicle body
    w_1=5,  # position of front wheel
    ):

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
    return fig

#fig = draw_vehicle(R=1, L=4, H=2, w_1=8)
#fig = draw_vehicle(R=0.5, L=5, H=2, w_1=8)
fig = draw_vehicle(R=2, L=7, H=1, w_1=10)
fig.draw()  # send all figures to plotting backend

drawing_tool.display()
drawing_tool.savefig('tmp1.png')
drawing_tool.savefig('tmp1.pdf')

raw_input()
