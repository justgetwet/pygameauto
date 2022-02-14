import numpy as np
from PIL import Image, ImageDraw
import pygame
from pygame.locals import QUIT
import sys

sundance = 197,186,75 # background
spunpearl = 162,162,173 # gray
freespeech = 75,86,197 # blue

im = Image.new('RGBA', (786, 500), (220,213,200,0))
draw = ImageDraw.Draw(im)
D = 900 / np.pi # 直径 286.4788975654116
R = (900 / np.pi ) / 2 # 半径 143.2394487827058
# 300 x 3 = 900px: 円周 100 x 3 x 2 = 600px: 直線
# course width 90

draw.chord((10, 10, 190+D, 190+D), start=90, end=270, fill=spunpearl)
draw.chord((310, 10, 310+D+180, 100+D+90), start=270, end=90, fill=spunpearl)
draw.rectangle((100+R, 10, 100+R+300, 100+D+90), fill=spunpearl)

v = 360 / 30 # 12 dgree -> 10m
draw.pieslice((10, 10, 10+D+180, 100+D+90), start=90+1*v, end=90+2*v, outline=sundance)
draw.pieslice((10, 10, 10+D+180, 100+D+90), start=90+3*v, end=90+4*v, outline=sundance)
draw.pieslice((10, 10, 10+D+180, 100+D+90), start=90+5*v, end=90+6*v, outline=sundance)

draw.chord((100, 100, 100+D, 100+D), start=90, end=270, fill=freespeech)
draw.chord((100+300, 100, 100+D+300, 100+D), start=270, end=90, fill=freespeech)
draw.rectangle((100+R, 100, 100+R+300, 100+D), fill=freespeech)

px, py = 100+R+300-30, 100+D
draw.line(((px, py+1),(px, py+90)), fill=sundance, width=2)

# px = px - 120
# draw.line(((px, py+1),(px, py+90)), fill=freespeech, width=2)

mode = im.mode
size = im.size
data = im.tobytes()

course = pygame.image.fromstring(data, size, mode)

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((786, 650)) # 150 for racer pictures
    screen.fill(sundance)

    while True:
        screen.blit(course, (0, 150), (0, 0, 786, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
