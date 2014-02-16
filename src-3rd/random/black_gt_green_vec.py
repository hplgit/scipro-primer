import sys
N = int(sys.argv[1])      # no of experiments

import numpy as np
r = np.random.random_integers(1, 6, size=(2, N))

black = r[0,:]            # eyes for all throws with black
green = r[1,:]            # eyes for all throws with green
success = black > green   # success[i] is true if black[i]>green[i]
M = np.sum(success)       # sum up all successes

p = float(M)/N
print 'probability:', p

