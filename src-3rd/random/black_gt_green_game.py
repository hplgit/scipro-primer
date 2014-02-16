import sys
N = int(sys.argv[1])               # no of experiments

import random
start_capital = 10
money = start_capital
for i in range(N):
    money -= 1                     # pay for the game
    black = random.randint(1, 6)   # throw black
    green = random.randint(1, 6)   # throw brown
    if black > green:              # success?
        money += 2                 # get award

net_profit_total = money - start_capital
net_profit_per_game = net_profit_total/float(N)
print 'Net profit per game in the long run:', net_profit_per_game


