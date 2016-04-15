from pysketcher import *

class Vehicle0(Shape):
    def __init__(self, w_1, R, L, H):
        wheel1 = Circle(center=(w_1, R), radius=R)
        wheel2 = wheel1.copy()
        wheel2.translate((L,0))

        under = Rectangle(lower_left_corner=(w_1-2*R, 2*R),
                          width=2*R + L + 2*R, height=H)
        over  = Rectangle(lower_left_corner=(w_1, 2*R + H),
                          width=2.5*R, height=1.25*H)

        wheels = Composition(
            {'wheel1': wheel1, 'wheel2': wheel2})
        body = Composition(
            {'under': under, 'over': over})

        vehicle = Composition({'wheels': wheels, 'body': body})
        xmax = w_1 + 2*L + 3*R
        ground = Wall(x=[R, xmax], y=[0, 0], thickness=-0.3*R)

        self.shapes = {'vehicle': vehicle, 'ground': ground}

    def colorful(self):
        wheels = self.shapes['vehicle']['wheels']
        wheels.set_filled_curves('blue')
        wheels.set_linewidth(6)
        wheels.set_linecolor('black')
        under = self.shapes['vehicle']['body']['under']
        under.set_filled_curves('red')
        over = self.shapes['vehicle']['body']['over']
        over.set_filled_curves(pattern='/')
        over.set_linewidth(14)

def _test():
    R = 1;  L = 4;  H = 2;  w_1 = 5
    xmax = w_1 + 2*L + 3*R
    drawing_tool.set_coordinate_system(
        xmin=0, xmax=xmax, ymin=-1, ymax=2*R + 3*H, axis=False)

    vehicle = Vehicle0(w_1, R, L, H)
    vehicle.draw()
    drawing_tool.display()
    print vehicle
    vehicle.graphviz_dot('Vehicle0', classname=False)
    vehicle.recurse('vehicle')


    drawing_tool.erase()
    vehicle.colorful()
    vehicle.draw()
    drawing_tool.display()

if __name__ == '__main__':
    _test()
    raw_input()
