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
        self.uiID = 0
        self.image = None

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def collideActive(self, opponent):
        pass

    def collideInactive(self, opponent):
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
        self.uiID = ID
        self.image = Button.image.get(self.uiID)
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = Button.size.get(self.uiID)[0]
        self.pngSizeY = Button.size.get(self.uiID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        self.rectSizeX = self.sizeX / 2
        self.rectSizeY = self.sizeY / 2

    def initialize_image(self):
        Button.image = {
            'start': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'start.png'))
        }

    def initialize_size(self):
        Button.size = {
            'start': [156, 16]
        }

    def collideActive(self, opponent):
        self.sizeX = self.pngSizeX * self.originSizeX * 1.25
        self.sizeY = self.pngSizeY * self.originSizeY * 1.25

    def collideInactive(self, opponent):
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY


class Bar(UI):
    pass

#
class Number(UI):
    pass
#

class Score(UI):
    pass
