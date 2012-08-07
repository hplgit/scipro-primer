"""As location_v4.py, but using Action objects."""
import argparse
from math import *
from scitools.std import StringFunction

class ActionEval(argparse.Action):
    def __call__(self, parser, namespace, values,
                 option_string=None):
        setattr(namespace, self.dest, eval(values))

class ActionStringFunction4s0(argparse.Action):
    def __call__(self, parser, namespace, values,
                 option_string=None):
        setattr(namespace, self.dest,
                StringFunction(values, independent_variable='p'))

# Set default values
s0 = v0 = 0; a = t = 1
parser = argparse.ArgumentParser()
parser.add_argument('--v0', '--initial_velocity',
                    default=0.0, help='initial velocity',
                    action=ActionEval)
parser.add_argument('--s0', '--initial_position',
                    default='0.0', help='initial position',
                    action=ActionStringFunction4s0)
parser.add_argument('--a', '--acceleration',
                    default=1.0, help='acceleration',
                    action=ActionEval)
parser.add_argument('--t', '--time',
                    default=1.0, help='time',
                    action=ActionEval)

example = "--s0 'exp(-1.5) + 10*(1-p**2)' --v0 pi/4"
#args = parser.parse_args(example.split())
args = parser.parse_args()
print args, type(args)

s0 = args.s0; v0 = args.v0; a = args.a; t = args.t
p = 0.5
s = s0(p) + v0*t + 0.5*a*t**2
print """
An object, starting at s=%s=%g (p=%g) at t=0 with initial
velocity %s m/s, and subject to a constant
acceleration %g m/s**2, is found at the
location s=%g m after %s seconds.
""" % (str(s0), s0(p), p, v0, a, s, t)

