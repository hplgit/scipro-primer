"""
Read CSV file into numpy array with numpy.genfromtxt,
extend array with new row with column sums, compute sums,
write array to CSV file using numpy.savetxt.
As rw_csv_numpy2.py, but with numpy constructions of output.
"""

"""Easy reading of CSV files using numpy.genfromtxt."""
import numpy as np
arr = np.genfromtxt('budget.csv', delimiter=',', dtype=str)

# Add row for sum of columns
arr.resize((arr.shape[0]+1, arr.shape[1]))
arr[-1,0] = '"sum"'
subtable = np.asarray(arr[1:-1,1:], dtype=np.float)
sum_row = np.sum(subtable, axis=1)
arr[-1,1:] = np.asarray(sum_row, dtype=str)

# numpy.savetxt writes table with a delimiter between entires
np.savetxt('budget2c.csv', arr, delimiter=',', fmt='%s')

