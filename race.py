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
from buttons import button

# tussock = 197,147,75

sundance = 197,186,75 # background
mintjulep = 225,217,162 # bg of racers info
spunpearl = 162,162,173 # gray
whisper = 232,232,232 # light gray
# racer
white = 239,239,239 # White Smoke
black = 7,6,2 # Maire
red = 136,31,18 # Falu Red
blue = 75,147,197 # Danube
yellow = 217,231,16 # Chartreuse Yellow
green = 75,197,147 # Shamrock
orange = 200,122,50 # Bronze
pink = 177,102,182 # Fuchsia

color_d = {1: white, 2: black, 3: red, 4: blue, 5: yellow, 6: green, 7: orange, 8: pink}

args = sys.argv 

filename = args[1]
with open(filename, mode="rb") as f:
    races = pickle.load(f)

entry_datas = []
for race in races:
    entry_df = race[1]
    data = entry_data(entry_df)
    entry_datas.append(data)

windows_title = " ".join(races[0][0][:2])

def racer_render(n, img_p, name, handi_rank, trial_time, mean_time, st_chakujun):

    x_d = {n: 15+96*(n-1) for n in range(1,9)}
    color_d = {1: white, 2: black, 3: red, 4: blue, 5: yellow, 6: green, 7: orange, 8: pink}

    x = x_d[n]
    color = color_d[n]
    img = pygame.image.load(img_p)
    img_scaled = pygame.transform.scale(img, (86, 86))
    screen.blit(img_scaled, (x, 50+14-30))
    pygame.draw.rect(screen, mintjulep, (x, 106+14, 86, 116))
    pygame.draw.rect(screen, color, (x+2, 106+14, 6, 21))
    
    name_text = font14.render(name, True, (0,0,0))
    screen.blit(name_text, (x+10, 140-30+14))
    
    rank_text = font14.render(handi_rank, True, (0,0,0))
    screen.blit(rank_text, (x+4, 158-30+14))
    
    trial_text = font14.render(trial_time, True, (0,0,0))
    screen.blit(trial_text, (x+4, 176-30+14))
    
    mean_text = font14.render(mean_time, True, (0,0,0))
    screen.blit(mean_text, (x+4, 194-30+14))

    st_text = font14.render(st_chakujun, True, (0,0,0))
    screen.blit(st_text, (x+4, 212-30+14))

    pred_text = font14.render("0.12 3.393", True, (0,0,0))
    screen.blit(pred_text, (x+4, 230-30+14))

def start_position(handi, c):
    c = c * 10
    pie = np.radians(12) # 360/30
    rd = np.pi/2 + pie + (handi / 10) * pie
    x = (R+c-10) * np.cos(rd)
    y = (R+c-10) * np.sin(rd)
    return x+100+R, y+230+100+R+6

def load_race(n):
    # exec racer_render()
    for racer in entry_datas[n-1]:
        n, filename, name, handi_rank, trail, mean_values, st_chakujun = racer
        p = "./photos/" + filename
        racer_render(n, p, name, handi_rank, trail, mean_values, st_chakujun)
        handi, _  = handi_rank.split()
        # h = int(handi.strip("m"))
        # pygame.draw.circle(screen,white,(start_position(h, n)),7)

def set_start_potision(n):

    pos = []
    for racer in entry_datas[n-1]:
        n, handi_rank = racer[0], racer[3]
        handi, _ = handi_rank.split()
        color = color_d[n]
        pos.append((n, color, int(handi.strip("m"))))

    return pos

def get_racers(n):
    racers = []
    for racer in entry_datas[n-1]:
        time = float(racer[5].split()[1])
        handi = int(racer[3].split()[0].strip("m"))
        c = int(racer[0])
        racers.append((time, handi, c))
    
    return racers

pygame.init()
screen = pygame.display.set_mode((786, 730))
font18 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 18)
font14 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 14)
ck = pygame.time.Clock()

# screen.fill((220,213,200))
screen.fill(sundance)
pygame.display.set_caption(windows_title)
# load_btn = pygame.Rect(300, 300, 80, 30)
# load_text = font14.render("load", True, white)

# start_btn = pygame.Rect(400, 300, 80, 30) 
# start_text = font14.render("start", True, white)

font = pygame.font.SysFont("arial", 16)
font.set_bold(True) 

# start_btn = pygame.Rect(200, 300, 80, 30)
start_text = font.render("start", True, spunpearl)
# screen.blit(button, (90+R, 350))
# screen.blit(start_text, (90+R+13, 350+6))

stop_text = font.render("stop", True, spunpearl)
# screen.blit(button, (200+R, 350))
# screen.blit(stop_text, (200+R+14, 350+6))

goal_text = font.render("goal", True, spunpearl)
# screen.blit(button, (310+R, 350))
# screen.blit(goal_text, (310+R+14, 350+6))

font12 = pygame.font.SysFont("arial", 12)
race_texts =  [str(n).rjust(3, " ") + "R" for n in range(1,13)]
race_fonts = [font12.render(r, True, (0,0,0)) for r in race_texts]
x = 0
for fnt in race_fonts:
    pygame.draw.rect(screen, whisper, pygame.Rect(15+x, 6, 39, 21))
    screen.blit(fnt, (20+x, 10))
    x += 40

btn_objs = [pygame.Rect(15+n*40, 6, 39, 21) for n in range(12)]

### 初期画面
load_race(1)
StartPositions = set_start_potision(1)

def start_acc(time):
    # 7秒間の加速 100m
    t = np.arange(0, 7, 0.01)
    v0, x0 = 3., 0.
    a = 5. - round((time-3.3)*10, 1)
    x = 1/2 * a * t**2 + t * v0 + x0

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
    print("corner_", corner_x[-2], corner_x[-1])
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

def base_straighttime(time, corner_mph=90.):
    # 最もtimeの遅いracerから算出、corner を時速90kmhに固定し
    # 直線のtimeを計算する
    mph2time = lambda x: 100 / (x / (3600 * 1/1000)) # 時速を100mタイムへ変換
    
    sum_racetime3k = time * 5
    cornertime = mph2time(corner_mph) # コーナーを90km/hと仮定する
    sum_cornertime = cornertime * 3
    sum_straighttime = sum_racetime3k - sum_cornertime
    straighttime = sum_straighttime / 2

    return straighttime

def get_cornertime(time, straighttime):
    # レースtime と直線timeからcorner timeを計算する
    sum_racetime3k = time * 5
    sum_straighttime = straighttime * 2
    sum_cornertime = sum_racetime3k - sum_straighttime
    cornertime = sum_cornertime / 3

    return cornertime

racers = get_racers(1)
slow_time = max([racer[0] for racer in racers])
straighttime = base_straighttime(slow_time)
runs=[]
for time, handi, c in racers:
    cornertime = get_cornertime(time, straighttime)
    lines = running(time, straighttime, cornertime, handi, c)
    runs.append(lines)

handi_d = {1: 0, 2: 10, 3: 10, 4: 20, 5: 20, 6: 30, 7: 30, 8: 40}

### Game Tick
OnYourMark = True
Start = False
# t, ms, ms_start = 0, 0, 0
t = 0
while True:
    res = ck.tick_busy_loop(10) # 100ms 0.1sec
    # print(res)
    # ms = pygame.time.get_ticks()
    screen.blit(course, (0, 230+6), (0, 0, 786, 500))

    ybtn = 230
    # pygame.draw.rect(screen, (255,0,0), pygame.Rect(90+R, 350+ybtn, 60, 30))
    start_button = pygame.Rect(90+R, 350+ybtn, 60, 30)
    screen.blit(button, (90+R, 350+ybtn))
    screen.blit(start_text, (90+R+13, 350+ybtn+6))

    screen.blit(button, (200+R, 350+ybtn))
    screen.blit(stop_text, (200+R+14, 350+ybtn+6))

    screen.blit(button, (310+R, 350+ybtn))
    screen.blit(goal_text, (310+R+14, 350+ybtn+6))

    if OnYourMark:
        for n, color, handi in StartPositions:
            pygame.draw.circle(screen,color,(start_position(handi, n+1)),7)

    # cx, cy = 100+R+300, 100+R+150
    # pygame.draw.circle(screen,pink,(cx, cy),7)

    if Start:
        pygame.draw.circle(screen,white,runs[0][t],7)
        pygame.draw.circle(screen,black,runs[1][t],7)
        
        if t < min([len(runs[0]), len(runs[1])])-11:
            t += 10

    # print(ck.get_time())
    pygame.display.update()

    # event process
    for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
        if event.type == QUIT:        # 閉じるボタンが押されたら終了
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                t = 0
                Start = True
                OnYourMark = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_objs[0].collidepoint(event.pos):
                load_race(1)
                OnYourMark = True
                StartPositions = set_start_potision(1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_objs[1].collidepoint(event.pos):
                load_race(2)
                # pygame.draw.rect(screen, (255,0,0), btn_objs[1])
                OnYourMark = True
                StartPositions = set_start_potision(2)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_objs[2].collidepoint(event.pos):
                load_race(3)
                OnYourMark = True
                StartPositions = set_start_potision(3)
