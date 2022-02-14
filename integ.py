import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

t = np.arange(0, 6, 0.01)
# print(t)
v0 = 3.
a = 5.

f0 =  [0, v0]  #初期条件(x,v)
def func_acc(f, t):
    x, v = f
    dxdt = v
    dvdt = a
    return [dxdt, dvdt]

sol = odeint(func_acc, f0, t)
print(sol[-1])

x0 = 0
x = a * t**2 / 2 + t * v0 + x0
res = x[x < 100.]
print(x[-1], len(res), res[-1])

print(100/3.33)
# ax = plt.figure().gca()
# ax.plot(t, v)
# plt.show()



