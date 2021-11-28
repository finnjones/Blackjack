import pygame
from pygame.locals import *
import os
import random
import math
import sys
import threading
from cards import *
from time import sleep

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
        if mainLoop.cardSelector == 6:
            self.card = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Back/Blue.png").convert_alpha(), (150, 213))
        else:
            self.card = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/" + list(cardShuffle.sCards)[mainLoop.cardSelector] + ".png").convert_alpha(), (150, 213))

        
        self.Playerpos = (self.x, self.y)

        self.ang = ((vec(self.pos) - self.Playerpos).angle_to(vec(1, 0))*-1)
        mainLoop.cardsL.append(self)
        
        
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
        img = pygame.transform.rotate(self.card, self.rot)
        window.blit(img, (self.x - int(img.get_width() / 2), self.y - int(img.get_height() / 2)))
        


class cardShuffleC():
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
            
                

        self.textRect = self.textF.get_rect()
        self.loc = (self.x, self.y)
        window.blit(self.textF, self.loc)
        
class dealCC(object):
    
    def __init__(self):
        self.hands = [[mainLoop.playerHand, 0.5], [mainLoop.CPU1Hand, 0.25], [mainLoop.CPU2Hand, 0.75]]
        self.locY = 780
        
        self.CPUS = [mainLoop.CPU1Hand, mainLoop.CPU2Hand]
        self.selPlayer = 0

    def dealF(self):
        

        

        for i in self.hands:
            cards(screenSize[0]/2, 0, (screenSize[0]*i[1], self.locY))
            i[0].append(cardShuffle.sCards[list(cardShuffle.sCards)[mainLoop.cardSelector]])
            mainLoop.cardSelector += 1
            cards(screenSize[0]/2, 0, (screenSize[0]*i[1] + 40, self.locY - 40))
            i[0].append(cardShuffle.sCards[list(cardShuffle.sCards)[mainLoop.cardSelector]])
            mainLoop.cardSelector += 1

        cards(screenSize[0]/2, 0, (screenSize[0]*0.5, 340))
        mainLoop.dealerHand.append(cardShuffle.sCards[list(cardShuffle.sCards)[mainLoop.cardSelector]])
        mainLoop.cardSelector += 1
        cards(screenSize[0]/2, 0, (screenSize[0]*0.5 + 40, 340 - 40))
        mainLoop.dealerHand.append(cardShuffle.sCards[list(cardShuffle.sCards)[mainLoop.cardSelector]])
        
        mainLoop.cardSelector += 1

    def hit(self, hand):
        ajustment = 0.5
        offsets = 40 * (len(hand))
        
        for i in self.hands:
            if i[0] == hand:
                ajustment = i[1]
        

        
        hand.append(cardShuffle.sCards[list(cardShuffle.sCards)[mainLoop.cardSelector]])

        if hand == mainLoop.dealerHand:
            cards(screenSize[0]/2, 0, (screenSize[0] * ajustment + offsets, 340 - offsets))
            if sum(hand) <= 21:
                mainLoop.hitText.append(drawText(black, 30, (int(screenSize[0] * ajustment), 100), True))
            # else:
            #     bustText.append(drawText(black, 30, (int(screenSize[0] * ajustment), 100), True))
        else:
            cards(screenSize[0]/2, 0, (screenSize[0] * ajustment + offsets, 780 - offsets))
            if sum(hand) <= 21:


                mainLoop.hitText.append(drawText(black, 30, (int(screenSize[0] * ajustment), 540), True))
            # else:
            #     mainLoop.bustText.append(drawText(black, 30, (int(screenSize[0] * ajustment), 540), True))
        mainLoop.cardSelector += 1
    

class betting(object):
    global mainLoop
    global bankBalance
    def __init__(self):
        self.bankT = drawText(black, 30, (100, 50), False)
        self.betT = drawText(black, 30, (100, 100), False)
        self.bankBalance = bankBalance
        self.betA = 0
        self.stop = False

    def bet(self, size):
        global bankBalance

        self.size = size
        if (self.betA + self.size) >= 0 and (self.betA + self.size) <= bankBalance:
            self.betA += self.size
            bankBalance -= self.size

    def win(self):
        global mainLoop
        global bankBalance
        
        if self.stop == False:
            print(mainLoop.allstand)
            if "3" in mainLoop.allstand and "1" in mainLoop.allstand and "2" in mainLoop.allstand and "4" in mainLoop.allstand:
                print(sum(mainLoop.playerHand))
                print(sum(mainLoop.dealerHand))
                if sum(mainLoop.playerHand) > 21 or sum(mainLoop.playerHand) < sum(mainLoop.dealerHand):
                    self.betA = 0
                    self.stop = True

                elif sum(mainLoop.playerHand) > sum(mainLoop.dealerHand) or sum(mainLoop.dealerHand) > 21:
                    if sum(mainLoop.playerHand) == 21:
                        bankBalance = bankBalance + (self.betA * 3)
                        self.betA = 0
                        print("win3")
                        self.stop = True
                    else:
                        bankBalance = self.betA * 2 + bankBalance
                        self.betA = 0

                        print("win2")
                        print("1")
                        self.stop = True

           

                elif sum(mainLoop.playerHand) == sum(mainLoop.dealerHand):
                    bankBalance += self.betA
                    self.betA = 0
                    self.stop = True
                




    def draw(self):

        self.bankT.draw("Bank: $" + str(bankBalance))
        self.betT.draw("Bet: $" + str(self.betA))


class CPUPC(object):
    def __init__(self):
        self.CPUS = [mainLoop.CPU1Hand, mainLoop.CPU2Hand]
        self.selPlayer = 0
        
    def play(self):

        if sum(self.CPUS[self.selPlayer]) < 17:
            
            dealC.hit(self.CPUS[self.selPlayer])
        
        else:
            if len(mainLoop.standText) <= 1:
                if mainLoop.CPU1Hand == self.CPUS[self.selPlayer]:
                    if sum(mainLoop.CPU1Hand) <= 21:
                        mainLoop.standText.append(drawText(black, 30, (int(screenSize[0]* 0.25), 540), True))
                        mainLoop.allstand.append("1")

                if mainLoop.CPU2Hand == self.CPUS[self.selPlayer]:
                    if sum(mainLoop.CPU2Hand) <= 21:
                        mainLoop.standText.append(drawText(black, 30, (int(screenSize[0]* 0.75), 540), True))
                        mainLoop.allstand.append("2")

            if self.selPlayer + 1 < len(self.CPUS):
                self.selPlayer += 1

class dealerP(object):
    def __init__(self):
        self.standD = False
    def play(self):
        global standD
        players = [sum(mainLoop.CPU1Hand), sum(mainLoop.CPU2Hand), sum(mainLoop.playerHand)]
        players.sort()
        if sum(mainLoop.dealerHand) <= 16:
            dealC.hit(mainLoop.dealerHand)
        
        elif self.standD == False:
            self.standD = True
            mainLoop.standText.append(drawText(black, 30, (int(screenSize[0]/2), 100), True))
            mainLoop.allstand.append("4")


def redraw():
    counter = 0
    window.fill(green)

    for i in mainLoop.cardsL:
        i.draw()
        if mainLoop.cardsL[6] == i:
            if "3" in mainLoop.allstand and "1" in mainLoop.allstand and "2" in mainLoop.allstand:
                window.blit(dealHide, (screenSize[0]/2 - 75, 234))

    allHands = [[mainLoop.CPU1Hand, 0.25], [mainLoop.CPU2Hand, 0.75], [mainLoop.playerHand, 0.5], [mainLoop.dealerHand, 0.5]]

    for i in allHands:
        counter += 1

        if sum(i[0]) > 21:
            
            
            if 11 in i[0]:
                for l in i[0]:
                    if l == 11:
                        i[0].remove(11)
                        i[0].append(1)

            
            elif not str(counter) in mainLoop.allstand:

                if i[0] != mainLoop.dealerHand:
                    mainLoop.bustText.append(drawText(black, 30, (int(screenSize[0]* i[1]), 540), True))
                    mainLoop.allstand.append(str(counter))

                else:
                    mainLoop.bustText.append(drawText(black, 30, (int(screenSize[0]* i[1]), 100), True))
                    mainLoop.allstand.append(str(counter))
         
    if mainLoop.deal == True:
        for i in mainLoop.standText:
            i.draw("Stand")
        for i in mainLoop.hitText:
            i.draw("Hit")
        for i in mainLoop.bustText:
            i.draw("Bust")

    mainLoop.bettingSys.draw()
    if mainLoop.minbuy == True:
        mainLoop.minB.draw("Minimum Buy In Of $10")


    if mainLoop.deal == True:
        mainLoop.playerHandT.draw("Player: "+ str(sum(mainLoop.playerHand)))
        mainLoop.CPU1T.draw("CPU 1: "+ str(sum(mainLoop.CPU1Hand)))
        mainLoop.CPU2T.draw("CPU 2: "+ str(sum(mainLoop.CPU2Hand)))
        if "3" in mainLoop.allstand and "1" in mainLoop.allstand and "2" in mainLoop.allstand:
            mainLoop.dealerT.draw("Dealer: "+ str(sum(mainLoop.dealerHand)))
        else:
            mainLoop.dealerT.draw("Dealer: "+ "~")

    mainLoop.bettingSys.win()
    pygame.display.flip()


def delayHit():
    global hitCPU
    global dealerH
    while True:
        if mainLoop.deal == True:
            sleep(1)
            if mainLoop.deal == True:
                mainLoop.hitCPU = True


            
bankBalance = 1000
class mainloop(object):
    global running
    def __init__(self):

        self.cardsL = []
        self.playerHand = []
        self.CPU1Hand = []
        self.CPU2Hand = []
        self.dealerHand = []
        self.hitText = []
        self.standText = []
        self.bustText = []
        self.allstand = []
        self.cardSelector = 0
        

        self.deal = False
        
        # cardShuffle.shuffle()
        self.cardSelector = 0
        self.playerHandT = drawText( black, 30, (screenSize[0]/2 - 45, 900), False)
        self.CPU1T = drawText( black, 30, (screenSize[0]/4 - 45, 900), False)
        self.CPU2T = drawText( black, 30, (screenSize[0]*0.75 - 45, 900), False)
        self.dealerT = drawText( black, 30, (screenSize[0]/2 - 45, 460), False)
        self.minB = drawText( black, 30, (screenSize[0]/2 - 200, 460), True)
        self.bettingSys = betting()
        self.dealerP = dealerP()
        # dealC.dealF()

        
        self.hitCPU = False
        self.hitP = False
        self.dealerH = False
        self.standP = False
        self.reset = False
        self.up = False
        self.down = False
        self.minbuy = False
    def loop(self):
        global running
        redraw()
        clock.tick(60)
        fps = str(int(clock. get_fps()))
        pygame.display.set_caption(fps)
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.bettingSys.bet(10)
                if event.key == pygame.K_9:
                    self.bettingSys.bet(-10)

                if event.key == pygame.K_h and "1" in self.allstand and "2" in self.allstand:
                    self.hitP = True
        
            if keys[pygame.K_SPACE]:
                if int(self.bettingSys.betA) != 0:
                    self.deal = True
                else:
                    self.minbuy = True
                
            
            if keys[pygame.K_r]:
                self.reset = True
            


            if self.reset == True:
                reInit()
                self.reset = False




            if keys[pygame.K_s] and "1" in self.allstand and "2" in self.allstand:
                self.standP = True
                
        if self.deal == True:
            
            for i in self.cardsL:
                i.slideCards()


            
            if self.standP == True:
                self.allstand.append("3")
                self.standText.append(drawText(black, 30, (int(screenSize[0]/2 - 20), 540), True))
                self.standP = False

            if self.dealerH == True:
                self.dealerP.play()
            
            if self.hitP == True and sum(self.playerHand) <= 21:

                dealC.hit(self.playerHand)
                self.hitP = False

                

            if self.hitCPU == True:
                if "3" in self.allstand and "1" in self.allstand and "2" in self.allstand:
                    self.dealerP.play()
                elif not "2" in self.allstand:
                    
                    CPUP.play()
                self.hitCPU = False

            
def reInit():
    global mainLoop
    global cardShuffle
    global dealC
    global CPUP
    global t1
    global dealHide
    global running

    mainLoop = mainloop()
    dealC = dealCC()
    CPUP = CPUPC()
    cardShuffle.shuffle()
    dealC.dealF()
    dealHide = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/"+ list(cardShuffle.sCards)[6] + ".png").convert_alpha(), (150, 213))


mainLoop = mainloop()
cardShuffle = cardShuffleC()
dealC = dealCC()
CPUP = CPUPC()
t1 = threading.Thread(target=delayHit) 
t1.daemon = True
t1.start()
cardShuffle.shuffle()
dealC.dealF()
dealHide = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/"+ list(cardShuffle.sCards)[6] + ".png").convert_alpha(), (150, 213))
running = True

    

running = True
while running:
    mainLoop.loop()
    
pygame.quit()