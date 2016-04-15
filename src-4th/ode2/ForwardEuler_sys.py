"""
Class implementing the Forward Euler method for scalar ODEs
and systems of ODEs.
"""

import numpy as np

class ForwardEuler(object):
    """
    Class for solving a scalar of vector ODE,

      du/dt = f(u, t)

    by the ForwardEuler solver.

    Class attributes:
    t: array of time values
    u: array of solution values (at time points t)
    k: step number of the most recently computed solution
    f: callable object implementing f(u, t)
    """
    def __init__(self, f):
        if not callable(f):
            raise TypeError('f is %s, not a function' % type(f))
        self.f = lambda u, t: np.asarray(f(u, t))

    def set_initial_condition(self, U0):
        if isinstance(U0, (float,int)):  # scalar ODE
            self.neq = 1
        else:                            # system of ODEs
            U0 = np.asarray(U0)
            self.neq = U0.size
        self.U0 = U0

    def solve(self, time_points):
        """Compute u for t values in time_points list."""
        self.t = np.asarray(time_points)
        n = self.t.size
        if self.neq == 1:  # scalar ODEs
            self.u = np.zeros(n)
        else:              # systems of ODEs
            self.u = np.zeros((n,self.neq))

        # Assume self.t[0] corresponds to self.U0
        self.u[0] = self.U0

        # Time loop
        for k in range(n-1):
            self.k = k
            self.u[k+1] = self.advance()
        return self.u, self.t

    def advance(self):
        """Advance the solution one time step."""
        u, f, k, t = self.u, self.f, self.k, self.t
        dt = t[k+1] - t[k]
        u_new = u[k] + dt*f(u[k], t[k])
        return u_new


def demo(T=8*np.pi, n=200):
    f = lambda u, t: [u[1], -u[0]]
    U0 = [0, 1]
    solver = ForwardEuler(f)
    solver.set_initial_condition(U0)
    time_points = np.linspace(0, T, n+1)
    u, t = solver.solve(time_points)
    u0 = u[:,0]

    # Plot u0 and compare with exact solution sin(t)
    from matplotlib.pyplot import plot, show, savefig, legend
    plot(t, u0, 'r-', t, np.sin(t), 'b--')
    legend(['ForwardEuler, n=%d' % n, 'exact'], loc='upper left')
    savefig('tmp.pdf')
    show()
