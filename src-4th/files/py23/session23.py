from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
# futurize -w -n -o py23 session23.py
# futurize --all-imports -w -n -o py23 session23.py

d = {1: 'a', 2: 'b', 3: 'c'}

for key in d:
    print('d[%s]=%s' % (key, d[key]))

for key in list(d.keys()):
    print('d[%s]=%s' % (key, d[key]))

for key, value in list(d.items()):
    print('d[%s]=%s' % (key, value))

keys = list(d.keys())

import urllib.request, urllib.parse, urllib.error
with urllib.request.urlopen('http://google.com') as webfile:
    text = webfile.read()
urllib.request.urlretrieve('http://google.com', filename='google.html')
