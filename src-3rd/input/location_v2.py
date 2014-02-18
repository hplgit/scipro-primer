"""
As location.py, but using our own function for interpreting each
string from the command-line via eval.
"""
# Set default values
s0 = v0 = 0; a = t = 1

from math import *

def evalcmlarg(text):
    return eval(text)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--v0', '--initial_velocity', type=evalcmlarg,
                    default=0.0, help='initial velocity')
parser.add_argument('--s0', '--initial_position', type=evalcmlarg,
                    default=0.0, help='initial position')
parser.add_argument('--a', '--acceleration', type=evalcmlarg,
                    default=1.0, help='acceleration')
parser.add_argument('--t', '--time', type=evalcmlarg,
                    default=1.0, help='time')

example = "--s0 'exp(-4.2)' --v0 pi/4"
#args = parser.parse_args(example.split())
args = parser.parse_args()
s0 = args.s0; v0 = args.v0; a = args.a; t = args.t
s = s0 + v0*t + 0.5*a*t**2
print """
An object, starting at s=%g at t=0 with initial
velocity %s m/s, and subject to a constant
acceleration %g m/s**2, is found at the
location s=%g m after %s seconds.
""" % (s0, v0, a, s, t)

