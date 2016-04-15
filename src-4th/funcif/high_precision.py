"""Use objects that work with floats with arbitrarily many digits."""

def diff2(f, x, h=1E-9, precision_type=float):
    x = precision_type(str(x))
    h = precision_type(str(h))
    r = (f(x-h) - 2*f(x) + f(x+h))/(h*h)
    return r

def g(t):
    return t**(-6)

def table(precision_type):
    for k in range(1,15):
        h = 10**(-k)
        print 'h=%.0e: %.5f' % (h, diff2(g, 1, h, precision_type))

def decimal_demo():
    import decimal
    decimal.getcontext().prec = 25  # use 25 digits
    table(decimal.Decimal)

def mpmath_demo():
    import sympy
    sympy.mpmath.mp.dps = 25 # use 25 digits
    table(sympy.mpmath.mpf)

print 'standard float:'
table(float)

print '\ndecimal.Decimal:'
decimal_demo()

print '\nsympy.mpmath.mpf:'
mpmath_demo()
