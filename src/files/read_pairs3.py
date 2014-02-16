with open('read_pairs3.dat', 'r') as infile:
    listtext = '['
    for line in infile:
        # add line, without \n (line[:-1]), with a trailing comma:
        listtext += line[:-1] + ', '
listtext = listtext + ']'
pairs = eval(listtext)
import pprint; pprint.pprint(pairs)
