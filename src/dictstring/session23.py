# futurize -w -n -o py23 session23.py
# futurize --all-imports -w -n -o py23 session23.py

d = {1: 'a', 2: 'b', 3: 'c'}

for key in d:
    print 'd[%s]=%s' % (key, d[key])

for key in d.keys():
    print 'd[%s]=%s' % (key, d[key])

for key, value in d.items():
    print 'd[%s]=%s' % (key, value)

keys = d.keys()

import urllib
with urllib.urlopen('http://google.com') as webfile:
    text = webfile.read()
urllib.urlretrieve('http://google.com', filename='google.html')
