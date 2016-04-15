import random

def MCint(f, a, b, n):
    s = 0
    for i in xrange(n):
        x = random.uniform(a, b)
        s += f(x)
    I = (float(b-a)/n)*s
    return I

import numpy as np

def MCint_vec(f, a, b, n):
    x = np.random.uniform(a, b, n)
    s = np.sum(f(x))
    I = (float(b-a)/n)*s
    return I

def MCint_vec2(f, a, b, n, arraysize=1000000):
    s = 0
    # Split sum into batches of size arraysize
    # + a sum of size rest (note: n//arraysize is integer division)
    rest = n % arraysize
    batch_sizes = [arraysize]*(n//arraysize) + [rest]
    for batch_size in batch_sizes:
        x = np.random.uniform(a, b, batch_size)
        s += np.sum(f(x))
    I = (float(b-a)/n)*s
    return I

def MCint2(f, a, b, n):
    s = 0
    # Store the intermediate integral approximations in an
    # array I, where I[k-1] corresponds to k function evals.
    I = np.zeros(n)
    for k in range(1, n+1):
        x = random.uniform(a, b)
        s += f(x)
        I[k-1] = (float(b-a)/k)*s
    return I

def MCint3(f, a, b, n, N=100):
    s = 0
    # Store every N intermediate integral approximations in an
    # array I and record the corresponding k value.
    I_values = []
    k_values = []
    for k in range(1, n+1):
        x = random.uniform(a, b)
        s += f(x)
        if k % N == 0:
            I = (float(b-a)/k)*s
            I_values.append(I)
            k_values.append(k)
    return k_values, I_values

def demo():
    def f1(x):
        return 2 + 3*x

    a = 1; b = 2; n = 1000000; N = 10000
    k, I = MCint3(f1, a, b, n, N)

    from scitools.std import plot
    error = 6.5 - np.array(I)
    plot(k, error, title='Monte Carlo integration',
         xlabel='n', ylabel='error', savefig='tmp.pdf')

def test_MCint_all():
    """Test MCint, MCint_vec, MCint_vec2."""
    # Let all functions use np.random
    global random
    random = np.random
    f = np.sin
    np.random.seed(30)
    I = MCint(f, 0, 2*np.pi, n=10)
    np.random.seed(30)
    I_vec = MCint_vec(f, 0, 2*np.pi, n=10)
    np.random.seed(30)
    I_vec2 = MCint_vec2(f, 0, 2*np.pi, n=10, arraysize=4)
    tol = 1E-15
    assert abs(I - I_vec)  < tol
    assert abs(I - I_vec2) < tol


if __name__ == '__main__':
    #demo()
    test_MCint_all()

