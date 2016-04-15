"""
As location.py, but type= is not specified (type=str by default).
Instead, all variables set on the command line are explicitly converted
to the right type.
"""
# Set default values
s0 = v0 = 0; a = t = 1
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--v0', '--initial_velocity',
                    default='0.0', help='initial velocity')
parser.add_argument('--s0', '--initial_position',
                    default='0.0', help='initial position')
parser.add_argument('--a', '--acceleration',
                    default='1.0', help='acceleration')
parser.add_argument('--t', '--time',
                    default='1.0', help='time')

example = "--s0 'exp(-1.5) + 10*(1-p**2)' --v0 pi/4"
#args = parser.parse_args(example.split())
args = parser.parse_args()

# Conversion
from math import *
from scitools.std import StringFunction
s0 = StringFunction(args.s0, independent_variable='p')
v0 = eval(args.v0)
a = eval(args.a)
t = eval(args.t)
p = 0.5
s = s0(p) + v0*t + 0.5*a*t**2
print """
An object, starting at s=%s=%g (p=%g) at t=0 with initial
velocity %s m/s, and subject to a constant
acceleration %g m/s**2, is found at the
location s=%g m after %s seconds.
""" % (str(s0), s0(p), p, v0, a, s, t)

