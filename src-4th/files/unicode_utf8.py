"""Demo of unicode and encodings like utf-8 and latin1."""
# -*- coding: utf-8 -*-

def check(s):
    """Print content, string type, bytecode and length of a string s."""
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
check(Gauss)
print '%s, UTF-8 bytecode: %s' % (Gauss, repr(Gauss)), type(Gauss)

# Mixing UTF-8 bytecode in unicode string gives strange output
Gauss = u'C. F. Gau\xc3\x9f'
check(Gauss)

# But plain print works
print 'Be prepared for strange output:', Gauss, repr(Gauss), type(Gauss)

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

# Writing to file with unicode
try:
    with open('tmp.txt', 'w') as f:
        f.write(Gauss)
except UnicodeEncodeError as e:
    print e

# Remedy: use codecs and convert explicitly to UTF-8
import codecs
with codecs.open('tmp.txt', 'w', 'utf-8') as f:
    f.write(Gauss)

# Writing to file with UTF-8 bytecode
Gauss = u'C. F. Gau\xdf'.encode('utf-8')
try:
    with open('tmp2.txt', 'w') as f:
        f.write(Gauss)
except UnicodeEncodeError as e:
    print e

# Type with a Norwegian keyboard
name = 'Åsmund Ødegård'
check(name)
name = u'Åsmund Ødegård'
check(name)
# Type with UTF-8 bytecode directly:
# Å is C3 85, Ø is C3 98, å is C3 A5
name = '\xc3\x85smund \xc3\x98deg\xc3\xa5rd'
check(name)
# Type with unicode directly:
# Å is C5, Ø is D8, å is E5
name = u'\xc5smund \xd8deg\xe5rd'
check(name)


