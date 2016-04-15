import sys, sympy
from scitools.std import StringFunction
f = StringFunction(sys.argv[1], independent_variable='x')
x = float(sys.argv[2])

def numerical_derivative(f, x, h=1E-5):
    return (f(x+h) - f(x-h))/(2*h)

print 'Numerical derivative:', numerical_derivative(f, x)

# Import all sin, cos, exp, ... functions from sympy such that
# we can build a sympy expression out of str(f)
from sympy import *
x_value = x
# Let x be a math symbol (not a float)
x = sympy.symbols('x')
# Turn the string formula in f (StringFunction) into
# a sympy expression
print "'%s'" % str(f)
formula = eval(str(f))  # ex: eval('exp(x)*sin(x)')
# Alternative: formula = eval(sys.argv[1])

# Differentiate formula wrt symbol x
dfdx = diff(formula, x)
# Substitute symbol x by x_value
dfdx_value = dfdx.subs(x, x_value)

print 'Exact derivative:', dfdx_value, '(error=%.3E)' % \
      (dfdx_value - numerical_derivative(f, x_value))
print 'Formula for the derivative:', dfdx
