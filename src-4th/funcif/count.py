def count_v1(dna, base):
    dna = list(dna)  # convert string to list of letters
    i = 0            # counter
    for c in dna:
        if c == base:
            i += 1
    return i

def count_v2(dna, base):
    i = 0 # counter
    for c in dna:
        if c == base:
            i += 1
    return i

dna = 'ATGCGGACCTAT'
base = 'C'
n = count_v2(dna, base)

# printf-style formatting
print '%s appears %d times in %s' % (base, n, dna)

# or (new) format string syntax
print '{base} appears {n} times in {dna}'.format(
    base=base, n=n, dna=dna)

def count_v2_demo(dna, base):
    print 'dna:', dna
    print 'base:', base
    i = 0 # counter
    for c in dna:
        print 'c:', c
        if c == base:
            print 'True if test'
            i += 1
    return i

n = count_v2_demo('ATGCGGACCTAT', 'C')

def count_v3(dna, base):
    i = 0 # counter
    for j in range(len(dna)):
        if dna[j] == base:
            i += 1
    return i

def count_v4(dna, base):
    i = 0 # counter
    j = 0 # string index
    while j < len(dna):
        if dna[j] == base:
            i += 1
        j += 1
    return i


def count_v5(dna, base):
    m = []   # matches for base in dna: m[i]=True if dna[i]==base
    for c in dna:
        if c == base:
            m.append(True)
        else:
            m.append(False)
    return sum(m)

def count_v6(dna, base):
    m = []   # matches for base in dna: m[i]=True if dna[i]==base
    for c in dna:
        m.append(True if c == base else False)
    return sum(m)

def count_v7(dna, base):
    m = []   # matches for base in dna: m[i]=True if dna[i]==base
    for c in dna:
        m.append(c == base)
    return sum(m)

def count_v8(dna, base):
    m = [c == base for c in dna]
    return sum(m)

def count_v9(dna, base):
    return sum([c == base for c in dna])

def count_v10(dna, base):
    return sum(c == base for c in dna)

def count_v11(dna, base):
    return len([i for i in range(len(dna)) if dna[i] == base])

def count_v12(dna, base):
    return dna.count(base)

def compare_efficiency():
    import random

    def generate_string(N, alphabet='ACGT'):
        return ''.join([random.choice(alphabet) for i in xrange(N)])

    dna = generate_string(600000)
    #dna = generate_string(6000000)

    import time
    functions = [count_v1, count_v2, count_v3, count_v4,
                 count_v5, count_v6, count_v7, count_v8,
                 count_v9, count_v10, count_v11, count_v12]
    timings = []  # timings[i] holds CPU time for functions[i]

    for function in functions:
        t0 = time.clock()
        function(dna, 'A')
        t1 = time.clock()
        cpu_time = t1 - t0
        timings.append(cpu_time)

    for cpu_time, function in zip(timings, functions):
        print '{f:<9s}: {cpu:.2f} s'.format(
            f=function.func_name, cpu=cpu_time)

    # Time count_v12 better: repeat 100 times because it's so fast
    t0 = time.clock()
    for i in range(100):
        count_v12(dna, 'A')
    t1 = time.clock()
    print '{f:<9s}: {cpu:.2e} s'.format(
        f='count_v12', cpu=(t1-t0)/100.)

def test_count_all():
    dna = 'ATTTGCGGTCCAAA'
    expected = dna.count('A')

    functions = [count_v1, count_v2, count_v3, count_v4,
                 count_v5, count_v6, count_v7, count_v8,
                 count_v9, count_v10, count_v11, count_v12]
    for f in functions:
        success = f(dna, 'A') == expected
        msg = '%s failed' % f.__name__
        assert success, msg

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == 'verify':
        test_count_all()
    elif len(sys.argv) >= 2 and sys.argv[1] == 'efficiency':
        compare_efficiency()
