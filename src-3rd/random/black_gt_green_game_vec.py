import sys
N = int(sys.argv[1])      # no of experiments

import numpy as np
r = np.random.random_integers(1, 6, size=(2, N))

money = 10 - N            # capital after N throws
black = r[0,:]            # eyes for all throws with black
green = r[1,:]            # eyes for all throws with green
success = black > green   # success[i] is true if black[i]>green[i]
M = np.sum(success)       # sum up all successes
money += 2*M              # add all awards for winning
print 'Net profit per game in the long run:', (money-10)/float(N)

