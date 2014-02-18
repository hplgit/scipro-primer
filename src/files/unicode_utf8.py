"""Demo of unicode and encodings like utf-8 and latin1."""
# -*- coding: utf-8 -*-
"""
There are two types of strings in Python: plain strings (known as
byte strings) with type `str`
and unicode strings with type `unicode`. Plain strings suffice as long
as you are writing English text only. A string is then just a
series of bytes representing integers between 0 and 255.
The first characters corresponding to the numbers 0 to 127 constitute
the ASCII set. These can be printed out:

\bpy
for i in range(0, 128):
    print i, chr(i)
\epy
The keys on an English keyboard can be recognized from `i=33` to `i=127`.
The next numbers are used to represent non-English characters.

Texts with non-English
characters are recommended to be represented by unicode strings.
This is the default string type in Python 3.x, while in Python
2.x we need to explicitly annotate a string as unicode by
a `u` prefix as in `s = u'my text'.
"""
def check(s):
    """Print content, bytecode and length of a string s."""
    print '%s, %s: %s (%d)' % \
          (s, s.__class__.__name__, repr(s), len(s))

# Type with a German keyboard
Gauss = 'C. F. Gauß'
check(Gauss)
# See what the characters correspond to as integer
for char in Gauss:
    print ord(char),
print
# Observe that there are 10 characters in the string, but
# len(Gauss) is 11, because the last character is represented
# by two bytes (195 and 159). The other characters are in the
# range 0-127.

# Define unicode string (Python 2.x)
Gauss = u'C. F. Gauß'
check(Gauss)
# Python 3.x has unicode strings by default (no initial u)

# The German ß has unicode DF and we can use this code directly:
Gauss = u'C. F. Gau\xdf'
check(Gauss)
# The UTF-8 bytecode of ß is C39F and we can use this too
Gauss = 'C. F. Gau\xc3\x9f'
print '%s, UTF-8 bytecode: %s' % (Gauss, repr(Gauss)), type(Gauss)

# But mixing UTF-8 bytecode in unicode string does not work
Gauss = u'C. F. Gau\xc3x9f'
try:
    check(Gauss)
except TypeError as e:
    print 'TypeError:', e
# But plain print works
print 'Be prepared for strange output:', \
      Gauss, repr(Gauss), type(Gauss)

# Convert unicode to UTF-8 and latin-1 encoding
Gauss = u'C. F. Gau\xdf'
print 'UTF-8:', repr(Gauss.encode('utf-8'))
print 'UTF-16:', repr(Gauss.encode('utf-16'))
print 'latin-1:', repr(Gauss.encode('latin-1'))
# (encode requires unicode strings)
# Encode + decode
Gauss_utf8 = Gauss.encode('utf-8')
Gauss2 = unicode(Gauss_utf8, 'utf-8')
print 'unicode:', repr(Gauss2)
print 'unicode(s.encode(encoding), encoding) == s:', Gauss2 == Gauss

# Type with a Norwegian keyboard
Odegaard = 'Åsmund Ødegård'
check(Odegaard)
Odegaard = u'Åsmund Ødegård'
check(Odegaard)
# Type with unicode directly:
# Å is C5, Ø is D8, å is E5
Odegaard = u'\xc5smund \xd8deg\xe5rd'
check(Odegaard)


