import ODESolver
from scitools.std import plot, figure, savefig, title, show
#from matplotlib.pyplot import plot, figure, savefig, title, show
import numpy as np

class Problem(object):
    def __init__(self, alpha, R, U0, T):
        """
        alpha, R: parameters in the ODE.
        U0: initial condition.
        T: max length of time interval for integration;
        asympotic value R must be reached within 1%
        accuracy for some t <= T.
        """
        self.alpha, self.R, self.U0, self.T = alpha, R, U0, T

    def __call__(self, u, t):
        """Return f(u,t) for logistic ODE."""
        return self.alpha*u*(1 - u/self.R)

    def terminate(self, u, t, step_no):
        """Return True when asymptotic value R is reached."""
        tol = self.R*0.01
        return abs(u[step_no] - self.R) < tol

    def __str__(self):
        """Pretty print of physical parameters."""
        return 'alpha=%g, R=%g, U0=%g' % \
               (self.alpha, self.R, self.U0)

class Solver(object):
    def __init__(self, problem, dt,
                 method=ODESolver.ForwardEuler):
        """
        problem: instance of class Problem.
        dt: time step.
        method: class in ODESolver hierarchy.
        """
        self.problem, self.dt = problem, dt
        self.solver = method

    def solve(self):
        solver = self.method(self.problem)
        solver.set_initial_condition(self.problem.U0)
        n = int(round(self.problem.T/self.dt))
        t_points = np.linspace(0, self.problem.T, n+1)
        self.u, self.t = solver.solve(t_points,
                                      self.problem.terminate)

        # The solution terminated if the limiting value was reached
        if solver.k+1 == n:  # no termination - we reached final T
            self.plot()
            raise ValueError(
                'termination criterion not reached, '\
                'give T > %g' % self.problem.T)

    def plot(self):
        filename = 'logistic_' + str(self.problem) + '.pdf'
        plot(self.t, self.u)
        title(str(self.problem) + ', dt=%g' % self.dt)
        savefig(filename)
        show()

def demo1():
    problem = Problem(alpha=0.1, R=500, U0=2, T=130)
    solver = Solver(problem, dt=1.)
    solver.solve()
    solver.plot()

def find_dt(problem, method=ODESolver.ForwardEuler,
            tol=0.01, dt_min=1E-6):
    """
    Return a "solved" class Solver instance where the
    difference in the solution and one with a double
    time step is less than tol.

    problem: class Problem instance.
    method: class in ODESolver hierarchy.
    tol: tolerance (chosen relative to problem.R).
    dt_min: minimum allowed time step.
    """
    dt = problem.T/10  # start with 10 intervals
    solver = Solver(problem, dt, method)
    solver.solve()
    from scitools.std import wrap2callable

    good_approximation = False
    while not good_approximation:
        dt = dt/2.0
        if dt < dt_min:
            raise ValueError('dt=%g < %g - abort' % (dt, dt_min))

        solver2 = Solver(problem, dt, method)
        solver2.solve()

        # Make continuous functions u(t) and u2(t)
        u  = wrap2callable((solver. t, solver. u))
        u2 = wrap2callable((solver2.t, solver2.u))

        # Sample the difference in n points in [0, t_end]
        n = 13
        t_end = min(solver2.t[-1], solver.t[-1])
        t = np.linspace(0, t_end, n)
        u_diff = np.abs(u(t) - u2(t)).max()
        print u_diff, dt, tol
        if u_diff < tol:
            good_approximation = True
        else:
            solver = solver2
    return solver2

def demo2():
    problem = Problem(alpha=0.1, R=500, U0=2, T=130)
    solver = find_dt(problem, method=ODESolver.RungeKutta4, tol=1)
    print 'dt:', solver.dt
    solver.plot()

class AutoSolver(Solver):
    def __init__(self, problem, dt=None,
                 method=ODESolver.ForwardEuler,
                 tol=0.01, dt_min=1E-6):
        Solver.__init__(self, problem, dt, method)
        if dt is None:
            solver = find_dt(self.problem, method,
                             tol, dt_min)
            self.dt = solver.dt
            self.u, self.t = solver.u, solver.t

    def solve(self, method=ODESolver.ForwardEuler):
        if hasattr(self, 'u'):
            # Solution was computed by find_dt in constructor
            pass
        else:
            Solver.solve(self)

def demo3():
    problem = Problem(alpha=0.1, R=500, U0=2, T=130)
    solver = AutoSolver(problem, tol=1)
    solver.solve(method=ODESolver.RungeKutta4)
    print 'dt:', solver.dt
    solver.plot()


class Problem2(Problem):
    def __init__(self, alpha, R, U0, T):
        """
        alpha, R: parameters in the ODE.
        U0: initial condition.
        T: max length of time interval for integration;
        asympotic value R must be reached within 1%
        accuracy for some t <= T.
        """
        self.alpha, self.U0, self.T = alpha, U0, T
        if isinstance(R, (float,int)):  # number?
            self.R = lambda t: R
        elif callable(R):
            self.R = R
        else:
            raise TypeError(
                'R is %s, has to be number of function' % type(R))

    def __call__(self, u, t):
        """Return f(u,t) for logistic ODE."""
        return self.alpha*u*(1 - u/self.R(t))

    def terminate(self, u, t, step_no):
        """Return True when asymptotic value R is reached."""
        tol = self.R(t[step_no])*0.01
        return abs(u[step_no] - self.R(t[step_no])) < tol

    def __str__(self):
        return 'alpha=%g, U0=%g' % (self.alpha, self.U0)

def demo4():
    problem = Problem2(alpha=0.1, U0=2, T=130,
                       R=lambda t: 500 if t < 60 else 100)
    solver = AutoSolver(problem, tol=1)
    solver.solve(method=ODESolver.RungeKutta4)
    print 'dt:', solver.dt
    solver.plot()


from scitools.std import StringFunction

class Problem3(Problem):
    def __init__(self):
        # Set default parameter values
        self.alpha = 1.
        self.R = StringFunction('1.0', independent_variable='t')
        self.U0 = 0.01
        self.T = 4.

    def define_command_line_arguments(self, parser):
        """Add arguments to parser (argparse.ArgumentParser)."""

        def evalcmlarg(text):
            return eval(text)

        def toStringFunction(text):
            return StringFunction(text, independent_variable='t')

        parser.add_argument(
            '--alpha', dest='alpha', type=evalcmlarg,
            default=self.alpha,
            help='initial growth rate in logistic model')
        parser.add_argument(
            '--R', dest='R', type=toStringFunction, default=self.R,
            help='carrying capacity of the environment')
        parser.add_argument(
            '--U0', dest='U0', type=evalcmlarg, default=self.U0,
            help='initial condition')
        parser.add_argument(
            '--T', dest='T', type=evalcmlarg, default=self.T,
            help='integration in time interval [0,T]')
        return parser

    def set(self, **kwargs):
        """
        Set parameters as keyword arguments alpha, R, U0, or T,
        or as args (object returned by parser.parse_args()).
        """
        for prm in ('alpha', 'U0', 'R', 'T'):
            if prm in kwargs:
                setattr(self, prm, kwargs[prm])
        if 'args' in kwargs:
            args = kwargs['args']
            for prm in ('alpha', 'U0', 'R', 'T'):
                if hasattr(args, prm):
                    setattr(self, prm, getattr(args, prm))
                else:
                    print 'Really strange', dir(args)

    def __call__(self, u, t):
        """Return f(u,t) for logistic ODE."""
        return self.alpha*u*(1 - u/self.R(t))

    def terminate(self, u, t, step_no):
        """Return True when asymptotic value R is reached."""
        tol = self.R(t[step_no])*0.01
        return abs(u[step_no] - self.R(t[step_no])) < tol

    def __str__(self):
        s = 'alpha=%g, U0=%g' % (self.alpha, self.U0)
        if isinstance(self.R, StringFunction):
            s += ', R=%s' % str(self.R)
        return s

def demo5():
    problem = Problem3()
    import argparse
    parser = argparse.ArgumentParser(
        description='Logistic ODE model')
    parser = problem.define_command_line_arguments(parser)

    # Try first with manual settings
    problem.set(alpha=0.1, U0=2, T=130,
                R=lambda t: 500 if t < 60 else 100)
    solver = AutoSolver(problem, tol=1)
    solver.solve(method=ODESolver.RungeKutta4)
    print 'dt:', solver.dt
    solver.plot()

    # New example with data from the command line
    # Try --alpha 0.11 --T 130 --U0 2 --R '500 if t < 60 else 300'
    args = parser.parse_args()
    problem.set(args=args)
    print problem.alpha, problem.R, problem.U0, problem.T
    solver = AutoSolver(problem, tol=1)
    solver.solve(method=ODESolver.RungeKutta4)
    print 'dt:', solver.dt
    figure()
    solver.plot()


if __name__ == '__main__':
    demo5()
