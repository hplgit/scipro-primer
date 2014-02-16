import sys, time
import numpy as np
import random

def dice6_py(N, ndice, nsix):
    M = 0                     # no of successful events
    for i in range(N):        # repeat N experiments
        six = 0               # how many dice with six eyes?
        for j in range(ndice):
            r = random.randint(1, 6)  # roll die no. j
            if r == 6:
               six += 1
        if six >= nsix:       # successful event?
            M += 1
    p = float(M)/N
    return p

def dice6_vec1(N, ndice, nsix):
    eyes = np.random.random_integers(1, 6, size=(N, ndice))
    compare = eyes == 6
    throws_with_6 = np.sum(compare, axis=1)  # sum over columns
    nsuccesses = throws_with_6 >= nsix
    M = np.sum(nsuccesses)
    p = float(M)/N
    return p

def dice6_vec2(N, ndice, nsix):
    eyes = np.random.random_integers(1, 6, (N, ndice))
    six = [6 for i in range(ndice)]
    M = 0
    for i in range(N):
        # Check experiment no. i:
        compare = eyes[i,:] == six
        if np.sum(compare) >= nsix:
            M += 1
    p = float(M)/N
    return p


def experiment_with_N_for_small_probabilities():
    """
    Choose ndice=nix (analytical result) and investigate
    how the accuracy depends on the no of MC simulations (N).
    """
    def exact(ndice):
        return 6.0**(-ndice)

    e = [None]*3
    for ndice in 3, 4, 5:
        e.append({})
        for k in 3, 4, 5, 6:
            N = 10**k
            repetitions = 25
            t0 = time.clock()
            e[ndice][N] = [dice6_py(N, ndice, ndice) \
                           for j in range(repetitions)]
            t1 = time.clock()
            cpu = (t1 - t0)/float(repetitions)
            p = e[ndice][N]
            print '%d dice, N=10^%d, mean=%.5f, stdev=%.2e, exact=%.5f, time=%.1f s' % (ndice, k, np.mean(p), np.std(p), exact(ndice), cpu)

if __name__ == '__main__':
    N = int(sys.argv[1])
    ndice = 6
    nsix =3

    vary_N_ndice()
