from pysketcher import *
import numpy as np

# Define the grid lines (uniform spacing)
x = np.linspace(0, 3, 4)
y = np.linspace(0, 1, 3)

# Define drawing area (add some space to each side of the grid)
xmin = x[0] - 0.5
xmax = x[-1] + 0.5
ymin = y[0] - 0.5
ymax = y[-1] + 0.5

drawing_tool.set_coordinate_system(xmin, xmax, ymin, ymax, axis=False)
drawing_tool.set_linecolor('black')
drawing_tool.set_linewidth(1)

# Store each line in lists for the two directions
x_lines = [Line((x[i], y[0]), (x[i], y[-1])) for i in range(len(x))]
y_lines = [Line((x[0], y[i]), (x[-1], y[i])) for i in range(len(y))]
# Transform lists to dicts since pysketcher works with dicts
x_lines = {'x%d' % i: x_line for i, x_line in enumerate(x_lines)}
y_lines = {'y%d' % i: y_line for i, y_line in enumerate(y_lines)}

# Collect all lines in one grid object
grid = Composition(dict(x_lines=Composition(x_lines),
                        y_lines=Composition(y_lines)))

# Make text objects for the coordinates of the grid points
coordinates = {}
d = point(0.02,0.02)  # text displacement, 45 degrees up-right
for x_ in x:
    for y_ in y:
        coordinates['%s%s' % (x_, y_)] = Text(
            '(%g,%g)' % (x_, y_),
            point(x_, y_) + d,
            alignment='left',
            fontsize=8)
coordinates = Composition(dict(coordinates=Composition(coordinates)))

# Draw grid with coordinates
grid.draw()
coordinates.draw()
drawing_tool.display()
drawing_tool.savefig('tmp1')

# Make new drawing with indices instead of coordinates
drawing_tool.erase()
indices = {}
for i, x_ in enumerate(x):
    for j, y_ in enumerate(y):
        indices['%s%s' % (i, j)] = Text(
            '(%g,%g)' % (i, j),
            point(x_, y_) + d,
            alignment='left',
            fontsize=8)
indices = Composition(dict(indices=Composition(indices)))

grid.draw()
indices.draw()
drawing_tool.display()
drawing_tool.savefig('tmp2')

raw_input()
