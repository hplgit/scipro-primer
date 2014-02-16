import numpy as np

def integral(g, a, x, N=20):
    index_set = range(N+1)
    x = np.linspace(a, x, N+1)
    g_ = np.zeros_like(x)
    f = np.zeros_like(x)
    g_[0] = g(x[0])
    f[0] = 0

    for n in index_set[1:]:
        g_[n] = g(x[n])
        f[n] = f[n-1] + 0.5*(x[n] - x[n-1])*(g_[n-1] + g_[n])
    return x, f

def _verify():
    """
    Check that the trapezoidal method implemented
    via difference equations works perfectly with linear g.
    """
    def g_test(t):
        """Linear integrand."""
        return 2*t + 1

    def f_test(x, a):
        """Exact integral of g_test."""
        return x**2 + x - (a**2 + a)


    a = 2
    x, f = integral(g_test, a, x=10)
    f_exact = f_test(x, a)
    if not np.allclose(f_exact, f):
        print 'ERROR in _verify'

def application1():
    """Integrate the Gaussian function."""

    from numpy import sqrt, pi, exp
    def g(t):
        return 1./sqrt(2*pi)*exp(-t**2)

    x, f = integral(g, a=-3, x=3, N=200)
    integrand = g(x)
    from scitools.std import plot
    plot(x, f, 'r-',
         x, integrand, 'y-',
         legend=('f', 'g'),
         legend_loc='upper left',
         savefig='tmp.eps')

_verify()
application1()

