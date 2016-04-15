"""Function implementing the Forward Euler method for scalar ODEs."""
import numpy as np


def ForwardEuler(f_user, U0, T, n):
    """Solve u'=f(u,t), u(0)=U0, with n steps until t=T."""
    f = lambda u, t: np.asarray(f_user(u, t))
    t = np.zeros(n+1)
    if isinstance(U0, (float, int)):
        u = np.zeros(n+1)  # u[k] is the solution at time t[k]
    else:
        U0 = np.asarray(U0)
        neq = U0.size
        u = np.zeros((n+1, neq))

    u[0] = U0
    t[0] = 0
    dt = T/float(n)
    for k in range(n):
        t[k+1] = t[k] + dt
        u[k+1] = u[k] + dt*f(u[k], t[k])
    return u, t

def demo(T=8*np.pi, n=200):
    def f(u, t):
        return [u[1], -u[0]]

    U0 = [0, 1]
    u, t = ForwardEuler(f, U0, T, n)
    u0 = u[:,0]

    # Plot u0 vs t and compare with exact solution sin(t)
    from matplotlib.pyplot import plot, show, savefig, legend
    plot(t, u0, 'r-', t, np.sin(t), 'b--')
    legend(['ForwardEuler, n=%d' % n, 'exact'], loc='upper left')
    savefig('tmp.pdf')
    show()

if __name__ == '__main__':
    demo(T=8*np.pi, n=200)   # demonstrate growing amplitude
    demo(T=8*np.pi, n=2000)  # demonstrate that smaller dt helps
