import pygame
from pygame.locals import QUIT
import sys

def event():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

pygame.init()
screen = pygame.display.set_mode((786, 650))
screen.fill((220,213,200))
ck = pygame.time.Clock()

while True:
    ret = ck.tick_busy_loop(100)
    print(ret)

    pygame.display.update()
    event()

