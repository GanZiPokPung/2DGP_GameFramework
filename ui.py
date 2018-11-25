from pico2d import *
import mainframe
import title_scene
import stage_scene

class UI:
    def __init__(self):
        self.posX, self.posY = 0, 0
        self.sizeX, self.sizeY = 0, 0
        self.originSizeX, self.originSizeY = 0, 0
        self.pngSizeX, self.pngSizeY = 0, 0
        self.rectSizeX, self.rectSizeY = 0, 0
        self.collideCheck = False
        self.uiID = 'default'
        self.image = None

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def collideActive(self, opponent):
        pass

    def collideInactive(self, opponent):
        pass

    def click(self):
        pass

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX, self.posY, self.sizeX, self.sizeY)

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

class Button(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, ID):
        self.posX, self.posY = x, y
        if Button.image == None:
            self.initialize_image()
        if Button.size == None:
            self.initialize_size()
        self.uiID = 'button'
        self.buttonID = ID
        self.image = Button.image.get(self.buttonID)
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = Button.size.get(self.buttonID)[0]
        self.pngSizeY = Button.size.get(self.buttonID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        self.rectSizeX = self.sizeX / 2
        self.rectSizeY = self.sizeY / 2

        self.clickCheck = False

    def initialize_image(self):
        Button.image = {
            'start': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'start.png')),
            'quit': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'quit.png'))
        }

    def initialize_size(self):
        Button.size = {
            'start': [497, 134],
            'quit': [497, 134]
        }

    def collideActive(self, opponent):
        if self.clickCheck == True:
            self.sizeX = self.pngSizeX * self.originSizeX * 0.75
            self.sizeY = self.pngSizeY * self.originSizeY * 0.75
        else:
            self.sizeX = self.pngSizeX * self.originSizeX * 1.25
            self.sizeY = self.pngSizeY * self.originSizeY * 1.25

        self.collideCheck = True

    def collideInactive(self, opponent):
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        self.collideCheck = False

    def click(self):
        self.clickCheck = True

    def unclick(self):
        self.clickCheck = False
        if self.buttonID == 'start':
            mainframe.change_state(stage_scene)

class Bar(UI):
    pass

#
class Number(UI):
    pass
#

class Score(UI):
    pass
