import random

def mutate_v1(dna):
    dna_list = list(dna)
    mutation_site = random.randint(0, len(dna_list) - 1)
    dna_list[mutation_site] = random.choice(list('ATCG'))
    return ''.join(dna_list)

def get_base_frequencies_v2(dna):
        return {base: dna.count(base)/float(len(dna))
                for base in 'ATGC'}

def format_frequencies(frequencies):
    return ', '.join(['%s: %.2f' % (base, frequencies[base])
                      for base in frequencies])

dna = 'ACGGAGATTTCGGTATGCAT'
print 'Starting DNA:', dna
print format_frequencies(get_base_frequencies_v2(dna))

nmutations = 10000
for i in range(nmutations):
    dna = mutate_v1(dna)

print 'DNA after %d mutations:' % nmutations, dna
print format_frequencies(get_base_frequencies_v2(dna))

# Vectorized version

import numpy as np
# Use integers in random numpy arrays and map these
# to characters according to
i2c = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}

def mutate_v2(dna, N):
    dna = np.array(dna, dtype='c')  # array of characters
    mutation_sites = np.random.random_integers(
        0, len(dna) - 1, size=N)
    # Must draw bases as integers
    new_bases_i = np.random.random_integers(0, 3, size=N)
    # Translate integers to characters
    new_bases_c = np.zeros(N, dtype='c')
    for i in i2c:
        new_bases_c[new_bases_i == i] = i2c[i]
    dna[mutation_sites] = new_bases_c
    return ''.join(dna.tolist())

dna = mutate_v2(dna, nmutations)
print 'DNA after %d new mutations:' % nmutations, dna
print format_frequencies(get_base_frequencies_v2(dna))

def generate_string_v1(N, alphabet='ACGT'):
    return ''.join([random.choice(alphabet) for i in xrange(N)])

def generate_string_v2(N, alphabet='ACGT'):
    # Draw random integers 0,1,2,3 to represent bases
    dna_i = np.random.random_integers(0, 3, N)
    # Translate integers to characters
    dna = np.zeros(N, dtype='c')
    for i in i2c:
        dna[dna_i == i] = i2c[i]
    return ''.join(dna.tolist())

def time_mutate(dna_length, N, repetitions_v2=100):
    import time
    t0 = time.clock()
    dna = generate_string_v1(dna_length)
    t1 = time.clock()
    cpu_generate_v1 = t1 - t0
    print cpu_generate_v1

    t0 = time.clock()
    for i in range(repetitions_v2):
        dna = generate_string_v2(dna_length)
    t1 = time.clock()
    cpu_generate_v2 = (t1 - t0)/float(repetitions_v2)
    print cpu_generate_v2

    t0 = time.clock()
    for j in range(N):
        dna = mutate_v1(dna)
    t1 = time.clock()
    cpu_mutate_v1 = t1 - t0
    print cpu_mutate_v1

    t0 = time.clock()
    for i in range(repetitions_v2):
        dna = mutate_v2(dna, N)
    t1 = time.clock()
    cpu_mutate_v2 = (t1 - t0)/float(repetitions_v2)
    print cpu_mutate_v2

    print 'Scaled timings:'
    print 'generate_string_v1: %.2f, generate_string_v2: 1' % \
          (cpu_generate_v1/cpu_generate_v2)
    print 'mutate_v1: %.2f, mutate_v2: 1' % \
          (cpu_mutate_v1/cpu_mutate_v2)

#time_mutate(dna_length=1000000, N=10000)
time_mutate(dna_length=10000, N=10)

random.seed(10)  # ensure the same random numbers every time

def create_markov_chain():
    markov_chain = {}
    for from_base in 'ATGC':
        # Generate random transition probabilities by dividing
        # [0,1] into four intervals of random length
       slice_points = sorted(
           [0] + [random.random()for i in range(3)] + [1])
       transition_probabilities = \
           [slice_points[i+1] - slice_points[i] for i in range(4)]
       markov_chain[from_base] = {base: p for base, p
                         in zip('ATGC', transition_probabilities)}
    return markov_chain

mc = create_markov_chain()
print mc
print mc['A']['T'] # probability of transition from A to T

def check_transition_probabilities(markov_chain):
    for from_base in 'ATGC':
        s = sum(markov_chain[from_base][to_base]
                for to_base in 'ATGC')
        if abs(s - 1) > 1E-15:
            raise ValueError('Wrong sum: %s for "%s"' % \
                             (s, from_base))

check_transition_probabilities(mc)

def draw(discrete_probdist):
    """
    Draw random value from discrete probability distribution
    represented as a dict: P(x=value) = discrete_probdist[value].
    """
    # Method:
    # http://en.wikipedia.org/wiki/Pseudo-random_number_sampling
    limit = 0
    r = random.random()
    for value in discrete_probdist:
        limit += discrete_probdist[value]
        if r < limit:
            return value

def draw_vec(discrete_probdist, N):
    """Vectorized version of draw."""
    limit = 0
    r = np.random.random(N)
    counter = {}
    for value in discrete_probdist:
        limit += discrete_probdist[value]
        counter[value] = np.sum(r < limit)
        r = r[r >= limit]
    s = []
    for value in counter:
        a = np.zeros(counter[value], dtype=type(value))
        a[:] = value
        s.append(a)
    values = np.concatenate(s)
    np.random.shuffle(values)
    return values

def check_draw_approx(discrete_probdist, N=1000000):
    """
    See if draw results in frequencies approx equal to
    the probability distribution.
    """
    frequencies = {value: 0 for value in discrete_probdist}
    for i in range(N):
        value = draw(discrete_probdist)
        frequencies[value] += 1
    for value in frequencies:
        frequencies[value] /= float(N)
    print ', '.join(['%s: %.4f (exact %.4f)' % \
                     (v, frequencies[v], discrete_probdist[v])
                     for v in frequencies])

def check_draw_vec_approx(discrete_probdist, N=1000000):
    """
    See if draw_vec results in frequencies approx equal to
    the probability distribution.
    """
    frequencies = {value: 0 for value in discrete_probdist}
    values = draw_vec(discrete_probdist, N)
    lst = values.tolist()
    for value in frequencies:
        frequencies[value] += lst.count(value)
    for value in frequencies:
        frequencies[value] /= float(N)
    print ', '.join(['%s: %.4f (exact %.4f)' % \
                     (v, frequencies[v], discrete_probdist[v])
                     for v in frequencies])

check_draw_approx(mc['A'])
check_draw_vec_approx(mc['A'])
for i in range(4):
    print 'A to', draw(mc['A'])

def mutate_via_markov_chain(dna, markov_chain):
    dna_list = list(dna)
    mutation_site = random.randint(0, len(dna_list) - 1)
    from_base = dna[mutation_site]
    to_base = draw(markov_chain[from_base])
    dna_list[mutation_site] = to_base
    return ''.join(dna_list)

dna = 'TTACGGAGATTTCGGTATGCAT'
print 'Starting DNA:', dna
print format_frequencies(get_base_frequencies_v2(dna))

mc = create_markov_chain()
import pprint
print 'Transition probabilities:\n', pprint.pformat(mc)
nmutations = 10000
for i in range(nmutations):
    dna = mutate_via_markov_chain(dna, mc)

print 'DNA after %d mutations (Markov chain):' % nmutations, dna
print format_frequencies(get_base_frequencies_v2(dna))

def transition_into_bases(markov_chain):
    return {to_base: sum(markov_chain[from_base][to_base]
                         for from_base in 'ATGC')/4.0
            for to_base in 'ATGC'}

print transition_into_bases(mc)

# Test large data
N = 1000000
dna = generate_string_v2(N)
print 'Very long DNA string:', dna[:10], '...', dna[-10:]
print format_frequencies(get_base_frequencies_v2(dna))
nmutations = 100000
for i in range(nmutations):
    dna = mutate_via_markov_chain(dna, mc)

print 'DNA after %d mutations (Markov chain):' % nmutations, \
      dna[:10], '...', dna[-10:]
print format_frequencies(get_base_frequencies_v2(dna))
print 'Compare with probabilities of transition into bases:'
print transition_into_bases(mc)

