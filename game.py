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
green = (25, 115, 78)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)

clock = pygame.time.Clock()
vec = pygame.math.Vector2
FlexyPath = os.path.dirname(os.path.abspath(__file__))
screenSize = (1620 , 1000)

window = pygame.display.set_mode(screenSize)
cardsL = []
playerHand = []
CPU1Hand = []
CPU2Hand = []
dealer = []


cardSelector = 0
print(cardDict)
class cards(object):
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.vel = 55
        self.rVel = 20
        self.friction = 1.5
        self.rFriction = 0.5
        self.pos = pos
        self.rot = 0
        self.cardBack = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/" + list(cardShuffle.sCards)[cardSelector] + ".png").convert_alpha(), (150, 213))
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
        self.sCards = dict(self.l)

class drawText(object):
    def __init__(self, colour, size, loc):
        self.size = size
        self.colour = colour
        self.loc = loc
        self.font = pygame.font.Font(FlexyPath + '/font/quicksand.ttf', self.size)
        self.loc = (self.loc[0] - self.font.size("12")[0]/2, self.loc[1])

        

    def draw(self, text):
        self.text = text

        self.textF = self.font.render(self.text, True, self.colour)
        self.textRect = self.textF.get_rect()
        window.blit(self.textF, self.loc)
def deals():
    global cardSelector
    global CPU1Hand
    global playerHand
    global CPU2Hand
    cards(screenSize[0]/2, 0, (screenSize[0]/2 - 20, 760))
    playerHand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 + 20, 780))
    playerHand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/4 - 20, 760))
    CPU1Hand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/4 + 20, 780))
    CPU1Hand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 - 20, 760))
    CPU2Hand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 + 20, 780))
    CPU2Hand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 + 20, 780))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 - 20, 385))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 + 20, 400))

def redraw():
    window.fill(green)
    for i in reversed(cardsL):
        i.draw()
    
    print(playerHand)
    if 11 in playerHand and sum(playerHand) > 21:
        playerHand.remove(11)
        playerHand.append(1)
    if 11 in CPU1Hand and sum(CPU1Hand) > 21:
        CPU1Hand.remove(11)
        CPU1Hand.append(1)
    if 11 in CPU2Hand and sum(CPU2Hand) > 21:
        CPU2Hand.remove(11)
        CPU2Hand.append(1)
    if deal == True:
        playerHandT.draw(str(sum(playerHand)))
        CPU1T.draw(str(sum(CPU1Hand)))
        CPU2T.draw(str(sum(CPU2Hand)))
    pygame.display.flip()




running = True
deal = False
cardShuffle = cardShuffle()
cardShuffle.shuffle()
cardSelector = 0
print(cardShuffle.sCards)
print(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
print(str(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]]))
playerHandT = drawText( black, 30, (screenSize[0]/2, 900))
CPU1T = drawText( black, 30, (screenSize[0]/4, 900))
CPU2T = drawText( black, 30, (screenSize[0]*0.75, 900))



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
            deal = True

    if deal == True:
        for i in cardsL:
            i.slideCards()
    

pygame.quit()