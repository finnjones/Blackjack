from game import * 
FlexyPath = os.path.dirname(os.path.abspath(__file__))
screenSize = (1620 , 1000)

window = pygame.display.set_mode(screenSize)

class drawText(object):
    def __init__(self, colour, size, loc, fade):
        self.fade = fade
        self.size = size
        self.colour = colour
        self.loc = loc
        self.font = pygame.font.Font(FlexyPath + '/font/quicksand.ttf', self.size)
        self.counter = 290
        self.text = ""

    def draw(self, text):
        self.x = self.loc[0]
        self.y = self.loc[1]
        self.text = text

        self.textF = self.font.render(self.text, True, self.colour)
        if self.fade == True:
            self.counter = self.counter * 0.90
            self.textF.set_alpha(self.counter)
            self.y -= 1
            
                

        self.textRect = self.textF.get_rect()
        self.loc = (self.x, self.y)
        window.blit(self.textF, self.loc)