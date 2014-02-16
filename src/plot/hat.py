"""Different vectorized versions of a hat function."""

import numpy as np

def N(x):
    if x < 0:
        return 0.0
    elif 0 <= x < 1:
        return x
    elif 1 <= x < 2:
        return 2 - x
    elif x >= 2:
        return 0.0

def N_loop(x):
    r = np.zeros(len(x))
    for i in xrange(len(x)):
        r[i] = N(x[i])
    return r

N_vec = np.vectorize(N)
N_vec.func_name = 'N_vec'  # must be set manually

def Nv1(x):
    condition1 = x < 0
    condition2 = np.logical_and(0 <= x, x < 1)
    condition3 = np.logical_and(1 <= x, x < 2)
    condition4 = x >= 2

    r = np.where(condition1, 0.0, 0.0)
    r = np.where(condition2, x,   r)
    r = np.where(condition3, 2-x, r)
    r = np.where(condition4, 0.0, r)
    return r

def Nv2(x):
    condition1 = x < 0
    condition2 = np.logical_and(0 <= x, x < 1)
    condition3 = np.logical_and(1 <= x, x < 2)
    condition4 = x >= 2

    r = np.zeros(len(x))
    r[condition1] = 0.0
    r[condition2] = x[condition2]
    r[condition3] = 2-x[condition3]
    r[condition4] = 0.0
    return r

funcs = [N_loop, N_vec, Nv1, Nv2]
n = 1000000
x = np.linspace(-2, 4, n+1)
selected_index = n/2
import time
timings = {}
testvalues = {}
for func in funcs:
    name = func.func_name
    t0 = time.clock()
    r = func(x)
    t1 = time.clock()
    testvalues[name] = r[selected_index]
    timings[name] = t1 - t0

from scitools.misc import hardware_info
import pprint; pprint.pprint(hardware_info())
pprint.pprint(timings)

# Test that the results are correct
exact = N(x[selected_index])
right = [testvalues[name] == exact for name in testvalues]
if right != [True]*len(right):
    print 'exact test:', exact, 'testvalues:', testvalues




