from pico2d import *
import mainframe
import title_scene
import stage_scene
import game_world
import player
from static import *

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

    def set_numbers(self, x, y, sizeX, sizeY, betweenLength, num):
        if self.numbers == None:
            self.numbers = Numbers(x, y, sizeX, sizeY, betweenLength, num)
        else:
            self.numbers.setNumbers(num)

    def set_additionalimage(self, x, y, sizeX, sizeY, ID, opacify):
        self.additionalImage = Others(x, y, sizeX, sizeY, ID, opacify)

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

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX, self.posY, self.sizeX, self.sizeY)

        if self.numbers != None:
            self.numbers.drawNumbers()

        if self.additionalImage != None:
            self.additionalImage.draw()

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

class Button(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, imageID, processID):
        UI.__init__(self)
        self.posX, self.posY = x, y
        if Button.image == None:
            self.initialize_image()
        if Button.size == None:
            self.initialize_size()
        self.uiID = 'button'
        self.buttonImageID = imageID
        self.buttonProcessID = processID
        self.image = Button.image.get(self.buttonImageID)
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = Button.size.get(self.buttonImageID)[0]
        self.pngSizeY = Button.size.get(self.buttonImageID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        self.rectSizeX = self.sizeX / 2
        self.rectSizeY = self.sizeY / 2

        self.clickCheck = False

    def initialize_image(self):
        Button.image = {
            'start': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'start.png')),
            'quit': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'quit.png')),
            'default': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'default.png')),
            'restart' : load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'restart.png'))
        }

    def initialize_size(self):
        Button.size = {
            'start': [497, 134],
            'quit': [497, 134],
            'default':  [99, 99],
            'restart': [301, 99]
        }

    def collideActive(self, opponent):
        if self.clickCheck == True:
            self.sizeX = self.pngSizeX * self.originSizeX * 0.9
            self.sizeY = self.pngSizeY * self.originSizeY * 0.9
            if self.numbers != None:
                self.numbers.setSize(0.9, 0.9)
            if self.additionalImage != None:
                self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX * 0.9
                self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY * 0.9
        else:
            self.sizeX = self.pngSizeX * self.originSizeX * 1.15
            self.sizeY = self.pngSizeY * self.originSizeY * 1.15
            if self.numbers != None:
                self.numbers.setSize(1.15, 1.15)
            if self.additionalImage != None:
                self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX * 1.15
                self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY * 1.15

        self.collideCheck = True

    def collideInactive(self, opponent):
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        if self.numbers != None:
            self.numbers.setOriginSize()
        if self.additionalImage != None:
            self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX
            self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY

        self.collideCheck = False

    def click(self):
        self.clickCheck = True

    def unclick(self):
        self.clickCheck = False
        if self.buttonProcessID == 'start':
            mainframe.change_state(stage_scene)
        elif self.buttonProcessID == 'quit':
            mainframe.quit()
        elif self.buttonProcessID == 'attUpgrade':
            if self.numbers.num < 13:
                self.set_numbers(0, 0, 0, 0, 0, self.numbers.num + 1)
            self.additionalImage.setOtherImageToIndex(int(self.additionalImage.othersID) + 1)
            # 정보 파싱
            game_world.curtain_object(PLAYER, 0).parsingDataSet(self.additionalImage.othersID)
        elif self.buttonProcessID == 'lifeUpgrade':
            pass
        elif self.buttonProcessID == 'magica':
            pass
        elif self.buttonProcessID == 'restart':
            mainframe.pop_state()

class Bar(UI):
    pass

#
class Numbers(UI):
    def __init__(self, x, y, sizeX, sizeY, between, num):
        UI.__init__(self)
        self.numberList = []
        self.numberValueList = []
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.between = between
        self.num = -num
        self.setNumbers(num)

    def setNumbers(self, num):
        if self.num == num:
            return -1
        self.num = num
        self.numberList.clear()
        self.numberValueList.clear()
        numStr = str(self.num)
        lengthCheck = 10

        for cnt in numStr:
            value = num % lengthCheck
            self.numberValueList.append(value)
            num -= value
            num //= lengthCheck

        betweenCnt = 0
        for value in self.numberValueList:
            self.numberList.append(Number(self.x - (self.between * betweenCnt), self.y, self.sizeX, self.sizeY, value))
            betweenCnt += 1

    def setSize(self, sizeX, sizeY):
        for n in self.numberList:
            n.setSize(sizeX, sizeY)

    def setOriginSize(self):
        for n in self.numberList:
            n.setOriginSize()

    def drawNumbers(self):
        for n in self.numberList:
            n.draw()

class Number(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, idx):
        UI.__init__(self)
        self.posX, self.posY = x, y
        if Number.image == None:
            Number.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Number',  'number2.png'))
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = 10
        self.pngSizeY = 14
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        self.frame = idx;

    def setNumberIdx(self, idx):
        self.frame = idx;

    def setSize(self, sizeX, sizeY):
        self.pngSizeX = 10
        self.pngSizeY = 14
        self.sizeX = self.pngSizeX * self.originSizeX * sizeX
        self.sizeY = self.pngSizeY * self.originSizeX * sizeY

    def setOriginSize(self):
        self.pngSizeX = 10
        self.pngSizeY = 14
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY* self.originSizeX

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

    def setOtherImageID(self, ID):
        self.othersID = ID
        self.image = Others.image.get(self.othersID)
        self.pngSizeX = Others.size.get(self.othersID)[0]
        self.pngSizeY = Others.size.get(self.othersID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

    def setOtherImageToIndex(self, idx):
        if idx > 13:
            return


        self.othersID = str(idx)
        self.image = Others.image.get(self.othersID)
        self.pngSizeX = Others.size.get(self.othersID)[0]
        self.pngSizeY = Others.size.get(self.othersID)[1]
        self.originSizeX = Others.size.get(self.othersID)[2]
        self.originSizeY = Others.size.get(self.othersID)[3]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

    def initialize_image(self):
        Others.image = {
            'shop_back': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'shop_background.png')),
            'shop_logo': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'shop.png')),
            'money_capacity': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Others', 'money.png')),
            'posion': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'item', 'posion.png')),
            'megica': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'item', 'book.png')),

            # bullet
            '1':  load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'SmallCircle.png')),
            '2':  load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'SmallMiss.png')),
            '3': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'Rug.png')),
            '4': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'GreenWeak.png')),
            '5': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleWeak.png')),
            '6': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'GreenNormal.png')),
            '7': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleNormal.png')),
            '8': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'GreenStrong.png')),
            '9': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleStrong.png')),
            '10': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleMax.png')),
            '11': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'ExplodeMiss.png')),
            '12': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'BlueCircle.png')),
            '13': load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'Eagle.png'))
        }

    def initialize_size(self):
        Others.size = {
            'shop_back': [500, 700],
            'shop_logo': [253, 58],
            'money_capacity': [138, 33],
            'posion': [61, 81],
            'megica': [101, 108],

            # bullet
            # 사이즈 조정 필요
            '1': [8, 8, 4, 4],
            '2': [16, 16, 2.7, 2.7],
            '3': [24, 24, 1.5, 1.5],
            '4': [36, 36, 1.5, 1.5],
            '5': [26, 26, 2.5, 2.5],
            '6': [28, 28, 2, 2],
            '7': [26, 26, 1.75, 1.75],
            '8': [32, 32, 2, 2],
            '9': [32, 32, 1.75, 1.75],
            '10': [48, 48, 1, 1],
            '11': [48 // 3, 22, 2, 2],
            '12': [36, 36, 1, 1],
            '13': [75, 49, 1, 1]
        }