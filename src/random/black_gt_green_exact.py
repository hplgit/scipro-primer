"""Exact computation of the probability simulated in incr_eyes.py."""

# Set up all combination of two throws
combinations = [(black, green)
                for black in range(1, 7)
                for green in range(1, 7)]
# Find all where black > green
success = [black > green for black, green in combinations]
M = sum(success)
p = float(M)/len(combinations)
print '%d/%d' % (M, len(combinations))
print p

