import pygame
from pygame.locals import *
import os
import random
import math
from cards import *
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)

clock = pygame.time.Clock()
vec = pygame.math.Vector2
FlexyPath = os.path.dirname(os.path.abspath(__file__))
screenSize = (1620 , 1000)

window = pygame.display.set_mode(screenSize)
cardsL = []

print(list(cardDict)[0])
cardSelector = 0
class cards(object):
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.vel = 10
        self.rVel = 4
        self.friction = 0.05
        self.rFriction = 0.01
        self.pos = pos
        self.rot = 0
        self.cardBack = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/" + list(cardShuffle.d)[cardSelector] + ".png").convert_alpha(), (150, 213))
        cardsL.append(self)
    def slideCards(self):


        self.rot = (vec(self.x, self.y) - vec(self.pos)).angle_to(vec(1, 0)) + 90
        print(self.rot)
        if self.x < self.pos[0]:
            self.x += self.vel
        elif self.x > self.pos[0]:
            self.x -= self.vel
        if self.y < self.pos[1]:
            self.y += self.vel
        elif self.y > self.pos[1]:
            self.y -= self.vel
            # self.vel -= self.friction
            # self.rVel -= self.rFriction
            # self.y += self.vel
            # self.rot += self.rVel

    def draw(self):
        img = pygame.transform.rotate(self.cardBack, self.rot)
        window.blit(img, (self.x - int(img.get_width() / 2), self.y - int(img.get_height() / 2)))

        # window.blit(pygame.transform.rotate(cardBack, self.rot), (self.x, self.y))

class cardShuffle():
    def shuffle(self):
        self.l = list(cardDict.items())
        random.shuffle(self.l)
        self.d = dict(self.l)

def redraw():
    window.fill(white)
    for i in cardsL:
        i.draw()
    
    pygame.display.flip()




running = True
spin = False
cardShuffle = cardShuffle()
cardShuffle.shuffle()
cards(screenSize[0]/2, 0, (900,900))


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
            cardSelector += 1

            cards(screenSize[0]/2, 0, (900,900))
    if spin == True:
        for i in cardsL:
            i.slideCards()
    

pygame.quit()