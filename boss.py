from pico2d import *
from static import *
import static
import custom_math
import game_world
import random

class Boss:
    def __init__(self, posX, posY, speed, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        self.speed = speed / 10
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.frame = 0
        self.shootTime = 0
        self.shootDelay = 0
        self.time = 0

    def initialize(self):
        pass

    def update(self):
        self.shootTime += 0.1
        self.time

        self.update_AI()
        self.update_anim()

    def draw(self):
        pass

    def update_anim(self):
        pass

    def update_AI(self):
        pass

    def modify_difficulty(self, difficulty):
        pass

class BossHead(Boss):
    image = None
    def __init__(self):
        posX = 250
        posY = 950
        speed = 10
        sizeX = 1.75
        sizeY = 1.75
        Boss.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 259
        self.pngSizeY = 125
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY

        self.bulletsizeX = 0.4
        self.bulletsizeY = 0.4

        self.originPos = [self.posX, self.posY]
        self.moveMode = True
        self.firstMode = True

        self.moveLocation = 0
        self.moveT = 0
        self.speedT = 0.2

        self.shootDelay = 15
        self.shootterm = False

        self.shootSpeed = 100

        if BossHead.image == None:
            BossHead.image = load_image(os.path.join(os.getcwd(), 'boss', 'head.png'))

        #hand
        self.initialize()

    def initialize(self):
        game_world.add_object(BossHand('Left', self), BOSS)
        game_world.add_object(BossHand('Right', self), BOSS)

    def draw(self):
        BossHead.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
       if self.firstMode == True:
            if self.moveT >= 100:
                self.firstMode = False
                self.moveMode = False
                self.moveT = 0
            else:
                self.moveT += self.speedT
                self.posX, self.posY = custom_math.move_line(self.originPos,
                                                         [250, 570],
                                                         self.moveT)

    def modify_difficulty(self, difficulty):
        pass

class BossHand(Boss):
    image = None

    def __init__(self, type, headinfo):
        posX = 0
        posY = 0
        speed = 10
        sizeX = 1.75
        sizeY = 1.75
        Boss.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 85
        self.pngSizeY = 49
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        self.bulletsizeX = 0.4
        self.bulletsizeY = 0.4

        self.originPos = [self.posX, self.posY]
        self.moveMode = True
        self.firstMode = True

        self.moveLocation = 0
        self.moveT = 0
        self.speedT = 1

        self.shootDelay = 15
        self.shootterm = False

        self.shootSpeed = 100

        if BossHand.image == None:
            BossHand.image = {'Left': load_image(os.path.join(os.getcwd(), 'boss', 'Hand_L.png')),
                              'Right': load_image(os.path.join(os.getcwd(), 'boss', 'Hand_R.png'))}

        self.type = type
        self.image = BossHand.image.get(self.type)
        self.headinfo = headinfo

    def initialize(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
        if self.type == 'Left':
            self.posX = self.headinfo.posX - 160
            self.posY = self.headinfo.posY - 100
            self.angle += 5

        elif self.type == 'Right':
            self.posX = self.headinfo.posX + 160
            self.posY = self.headinfo.posY - 100
            self.angle -= 5

        self.posX = self.posX + math.cos(math.radians(self.angle)) * 4
        self.posY = self.posY + math.sin(math.radians(self.angle)) * 4

    def modify_difficulty(self, difficulty):
        pass