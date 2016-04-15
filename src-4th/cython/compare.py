import sys, os, time

def run_experiments(N, ndice, nsix):
    # Pure Python versions
    from dice6 import dice6_py, dice6_vec1, dice6_vec2
    # Try to import compiled versions
    try:
        from _dice6_cy import dice6_cy1, dice6_cy2, dice6_cy3
        from _dice6_c1 import dice6 as dice6_c_f2py
        from _dice6_c2 import dice6_cwrap as dice6_c_cy
    except ImportError:
        raise ImportError('Extension modules needs to be built. Run make.sh!')

    # Benchmark the various methods
    from scitools.misc import hardware_info
    import pprint; pprint.pprint(hardware_info())
    timings = {}

    t0 = time.clock()
    p = dice6_cy2(N, ndice, nsix)
    t1 = time.clock()
    timings['Cython numpy.random'] = t1-t0
    print '\n\nLoops in Cython with numpy.random: ', t1-t0, p

    t0 = time.clock()
    p = dice6_cy3(N, ndice, nsix)
    t1 = time.clock()
    timings['Cython stdlib.rand'] = t1-t0
    print '\n\nLoops in Cython with stdlib.rand: ', t1-t0, p

    t0 = time.clock()
    p = dice6_c_f2py(N, ndice, nsix)
    t1 = time.clock()
    timings['C via f2py'] = t1-t0
    print 'Loops in C, interfaced via f2py        ', t1-t0, p

    t0 = time.clock()
    p = dice6_c_cy(N, ndice, nsix)
    t1 = time.clock()
    timings['C via Cython'] = t1-t0
    print 'Loops in C, interfaced via Cython      ', t1-t0, p

    capp = './dice6.capp'
    if not os.path.isfile(capp):
        raise Exception('stand-alone C program is not compiled!')
    t0 = time.time()
    os.system('time %s %d' % (capp, N))
    t1 = time.time()
    timings['C program'] = t1-t0
    print 'Loops in C, stand-alone C program      %.2f' % (t1-t0)

    t0 = time.clock()
    p = dice6_py(N, ndice, nsix)
    t1 = time.clock()
    timings['Python, plain'] = t1-t0
    print 'Loops in Python:                   ', t1-t0, p

    t0 = time.clock()
    p = dice6_vec1(N, ndice, nsix)
    t1 = time.clock()
    timings['Python, vectorized v1'] = t1-t0
    print 'Vectorized Python v1:              ', t1-t0, p

    t0 = time.clock()
    p = dice6_vec2(N, ndice, nsix)
    t1 = time.clock()
    timings['Python, vectorized v2'] = t1-t0
    print 'Vectorized Python v2:              ', t1-t0, p

    t0 = time.clock()
    p = dice6_cy1(N, ndice, nsix)
    t1 = time.clock()
    timings['Cython random.randint'] = t1-t0
    print 'Loops in Cython with random.randint:', t1-t0, p

    cpu_best = min([timings[m] for m in timings])
    for method in timings:
        print '%s: %.2f' % (method, timings[method]/cpu_best)


    # Profiling of dice6_cy1
    print '\n\n'
    import cProfile, pstats
    cProfile.runctx('dice6_cy1(N, ndice, nsix)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof')
    s.strip_dirs().sort_stats('time').print_stats(30)


"""
N=600,000
Cython numpy.random: 1.57
Cython random.randint: 45.00
C via f2py: 1.57
C program: 1.00
Python, vectorized v1: 1.57
Python, vectorized v2: 131.42
Python, plain: 46.81
C via Cython: 1.57

N=450,000
Cython numpy.random: 1.22
Cython random.randint: 33.65
C via f2py: 2.08
C program: 1.00
Python, vectorized v1: 1.92
Python, vectorized v2: 105.26
Python, plain: 37.70
Cython stdlib.rand: 1.17
C via Cython: 1.28

Numbers change *a lot* from experiment to experiment.
"""

if __name__ == '__main__':
    N = int(sys.argv[1])
    ndice = 6
    nsix =3
    run_experiments(N, ndice, nsix)
    # Suitable N on MacBook Air 11'' 4 Gb memory is 600,000
    # (don't choose a too large N that gets the machine too exhausted)
