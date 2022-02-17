import numpy as np
from PIL import Image, ImageDraw
import pygame
from pygame.locals import QUIT
import sys

from course import course, R
sundance = 197,186,75 # background
spunpearl = 162,162,173 # gray course color
deepkoamaru = 41,42,103 # blue button color

im = Image.new('RGBA', (200, 100), (0,0,0,0))
draw = ImageDraw.Draw(im)

draw.chord((0, 0, 20, 30), start=90, end=270, fill=deepkoamaru)
draw.rectangle((10, 0, 50, 30), fill=deepkoamaru)
draw.chord((40, 0, 60, 30), start=270, end=90, fill=deepkoamaru)

mode = im.mode
size = im.size
data = im.tobytes()

button = pygame.image.fromstring(data, size, mode)

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((786, 500))
    screen.fill(sundance)
    screen.blit(course, (0, 5), (0, 0, 786, 500))
    
    font14 = pygame.font.Font("./fonts/RictyDiminished-Regular.ttf", 14)
    font = pygame.font.SysFont("arial", 16)
    font.set_bold(True) 
    
    # start_btn = pygame.Rect(200, 300, 80, 30)
    start_text = font.render("start", True, spunpearl)
    screen.blit(button, (90+R, 350))
    screen.blit(start_text, (90+R+13, 350+6))

    stop_text = font.render("stop", True, spunpearl)
    screen.blit(button, (200+R, 350))
    screen.blit(stop_text, (200+R+14, 350+6))

    goal_text = font.render("goal", True, spunpearl)
    screen.blit(button, (310+R, 350))
    screen.blit(goal_text, (310+R+14, 350+6))

    while True:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()