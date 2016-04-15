def extract_data(filename):
    infile = open(filename, 'r')
    infile.readline()  # skip the first line
    data = [line.split() for line in infile]
    annual_avg = data[-1][1]
    data = [(m, float(r)) for m, r in data[:-1]]
    infile.close()
    return data, annual_avg

data, avg = extract_data('rainfall.dat')
print 'The average rainfall for the months:'
for month, value in data:
    print month, value
print 'The average rainfall for the year:', avg
