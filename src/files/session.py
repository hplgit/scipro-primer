infile = open('deg1.dat', 'r')
filestr = infile.read()
filestr
words = filestr.split()
words
numbers = [float(w) for w in words]
mean = sum(numbers)/len(numbers)
mean

temps = {'Oslo': 13, 'London': 15.4, 'Paris': 17.5}
temps['Madrid'] = 26.0
for city in temps:
    print 'The temperature in %s is %g' % (city, temps[city])

if 'Berlin' in temps:
    print 'Berlin:', temps['Berlin']
else:
    print 'No temperature data for Berlin'

temps.keys()
temps.values()

'Oslo' in temps

for city in sorted(temps.keys()):
    print city

del temps['Oslo']
temps
len(temps)   # no of key-value pairs in dictionary

d = {'key1': {'key1': 2, 'key2': 3}, 'key2': 7}
type(d['key1'])
d['key1']
d['key1']['key1']
d['key1']['key2']
d['key2']['key1']  # nonsense, no dict in d['key2']
type(d['key2'])

# defaultdict
p1 = {-3: 2, -1: -1.5, 2: -2}
p1[1]
if 1 in p1:
    p1[1]

value = p1.get(1, 0)

from collections import defaultdict

def polynomial_coeff_default():
    # default value for polynomial dictionary
    return 0.0

p2 = defaultdict(polynomial_coeff_default)
p2 = defaultdict(lambda: 0.0)
p2 = defaultdict(float)

p2.update(p1)
p2[-3]
p2[1]   # not in dict

p2 = defaultdict(lambda: 0.0)
p2.update({2: 8})
p2[1]
p2[0]
p2[-2]
print p2

# OrderedDict

p1 = {-3: 2, -1: -1.5, 2: -2}
print p1
for key in sorted(p1):
    print key, p1[key]

from collections import OrderedDict
p2 = OrderedDict({-3: 2, -1: -1.5, 2: -2})
print p2
p2[-5] = 6
for key in p2:
    print key, p2[key]

data = {'Jan 2': 33, 'Jan 16': 0.1, 'Feb 2': 2}
for date in data:
    print date, data[date]

for date in sorted(data):
    print date, data[date]

import datetime
d = datetime.datetime.strptime('Feb 2, 2017', '%b %d, %Y')
print d
data = {}
d = datetime.datetime.strptime
data[d('Jan 2, 2017', '%b %d, %Y')] = 33
data[d('Jan 16, 2017', '%b %d, %Y')] = 0.1
data[d('Feb 2, 2017', '%b %d, %Y')] = 2
for date in sorted(data):
    print date, data[date]

data = OrderedDict()
data['Jan 2'] = 33
data['Jan 16'] = 0.1
data['Feb 2'] = 2
for date in data:
    print date, data[date]


# string operations

s = 'Berlin: 18.4 C at 4 pm'
s[8:]     # from index 8 to the end of the string
s[8:12]   # index 8, 9, 10 and 11 (not 12!)
s[8:-1]   # from index 8 to the next last character
s[8:-8]

s.find('Berlin')  # where does 'Berlin' start?
s.find('pm')
s.find('Oslo')    # not found...
'Berlin' in s
'Oslo' in s
if 'C' in s:
    print 'C found'
else:
    print 'no C'

s.replace(' ', '__')
s.replace('Berlin', 'Bonn')
s.replace(s[:s.find(':')], 'Bonn')

s.split()

s.split(':')
s.split(':')[1].split('C')[0]

'file1.dat, file2.dat, file3.dat'.split(', ')

t = '1st line\n2nd line\n3rd line'
print t
t.splitlines()

s.lower()
s.upper()

s[18]
s[18] = 5
s[:18] + '5' + s[19:]

'a word'.isdigit()
'214'.isdigit()

', '.join(['Newton', 'Secant', 'Bisection'])

s = '   text with leading/trailing whitespace   '
s.strip()
s.lstrip()
s.rstrip()

'sentence with no capitals'.capitalize()

'Heading'.center(40, '*')
' Heading '.center(40, '*')


