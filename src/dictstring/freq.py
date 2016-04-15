def freq_lists(dna_list):
    n = len(dna_list[0])
    A = [0]*n
    T = [0]*n
    G = [0]*n
    C = [0]*n
    for dna in dna_list:
        for index, base in enumerate(dna):
            if base == 'A':
                A[index] += 1
            elif base == 'C':
                C[index] += 1
            elif base == 'G':
                G[index] += 1
            elif base == 'T':
                T[index] += 1
    return A, C, G, T

dna_list = ['GGTAG', 'GGTAC', 'GGTGC']
A, C, G, T = freq_lists(dna_list)
print A
print C
print G
print T

frequency_matrix = [A, C, G, T]

def freq_list_of_lists_v1(dna_list):
    # Create empty frequency_matrix[i][j] = 0
    # i=0,1,2,3 corresponds to A,T,G,C
    # j=0,...,length of dna_list[0]
    frequency_matrix = [[0 for v in dna_list[0]] for x in 'ACGT']

    for dna in dna_list:
      for index, base in enumerate(dna):
          if base == 'A':
              frequency_matrix[0][index] +=1
          elif base == 'C':
              frequency_matrix[1][index] +=1
          elif base == 'G':
              frequency_matrix[2][index] +=1
          elif base == 'T':
              frequency_matrix[3][index] +=1

    return frequency_matrix

frequency_matrix = freq_list_of_lists_v1(dna_list)
print frequency_matrix

def freq_list_of_lists_v2(dna_list):
    frequency_matrix = [[0 for v in dna_list[0]] for x in 'ACGT']
    base2index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base2index[base]][index] += 1

    return frequency_matrix

import numpy as np

def freq_numpy(dna_list):
    frequency_matrix = np.zeros((4, len(dna_list[0])), dtype=int)
    base2index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base2index[base]][index] += 1

    return frequency_matrix


def freq_dict_of_lists_v1(dna_list):
    n = max([len(dna) for dna in dna_list])
    frequency_matrix = {
        'A': [0]*n,
        'C': [0]*n,
        'G': [0]*n,
        'T': [0]*n,
        }
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base][index] += 1

    return frequency_matrix

frequency_matrix = freq_dict_of_lists_v1(dna_list)
import pprint   # for nice printout of nested data structures
pprint.pprint(frequency_matrix)

def freq_dict_of_lists_v2(dna_list):
    n = max([len(dna) for dna in dna_list])
    frequency_matrix = {base: [0]*n for base in 'ACGT'}
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base][index] += 1

    return frequency_matrix

def freq_dict_of_dicts_v1(dna_list):
    n = max([len(dna) for dna in dna_list])
    frequency_matrix = {base: {index: 0 for index in range(n)}
                        for base in 'ACGT'}
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base][index] += 1

    return frequency_matrix

from collections import defaultdict

def freq_dict_of_dicts_v2(dna_list):
    n = max([len(dna) for dna in dna_list])
    frequency_matrix = {base: defaultdict(lambda: 0)
                        for base in 'ACGT'}
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base][index] += 1

    return frequency_matrix

frequency_matrix = freq_list_of_lists_v2(dna_list)
pprint.pprint(frequency_matrix)
frequency_matrix = freq_dict_of_dicts_v1(dna_list)
pprint.pprint(frequency_matrix)
frequency_matrix = freq_dict_of_dicts_v2(dna_list)
pprint.pprint(frequency_matrix)

def freq_dict_of_arrays_v1(dna_list):
    n = max([len(dna) for dna in dna_list])
    frequency_matrix = {base: np.zeros(n, dtype=np.int)
                        for base in 'ACGT'}
    for dna in dna_list:
        for index, base in enumerate(dna):
            frequency_matrix[base][index] += 1

    return frequency_matrix

def freq_dict_of_arrays_v2(dna_list):
    n = max([len(dna) for dna in dna_list])
    frequency_matrix = {base: np.zeros(n, dtype=np.int)
                        for base in 'ACGT'}
    for dna in dna_list:
        dna = np.array(dna, dtype='c')
        for base in 'ACCT':
            frequency_matrix[base] += dna == base

    return frequency_matrix

# -----------------------------------------------------------------------

def find_consensus_v1(frequency_matrix):
    base2index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    consensus = ''
    dna_length = len(frequency_matrix[0])

    for i in range(dna_length):  # loop over positions in string
        max_freq = -1            # holds the max freq. for this i
        max_freq_base = None     # holds the corresponding base

        for base in 'ATGC':
            if frequency_matrix[base2index[base]][i] > max_freq:
                max_freq = frequency_matrix[base2index[base]][i]
                max_freq_base = base
            elif frequency_matrix[base2index[base]][i] \
                     == max_freq:
                max_freq_base = '-' # more than one base as max

        consensus += max_freq_base  # add new base with max freq
    return consensus

def find_consensus_v2(frequency_matrix):
    if isinstance(frequency_matrix, list) and \
       isinstance(frequency_matrix[0], list):
        pass # right type
    else:
        raise TypeError('frequency_matrix must be list of lists')

    base2index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    consensus = ''
    dna_length = len(frequency_matrix[0])

    for i in range(dna_length):  # loop over positions in string
        max_freq = -1            # holds the max freq. for this i
        max_freq_base = None     # holds the corresponding base

        for base in 'ACGT':
            if frequency_matrix[base2index[base]][i] > max_freq:
                max_freq = frequency_matrix[base2index[base]][i]
                max_freq_base = base
            elif frequency_matrix[base2index[base]][i] == max_freq:
                max_freq_base = '-' # more than one base as max

        consensus += max_freq_base  # add new base with max freq
    return consensus

frequency_matrix = freq_list_of_lists_v1(dna_list)
pprint.pprint(frequency_matrix)
print find_consensus_v2(frequency_matrix)

def find_consensus_v3(frequency_matrix):
    if isinstance(frequency_matrix, dict) and \
       isinstance(frequency_matrix['A'], dict):
        pass # right type
    else:
        raise TypeError('frequency_matrix must be dict of dicts')

    consensus = ''
    dna_length = len(frequency_matrix['A'])

    for i in range(dna_length):  # loop over positions in string
        max_freq = -1            # holds the max freq. for this i
        max_freq_base = None     # holds the corresponding base

        for base in 'ACGT':
            if frequency_matrix[base][i] > max_freq:
                max_freq = frequency_matrix[base][i]
                max_freq_base = base
            elif frequency_matrix[base][i] == max_freq:
                max_freq_base = '-' # more than one base as max

        consensus += max_freq_base  # add new base with max freq
    return consensus

frequency_matrix = freq_dict_of_dicts_v1(dna_list)
pprint.pprint(frequency_matrix)
print 'Consensus string:', find_consensus_v3(frequency_matrix)

# Does not work with defaultdict because 0 is not counted
# when doing len(frequency_matrix)
frequency_matrix = freq_dict_of_dicts_v2(dna_list)
pprint.pprint(frequency_matrix)
print find_consensus_v3(frequency_matrix), ' (wrong due to len(defaultdict))'

def find_consensus_v4(frequency_matrix, dna_length):
    if isinstance(frequency_matrix, dict) and \
       isinstance(frequency_matrix['A'], dict):
        pass # right type
    else:
        raise TypeError('frequency_matrix must be dict of dicts')

    consensus = ''

    for i in range(dna_length):  # loop over positions in string
        max_freq = -1            # holds the max freq. for this i
        max_freq_base = None     # holds the corresponding base

        for base in 'ACGT':
            if frequency_matrix[base][i] > max_freq:
                max_freq = frequency_matrix[base][i]
                max_freq_base = base
            elif frequency_matrix[base][i] == max_freq:
                max_freq_base = '-' # more than one base as max

        consensus += max_freq_base  # add new base with max freq
    return consensus

print find_consensus_v4(frequency_matrix, len(dna_list[0]))

import random, time

def generate_string(N, alphabet='ACGT'):
    return ''.join([random.choice(alphabet) for i in xrange(N)])

dna_list = [generate_string(500000) for i in range(10)]
print 'Testing efficiency of vectorized code on long strings.......'
t0 = time.clock()
frequency_matrix = freq_dict_of_arrays_v1(dna_list)
t1 = time.clock()
frequency_matrix = freq_dict_of_arrays_v2(dna_list)
t2 = time.clock()
factor = (t1 - t0)/(t2 - t1)
print 'freq_dict_of_arrays: v1 (scalar) / v2 (vectorized):', factor
np.save('tmp.npy', np.array(dna_list[0], dtype='c'))
