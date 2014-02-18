"""
As rw_csv_numpy.py, but with easy reading of CSV files
using numpy.genfromtxt.
"""
import numpy as np
arr = np.genfromtxt('budget.csv', delimiter=',', dtype=str)

data = {'column headings': arr[0,1:].tolist(),
        'row headings': arr[1:,0].tolist(),
        'array': np.asarray(arr[1:,1:], dtype=np.float)}

data['row headings'].append('sum')
data['column sum'] = np.sum(data['array'], axis=1).tolist()

outfile = open('budget2b.csv', 'w')
import csv
writer = csv.writer(outfile)
# Turn data dictionary into a nested list first (for easy writing)
table = data['array'].tolist()
table.append(data['column sum'])
table.insert(0, data['column headings'])
# Extend table with row headings (a new column)
[table[r+1].insert(0, data['row headings'][r])
 for r in range(len(table)-1)]
for row in table:
    writer.writerow(row)
outfile.close()
