import pygame
from pygame.locals import *
import os
import random
import math
from cards import *
from deal import *
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

cardSelector = -1
class cards(object):
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.vel = 20
        self.rVel = 6
        self.friction = 0.18
        self.rFriction = 0.009
        self.pos = pos
        self.rot = 0
        self.cardBack = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/" + list(cardShuffle.d)[cardSelector] + ".png").convert_alpha(), (150, 213))
        cardsL.append(self)
        
    def slideCards(self):
        self.Playerpos = (self.x, self.y)
        if self.rot >= 360:
            self.rot = 0
        
        if abs(self.Playerpos[0] - self.pos[0]) > self.vel or abs(self.Playerpos[1] - self.pos[1]) > self.vel:
            self.vel -= self.friction
            self.rVel -= self.rFriction
            self.ang = ((vec(self.pos) - self.Playerpos).angle_to(vec(1, 0))*-1)

            move_vec = pygame.math.Vector2()
            
            move_vec.from_polar((self.vel, self.ang))
            
            self.x += move_vec[0]
            self.y += move_vec[1]
            
            self.rot += self.rVel

        else:
            
            if self.rot != 0:
                self.rot += self.rVel


    def draw(self):
        img = pygame.transform.rotate(self.cardBack, self.rot)
        window.blit(img, (self.x - int(img.get_width() / 2), self.y - int(img.get_height() / 2)))


class cardShuffle():
    def shuffle(self):
        self.l = list(cardDict.items())
        random.shuffle(self.l)
        self.d = dict(self.l)

class drawText(object):
    def __init__(self, text, colour, size, loc):
        self.text = text
        self.size = size
        self.colour = colour
        self.loc = loc
        self.font = pygame.font.Font(FlexyPath + '/font/quicksand.ttf', self.size)
        self.textF = self.font.render(self.text, True, self.colour)
        self.textRect = self.textF.get_rect()
        self.loc = (self.loc[0] - self.font.size(self.text)[0]/2, self.loc[1])
        

    def draw(self):
        window.blit(self.textF, self.loc)
def deals():
    global cardSelector
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 - 20, 760))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 + 20, 780))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/4 - 20, 760))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/4 + 20, 780))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 - 20, 760))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 + 20, 780))

def redraw():
    window.fill(white)
    for i in cardsL:
        i.draw()
    playerHand.draw()
    pygame.display.flip()




running = True
spin = False
cardShuffle = cardShuffle()
cardShuffle.shuffle()
playerHand = drawText("hello", black, 30, (screenSize[0]/2, 900))


deals()


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
        for i in cardsL:
            i.slideCards()
    

pygame.quit()