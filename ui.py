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
        self.numbers = None
        self.additionalImage = None
        self.additionalIdx = 0

    def set_numbers(self, numlist):
        self.numbers = numlist

    def update_numbers(self, number):
        pass

    def update_additionalImage(self, idx):
        pass

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

        if self.NumOrWords != None:
            for o in self.NumOrWords:
                o.draw()

        if self.additionalImage != None:
            self.additionalImage.draw

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

class Button(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, ID):
        UI.__init__(self)
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
            'quit': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'quit.png')),
            'default': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'default.png'))
        }

    def initialize_size(self):
        Button.size = {
            'start': [497, 134],
            'quit': [497, 134],
            'default':  [99, 99]
        }

    def collideActive(self, opponent):
        if self.clickCheck == True:
            self.sizeX = self.pngSizeX * self.originSizeX * 0.9
            self.sizeY = self.pngSizeY * self.originSizeY * 0.9
            if self.numbers != None:
                for o in self.numbers:
                    o.sizeX = o.pngSizeX * o.originSizeX * 0.9
                    o.sizeY = o.pngSizeY * o.originSizeY * 0.9
            if self.additionalImage != None:
                self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX * 0.9
                self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY * 0.9
        else:
            self.sizeX = self.pngSizeX * self.originSizeX * 1.15
            self.sizeY = self.pngSizeY * self.originSizeY * 1.15
            if self.numbers != None:
                for o in self.numbers:
                    o.sizeX = o.pngSizeX * o.originSizeX * 1.15
                    o.sizeY = o.pngSizeY * o.originSizeY * 1.15
            if self.additionalImage != None:
                self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX * 1.15
                self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY * 1.15

        self.collideCheck = True

    def collideInactive(self, opponent):
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        if self.numbers != None:
            for o in self.numbers:
                o.sizeX = o.pngSizeX * o.originSizeX
                o.sizeY = o.pngSizeY * o.originSizeY
        if self.additionalImage != None:
            self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX
            self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY

        self.collideCheck = False

    def click(self):
        self.clickCheck = True

    def unclick(self):
        self.clickCheck = False
        if self.buttonID == 'start':
            mainframe.change_state(stage_scene)
        elif self.buttonID == 'quit':
            mainframe.quit()

class Bar(UI):
    pass

#
class Number(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, num):
        UI.__init__(self)
        self.posX, self.posY = x, y
        if Number.image == None:
            Number.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Number',  'number.png'))
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = 60
        self.pngSizeY = 78
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        self.frame = 0

    def draw(self):
        Number.image.clip_draw(self.frame * self.pngSizeX, 0, self.pngSizeX, self.pngSizeY, self.posX, self.posY,
                                self.sizeX, self.sizeY)

class Score(UI):
    pass

class Others(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, ID, opacify):
        UI.__init__(self)
        self.posX, self.posY = x, y
        if Others.image == None:
            self.initialize_image()
        if Others.size == None:
            self.initialize_size()
        self.uiID = 'others'
        self.othersID = ID
        self.image = Others.image.get(self.othersID)
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = Others.size.get(self.othersID)[0]
        self.pngSizeY = Others.size.get(self.othersID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        self.opacify = opacify
        self.image.opacify(self.opacify)

    def initialize_image(self):
        Others.image = {
            'shop_back': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'shop_background.png')),
            'shop_logo': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'shop.png')),
            'money_capacity': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'money.png'))
        }

    def initialize_size(self):
        Others.size = {
            'shop_back': [500, 700],
            'shop_logo': [253, 58],
            'money_capacity': [138, 33]
        }
