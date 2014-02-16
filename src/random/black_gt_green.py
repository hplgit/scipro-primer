import sys
N = int(sys.argv[1])               # no of experiments

import random
M = 0                              # no of successful events
for i in range(N):
    black = random.randint(1, 6)   # throw black
    green = random.randint(1, 6)   # throw brown
    if black > green:              # success?
        M += 1
p = float(M)/N
print 'probability:', p

