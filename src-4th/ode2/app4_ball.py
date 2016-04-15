"""Solve an ODE system for the trajectory of a ball."""

import ODESolver
from scitools.std import *
#from matplotlib.pyplot import *

def f(u, t):
    x, vx, y, vy = u
    g = 9.81
    return [vx, 0, vy, -g]

v0 = 5
theta = 80*pi/180
U0 = [0, v0*cos(theta), 0, v0*sin(theta)]
T = 1.2; dt = 0.01; n = int(round(T/dt))
solver = ODESolver.ForwardEuler(f)
solver.set_initial_condition(U0)

def terminate(u, t, step_no):
    y = u[:,2]                   # all the y coordinates
    return y[step_no] < 0

u, t = solver.solve(linspace(0, T, n+1), terminate)
x = u[:,0]  # or array([x for x, vx, y, vy in u])
y = u[:,2]  # or array([y for x, vx, y, vy in u])

def exact(x):
    g = 9.81
    y0 = U0[2]  # get y0 from the initial values
    return x*tan(theta) - g*x**2/(2*v0**2)*1/(cos(theta))**2 + y0

plot(x, y, 'r', x, exact(x), 'b')
legend(('numerical', 'exact'))
title('dt=%g' % dt)
savefig('tmp_ball.pdf')
show()
