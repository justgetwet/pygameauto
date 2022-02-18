import numpy as np
import pickle
import pygame
from pygame.locals import QUIT
import sys

from course import course, D, R # 286.4788975654116, 143.2394487827058
from equations import quadratic_equation
from args import entry_data, entry
from buttons import button

from simulation import simulate

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

entries = []
for race in races:
    entry_df = race[1]
    entry_data = entry(entry_df)
    entries.append(entry_data)

def racer_render(entry):

    n, filename, name, rank, handi = entry[:5]
    trial, dev, mean_trial, mean_race, st, chakujun = entry[5:]
    
    handi_rank = str(handi) + " " + rank
    trial_time = str(trial) + " " + str(dev)
    mean_time = str(mean_trial) + " " + str(mean_race)
    st_chakujun = str(st) + " " + chakujun

    x_d = {n: 15+96*(n-1) for n in range(1,9)}
    # color_d = {1: white, 2: black, 3: red, 4: blue, 5: yellow, 6: green, 7: orange, 8: pink}

    x = x_d[n]
    color = color_d[n]
    p = "./photos/" + filename
    img = pygame.image.load(p)
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

def load_race(n):
    # exec racer_render()
    for entry in entries[n-1]:
        racer_render(entry)

    lines = simulate(entries[n-1])

    start_positions, goal_positions = [], []
    for line in lines:
        start_positions.append(line[0])
        goal_positions.append(line[-1])

    return lines, start_positions, goal_positions   

windows_title = " ".join(races[0][0][:2])

pygame.init()
screen = pygame.display.set_mode((786, 730))
font18 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 18)
font14 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 14)
ck = pygame.time.Clock()

# screen.fill((220,213,200))
screen.fill(sundance)
pygame.display.set_caption(windows_title)

font = pygame.font.SysFont("arial", 16)
font.set_bold(True) 
start_text = font.render("start", True, spunpearl)
stop_text = font.render("stop", True, spunpearl)
goal_text = font.render("goal", True, spunpearl)

font12 = pygame.font.SysFont("arial", 12)
race_texts =  [str(n).rjust(3, " ") + "R" for n in range(1,13)]
race_fonts = [font12.render(r, True, (0,0,0)) for r in race_texts]
# x = 0
# for fnt in race_fonts:
#     pygame.draw.rect(screen, whisper, pygame.Rect(15+x, 6, 39, 21))
#     screen.blit(fnt, (20+x, 10))
#     x += 40

def spam(n):
    x = 0
    for idx, fnt in enumerate(race_fonts):
        if idx+1 == n:
            pygame.draw.rect(screen, pink, pygame.Rect(15+x, 6, 39, 21))
        else:
            pygame.draw.rect(screen, whisper, pygame.Rect(15+x, 6, 39, 21))
        screen.blit(fnt, (20+x, 10))
        x += 40

btn_objs = [pygame.Rect(15+n*40, 6, 39, 21) for n in range(12)]

### 初期画面
spam(1)
lines, start_positions, goal_positions = load_race(1)

Set = True
Start, Stop, Goal = False, False, False
t = 0
while True:
    res = ck.tick_busy_loop(10) # 100ms 0.1sec
    # print(res)
    screen.blit(course, (0, 230+6), (0, 0, 786, 500))

    ybtn = 230
    start_button = pygame.Rect(90+R, 350+ybtn, 60, 30)
    screen.blit(button, (90+R, 350+ybtn))
    screen.blit(start_text, (90+R+13, 350+ybtn+6))

    stop_button = pygame.Rect(200+R, 350+ybtn, 60, 30)
    screen.blit(button, (200+R, 350+ybtn))
    screen.blit(stop_text, (200+R+14, 350+ybtn+6))

    goal_button = pygame.Rect(310+R, 350+ybtn, 60, 30)
    screen.blit(button, (310+R, 350+ybtn))
    screen.blit(goal_text, (310+R+14, 350+ybtn+6))

    if Set:
        for idx, p in enumerate(start_positions):
            pygame.draw.circle(screen,color_d[idx+1],p,7)

    if Start:
        for idx, line in enumerate(lines):
            if t < len(line):
                pygame.draw.circle(screen,color_d[idx+1],line[t],7)
            else:
                pygame.draw.circle(screen,color_d[idx+1],line[-1],7)
        t += 10

    if Stop:
        for idx, line in enumerate(lines):
            pygame.draw.circle(screen,color_d[idx+1],line[t],7)

    if Goal:
        for idx, p in enumerate(goal_positions):
            pygame.draw.circle(screen,color_d[idx+1],p,7)

    pygame.display.update()

    # event process
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                t = 0
                Start = True
                Set, Stop, Goal = False, False, False
            if stop_button.collidepoint(event.pos):
                Stop = True
                Set, Start, Goal = False, False, False
            if goal_button.collidepoint(event.pos):
                Goal = True 
                Set, Start, Stop = False, False, False

            for n in range(1, 13):
                if btn_objs[n-1].collidepoint(event.pos):
                    lines, start_positions, goal_positions = load_race(n)
                    spam(n)
