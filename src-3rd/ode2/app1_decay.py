from scitools.std import *
import ODESolver

def f(u, t):
    return -u

solver = ODESolver.ForwardEuler(f)
solver.set_initial_condition(1.0)
t_points = linspace(0, 3, 31)
u, t = solver.solve(t_points)
plot(t, u)

# Test various dt values and plot
figure()
T = 3
for dt in 2.0, 1.0, 0.5, 0.1:
    n = int(round(T/dt))
    solver = ODESolver.ForwardEuler(f)
    solver.set_initial_condition(1)
    u, t = solver.solve(linspace(0, T, n+1))
    plot(t, u, legend='dt=%g' % dt)
    hold('on')
plot(t, exp(-t), 'bo', legend='exact')
savefig('tmp_decay1.eps')

# Test ForwardEuler vs RungeKutta4
T = 3
dt = 0.5
n = int(round(T/dt))
t_points = linspace(0, T, n+1)
figure()
for solver_class in ODESolver.RungeKutta4, ODESolver.ForwardEuler:
    solver = solver_class(f)
    solver.set_initial_condition(1)
    u, t = solver.solve(t_points)
    plot(t, u, legend='%s' % solver_class.__name__)
    hold('on')
plot(t, exp(-t), 'bo', legend='exact')
savefig('tmp_decay2.eps')

# Test various dt values for RungeKutta4
figure()
T = 3
for dt in 2.0, 1.0, 0.5, 0.1:
    n = int(round(T/dt))
    solver = ODESolver.RungeKutta4(f)
    solver.set_initial_condition(1)
    u, t = solver.solve(linspace(0, T, n+1))
    plot(t, u, legend='dt=%g' % dt)
    hold('on')
plot(t, exp(-t), 'bo', legend='exact')
savefig('tmp_decay3.eps')

show()
