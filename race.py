import numpy as np
import pickle
import pygame
from pygame.locals import QUIT
from scipy.integrate import odeint
import sys

from sympy import stationary_points

from course import course, D, R # 286.4788975654116, 143.2394487827058
from equations import quadratic_equation
from args import entry_data

tussock = 197,147,75
sundance = 197,186,75 # background
mintjulep = 225,217,162 # bg of racers info
# racer
white = 239,239,239 # White Smoke
black = 7,6,2 # Maire
red = 136,31,18 # Falu Red
blue = 75,147,197 # Danube
yellow = 217,231,16 # Chartreuse Yellow
green = 75,197,147 # Shamrock
orange = 200,122,50 # Bronze
pink = 177,102,182 # Fuchsia

args = sys.argv 

filename = args[1]
with open(filename, mode="rb") as f:
    races = pickle.load(f)

entry_datas = []
for race in races:
    entry_df = race[0]
    data = entry_data(entry_df)
    entry_datas.append(data)

def racer_render(n, img_p, name, handi_rank, trial_time, mean_time):

    x_d = {n: 15+96*(n-1) for n in range(1,9)}
    color_d = {1: white, 2: black, 3: red, 4: blue, 5: yellow, 6: green, 7: orange, 8: pink}

    x = x_d[n]
    color = color_d[n]
    img = pygame.image.load(img_p)
    img_tf = pygame.transform.scale(img, (86, 86))
    screen.blit(img_tf, (x, 50+14))
    pygame.draw.rect(screen, mintjulep, (x, 106+30+14, 86, 80))
    pygame.draw.rect(screen, color, (x+2, 106+30+14, 6, 21))
    
    name_text = font14.render(name, True, (0,0,0))
    screen.blit(name_text, (x+10, 140+14))
    
    rank_text = font14.render(handi_rank, True, (0,0,0))
    screen.blit(rank_text, (x+2, 158+14))
    
    trial_text = font14.render(trial_time, True, (0,0,0))
    screen.blit(trial_text, (x+2, 176+14))
    
    mean_text = font14.render(mean_time, True, (0,0,0))
    screen.blit(mean_text, (x+2, 194+14))

def load_race(n):
    for racer in entry_datas[n-1]:
        n, filename, name, handi_rank, trail, mean_values = racer
        p = "./photos/" + filename
        racer_render(n, p, name, handi_rank, trail, mean_values)

pygame.init()
screen = pygame.display.set_mode((786, 730))
font18 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 18)
font14 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 14)
ck = pygame.time.Clock()

# screen.fill((220,213,200))
screen.fill(sundance)

load_btn = pygame.Rect(300, 300, 80, 30)
load_text = font14.render("load", True, white)

start_btn = pygame.Rect(400, 300, 80, 30) 
start_text = font14.render("start", True, white)

race_btn1 = pygame.Rect(200, 10, 20, 20)
r1_text = font18.render("1R", True, (0,0,0))
screen.blit(r1_text, (200, 10))

race_btn2 = pygame.Rect(200+30, 10, 20, 20)
r2_text = font18.render("2R", True, (0,0,0))
screen.blit(r2_text, (200+30, 10))

title = "2022/02/13 伊勢崎"
title_text = font18.render(title, True, (0,0,0))
screen.blit(title_text, (20, 10))

title = "1R 一般戦Ｂ 3100m(6周)"
title_text = font18.render(title, True, (0,0,0))
screen.blit(title_text, (20, 10+24))

load_race(1)




# for data in entry_datas[0]:
#     n, filename, name, handi_rank, trail, mean_values = data
#     p = "./photos/" + filename
#     racer_render(n, p, name, handi_rank, trail, mean_values)



def start_acc(time):
    # 7秒間の加速 100m
    t = np.arange(0, 7, 0.01)
    v0, x0 = 3., 0.
    a = 5. - round((time-3.3)*10, 1)
    x = 1/2 * a * t**2 + t * v0 + x0
    # x = x[x < 100.] * 3
    # ex = 300/(time*100)
    # while True:
    #     if 300 - x[-1] > ex:
    #         x = np.hstack((x, np.array([x[-1]+ex])))
    #     else:
    #         break
    return x * 3

# 3.3sec/100m ミリ秒に変換 3300ms circle 300m lines 100m x 2 16.5sec/500
# 1m = 100ms  1m = 33ms 1m = 10ms
def running(time, stime, ctime, handi, c): # c: 1, 2, 3, 4
    # print(ctime, stime)
    line = []
    c = c * 10
    for rad in np.linspace(np.pi/2, -np.pi/2, int(ctime*150)):
        x = (R+c) * np.cos(rad)
        y = (R+c) * np.sin(rad)
        line.append((x+100+R+300, y+230+6+100+R))
    del line[-1]

    for px in np.linspace(400+R, 100+R, int(stime*100)):
        x, y = px, 230+6+100-c
        line.append((x, y))
    del line[-1]
    # print(line[-2][0]-line[-1][0])
    for rad in np.linspace(-np.pi/2, -np.pi*1.5, int(ctime*150)):
        x = (R+c) * np.cos(rad)
        y = (R+c) * np.sin(rad)
        line.append((x+100+R, y+230+6+100+R))
    del line[-1]

    for px in np.linspace(100+R, 400+R, int(stime*100)):
        x, y = px, 230+6+100+D+c
        line.append((x, y))
    del line[-1]

    lines = []
    acc_x = start_acc(time)

    corner_x = acc_x[acc_x < handi + 10]
    print(corner_x[-2], corner_x[-1])
    straight_x = acc_x[acc_x >= handi + 10]

    start_rad = np.radians(360 * (handi + 10)/300) + np.radians(90)
    for px in corner_x:
        rad = start_rad + np.radians(360 * -px/300)
        x = (R+c) * np.cos(rad)
        y = (R+c) * np.sin(rad)
        lines.append((x+100+R, y+100+230+6+R))

    straight_x = straight_x - straight_x[0]
    sx = straight_x[straight_x < 300.]
    ex = 300/(time*100)
    while True:
        if 300 - sx[-1] > ex:
            sx = np.hstack((sx, np.array([sx[-1]+ex])))
        else:
            break

    for px in sx:
        x, y = px+100+R, 230+6+100+D+c
        lines.append((x, y))

    for _ in range(1):
        lines += line

    return lines + line[:200]

def get_basetime(time, corner_mph=90.):
    # 最もtimeの遅いracerから算出、corner を時速90kmhに固定し
    # 直線のtimeを計算する
    mph2time = lambda x: 100 / (x / (3600 * 1/1000)) # 時速を100mタイムへ変換
    
    sum_racetime3k = time * 5
    cornertime = mph2time(corner_mph) # コーナーを90km/hと仮定する
    sum_cornertime = cornertime * 3
    sum_straighttime = sum_racetime3k - sum_cornertime
    straighttime = sum_straighttime / 2

    return straighttime, cornertime

def get_cornertime(time, straighttime):
    # レースtime と直線timeからcorner timeを計算する
    sum_racetime3k = time * 5
    sum_straighttime = straighttime * 2
    sum_cornertime = sum_racetime3k - sum_straighttime
    cornertime = sum_cornertime / 3

    return cornertime

stime, ctime = get_basetime(3.37)
ctime2 = get_cornertime(3.32, stime)

r1 = running(3.37, stime, ctime, handi=0, c=1)
r2 = running(3.32, stime, ctime2, handi=10, c=2)

handi_d = {1: 0, 2: 10, 3: 10, 4: 20, 5: 20, 6: 30, 7: 30, 8: 40}

def start_position(handi, c):
    c = c * 10
    pie = np.radians(12) # 360/30
    rd = np.pi/2 + pie + (handi / 10) * pie
    x = (R+c) * np.cos(rd)
    y = (R+c) * np.sin(rd)
    return x+100+R, y+230+6+100+R

# def start_p(handi, c):
#     c = c * 10
#     start_rad = np.radians(360 * (handi + 10)/300) + np.radians(90)
#     for ax in acc_x:
#         rad = start_rad + np.radians(360 * ax/300)
#         x = (R+c) * np.cos(rad)
#         y = (R+c) * np.sin(rad)
#         lines.append((x+100+R, y+230+100+R))

OnYourMark = False
Start = False
# t, ms, ms_start = 0, 0, 0
t = 0
while True:
    res = ck.tick_busy_loop(10) # 100ms 0.1sec
    # print(res)
    # ms = pygame.time.get_ticks()
    screen.blit(course, (0, 230+6), (0, 0, 786, 500))
    pygame.draw.rect(screen, tussock, load_btn)
    screen.blit(load_text, (300+18, 300+5))

    pygame.draw.rect(screen, tussock, start_btn)
    screen.blit(start_text, (400+15, 300+5))

    if OnYourMark:
        pygame.draw.circle(screen,white,(start_position(0, 1)),7)
        pygame.draw.circle(screen,black,(start_position(10, 2)),7)
        pygame.draw.circle(screen,red,(start_position(10, 3)),7)
        pygame.draw.circle(screen,blue,(start_position(20, 4)),7)
        pygame.draw.circle(screen,yellow,(start_position(20, 5)),7)
        pygame.draw.circle(screen,green,(start_position(30, 6)),7)
        pygame.draw.circle(screen,orange,(start_position(30, 7)),7)
        pygame.draw.circle(screen,pink,(start_position(40, 8)),7)

    # cx, cy = 100+R+300, 100+R+150
    # pygame.draw.circle(screen,pink,(cx, cy),7)

    if Start:
        pygame.draw.circle(screen,white,r1[t],7)
        pygame.draw.circle(screen,black,r2[t],7)
        
        if t < min([len(r1), len(r2)])-11:
            t += 10

    # print(ck.get_time())
    pygame.display.update()

    # event process
    for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
        if event.type == QUIT:        # 閉じるボタンが押されたら終了
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_btn.collidepoint(event.pos):
                print("OK, Let’s get started.")
                t = 0
                Start = True
                OnYourMark = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if load_btn.collidepoint(event.pos):
                Start = False
                OnYourMark = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if race_btn1.collidepoint(event.pos):
                load_race(1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if race_btn2.collidepoint(event.pos):
                load_race(2)


