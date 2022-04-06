from ast import While
import numpy as np
import pickle
import pygame
from pygame.locals import QUIT, KEYDOWN, K_s
import sys

from course import course, D, R # 286.4788975654116, 143.2394487827058
from entries4pygame import set_entry

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

def start_acc(time):
    # スタートの加速区間 7秒間 100m+α
    t = np.arange(0, 7, 0.01)
    v0, x0 = 5., 0.
    a = 11-(time-3.)*10
    x = 1/2 * a * t**2 + t * v0 + x0
    return x * 3, a

def running(n, time, basetime): 
    # 周回区間
    if time != 0.0:
        around_course_time = time * 5
    else: # 休場明けをどうしよう
        around_course_time = 3.6 * 5
    straighttime = basetime * 2
    cornertime = (around_course_time - straighttime) / 3 # per 100m
    
    line = []
    c = n * 10
    for rad in np.linspace(np.pi/2, -np.pi/2, int(cornertime*300)):
        x = (R+c) * np.cos(rad)
        y = (R+c) * np.sin(rad)
        line.append((x+100+R+300, y+230+6+100+18+R))
    del line[-1]

    for px in np.linspace(400+R, 100+R, int(basetime*100)):
        x, y = px, 230+6+100+18-c
        line.append((x, y))
    del line[-1]
    # print(line[-2][0]-line[-1][0])
    for rad in np.linspace(-np.pi/2, -np.pi*1.5, int(cornertime*300)):
        x = (R+c) * np.cos(rad)
        y = (R+c) * np.sin(rad)
        line.append((x+100+R, y+230+6+100+18+R))
    del line[-1]

    for px in np.linspace(100+R, 400+R, int(basetime*100)):
        x, y = px, 230+6+100+18+D+c
        line.append((x, y))
    del line[-1]

    lines=[]
    for _ in range(5):
        lines += line

    return lines

def goalrun(n, s, time=3.9):
    line = []
    c = n * 10
    for rad in np.linspace(np.pi/2, -np.pi/2, int(time*300)):
        x = (R+c) * np.cos(rad)
        y = (R+c) * np.sin(rad)
        line.append((x+100+R+300, y+230+6+100+18+R))
    
    return line[:s]

def simulate(entry):

    n_data = [int(d[0]) for d in entry]
    if entry[0][8] == "-":
        time_data = [float(d[11])  for d in entry]
    else:
        time_data = [float(d[8])+float(d[9]) if d[8] != "-" else 3.99 for d in entry]
    f = lambda x: np.radians(360 * x)/300 + np.radians(90)
    handi_rads = [f(int(d[7].strip("m"))+10) for d in entry] 

    start_accs = [start_acc(t) for t in time_data]
    start_data = [s[0] for s in start_accs]
    acc_data = [s[1] for s in start_accs]

    corners=[]
    for n, acc, r in zip(n_data, start_data, handi_rads):
        line=[]
        for px in acc:
            rad = r + np.radians(360 * -px/900)
            if rad > np.radians(90):
                c = 10 * n
                x = (R+c) * np.cos(rad)
                y = (R+c) * np.sin(rad)
                line.append((x+100+R, y+100+230+6+18+R))
            else:
                break
        corners.append(line)

    straights=[]
    for n, acc in zip(n_data, start_data):
        line=[]
        arr = np.array(acc[len(corners[n-1]):])
        acc_straight = arr - arr[0] 
        for px in acc_straight:
            if px < 300:
                c = 10 * n
                x, y = px+100+R, 230+100+6+18+D+c
                line.append((x, y))
            else:
                break
        straights.append(line)

    slowtime = max(time_data)
    mph2time = lambda x: 100 / (x / (3600 * 1/1000)) # 時速を100mタイムへ変換
    cornertime = mph2time(90)
    basetime = ((slowtime * 5) - (cornertime * 2)) / 2

    arounds = []
    for n, time in zip(n_data, time_data):
        lines = running(n, time, basetime)
        arounds.append(lines)

    _lines = []
    for c, s, a in zip(corners, straights, arounds):
        _lines.append(c+s+a)

    l1 = [(idx+1, len(line)) for idx, line in enumerate(_lines)]
    l2 = sorted(l1, key=lambda x: x[1])
    l3 = [x[0] for x in l2]
    l4 = [(x, (len(l2)+1-idx)*50) for idx, x in enumerate(l3)]
    l5 = sorted(l4, key=lambda x: x[0])
    goals=[]
    for n, s in l5:
        g = goalrun(n, s, basetime)
        goals.append(g)

    lines=[]
    for line, goal in zip(_lines, goals):
        line += goal
        lines.append(line)

    return lines, acc_data



# rad = np.radians(90)
# sx = (R+10) * np.cos(rad) + 100+R
# sy = (R+10) * np.sin(rad) + 100+230+6+R

color_d = {0: white, 1: black, 2: red, 3: blue, 4: yellow, 5: green, 6: orange, 7: pink}

if __name__ == '__main__':

    args = sys.argv 

    filename = args[1]
    with open(filename, mode="rb") as f:
        races = pickle.load(f)

    entries = []
    for race in races:
        entry_df = race[1]
        entry_data = set_entry(entry_df)
        entries.append(entry_data)

    lines = simulate(entries, 3)

    pygame.init()
    ck = pygame.time.Clock()
    screen = pygame.display.set_mode((786, 650+85))
    screen.fill(sundance)
    OnYourMark = True
    Start = False
    t = 0
    while True:
        ck.tick_busy_loop(10) # 100ms 0.1sec
        screen.blit(course, (0, 230+6), (0, 0, 786, 500))

        if OnYourMark:
            pass
            # pygame.draw.circle(screen, red, (sx, sy), 7)

        if Start:
            for idx, line in enumerate(lines):
                if t < len(line):
                    pygame.draw.circle(screen,color_d[idx],line[t],7)
                else:
                    pygame.draw.circle(screen,color_d[idx],line[-1],7)
            t += 10

        pygame.display.update()


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    t = 0
                    OnYourMark = False
                    Start = True