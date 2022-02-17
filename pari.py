import numpy as np
import numpy.random as rng

R = 6
BET = 100
deduction = 0.7
trial = 10**5
payout = 0
races = np.random.randint(1, R+1, size=(trial, BET))
for race in races:
    bet = np.sum(race==1)
    p = bet/BET
    odds = BET*deduction/bet
    win = rng.choice([1, 0], p=[p, 1-p])
    if win:
        payout += odds * 100

invest = trial * 100
print(payout/invest)
# -> 0.7071460578508697
# print(1/deduction * 1.1) # 1.57