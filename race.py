import numpy as np
import pickle
import pygame
from pygame.locals import QUIT
import re
import sys

from course import course, D, R # 286.4788975654116, 143.2394487827058
from scrape_oneday_favodds import odds_update
from entries4pygame import set_entry
from buttons import button

from simulation import simulate

sundance = 197,186,75 # background
mintjulep = 225,217,162 # bg of racers info
spunpearl = 162,162,173 # gray
whisper = 232,232,232 # light gray
oldrose = 201,60,89 # pink

nero = 26,26,26
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
place_d = {"kawaguchi": "川口", "isesaki": "伊勢崎", "hamamatsu": "浜松", "iizuka": "飯塚", "sanyo": "山陽"}

args = sys.argv 

filename = args[1]
with open(filename, mode="rb") as f:
    races = pickle.load(f)

res = filename.strip("./data/")
# res = filename.strip(".\\data")
dt, place_en, _ = res.split("_")
place = place_d[place_en]

race_titles = []
entries = []
montes = []
for race in races:
    if race:
        race_titles.append(race[0])
        entry_df = race[1]
        entry_data = set_entry(entry_df)
        entries.append(entry_data)
        montes.append(race[3]) 

def racer_render(entry, a):

    n, filename, name, gradu, machine, team, rank, handi = entry[:8]
    trial, dev, mean_trial, mean_time, mean_st = entry[8:]
    
    handi_rank = handi.rjust(4, " ") + " " + rank
    trial_time = trial + " " + dev
    mean_time = mean_trial + " " + mean_time
    trialxdist = 0.0
    if trial == "-":
        trial_time, st_trialplusdev, acc_time = "", mean_st, ""
    else:
        # 試走偏差
        trialplusdev = float(trial) + float(dev)
        dist = 31 + int(handi.strip("m"))/100
        trialxdist = trialplusdev * dist
        
        st_trialplusdev = mean_st + " " + str(round(trialplusdev, 3))
        acc_time = str(round(a, 1)) + "  "  + str(round(float(trial) + float(dev), 3))

    x_d = {n: 15+96*(n-1) for n in range(1,9)}
    # color_d = {1: white, 2: black, 3: red, 4: blue, 5: yellow, 6: green, 7: orange, 8: pink}

    x = x_d[n]
    color = color_d[n]
    p = "./photos/" + filename
    img = pygame.image.load(p)
    img_scaled = pygame.transform.scale(img, (86, 86))
    screen.blit(img_scaled, (x, 50+14-30))
    pygame.draw.rect(screen, mintjulep, (x, 106+14, 86, 116+18))
    pygame.draw.rect(screen, color, (x+2, 106+14, 6, 21))
    
    team_text = font14.render(team[0], True, (0,0,0))
    screen.blit(team_text, (x+3, 50-30+14))

    gradu_text = font14.render(gradu, True, (0,0,0))
    screen.blit(gradu_text, (x+70, 50-30+14))

    name_text = font14.render(name, True, (0,0,0))
    screen.blit(name_text, (x+10, 140-30+14))
    
    machine_text = font12RD.render(machine, True, (0,0,0))
    screen.blit(machine_text, (x+4, 158-30+14+1))

    rank_text = font14.render(handi_rank, True, nero)
    screen.blit(rank_text, (x+4, 158-30+14+18))
    
    trial_text = font14.render(trial_time, True, (0,0,0))
    screen.blit(trial_text, (x+4, 176-30+14+18))
    
    mean_text = font14.render(mean_time, True, nero)
    screen.blit(mean_text, (x+4, 194-30+14+18))

    st_text = font14.render(st_trialplusdev, True, (0,0,0))
    screen.blit(st_text, (x+4, 212-30+14+18))

    acc_text = font14.render(acc_time, True, nero)
    screen.blit(acc_text, (x+4, 230-30+14+18))

    return trialxdist

def load_race(n):
    # exec racer_render()
    lines, acc = simulate(entries[n-1])

    trialxdists = []
    for entry, a in zip(entries[n-1], acc):
        # rendering
        trialxdist = racer_render(entry, a)
        trialxdists.append(trialxdist)

    start_positions, goal_positions = [], []
    for line in lines:
        start_positions.append(line[0])
        goal_positions.append(line[-1])

    return lines, start_positions, goal_positions

update_data = []

def update_trial():
    x_d = {n: 15+96*(n-1) for n in range(1,9)}
    if update_data:
        entry_df = update_data[0]
        racers = set_entry(entry_df)
        trialxdists = []
        for i, racer in enumerate(racers):
            trial, dev, mean_st = racer[8], racer[9], racer[12]
            handi = racer[7]
            if trial == "-":
                print("no trial data.")
            else:
                trial_time = trial + " " + dev
                # 試走偏差
                trialplusdev = float(trial) + float(dev)
                dist = 31 + int(handi.strip("m"))/100
                trialxdist = trialplusdev * dist
                trialxdists.append(trialxdist)

                st_trialplusdev = mean_st + " " + str(round(trialplusdev, 3))
                st_text = font14.render(st_trialplusdev, True, (0,0,0))
                trial_text = font14.render(trial_time, True, (0,0,0))
                x = x_d[i+1]
                # print(x)
                screen.blit(trial_text, (x+4, 176-30+14+18))
                screen.blit(st_text, (x+4, 212-30+14+18))

        minFullTime = min(trialxdists)
        goaldists = (np.array(trialxdists) - minFullTime) * 100
        for i, dist in enumerate(goaldists):
            print(i+1, round(dist))

windows_title = " ".join(races[0][0][:2])

pygame.init()
screen = pygame.display.set_mode((786, 730+18))
font18 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 18)
font14 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 14)
font12RD = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 12)
ck = pygame.time.Clock()  

# screen.fill((220,213,200))
screen.fill(sundance)
pygame.display.set_caption(windows_title)

mainSurface = pygame.Surface((786, 223))
mainSurface.fill(sundance)    
screen.blit(mainSurface, (0, 32)) 

font = pygame.font.SysFont("arial", 16)
font15 = pygame.font.SysFont("arial", 15)
font.set_bold(True) 
font15.set_bold(True)
start_text = font.render("start", True, spunpearl)
stop_text = font.render("stop", True, spunpearl)
goal_text = font.render("goal", True, spunpearl)
update_text = font15.render("update", True, spunpearl)

font12 = pygame.font.SysFont("arial", 12)
race_texts =  [str(n).rjust(3, " ") + "R" for n in range(1,len(entries)+1)]
race_fonts = [font12.render(r, True, (0,0,0)) for r in race_texts]

def raceboad(n):
    x = 0
    for idx, fnt in enumerate(race_fonts):
        if idx+1 == n:
            pygame.draw.rect(screen, oldrose, pygame.Rect(15+x, 6, 39, 21))
        else:
            pygame.draw.rect(screen, whisper, pygame.Rect(15+x, 6, 39, 21))
        screen.blit(fnt, (20+x, 10))
        x += 40

btn_objs = [pygame.Rect(15+n*40, 6, 39, 21) for n in range(12)]

### 初期画面
lines, start_positions, goal_positions = load_race(1)
raceboad(1)
racetitle = race_titles[0]
num = racetitle[2].strip("R")
num_name = num.rjust(2, " ") + "R " + racetitle[3]
title_text = font18.render(num_name, True, (0,0,0))

weather_ground = racetitle[4] + " " + racetitle[5] + " " + racetitle[6]
wg_text = font14.render(weather_ground, True, (0,0,0))

names = [entry[2] for entry in entries[0]]
name_objs = [font14.render(str(i+1) + " " + name, True, (0,0,0)) for i, name in enumerate(names)]

def favorite_odds(n):
    _quinella = races[n-1][2][1][2].astype("str").iloc[0,1:].tolist()
    _exacta1 = races[n-1][2][2][2].astype("str").iloc[0,1:].tolist()
    _exacta2 = races[n-1][2][2][2].astype("str").iloc[1,1:].tolist()
    _exacta3 = races[n-1][2][2][2].astype("str").iloc[2,1:].tolist()
    _trio = races[n-1][2][4][2].astype("str").iloc[0,1:].tolist()
    _trifecta1 = races[n-1][2][5][2].astype("str").iloc[0,1:].tolist()
    _trifecta2 = races[n-1][2][5][2].astype("str").iloc[1,1:].tolist()
    _trifecta3 = races[n-1][2][5][2].astype("str").iloc[2,1:].tolist()
    quinella = [re.sub("\xa0| ", "", s) for s in _quinella]
    exacta1 = [re.sub("\xa0| ", "", s) for s in _exacta1]
    exacta2 = [re.sub("\xa0| ", "", s) for s in _exacta2]
    exacta3 = [re.sub("\xa0| ", "", s) for s in _exacta3]
    trio = [re.sub("\xa0| ", "", s) for s in _trio]
    trifecta1 = [re.sub("\xa0| ", "", s) for s in _trifecta1]
    trifecta2 = [re.sub("\xa0| ", "", s) for s in _trifecta2]
    trifecta3 = [re.sub("\xa0| ", "", s) for s in _trifecta3]
    odds_sets = [quinella, exacta1, exacta2, exacta3, trio, trifecta1, trifecta2, trifecta3]
    odds_items = [font14.render(ods[0], True, (0,0,0)) for ods in odds_sets]
    odds_values = [font14.render(ods[1].rjust(6, " "), True, (0,0,0)) for ods in odds_sets]

    return odds_items, odds_values

def update_odds():
    odds_objs, odds_items, odds_values = [], [], []
    if update_data:
        odds = update_data[1][0][0]["単勝オッズ"].tolist()
        odds_objs = [font14.render(str(ods).rjust(5, " "), True, (0,0,0)) for ods in odds]
        
        _quinella = update_data[1][1][2].astype("str").iloc[0,1:].tolist()
        _exacta1 = update_data[1][2][2].astype("str").iloc[0,1:].tolist()
        _exacta2 = update_data[1][2][2].astype("str").iloc[1,1:].tolist()
        _exacta3 = update_data[1][2][2].astype("str").iloc[2,1:].tolist()
        _trio = update_data[1][4][2].astype("str").iloc[0,1:].tolist()
        _trifecta1 = update_data[1][5][2].astype("str").iloc[0,1:].tolist()
        _trifecta2 = update_data[1][5][2].astype("str").iloc[1,1:].tolist()
        _trifecta3 = update_data[1][5][2].astype("str").iloc[2,1:].tolist()
        quinella = [re.sub("\xa0| ", "", s) for s in _quinella]
        exacta1 = [re.sub("\xa0| ", "", s) for s in _exacta1]
        exacta2 = [re.sub("\xa0| ", "", s) for s in _exacta2]
        exacta3 = [re.sub("\xa0| ", "", s) for s in _exacta3]
        trio = [re.sub("\xa0| ", "", s) for s in _trio]
        trifecta1 = [re.sub("\xa0| ", "", s) for s in _trifecta1]
        trifecta2 = [re.sub("\xa0| ", "", s) for s in _trifecta2]
        trifecta3 = [re.sub("\xa0| ", "", s) for s in _trifecta3]
        odds_sets = [quinella, exacta1, exacta2, exacta3, trio, trifecta1, trifecta2, trifecta3]
        odds_items = [font14.render(ods[0], True, (0,0,0)) for ods in odds_sets]
        odds_values = [font14.render(ods[1].rjust(6, " "), True, (0,0,0)) for ods in odds_sets]

    return odds_objs, odds_items, odds_values

if races[0][2][0] == []:
    odds_objs = [font14.render("", True, (0,0,0)) for _ in range(len(entries))]
    odds_items = [font14.render("", True, (0,0,0))]
    odds_values = [font14.render("", True, (0,0,0))]
else:
    odds = races[0][2][0][0]["単勝オッズ"].tolist()
    odds_objs = [font14.render(str(ods).rjust(5, " "), True, (0,0,0)) for ods in odds]
    odds_items, odds_values = favorite_odds(1)

# 予想
ml_objs = [font14.render(str(round(m[1], 1)).rjust(5, " "), True, (0,0,0)) for m in montes[0]]
mw_objs = [font14.render(str(round(m[2], 1)).rjust(5, " "), True, (0,0,0)) for m in montes[0]]
mp_objs = [font14.render(str(round(m[3], 1)).rjust(5, " "), True, (0,0,0)) for m in montes[0]]


Set = True
Start, Stop, Goal = False, False, False
this_race = 1
t = 0
while True:
    res = ck.tick_busy_loop(10) # 100ms 0.1sec
    # print(res)
    screen.blit(course, (0, 230+6+18), (0, 0, 786, 500+18))

    screen.blit(title_text, (90+R, 350+18))
    screen.blit(wg_text, (90+36+R, 378+18))
    y=0
    # 単勝
    for name_text, mw_text, ml_text, mp_text, odds_text in zip(name_objs, ml_objs, mw_objs, mp_objs, odds_objs):
        screen.blit(name_text, (90+R-50, 405+18+y))
        screen.blit(ml_text, (90+85+R-50, 405+18+y))
        screen.blit(mw_text, (90+85+R-50+50, 405+18+y))
        screen.blit(mp_text, (90+85+R+50-50+50, 405+18+y))
        screen.blit(odds_text, (90+85+R+50-50+100, 405+18+y))
        y += 20
    # ２連複、２連単 〜
    y=0
    for item_text, value_text in zip(odds_items, odds_values):
        screen.blit(item_text, (90+150-10+R+50+50, 405+18+y))
        screen.blit(value_text, (90+150-10+50+R+60+50, 405+18+y))
        y += 20

    ybtn = 230 + 18
    start_button = pygame.Rect(90+R-20, 350+ybtn, 60, 30)
    screen.blit(button, (90+R-20, 350+ybtn))
    screen.blit(start_text, (90+R+13-20, 350+ybtn+6))

    stop_button = pygame.Rect(200+R-50, 350+ybtn, 60, 30)
    screen.blit(button, (200+R-50, 350+ybtn))
    screen.blit(stop_text, (200+R+14-50, 350+ybtn+6))

    goal_button = pygame.Rect(310+R-80, 350+ybtn, 60, 30)
    screen.blit(button, (310+R-80, 350+ybtn))
    screen.blit(goal_text, (310+R+14-80, 350+ybtn+6))

    update_button = pygame.Rect(400+R-95, 235+115+ybtn, 60, 30)
    screen.blit(button, (400+R+3-95, 235+115+ybtn))
    screen.blit(update_text, (400+R+9-95, 235+115+ybtn+6))

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

            if update_button.collidepoint(event.pos):
                print(dt, place, this_race)
                update_data = odds_update(dt, place, this_race)
                odds_objs, odds_items, odds_values = update_odds()
                update_trial()
                # lines, start_positions, goal_positions = update_race(int(this_race))

            for n in range(1, len(entries)+1):
                if btn_objs[n-1].collidepoint(event.pos):

                    screen.blit(mainSurface, (0, 32)) # 

                    this_race = n
                    lines, start_positions, goal_positions = load_race(n)
                    raceboad(n)
                    Set = True
                    Start, Stop, Goal = False, False, False
                    
                    racetitle = race_titles[n-1]
                    num = racetitle[2].strip("R")
                    txt = num.rjust(2, " ") + "R " + racetitle[3]
                    title_text = font18.render(txt, True, (0,0,0))

                    weather_ground = racetitle[4] + " " + racetitle[5] + " " + racetitle[6]
                    wg_text = font14.render(weather_ground, True, (0,0,0))

                    names = [entry[2] for entry in entries[n-1]]
                    name_objs = [font14.render(str(i+1) + " " + name, True, (0,0,0)) for i, name in enumerate(names)]
                    
                    if races[n-1][2][0] == []:
                        odds_objs = [font14.render("", True, (0,0,0)) for _ in range(len(entries))]
                        odds_items = [font14.render("", True, (0,0,0))]
                        odds_values = [font14.render("", True, (0,0,0))]
                    else:
                        odds = races[n-1][2][0][0]["単勝オッズ"].tolist()
                        odds_objs = [font14.render(str(ods).rjust(5, " "), True, (0,0,0)) for ods in odds]
                        odds_items, odds_values = favorite_odds(n)

                    ml_objs = [font14.render(str(round(m[1], 1)).rjust(5, " "), True, (0,0,0)) for m in montes[n-1]]
                    mw_objs = [font14.render(str(round(m[2], 1)).rjust(5, " "), True, (0,0,0)) for m in montes[n-1]]
                    mp_objs = [font14.render(str(round(m[3], 1)).rjust(5, " "), True, (0,0,0)) for m in montes[n-1]]