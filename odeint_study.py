import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.8 #重力加速度[m/s^2]
interval = 10
t = np.arange(0, 1.2, 10/1000)
y0 =  [7,0]  #初期条件(y,v)

# def equation(y,t,g):
#     dfdt = [y[1],-1*g]
#     return dfdt

def equation(f, t, g):
    y, v = f
    dfdt = [v, -g]
    return dfdt

f0 = [7, 0]
sol = odeint(equation, f0, t, args=(g,))
print(sol)

# y = odeint(equation,y0,t,args=(g,))
# print(y)

fig,ax = plt.subplots()
obj, = ax.plot([],[],'ro')
ax.set_xlim(0,8)
ax.set_ylim(0,8)
ax.set_aspect('equal')

def update_anim(frame_num):
    obj.set_data(4, sol.T[0][frame_num])
    return obj,

anim = FuncAnimation(fig,update_anim,frames=np.arange(0,len(t)),interval=interval,blit=True,repeat=True)
plt.show()