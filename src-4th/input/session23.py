# futurize -w -n -o py23 session23.py
# futurize --all-imports -w -n -o py23 session23.py

a = 1
print a
print 'The value of a is', a
print 'The value of a is', a,
b = 2
print 'and b=%g' % b

a = float(raw_input('Give a: '))
a = input('Give a: ')
