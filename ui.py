from pico2d import *
import mainframe
import title_scene
import stage_scene
import game_world
from static import *
import shop_state

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
        self.numbers_others = {}
        self.additionalImage = None
        self.additionalIdx = 0

    def set_numbers(self, x, y, sizeX, sizeY, betweenLength, num):
        if self.numbers == None:
            self.numbers = Numbers(x, y, sizeX, sizeY, betweenLength, num)
        else:
            self.numbers.setNumbers(num)

    def set_additionalimage(self, x, y, sizeX, sizeY, ID, opacify):
        self.additionalImage = Others(x, y, sizeX, sizeY, ID, opacify)

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def update_numbers(self, number):
        pass

    def update_additionalImage(self, idx):
        pass

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

        if len(self.numbers_others) != 0:
            for numbers in self.numbers_others.values():
                numbers.draw()

        if self.additionalImage != None:
            self.additionalImage.draw()

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

class Button(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, imageID, processID):
        UI.__init__(self)
        # ID
        self.uiID = 'button'
        self.buttonImageID = imageID
        self.buttonProcessID = processID

        # position
        self.posX, self.posY = x, y

        # image
        if Button.image == None:
            self.initialize_image()
        self.image = Button.image.get(self.buttonImageID)

        # size
        if Button.size == None:
            self.initialize_size()
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = Button.size.get(self.buttonImageID)[0]
        self.pngSizeY = Button.size.get(self.buttonImageID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        self.rectSizeX = self.sizeX / 2
        self.rectSizeY = self.sizeY / 2

        # check
        self.clickCheck = False

        #sound
        self.collideSound = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'ui', 'buttoncollide.wav'))
        self.collideSound.set_volume(100)
        self.clickSound = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'ui', 'click2_other.wav'))
        self.clickSound.set_volume(50)

    def initialize_image(self):
        Button.image = {
            'start': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'start.png')),
            'quit': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'quit.png')),
            'default': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'default.png')),
            'restart': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'restart.png')),
            'confirm': load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'button', 'confirm.png'))
        }

    def initialize_size(self):
        Button.size = {
            'start': [497, 134],
            'quit': [497, 134],
            'default':  [99, 99],
            'restart': [301, 99],
            'confirm': [273, 82]
        }

    def collideActive(self, opponent):
        # clicked
        if self.clickCheck == True:
            self.sizeX = self.pngSizeX * self.originSizeX * 0.9
            self.sizeY = self.pngSizeY * self.originSizeY * 0.9
            # Number size change
            if self.numbers != None:
                self.numbers.setSize(0.9, 0.9)
            # AdditionalImage size change
            if self.additionalImage != None:
                self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX * 0.9
                self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY * 0.9
        # non clicked
        else:
            self.sizeX = self.pngSizeX * self.originSizeX * 1.15
            self.sizeY = self.pngSizeY * self.originSizeY * 1.15
            # Number size change
            if self.numbers != None:
                self.numbers.setSize(1.15, 1.15)
            # AdditionalImage size change
            if self.additionalImage != None:
                self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX * 1.15
                self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY * 1.15

        if self.collideCheck == False:
            self.collideSound.play()
            self.collideCheck = True

    def collideInactive(self, opponent):
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        # Number size change
        if self.numbers != None:
            self.numbers.setOriginSize()
        # AdditionalImage size change
        if self.additionalImage != None:
            self.additionalImage.sizeX = self.additionalImage.pngSizeX * self.additionalImage.originSizeX
            self.additionalImage.sizeY = self.additionalImage.pngSizeY * self.additionalImage.originSizeY

        self.collideCheck = False

    def click(self):
        if self.clickCheck == False:
            self.clickSound.play()
            self.clickCheck = True

    def unclick(self):
        self.clickCheck = False
        if self.buttonProcessID == 'start':
            mainframe.change_state(stage_scene)
        elif self.buttonProcessID == 'quit':
            mainframe.quit()
        elif self.buttonProcessID == 'resume':
            mainframe.pop_state()
        elif self.buttonProcessID == 'confirm':
            mainframe.change_state(title_scene)
        # shop upgrade buttons
        elif self.buttonProcessID == 'attUpgrade':
            price = self.numbers_others[1].num
            moneyCheck = game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-price)
            if moneyCheck == False:
                return
            if self.numbers.num < 13:
                self.set_numbers(0, 0, 0, 0, 0, self.numbers.num + 1)
            self.additionalImage.setOtherImageToIndex(int(self.additionalImage.othersID) + 1)
            attCheck =  game_world.curtain_object(PLAYER, 0).parsingAttData(self.additionalImage.othersID)
            if attCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(price)
            price *= 2
            self.numbers_others[1].setNumbers(int(price))
            shop_state.price = price
        elif self.buttonProcessID == 'lifeUpgrade':
            moneyCheck = game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-1000)
            if moneyCheck == False:
                 return
            heartCheck = game_world.curtain_object(PLAYER, 0).parsingHPBar(50)
            if heartCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(1000)
        elif self.buttonProcessID == 'magicaUpgrade':
            moneyCheck = game_world.curtain_object(PLAYER, 0).parsingMoneyBar(-10000)
            if moneyCheck == False:
                return
            bombCheck = game_world.curtain_object(PLAYER, 0).parsingBombBar(1)
            if bombCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(10000)

    def click_right(self):
        if self.clickCheck == False:
            self.clickSound.play()
            self.clickCheck = True

    def unclick_right(self):
        self.clickCheck = False
        if self.buttonProcessID == 'attUpgrade':
            if self.numbers.num - 1 > 0:
                self.set_numbers(0, 0, 0, 0, 0, self.numbers.num - 1)
            else:
                return
            price = self.numbers_others[1].num
            self.additionalImage.setOtherImageToIndex(int(self.additionalImage.othersID) - 1)
            attCheck = game_world.curtain_object(PLAYER, 0).parsingAttData(self.additionalImage.othersID)
            if attCheck == False:
                game_world.curtain_object(PLAYER, 0).parsingMoneyBar(price)
            price //= 2
            game_world.curtain_object(PLAYER, 0).parsingMoneyBar(price)
            self.numbers_others[1].setNumbers(int(price))
            shop_state.price = price

#
class Numbers(UI):
    def __init__(self, x, y, sizeX, sizeY, between, num):
        UI.__init__(self)
        self.uiID = 'numbers'
        self.numberList = []
        self.numberValueList = []
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.between = between
        self.num = 0
        self.setNumbers(num)

    # 숫자를 쪼개어 알맞는 스프라이트로 만들어주는 작업
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

    # change size
    def setSize(self, sizeX, sizeY):
        for n in self.numberList:
            n.setSize(sizeX, sizeY)

    # change size
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
        self.uiID = 'number'
        # position
        self.posX, self.posY = x, y
        # image
        if Number.image == None:
            Number.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Number',  'number2.png'))
        # size
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = 10
        self.pngSizeY = 14
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY
        # frame
        self.frame = idx;

    def setNumberIdx(self, idx):
        self.frame = idx;

    # change size
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
        self.uiID = 'bombbar'
        self.posX, self.posY = x, y
        self.bombs = []
        self.bombCount = bombCount
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
        self.uiID = 'bomb'
        # image
        if Bomb.image == None:
            Bomb.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'thunder.png'))
        self.image = Bomb.image
        # position
        self.posX, self.posY = x, y
        # size
        self.originSizeX = 0.015
        self.originSizeY = 0.015
        self.moveSizeX = self.originSizeX
        self.moveSizeY = self.originSizeY
        self.pngSizeX = 2400
        self.pngSizeY = 2400
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

class HPBar(UI):
    def __init__(self, x, y, hp):
        UI.__init__(self)
        self.uiID = 'hpbar'
        self.posX, self.posY = x, y
        self.hearts = []
        self.divideNum = 50
        self.hp = hp
        self.setHPImage(hp)

    # 체력에 맞게 HP 이미지를 만들어 주는 작업
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
        self.uiID = 'heart'
        self.moveID = 'big'
        # position
        self.posX, self.posY = x, y
        # image
        if Heart.image == None:
            Heart.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'heart.png'))
        self.image = Heart.image

        self.hp = hp

        # size
        self.originSizeX = 0.25 * (self.hp * (1 / divide))
        self.originSizeY = 0.25 * (self.hp * (1 / divide))
        self.moveSizeX = self.originSizeX
        self.moveSizeY = self.originSizeY
        self.pngSizeX = 170
        self.pngSizeY = 150
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY


        # heart가 움직이는 속도
        self.hpDifferSpeed = 0.5

    # 하트를 움직임
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
        self.uiID = 'score'
        self.posX, self.posY = x, y
        self.score = score
        self.numbers = Numbers(self.posX, self.posY, 2, 2, 17, self.score)

    def setScore(self, score):
        # 스코어 숫자에 제한을 걸음
        if score > 99999999:
            return
        self.score = score
        self.numbers.setNumbers(self.score)

    def draw(self):
        self.numbers.draw()

class Money(UI):
    image = None
    def __init__(self, x, y, sizeImg, imgFar, sizeNum, between, money):
        UI.__init__(self)
        self.uiID = 'money'
        # position
        self.posX, self.posY = x, y
        # image
        if Money.image == None:
            Money.image =  load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'money.png'))
        # size
        self.originSizeX = 0.05 * sizeImg
        self.originSizeY = 0.05 * sizeImg
        self.pngSizeX = 600
        self.pngSizeY = 600
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        self.far = imgFar
        self.money = money
        self.numbers = Numbers(self.posX, self.posY, sizeNum, sizeNum, between, self.money)


    def setMoney(self, money):
        if money > 99999999:
            return
        self.money = money
        self.numbers.setNumbers(self.money)

    def draw(self):
        Money.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX - self.far, self.posY, self.sizeX, self.sizeY)
        self.numbers.draw()

class Others(UI):
    image = None
    size = None
    def __init__(self, x, y, sizeX, sizeY, ID, opacify):
        UI.__init__(self)
        self.uiID = 'others'
        self.othersID = ID
        # position
        self.posX, self.posY = x, y
        # image
        if Others.image == None:
            self.initialize_image()
        self.image = Others.image.get(self.othersID)
        # size
        if Others.size == None:
            self.initialize_size()
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.pngSizeX = Others.size.get(self.othersID)[0]
        self.pngSizeY = Others.size.get(self.othersID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        # alpha
        self.opacify = opacify
        self.image.opacify(self.opacify)

    # default image
    def setOtherImageID(self, ID):
        self.othersID = ID
        self.image = Others.image.get(self.othersID)
        self.pngSizeX = Others.size.get(self.othersID)[0]
        self.pngSizeY = Others.size.get(self.othersID)[1]
        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

    # for att upgrade bullet image
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
            # pngSizeXY, SizeXY
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