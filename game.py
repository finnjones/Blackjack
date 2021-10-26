import pygame
from pygame.locals import *
import os
import random
from cards import *
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)

clock = pygame.time.Clock()
FlexyPath = os.path.dirname(os.path.abspath(__file__))
screenSize = (1620 , 1000)

window = pygame.display.set_mode(screenSize)


cardBack = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Back/red.png"), (150, 213))

class cards(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.rVel = 4
        self.friction = 0.05
        self.rFriction = 0.01
        self.rot = 0

    def slideCards(self):
        if self.vel > 0:
            self.vel -= self.friction
            self.rVel -= self.rFriction
            self.y += self.vel
            self.rot += self.rVel

    def draw(self):
        
        
        img = pygame.transform.rotate(cardBack, self.rot)
        window.blit(img, (self.x - int(img.get_width() / 2), self.y - int(img.get_height() / 2)))

        # window.blit(pygame.transform.rotate(cardBack, self.rot), (self.x, self.y))


def redraw():
    window.fill(white)
    cards.draw()
    pygame.display.flip()

def shuffle(self):
    l = list(cardDict.items())
    random.shuffle(l)
    d = dict(l)
    print(d)


running = True
spin = False
while running:
    redraw()
    clock.tick(60)
    fps = str(int(clock. get_fps()))
    pygame.display.set_caption(fps)
    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        
        if keys[pygame.K_SPACE]:
            spin = True
    if spin == True:
        cards.slideCards()
    

pygame.quit()