combinations = [(black, green)
                for black in range(1, 7)
                for green in range(1, 7)]
success = [black > green for black, green in combinations]
M = sum(success)
print 'probability:', float(M)/len(combinations)
