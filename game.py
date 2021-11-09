import pygame
from pygame.locals import *
import os
import random
import math
import logging
import threading
from cards import *
from time import sleep
# from CPU import *
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
dealerHand = []
hitText = []
standText = []
cardSelector = 0

class cards(object):
    global hitCPU
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.vel = 55
        self.rVel = 20
        self.friction = 1.5
        self.rFriction = 0.5
        self.pos = pos
        self.rot = 0
        if cardSelector == 6:
            self.cardBack = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Back/Blue.png").convert_alpha(), (150, 213))
        else:
            self.cardBack = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/" + list(cardShuffle.sCards)[cardSelector] + ".png").convert_alpha(), (150, 213))
        
        self.Playerpos = (self.x, self.y)

        self.ang = ((vec(self.pos) - self.Playerpos).angle_to(vec(1, 0))*-1)
        cardsL.append(self)
        
        
    def slideCards(self):
        global hitCPU
        self.Playerpos = (self.x, self.y)
        if self.rot >= 360:
            self.rot = 0
        
        if abs(self.Playerpos[0] - self.pos[0]) > self.vel or abs(self.Playerpos[1] - self.pos[1]) > self.vel:
            self.vel -= self.friction
            self.rVel -= self.rFriction
            move_vec = pygame.math.Vector2()
            move_vec.from_polar((self.vel, self.ang))
            
            self.x += move_vec[0]
            self.y += move_vec[1]
            
            self.rot += self.rVel

        else:
            self.x = self.pos[0]
            self.y = self.pos[1]
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
    def __init__(self, colour, size, loc, fade):
        self.fade = fade
        self.size = size
        self.colour = colour
        self.loc = loc
        self.font = pygame.font.Font(FlexyPath + '/font/quicksand.ttf', self.size)
        self.counter = 290
        

    def draw(self, text):
        self.x = self.loc[0]
        self.y = self.loc[1]
        self.text = text

        self.textF = self.font.render(self.text, True, self.colour)
        if self.fade == True:
            self.counter = self.counter * 0.85
            self.textF.set_alpha(self.counter)
            self.y -= 1

            if self.counter * 0.91 < 1:
                if self.text == "hit":
                    hitText.remove(self)
                elif self.text == "stand":
                    standText.remove(self)

        self.textRect = self.textF.get_rect()
        self.loc = (self.x, self.y)
        window.blit(self.textF, self.loc)
        
class dealC(object):
    global cardSelector
    def __init__(self):
        self.hands = [[playerHand, 0.5], [CPU1Hand, 0.25], [CPU2Hand, 0.75]]
        self.locY = 780
        
        self.CPUS = [CPU1Hand, CPU2Hand]
        self.selPlayer = 0

    def dealF(self):
        global cardSelector

        

        for i in self.hands:
            cards(screenSize[0]/2, 0, (screenSize[0]*i[1], self.locY))
            i[0].append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
            cardSelector += 1
            cards(screenSize[0]/2, 0, (screenSize[0]*i[1] + 40, self.locY - 40))
            i[0].append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
            cardSelector += 1

        cards(screenSize[0]/2, 0, (screenSize[0]*0.5, 340))
        dealerHand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
        cardSelector += 1
        cards(screenSize[0]/2, 0, (screenSize[0]*0.5 + 40, 340 - 40))
        dealerHand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
        
        cardSelector += 1

    def hit(self, hand):
        global cardSelector
        ajustment = 0.5
        offsets = 40 * (len(hand))
        
        for i in self.hands:
            if i[0] == hand:
                ajustment = i[1]
        

        cards(screenSize[0]/2, 0, (screenSize[0] * ajustment + offsets, 780 - offsets))
        hand.append(cardShuffle.sCards[list(cardShuffle.sCards)[cardSelector]])
        hitText.append(drawText(black, 30, (int(screenSize[0] * ajustment), 540), True))
        cardSelector += 1
    


class CPUP(object):
    def __init__(self):
        self.CPUS = [CPU1Hand, CPU2Hand]
        self.selPlayer = 0
        
    def play(self):

        if sum(self.CPUS[self.selPlayer]) < 17:
            
            dealC.hit(self.CPUS[self.selPlayer])
        else:
            if CPU1Hand == self.CPUS[self.selPlayer]:
                standText.append(drawText(black, 30, (int(screenSize[0]* 0.25), 540), True))
                print(CPU1Hand)
            if CPU2Hand == self.CPUS[self.selPlayer]:
                standText.append(drawText(black, 30, (int(screenSize[0]* 0.75), 540), True))

            if self.selPlayer + 1 < len(self.CPUS):
                self.selPlayer += 1


def redraw():
    window.fill(green)
    for i in standText:
        i.draw("stand")
    for i in hitText:
        i.draw("hit")
    for i in cardsL:
        i.draw()
    
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
        dealerT.draw(str(sum(dealerHand)))
    

    
    pygame.display.flip()


def delayHit():
    global hitCPU
    
    while True:
        if deal == True:
            sleep(1)
            hitCPU = True

            

t1 = threading.Thread(target=delayHit) 
t1.daemon = True

running = True
deal = False
cardShuffle = cardShuffle()
cardShuffle.shuffle()
cardSelector = 0
playerHandT = drawText( black, 30, (screenSize[0]/2, 900), False)
CPU1T = drawText( black, 30, (screenSize[0]/4, 900), False)
CPU2T = drawText( black, 30, (screenSize[0]*0.75, 900), False)
dealerT = drawText( black, 30, (screenSize[0]/2, 460), False)

t1.start()

dealC = dealC()

dealC.dealF()

CPUP = CPUP()

hitCPU = False
hitP = False
standP = False
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
        
        if keys[pygame.K_h]:
            hitP = True
        if keys[pygame.K_s]:
            standP = True


    if deal == True:
        for i in cardsL:
            i.slideCards()
    
    if standP == True:
        standText.append(drawText(black, 30, (int(screenSize[0]), 540), True))
        standP = False


    if hitP == True:
        dealC.hit(playerHand)
        
        hitP = False

    if hitCPU == True:
        CPUP.play()
        hitCPU = False

pygame.quit()