import matplotlib.pyplot as plt
import numpy as np

from course import dia, rad # 286.4788975654116, 143.2394487827058
from equations import quadratic_equation

t1 = 3.39
t2 = 3.32

racetime = lambda x: (x*5)*6 + x
print("racetime", racetime(t1))
jisoku = lambda x:  (100 / x) * 3600 * 1/1000

print(jisoku(t1), "km")
print(jisoku(t2), "km")

rt = lambda x: 100 / (x / (3600 * 1/1000))
print(rt(jisoku(t1)), "100m/**s")

mph2time = lambda x: 100 / (x / (3600 * 1/1000)) # 時速を100mタイムへ変換
time = t2
sum_racetime3k = time * 5
cornertime = mph2time(90.) # コーナーを90km/hと仮定する
sum_cornertime = cornertime * 3
sum_straighttime = sum_racetime3k - sum_cornertime
straighttime = sum_straighttime / 2
print(cornertime, straighttime, jisoku(straighttime), "km")

def course_times(time, corner_mph=90.):
    # 100m time から直線とコーナーのtimeを計算する
    mph2time = lambda x: 100 / (x / (3600 * 1/1000)) # 時速を100mタイムへ変換
    
    sum_racetime3k = time * 5 * 6
    cornertime = mph2time(corner_mph) # コーナーを90km/hと仮定する
    sum_cornertime = cornertime * 3 * 6
    sum_straighttime = sum_racetime3k - sum_cornertime
    straighttime = sum_straighttime / (2 * 6)

    return cornertime, straighttime

print(course_times(3.31))
print(course_times(3.37))

def acc():
    line = []
    time = 3.3
    c = 0
    # t = np.linspace(100+rad, 400+rad, int(round(1000/time)))
    a = 0.7
    v0 = 3 * time
    print("v0", v0)
    # print("v0", v0)
    x0 = 100+rad
    xmax = x0+300
    tr, _ = quadratic_equation(a/2, v0, x0-xmax) # time required
    print("time required", tr)
    
    # a = -2 * (v0 * t + x0) / t**2
    # v = (x - x0) / t
    # a = (v - v0) / t 

    t = np.arange(0, tr, 0.1)
    xlist = 1/2 * a * t**2 + v0 * t + x0
    for px in xlist:
        x, y = px, 150+90+dia+20+c
        line.append((x, y))
    
    # del line[-1]

def course_times2(time, straighttime):
    # レースtime と直線 100m timeからコーナリングtimeを計算する
    sum_racetime3k = time * 5 * 6
    sum_straighttime = straighttime * 2 * 6
    sum_cornertime = sum_racetime3k - sum_straighttime
    cornertime = sum_cornertime / (3 * 6)

    return cornertime


dif = racetime(t2)-racetime(t1)
# print(dif/14)