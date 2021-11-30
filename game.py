import pygame
from pygame.locals import *
import os
import random
import math
import threading
from cards import *
from text import *
from time import sleep
from itertools import islice

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (25, 115, 78)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)


lightGrey = (211,211,211)
clock = pygame.time.Clock()
vec = pygame.math.Vector2
FlexyPath = os.path.dirname(os.path.abspath(__file__))
screenSize = (1620 , 1000)

window = pygame.display.set_mode(screenSize)

bankBalance = 1000

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

        self.imgSize = self.card.get_size()
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
                



    def draw(self, split):
        self.split = split
        self.card = pygame.transform.scale(self.card, (int(150/self.split), int(213/self.split)))
        img = pygame.transform.rotate(self.card, self.rot)
        window.blit(img, (self.x - int(img.get_width() / 2), self.y - int(img.get_height() / 2)))
          
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

        else:
            cards(screenSize[0]/2, 0, (screenSize[0] * ajustment + offsets, 780 - offsets))
            if sum(hand) <= 21:


                mainLoop.hitText.append(drawText(black, 30, (int(screenSize[0] * ajustment), 540), True))

        mainLoop.cardSelector += 1

class betting(object):
    global mainLoop
    global bankBalance
    def __init__(self):

        self.bankT = drawText(black, 50, (screenSize[0]/2 - 140, 100), False)
        self.betT = drawText(black, 30, (screenSize[0]/2 - 50, 260), False)
        self.addCpuT = button((screenSize[0]/2 - (50/2) - 100, 260), (50,50), "-", (betting.betM))
        self.minusCpuT = button((screenSize[0]/2 - (50/2) + 100, 260), (50,50), "+", (betting.betA))
        self.back = button((screenSize[0]/2 - (250/2), 500), (240,50), "Back", (backF))

        self.deal = button((screenSize[0]/2 - (250/2), 400), (240,50), "Deal", (deal))

        self.title = drawText(black, 100, (10, 0), False)
        self.bankBalance = bankBalance
        self.betA = 0
        self.stop = False

    def bet(self, size):
        global bankBalance

        self.size = size
        if (self.betA + self.size) >= 0 and self.bankBalance - (self.size + self.betA) >= 0:
            self.betA += self.size
            bankBalance -= self.size

    def betA():
        mainLoop.bettingSys.bet(10)

    def betM():
        mainLoop.bettingSys.bet(-10)


    def win(self):
        global mainLoop
        global bankBalance
        
        if self.stop == False:
            if "3" in mainLoop.allstand and "1" in mainLoop.allstand and "2" in mainLoop.allstand and "4" in mainLoop.allstand:
                if sum(mainLoop.playerHand) > 21 or sum(mainLoop.playerHand) < sum(mainLoop.dealerHand) and sum(mainLoop.dealerHand) <= 21:
                    self.betA = 0
                    self.stop = True

                elif sum(mainLoop.playerHand) > sum(mainLoop.dealerHand) or sum(mainLoop.dealerHand) > 21:
                    if sum(mainLoop.playerHand) == 21:
                        bankBalance = bankBalance + (self.betA * 3)
                        self.betA = 0
                        self.stop = True
                    else:
                        bankBalance = self.betA * 2 + bankBalance
                        self.betA = 0
                        self.stop = True

           

                elif sum(mainLoop.playerHand) == sum(mainLoop.dealerHand):
                    bankBalance += self.betA
                    self.betA = 0
                    self.stop = True
        print(mainLoop.allstand)




    def draw(self):
        if mainLoop.deal == True:
            self.bankT = drawText(black, 50, (100, 50), False)
            self.betT = drawText(black, 30, (100, 100), False)
        else:
            self.bankT = drawText(black, 50, (screenSize[0]/2 - 140, 100), False)
            self.betT = drawText(black, 30, (screenSize[0]/2 - 50, 260), False)
            self.title.draw("Betting")
            self.deal.draw()
            self.addCpuT.draw()
            self.minusCpuT.draw()
            self.back.draw()
        self.bankT.draw("Bank: $" + str(bankBalance))
        self.betT.draw("Bet: $" + str(self.betA))

class CPUPC(object):
    def __init__(self):
        self.CPUS = [mainLoop.CPU1Hand, mainLoop.CPU2Hand]
        self.selPlayer = 0
        
    def play(self):

        if sum(self.CPUS[self.selPlayer]) < mainLoop.cpuThreshold:
            
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
    def update(self):
        if mainLoop.CPU1Hand == self.CPUS[self.selPlayer]:
            mainLoop.colourDealer = black
            mainLoop.colourPlayer = black
            mainLoop.colourCPU1 = red
            mainLoop.colourCPU2 = black
        if mainLoop.CPU2Hand == self.CPUS[self.selPlayer] and not "2" in mainLoop.allstand:
            mainLoop.colourDealer = black
            mainLoop.colourPlayer = black
            mainLoop.colourCPU1 = black
            mainLoop.colourCPU2 = red

class dealerP(object):
    def __init__(self):
        self.standD = False
    def play(self):
        global standD
        players = [sum(mainLoop.CPU1Hand), sum(mainLoop.CPU2Hand), sum(mainLoop.playerHand)]
        players.sort()
        if sum(mainLoop.dealerHand) < mainLoop.dealerThreshold:
            dealC.hit(mainLoop.dealerHand)
            mainLoop.colourDealer = red
            mainLoop.colourPlayer = black
            mainLoop.colourCPU1 = black
            mainLoop.colourCPU2 = black
        
        elif self.standD == False:
            
            self.standD = True
            if not "4" in mainLoop.allstand:
                mainLoop.standText.append(drawText(black, 30, (int(screenSize[0]/2), 100), True))
                mainLoop.allstand.append("4")

class titleScreenF(object):
    def __init__(self):
        self.title = drawText(black, 100, (10, 0), False)
        self.owner = drawText(black, 50, (15, 100), False)
        self.startB = button((screenSize[0]/2 - (240/2), 300), (240,50), "Start", start)
        self.optionsB = button((screenSize[0]/2 - (240/2), 400), (240,50), "Options", options)

    def draw(self):
        self.title.draw("Blackjack")
        self.owner.draw("By Finn Jones")
        self.startB.draw()
        self.optionsB.draw()

class optionScreenF(object):
    def __init__(self):
        self.title = drawText(black, 100, (10, 0), False)
        self.addCpuT = button((screenSize[0]/2 - (50/2) - 100, 260), (50,50), "-", (optionScreenF.cpuM))
        self.minusCpuT = button((screenSize[0]/2 - (50/2) + 100, 260), (50,50), "+", (optionScreenF.cpuA))
        self.addDealerT = button((screenSize[0]/2 - (50/2) - 100, 400), (50,50), "-", (optionScreenF.dealerM))
        self.munusDealerT = button((screenSize[0]/2 - (50/2) + 100, 400), (50,50), "+", (optionScreenF.dealerA))
        self.back = button((screenSize[0]/2 - (250/2), 500), (240,50), "Back", (backF))
        self.cpuThreshT = drawText(black, 40, (screenSize[0]/2 - (40/2), 260, 0), False)
        self.dealerThreshT = drawText(black, 40, (screenSize[0]/2 - (40/2), 400, 0), False)
        self.CPUTitle = drawText(black, 40, (screenSize[0]/2 - 140, 200, 0), False)
        self.dealerTitle = drawText(black, 40, (screenSize[0]/2 - 160, 350, 0), False)

    
    def draw(self):
        self.title.draw("Options")
        self.dealerTitle.draw("Dealer Threshold")
        self.CPUTitle.draw("CPU Threshold")
        self.cpuThreshT.draw(str(mainLoop.cpuThreshold))
        self.dealerThreshT.draw(str(mainLoop.dealerThreshold))
        self.addCpuT.draw()
        self.minusCpuT.draw()
        self.addDealerT.draw()
        self.munusDealerT.draw()
        self.back.draw()
        
    def cpuM():
        if mainLoop.cpuThreshold > 1 :
            mainLoop.cpuThreshold -= 1
    def cpuA():
        if mainLoop.cpuThreshold < 21:
            mainLoop.cpuThreshold += 1
    def dealerM():
        if mainLoop.dealerThreshold > 1 :
            mainLoop.dealerThreshold -= 1
    def dealerA():
        if mainLoop.dealerThreshold < 21:
            mainLoop.dealerThreshold += 1

class button(object):
    def __init__(self, loc, size, text, function):
        self.loc = loc
        self.size = size
        self.x = self.loc[0]
        self.y = self.loc[1]
        self.text = text
        self.function = function
        self.font = pygame.font.Font(FlexyPath + '/font/quicksand.ttf', 40)
        self.textSize = self.font.size(self.text)
        self.rectangle = pygame.Rect(self.x,self.y,size[0],size[1])
        self.t = drawText(black, 40, ((self.x + self.size[0]/2) - self.textSize[0]/2, (self.y + self.size[1]/2) - self.textSize[1]/2), False)
    def draw(self):
        self.colour = lightGrey
        if self.rectangle.collidepoint(pygame.mouse.get_pos()):

            
            if mainLoop.mouseClick == True:
                
                self.colour = black
                pygame.draw.rect(window, self.colour, self.rectangle)
                self.t.draw(self.text)
                self.function()
                mainLoop.mouseClick = False
            else:
                self.colour = grey

        pygame.draw.rect(window, self.colour, self.rectangle)
        self.t.draw(self.text)

class stats(object):
    def __init__(self):
        self.aceChance = 0
        self.kingChance = 0
        
    def draw(self):
        self.frequency = {}
        lst = []
        for i in islice(cardShuffle.sCards, mainLoop.cardSelector - 1, None):
            i = i[0]
            # checking the element in dictionary
            if i in self.frequency:
                # incrementing the counr
                self.frequency[i] += 1
            else:
                # initializing the count
                self.frequency[i] = 1
        
        print(self.frequency)

            
        

def start():
    mainLoop.start = True
    mainLoop.startMenu = False
    print("start")

def options():
    mainLoop.startMenu = False
    mainLoop.optionMenu = True
    print("options")

def backF():
    mainLoop.start = False
    mainLoop.startMenu = True
    mainLoop.optionMenu = False

def deal():
    if int(mainLoop.bettingSys.betA) != 0:
        mainLoop.deal = True
    else:
        mainLoop.minBet.append(drawText( black, 30, (screenSize[0]/2 - 165, 360), True))

def redraw():
    global event

    counter = 0
    window.fill(green)
    if mainLoop.deal == True:
        for i in mainLoop.cardsL:
            i.draw(1)
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

    for i in mainLoop.minBet:
        i.draw("Minimum Buy In Of $10")

    CPUP.update()
    if mainLoop.deal == True:
        mainLoop.playerHandT.draw("Player: "+ str(sum(mainLoop.playerHand)))
        mainLoop.CPU1T.draw("CPU 1: "+ str(sum(mainLoop.CPU1Hand)))
        mainLoop.CPU2T.draw("CPU 2: "+ str(sum(mainLoop.CPU2Hand)))
        if "3" in mainLoop.allstand and "1" in mainLoop.allstand and "2" in mainLoop.allstand:
            mainLoop.dealerT.draw("Dealer: "+ str(sum(mainLoop.dealerHand)))
        else:
            mainLoop.dealerT.draw("Dealer: "+ "~")
            
    if mainLoop.startMenu == True:
        mainLoop.titleScreen.draw()
    if mainLoop.optionMenu == True:
        mainLoop.optionScreen.draw()
    if mainLoop.start == True:
        mainLoop.bettingSys.draw()
    mainLoop.stats.draw()
    if mainLoop.dealerP.standD == True:
        mainLoop.newRound.draw()
    
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

class mainloop(object):
    global running
    global state
    def __init__(self):
        self.cpuThreshold = 16
        self.dealerThreshold = 17
        self.minB = drawText( black, 30, (screenSize[0]/2 - 200, 460), True)
        self.titleScreen = titleScreenF()
        self.optionScreen = optionScreenF()
        self.newRound = button((1300, 50), (240,50), "New Round", (self.resetGame))
        self.optionMenu = False
        self.mouseClick = False
        
        

    def resetGame(self):
        global state
        self.stats = stats()
        self.cardsL = []
        self.playerHand = []
        self.CPU1Hand = []
        self.CPU2Hand = []
        self.dealerHand = []
        self.hitText = []
        self.standText = []
        self.bustText = []
        self.allstand = []
        self.minBet = []

        self.cardSelector = 0

        self.colourDealer = black
        self.colourPlayer = black
        self.colourCPU1 = black
        self.colourCPU2 = black
              
        self.bettingSys = betting()
        self.dealerP = dealerP()
        
        self.deal = False
        self.hitCPU = False
        self.hitP = False
        self.dealerH = False
        self.standP = False
        self.reset = False
        self.startMenu = False
        self.start = True
        if state == True:
            reInit()
        state = True
       
    def loop(self):
        global running
        redraw()
        self.playerHandT = drawText( self.colourPlayer, 30, (screenSize[0]/2 - 45, 900), False)
        self.CPU1T = drawText( self.colourCPU1, 30, (screenSize[0]/4 - 45, 900), False)
        self.CPU2T = drawText( self.colourCPU2, 30, (screenSize[0]*0.75 - 45, 900), False)
        self.dealerT = drawText( self.colourDealer, 30, (screenSize[0]/2 - 45, 460), False)
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

                if event.key == pygame.K_s and "1" in self.allstand and "2" in self.allstand and not "3" in self.allstand:
                    self.standP = True
            


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouseClick = True
            else:
                self.mouseClick = False
                
            
            if keys[pygame.K_r]:
                self.reset = True
            
            if self.reset == True:
                reInit()
                self.reset = False

        if "1" in self.allstand and "2" in self.allstand and not "3" in self.allstand:
            self.colourDealer = black
            self.colourPlayer = red
            self.colourCPU1 = black
            self.colourCPU2 = black
        
        if "1" in self.allstand and "2" in self.allstand and "3" in self.allstand:
            self.colourDealer = red
            self.colourPlayer = black
            self.colourCPU1 = black
            self.colourCPU2 = black


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
    global cardShuffle
    global dealC
    global CPUP
    global dealHide

    dealC = dealCC()
    CPUP = CPUPC()
    cardShuffle.shuffle()
    dealC.dealF()
    dealHide = pygame.transform.scale(pygame.image.load(FlexyPath + "/Cards/Front/"+ list(cardShuffle.sCards)[6] + ".png").convert_alpha(), (150, 213))

state = False
mainLoop = mainloop()

mainLoop.resetGame()
mainLoop.startMenu = True
mainLoop.start = False

cardShuffle = cardShuffleC()
reInit()
t1 = threading.Thread(target=delayHit) 
t1.daemon = True
t1.start()
running = True

while running:
    mainLoop.loop()
    
pygame.quit()