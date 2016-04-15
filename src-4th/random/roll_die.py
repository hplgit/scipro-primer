import random

def six_eyes(N):
    M = 0                  # no of times we get 6 eyes
    for i in xrange(N):
        outcome = random.randint(1, 6)
        if outcome == 6:
            M += 1
    return float(M)/N

import numpy as np

def six_eyes_vec(N):
    eyes = np.random.randint(1, 7, N)
    success = eyes == 6     # True/False array
    M = np.sum(success)     # treats True as 1, False as 0
    return float(M)/N

def six_eyes_vec2(N, arraysize=1000000):
    # Split all experiments into batches of size arraysize,
    # plus a final batch of size rest
    # (note: N//arraysize is integer division)
    rest = N % arraysize
    batch_sizes = [arraysize]*(N//arraysize) + [rest]

    M = 0
    for batch_size in batch_sizes:
        eyes = np.random.randint(1, 7, batch_size)
        success = eyes == 6      # True/False array
        M += np.sum(success)     # treats True as 1, False as 0
    return float(M)/N

def test_scalar():
    random.seed(3)
    f = six_eyes(100)
    f_exact = 0.26
    assert abs(f_exact - f) < 1E-15

def test_all():
    # Use np.random as random number generator for all three
    # functions and make sure all of them applies the same seed
    N = 100
    arraysize = 40
    random.randint = lambda a, b: np.random.randint(a, b+1, 1)[0]
    tol = 1E-15

    np.random.seed(3)
    f_scalar = six_eyes(N)
    np.random.seed(3)
    f_vec = six_eyes_vec(N)
    assert abs(f_scalar - f_vec) < tol

    np.random.seed(3)
    f_vec2 = six_eyes_vec2(N, arraysize=80)
    assert abs(f_vec - f_vec2) < tol

if __name__ == '__main__':
    import sys
    try:
        N = int(sys.argv[1])   # perform N experiments
        version = sys.argv[2]
    except:
        print '%s N scalar|vec|vec2' % sys.argv[0]
        sys.exit(1)
    if version == 'scalar':
        f = six_eyes(N)
        print f
    elif version == 'vec':
        f = six_eyes_vec(N)
        print f
    elif version == 'vec2':
        f = six_eyes_vec2(N)
        print f
    elif version == 'verify':
        test_all()




