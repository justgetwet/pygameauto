import numpy as np
import pygame
from pygame.locals import QUIT
import sys

from course import course, D, R # 286.4788975654116, 143.2394487827058

sundance = 197,186,75 # background


mintjulep = 225,217,162
# racer
white = 239,239,239 # White Smoke
black = 7,6,2 # Maire
red = 136,31,18 # Falu Red
blue = 75,147,197 # Danube
yellow = 217,231,16 # Chartreuse Yellow
green = 75,197,147 # Shamrock
orange = 200,122,50 # Bronze
pink = 177,102,182 # Fuchsia

title = "2022/02/13 伊勢崎 1R 一般戦Ｂ 3100m(6周)"

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((786, 650+85)) # 150 for racer pictures
    screen.fill(sundance)
    font18 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 18)
    font14 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 14)

    title_text = font18.render(title, True, (0,0,0))
    screen.blit(title_text, (20, 20))

    x_d = {n: 15+96*(n-1) for n in range(1,9)}
    color_d = {1: white, 2: black, 3: red, 4: blue, 5: yellow, 6: green, 7: orange, 8: pink}

    def racer_render(n, img_p, name, handi_rank, trial_time, mean_time):
        x = x_d[n]
        color = color_d[n]
        img = pygame.image.load(img_p)
        img_tf = pygame.transform.scale(img, (86, 86))
        screen.blit(img_tf, (x, 50))
        pygame.draw.rect(screen, mintjulep, (x, 106+30, 86, 80))
        pygame.draw.rect(screen, color, (x+2, 106+30, 6, 21))
        
        name_text = font14.render(name, True, (0,0,0))
        screen.blit(name_text, (x+10, 140))
        
        rank_text = font14.render(handi_rank, True, (0,0,0))
        screen.blit(rank_text, (x+2, 158))
        
        trial_text = font14.render(trial_time, True, (0,0,0))
        screen.blit(trial_text, (x+2, 176))
        
        mean_text = font14.render(mean_time, True, (0,0,0))
        screen.blit(mean_text, (x+2, 194))

    x = 30
    img_p = "./images/9014_吉川麻季.jpg"
    name = "吉川麻季子"
    handi_rank = "  0m  B-94"
    trial_time = "   -  0.067"
    mean_time = " 3.36 3.477"

    for n in range(1, 9):
        racer_render(n, img_p, name, handi_rank, trial_time, mean_time)

    while True:
        screen.blit(course, (0, 150+80), (0, 0, 786, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()