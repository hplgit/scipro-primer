"""Solve the logistic equation for t in [0,T] with n steps."""

def f(u, t):
    return alpha*u*(1 - u/R)

alpha = 0.2
R = 1.0

# Note: ForwardEuler_func2 is a clean up of ForwardEuler_func
# to make a proper module file with no execution of a main program
from ForwardEuler_func2 import ForwardEuler
u, t = ForwardEuler(f, U0=0.1, T=40, n=400)

from matplotlib.pyplot import *
plot(t, u)
xlabel('t'); ylabel('u')
title('Logistic growth: alpha=%s, R=%g, dt=%g'
      % (alpha, R, t[1]-t[0]))
savefig('tmp.pdf'); savefig('tmp.png')
show()
