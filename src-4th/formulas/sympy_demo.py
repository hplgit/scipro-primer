from sympy import (
    symbols,   # define mathematical symbols for symbolic computing
    diff,      # differentiate expressions
    integrate, # integrate expressions
    Rational,  # define rational numbers
    lambdify,  # turn symbolic expressions into Python functions
    )
t, v0, g = symbols('t v0 g')
y = v0*t - Rational(1,2)*g*t**2
dydt = diff(y, t)
print 'dydt:', dydt
print 'acceleration:', diff(y, t, t)
y2 = integrate(dydt, t)
print 'y integrated from dydt:', y2
# Turn dydt into an ordinary Python function v(t):
v = lambdify([t, v0, g], dydt)
print v(2, 5, 9.81), 5 - 9.81*2

# Find t values such that y=0
from sympy import solve
roots = solve(y, t)
print 'roots of y=0 are', roots
# Check the result
print 'y(root):', y.subs(t, roots[0])
print 'y(root):', y.subs(t, roots[1])

# Taylor series
from sympy import exp, sin, cos
f = exp(t)
print 'Taylor series of %s:' % f, f.series(t, 0, 3)
f = exp(sin(t))
print 'Taylor series of %s:\n' % f, f.series(t, 0, 8)

# Pretty LaTeX output
from sympy import latex
print latex(f.series(t, 0, 8))

# Summation
n, i = symbols('n i', integer=True)
from sympy import summation, oo  # oo denotes infinity
print 'Sum of natural numbers to n:', summation(i, (i, 0, n))
print 'Sum of all natural numbers:',  summation(i, (i, 0, oo))
from sympy import factorial
print 'Sum of infinite Taylor series:', \
      summation(t**i/factorial(i), (i, 0, oo))

# Simplify and expand expressions
from sympy import simplify, expand
x, y = symbols('x y')
f = -sin(x)*sin(y) + cos(x)*cos(y)
simplify(f)
expand(sin(x+y))
expand(sin(x+y), trig=True)
