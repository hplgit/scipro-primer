"""
As location.py, but using our own functions for converting
between strings and the right types.
"""
# Set default values
s0 = v0 = 0; a = t = 1

def evalcmlarg(text):
    return eval(text)

def toStringFunction4s0(text):
    from scitools.std import StringFunction
    return StringFunction(text, independent_variable='p')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--v0', '--initial_velocity', type=evalcmlarg,
                    default=0.0, help='initial velocity')
parser.add_argument('--s0', '--initial_position',
                    type=toStringFunction4s0,
                    default='0.0', help='initial position')
parser.add_argument('--a', '--acceleration', type=evalcmlarg,
                    default=1.0, help='acceleration')
parser.add_argument('--t', '--time', type=evalcmlarg,
                    default=1.0, help='time')

from math import *
example = "--s0 '10*(1-p**2)' --v0 pi/4"
#args = parser.parse_args(example.split())
args = parser.parse_args()
s0 = args.s0; v0 = args.v0; a = args.a; t = args.t
p = 0.5
s = s0(p) + v0*t + 0.5*a*t**2
print """
An object, starting at s=%g=%s (p=%g) at t=0 with initial
velocity %s m/s, and subject to a constant
acceleration %g m/s**2, is found at the
location s=%g m after %s seconds.
""" % (str(s0), s0(p), p, v0, a, s, t)

