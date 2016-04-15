@profile
def axpy1(a, x, y, dummy=None):
    r = a*x + y
    return r

@profile
def axpy2(a, x, y, r):
    r[:] = x
    r *= a
    r += y
    return r

@profile
def axpy3(a, x, y, r):
    r[:] = x
    r *= a
    r += y

@profile
def axpy4(a, x, y, r):
    r[:] = x
    r[:] *= a
    r[:] += y
    return r

@profile
def axpy_loop(a, x, y, r):
    for i in range(r.size):
        r[i] = a*x[i] + y[i]
    return r

@profile
def axpy_loop_newr(a, x, y, dummy=None):
    r = np.zeros_like(x)
    for i in range(r.size):
        r[i] = a*x[i] + y[i]
    return r

def demo():
    x = np.linspace(0, 1, 11)
    y = np.zeros_like(x)
    a = 2
    # Classical y <- a*x + y
    y = axpy2(a, x, y, y)
    # Result in separate array
    r = np.zeros_like(x)
    r = axpy2(a, x, y, r)

def effect_of_vec():
    n_values = []
    speed_ups = []
    for k in range(4, 22, 2):
        n = 2**k
        x = np.linspace(0, 1, n)
        y = x.copy()
        a = 2.3
        t0 = time.clock()
        r = axpy_loop(a, x, y, np.zeros_like(x))
        t1 = time.clock()
        r = axpy1(a, x, y)
        t2 = time.clock()
        n_values.append(n)
        f = float(t1-t0)/(t2-t1)
        speed_ups.append(f)
        print 'n:', n, 'speed up:', f
    import matplotlib.pyplot as plt
    plt.semilogx(n_values, speed_ups, 'ro')
    plt.xlabel('array length')
    plt.ylabel('speed up')
    plt.savefig('tmp.png'); plt.savefig('tmp.pdf')
    print speed_ups


def investigate_efficiency(array_size=1000000, num_repetitions=10):
    x = np.linspace(0, 1, array_size+1)
    #y = x.copy()
    r = np.zeros_like(x)
    funcs = [eval('axpy' + str(i)) for i in range(1,4)] + \
            [axpy_loop, axpy_loop_newr]
    for func in funcs:
        if array_size > 500000 and 'loop' in func.__name__:
            # Drop scalar implemenation for large arrays
            continue

        print func.__name__,
        r_id = id(r)
        changed_r_id = False
        t0 = time.clock()
        for i in range(num_repetitions):
            value = func(a, x, r, r)
            if value is not None:
                r = value
            if id(r) != r_id:
                changed_r_id = True
        t1 = time.clock()
        print 'changed id(r)' if changed_r_id else 'same id(r)',
        print 'cpu: %.3g' % (t1-t0)
    print

import numpy as np
import time
a = 3.5
n = 1000000

def test_axpy():
    a = 3.2
    x = np.array([1, 4.5])
    y = x + 1
    r = np.zeros_like(x)
    expected = a*x + y
    tol = 1E-15
    funcs = [eval('axpy' + str(i)) for i in range(1,4)] + \
            [axpy_loop, axpy_loop_newr]
    for func in funcs:
        computed = func(a, x, y, r)
        if computed is None:
            computed = r
        assert np.abs(expected - computed).max() < tol

import sys
#test_axpy()
#effect_of_vec()
#sys.exit(1)
#investigate_efficiency(10000000, 3)
investigate_efficiency(500000, 3)


'''
Terminal> python -m memory_profiler test1.py
axpy1 changed id(r) cpu: 0.157
axpy2 same id(r) cpu: 0.0875
axpy3 same id(r) cpu: 0.0885
axpy4 same id(r) cpu: 0.0992
axpy1 changed id(r) cpu: 0.00112
axpy2 same id(r) cpu: 0.00124
axpy3 same id(r) cpu: 0.00119
axpy4 same id(r) cpu: 0.000903
axpy_loop same id(r) cpu: 4.1
axpy_loop_newr changed id(r) cpu: 3.97

Filename: test1.py

Line #    Mem usage    Increment   Line Contents
================================================
     7  175.527 MiB    0.000 MiB   @profile
     8                             def axpy2(a, x, y, r):
     9                                 """In-place computation in r."""
    10  175.527 MiB    0.000 MiB       r[:] = x
    11  175.527 MiB    0.000 MiB       r *= a
    12  175.527 MiB    0.000 MiB       r += y
    13  175.527 MiB    0.000 MiB       return r


Filename: test1.py

Line #    Mem usage    Increment   Line Contents
================================================
    30   23.281 MiB    0.000 MiB   @profile
    31                             def axpy_loop(a, x, y, r):
    32                                 """Classical scalar loop implementation."""
    33   23.281 MiB    0.000 MiB       for i in range(r.size):
    34   23.281 MiB    0.000 MiB           r[i] = a*x[i] + y[i]
    35   23.281 MiB    0.000 MiB       return r


Filename: test1.py

Line #    Mem usage    Increment   Line Contents
================================================
     1  251.824 MiB    0.000 MiB   @profile
     2                             def axpy1(a, x, y, dummy=None):
     3                                 """Standard numpy expression."""
     4  328.121 MiB   76.297 MiB       r = a*x + y
     5  328.121 MiB    0.000 MiB       return r


Filename: test1.py

Line #    Mem usage    Increment   Line Contents
================================================
    37   23.422 MiB    0.000 MiB   @profile
    38                             def axpy_loop_newr(a, x, y, dummy=None):
    39                                 """As axpy_loop, but allocate return array."""
    40   23.422 MiB    0.000 MiB       r = np.zeros_like(x)
    41   23.422 MiB    0.000 MiB       for i in range(r.size):
    42   23.422 MiB    0.000 MiB           r[i] = a*x[i] + y[i]
    43   23.422 MiB    0.000 MiB       return r


Filename: test1.py

Line #    Mem usage    Increment   Line Contents
================================================
    15  175.527 MiB    0.000 MiB   @profile
    16                             def axpy3(a, x, y, r):
    17                                 """In-place computation in r."""
    18  175.527 MiB    0.000 MiB       r[:] = x
    19  175.527 MiB    0.000 MiB       r[:] *= a
    20  175.527 MiB    0.000 MiB       r[:] += y
    21  175.527 MiB    0.000 MiB       return r


Filename: test1.py

Line #    Mem usage    Increment   Line Contents
================================================
    23  175.527 MiB    0.000 MiB   @profile
    24                             def axpy4(a, x, y, r):
    25                                 """In-place computation in r, but no return."""
    26  175.527 MiB    0.000 MiB       r[:] = x
    27  175.527 MiB    0.000 MiB       r *= a
    28  175.527 MiB    0.000 MiB       r += y


Terminal> kernprof -l -v test1.py

axpy1 changed id(r) cpu: 0.148
axpy2 same id(r) cpu: 0.0855
axpy3 same id(r) cpu: 0.0859
axpy4 same id(r) cpu: 0.0918

axpy1 changed id(r) cpu: 0.000132
axpy2 same id(r) cpu: 5.6e-05
axpy3 same id(r) cpu: 5.3e-05
axpy4 same id(r) cpu: 4.9e-05
axpy_loop same id(r) cpu: 0.036
axpy_loop_newr changed id(r) cpu: 0.0376

Wrote profile results to test1.py.lprof
Timer unit: 1e-06 s

Total time: 0.149182 s
File: test1.py
Function: axpy1 at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def axpy1(a, x, y, dummy=None):
     3                                               """Standard numpy expression."""
     4        12       149156  12429.7    100.0      r = a*x + y
     5        12           26      2.2      0.0      return r

Total time: 0.085663 s
File: test1.py
Function: axpy2 at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           @profile
     8                                           def axpy2(a, x, y, r):
     9                                               """In-place computation in r."""
    10         6        29527   4921.2     34.5      r[:] = x
    11         6        27759   4626.5     32.4      r *= a
    12         6        28367   4727.8     33.1      r += y
    13         6           10      1.7      0.0      return r

Total time: 0.085965 s
File: test1.py
Function: axpy3 at line 15

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    15                                           @profile
    16                                           def axpy3(a, x, y, r):
    17                                               """In-place computation in r."""
    18         6        29345   4890.8     34.1      r[:] = x
    19         6        27875   4645.8     32.4      r[:] *= a
    20         6        28737   4789.5     33.4      r[:] += y
    21         6            8      1.3      0.0      return r

Total time: 0.093952 s
File: test1.py
Function: axpy4 at line 23

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    23                                           @profile
    24                                           def axpy4(a, x, y, r):
    25                                               """In-place computation in r, but no return."""
    26         6        37124   6187.3     39.5      r[:] = x
    27         6        28624   4770.7     30.5      r *= a
    28         6        28204   4700.7     30.0      r += y

Total time: 0.025614 s
File: test1.py
Function: axpy_loop at line 30

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    30                                           @profile
    31                                           def axpy_loop(a, x, y, r):
    32                                               """Classical scalar loop implementation."""
    33     27006         7785      0.3     30.4      for i in range(r.size):
    34     27003        17827      0.7     69.6          r[i] = a*x[i] + y[i]
    35         3            2      0.7      0.0      return r

Total time: 0.024221 s
File: test1.py
Function: axpy_loop_newr at line 37

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    37                                           @profile
    38                                           def axpy_loop_newr(a, x, y, dummy=None):
    39                                               """As axpy_loop, but allocate return array."""
    40         3           67     22.3      0.3      r = np.zeros_like(x)
    41     27006         7284      0.3     30.1      for i in range(r.size):
    42     27003        16868      0.6     69.6          r[i] = a*x[i] + y[i]
    43         3            2      0.7      0.0      return r


'''
