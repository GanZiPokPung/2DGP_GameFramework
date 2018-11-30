from pico2d import *
import mainframe
import stage_scene
import game_world
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
            self.numbers.draw()

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
            moneyCheck = game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-1500)
            if moneyCheck == False:
                return
            if self.numbers.num < 13:
                self.set_numbers(0, 0, 0, 0, 0, self.numbers.num + 1)
            self.additionalImage.setOtherImageToIndex(int(self.additionalImage.othersID) + 1)
            attCheck =  game_world.curtain_object(PLAYER, 0).parsingAttData(self.additionalImage.othersID)
            if attCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(1500)
        elif self.buttonProcessID == 'lifeUpgrade':
            moneyCheck = game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-500)
            if moneyCheck == False:
                 return
            heartCheck = game_world.curtain_object(PLAYER, 0).parsingHPBar(50)
            if heartCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(500)
        elif self.buttonProcessID == 'magicaUpgrade':
            moneyCheck = game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-1000)
            if moneyCheck == False:
                return
            bombCheck = game_world.curtain_object(PLAYER, 0).parsingBombBar(1)
            if bombCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-1000)
        elif self.buttonProcessID == 'restart':
            mainframe.pop_state()
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
        self.num = 0
        self.setNumbers(num)
        self.uiID = 'numbers'

    def setNumbers(self, num):
        self.num = num
        self.numberList.clear()
        self.numberValueList.clear()

        if self.num == 0:
            self.numberList.append(Number(self.x, self.y, self.sizeX, self.sizeY, 0))
            return 0

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

    def draw(self):
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
        self.uiID = 'number'

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

class BombBar(UI):
    def __init__(self, x, y, bombCount):
        UI.__init__(self)
        self.posX, self.posY = x, y
        self.bombCount = bombCount
        self.uiID = 'bombbar'
        self.bombs = []
        self.setBombImage(bombCount)

    def setBombImage(self, bombCount):
        self.bombs.clear()

        for cnt in range(0, bombCount):
            self.bombs.append(Bomb(self.posX - (50 * cnt), self.posY))

    def draw(self):
        for bomb in self.bombs:
            bomb.draw()

class Bomb(UI):
    image = None
    def __init__(self, x, y):
        UI.__init__(self)
        self.posX, self.posY = x, y
        self.originSizeX = 0.015
        self.originSizeY = 0.015
        self.moveSizeX = self.originSizeX
        self.moveSizeY = self.originSizeY
        self.pngSizeX = 2400
        self.pngSizeY = 2400
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        self.uiID = 'bomb'
        if Bomb.image == None:
            Bomb.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'thunder.png'))
        self.image = Bomb.image

class HPBar(UI):
    def __init__(self, x, y, hp):
        UI.__init__(self)
        self.posX, self.posY = x, y
        self.hp = hp
        self.uiID = 'hpbar'
        self.divideNum = 50
        self.hearts = []
        self.setHPImage(hp)

    def setHPImage(self, hp):
        self.hearts.clear()

        if hp <= 0:
            self.hp = 0
            return

        self.hp = hp
        fullHeart = int(hp // self.divideNum)
        lastHeart = int(hp % self.divideNum)

        far = 0
        if fullHeart != 0:
            for cnt in range(0, fullHeart):
                self.hearts.append(Heart(self.posX - (50 * far), self.posY, self.divideNum, self.divideNum))
                far += 1
        if lastHeart != 0:
            self.hearts.append(Heart(self.posX - (50 * far), self.posY, lastHeart, self.divideNum))

    def update(self):
        for heart in self.hearts:
            heart.update(mainframe.frame_time)

    def draw(self):
        for heart in self.hearts:
            heart.draw()

class Heart(UI):
    image = None
    def __init__(self, x, y, hp, divide):
        UI.__init__(self)
        self.posX, self.posY = x, y
        self.hp = hp
        self.originSizeX = 0.25 * (self.hp * (1 / divide))
        self.originSizeY = 0.25 * (self.hp * (1 / divide))
        self.moveSizeX = self.originSizeX
        self.moveSizeY = self.originSizeY
        self.moveID = 'big'
        self.pngSizeX = 170
        self.pngSizeY = 150
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        self.uiID = 'heart'
        self.hpDifferSpeed = 0.5
        if Heart.image == None:
            Heart.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'heart.png'))
        self.image = Heart.image

    def update(self, time):
        if self.moveID == 'big':
            self.moveSizeX += time * self.hpDifferSpeed
            self.moveSizeY += time * self.hpDifferSpeed
            if self.moveSizeX > self.originSizeX * 1.1:
                self.moveID = 'small'
                self.hpDifferSpeed /= 3
        elif self.moveID == 'small':
            self.moveSizeX -= time * self.hpDifferSpeed
            self.moveSizeY -= time * self.hpDifferSpeed
            if self.moveSizeX < self.originSizeX * 0.9:
                self.moveID = 'big'
                self.hpDifferSpeed *= 3

        self.sizeX = self.pngSizeX * self.moveSizeX
        self.sizeY = self.pngSizeY * self.moveSizeY

class Score(UI):
    image = None
    def __init__(self, x, y, score):
        UI.__init__(self)
        self.posX, self.posY = x, y
        self.score = score
        self.uiID = 'score'
        self.numbers = Numbers(self.posX, self.posY, 2, 2, 17, self.score)

    def setScore(self, score):
        if score > 99999999:
            return
        self.score = score
        self.numbers.setNumbers(self.score)

    def draw(self):
        self.numbers.draw()

class Money(UI):
    image = None
    def __init__(self, x, y, money):
        UI.__init__(self)
        self.posX, self.posY = x, y
        self.money = money
        self.uiID = 'money'
        self.numbers = Numbers(self.posX, self.posY, 2, 2, 17, self.money)
        if Money.image == None:
            Money.image =  load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'money.png'))
        self.originSizeX = 0.05
        self.originSizeY = 0.05
        self.pngSizeX = 600
        self.pngSizeY = 600
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

    def setMoney(self, money):
        if money > 99999999:
            return
        self.money = money
        self.numbers.setNumbers(self.money)

    def draw(self):
        Money.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX - 100, self.posY, self.sizeX, self.sizeY)
        self.numbers.draw()

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
            'magica': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'item', 'book.png')),

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
            'magica': [101, 108],

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