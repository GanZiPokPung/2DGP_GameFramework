from pico2d import *
from static import *
from bullet import Bullet
import static
import custom_math
import game_world
import random
import stage_scene

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

        self.delayCheck = False
        self.delayTerm = 0
        self.delayTime = 0

    def initialize(self):
        pass

    def update(self):
        self.shootTime += 0.1
        self.time += 0.1

        if self.delayCheck == True:
            self.delayTime += 0.1

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

        # size
        self.pngSizeX = 259
        self.pngSizeY = 125

        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY

        self.originPos = [self.posX, self.posY]
        self.startPos = [250, 570]
        self.currentPos = []
        self.movePattern = [self.startPos,
                            [self.startPos[0] - 5, self.startPos[1] - 5],
                            [self.startPos[0] + 5, self.startPos[1] + 5],
                            [self.startPos[0] + 5, self.startPos[1] - 5],
                            [self.startPos[0] - 5, self.startPos[1] + 5]]

        self.firstMode = True
        self.moveMode = False
        self.attackMode = False
        self.attacking = False
        self.attackInfoInit = False
        self.attackID = 99

        self.attackingTime = 0
        self.attackDelay = 0

        self.moveT_Curv = 0
        self.moveLocation = 2
        self.moveT = 0
        self.speedT = 0.2

        self.shootDelay = 0
        self.shootSpeed = 0
        self.bulletsizeX = 0
        self.bulletsizeY = 0
        self.shootMax = 0
        self.shootCount = 0
        self.shootterm = False
        self.shootAngle = 0
        self.LR_decision = 0

        if BossHead.image == None:
            BossHead.image = load_image(os.path.join(os.getcwd(), 'boss', 'head.png'))

        #hand
        self.initialize()

    def initialize(self):
        self.BossHandLeft = BossHand('Left', self)
        self.BossHandRight = BossHand('Right', self)
        game_world.add_object(self.BossHandLeft, BOSS)
        game_world.add_object( self.BossHandRight, BOSS)

    def draw(self):
        BossHead.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
        # move
       if self.firstMode == True:
            if self.moveT >= 100:
                self.firstMode = False
                self.moveMode = True
                self.moveT = 0
            else:
                self.moveT += self.speedT
                self.posX, self.posY = custom_math.move_line(self.originPos,
                                                             self.startPos,
                                                             self.moveT)
       else:
           if self.moveMode == True:
                if self.moveT_Curv >= 100:
                    self.moveT_Curv = 0
                    if self.moveLocation == 4:
                        self.moveLocation = 0
                    else:
                        self.moveLocation += 1
                else:
                    self.moveT_Curv += self.speedT * 5
                    if self.moveLocation == 4:
                        dstLocation = 0
                    else:
                        dstLocation = self.moveLocation + 1
                    self.posX, self.posY = custom_math.move_curve(self.movePattern[self.moveLocation - 3],
                                                                  self.movePattern[self.moveLocation - 2],
                                                                  self.movePattern[self.moveLocation - 1],
                                                                  self.movePattern[self.moveLocation],
                                                                  self.moveT_Curv)

           if self.attackID == 0:
               check = self.Pattern_Normal()
               if check == False:
                   self.attackID = 99
           elif self.attackID == 1:
               check = self.Pattern_Lazer_One()
               if check == False:
                   self.attackID = 99
           elif self.attackID == 2:
                check = self.Pattern_Lazer_Two()
                if check == False:
                    self.attackID = 99
           elif self.attackID == 3:
                check = self.Pattern_Hand_One()
                if check == False:
                    self.attackID = 99
           elif self.attackID == 4:
                check = self.Pattern_Hand_Two()
                if check == False:
                    self.attackID = 99

                        # normal attack
                    # self.Pattern_Normal()
                    # self.Pattern_Lazer_One()
                    # self.Pattern_Lazer_Two()

                    # self.moveMode = False
                    # self.currentPos = [self.posX, self.posY]



           # special attack
           # else:
           #     if self.attackMode == False:
           #         if self.moveT >= 100:
           #             self.attackMode = True
           #             self.moveT = 0
           #             self.moveLocation = 2
           #         else:
           #             self.moveT += self.speedT * 2
           #             self.posX, self.posY = custom_math.move_line(self.currentPos,
           #                                                          self.startPos,
           #                                                          self.moveT)


    def modify_difficulty(self, difficulty):
        pass

    def Pattern_Normal(self):
        if self.attackInfoInit == False:
            self.shootDelay = 0.5
            self.shootSpeed = 50
            self.bulletsizeX = 1
            self.bulletsizeY = 1
            self.shootMax = 30
            self.attackInfoInit = True

        if self.shootTime > self.shootDelay:
            self.shootAngle = random.randint(270 - 40, 270 + 40)

            game_world.add_object(Bullet(self.posX, self.posY - 50, self.shootAngle ,
                                    self.shootSpeed, 'Small_A', '', '',
                                    self.bulletsizeX, self.bulletsizeY), BULLET)

            self.shootTime = 0
            self.shootCount += 1

        if self.shootCount > self.shootMax:
            self.shootCout = 0
            self.attackInfoInit = False
            return False
        else:
            return True

    def Pattern_Lazer_One(self):
        if self.attackInfoInit == False:
            self.shootDelay = 0.5
            self.shootSpeed = 100
            self.bulletsizeX = 0.7
            self.bulletsizeY = 0.7

            self.LR_decision = random.randint(0, 1)

            if self.LR_decision == 0:
                self.shootAngle = 270 - 80
            else:
                self.shootAngle = 270 + 80

            self.time = 0
            self.attackingTime = 5
            self.delayTerm = 5

            self.delayCheck = False
            self.attackInfoInit = True

        if self.delayCheck == False:
            if self.time > self.attackingTime:
                self.delayCheck = True
        else:
            if self.delayTime > self.delayTerm:
                self.delayCheck = False
                self.delayTime = 0
                self.time = 0

        if self.LR_decision == 0:
            self.shootAngle += 0.5
        else:
            self.shootAngle -= 0.5

        if self.shootTime > self.shootDelay:
            if self.delayCheck == False:
                game_world.add_object(Bullet(self.posX - 40, self.posY + 5, self.shootAngle,
                                             self.shootSpeed, 'Y', '', 'Anim',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
                game_world.add_object(Bullet(self.posX + 40, self.posY + 5, self.shootAngle,
                                             self.shootSpeed, 'Y', '', 'Anim',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)

            self.shootTime = 0

        if self.LR_decision == 0:
            if self.shootAngle > 270 + 80:
                self.attackInfoInit = False
                return False
        else:
            if self.shootAngle < 270 - 80:
                self.attackInfoInit = False
                return False

        return True

    def Pattern_Lazer_Two(self):
        if self.attackInfoInit == False:
            self.shootDelay = 0.5
            self.shootSpeed = 100
            self.bulletsizeX = 1.5
            self.bulletsizeY = 1.5
            self.shootAngle = 0
            self.attackInfoInit = True

        self.shootAngle += 0.4

        if self.shootTime > self.shootDelay:
            game_world.add_object(Bullet(self.posX - 40, self.posY, 180 + self.shootAngle,
                                         self.shootSpeed, 'BlueCircle_Anim', '', 'Anim',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX + 40, self.posY, 360 - self.shootAngle,
                                         self.shootSpeed, 'BlueCircle_Anim', '', 'Anim',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)

            self.shootTime = 0


        if self.shootAngle > 85:
            self.attackInfoInit = False
            return False

        return True

    def Pattern_Hand_One(self):
        self.BossHandLeft.attackID = 0
        self.BossHandRight.attackID = 0

    def Pattern_Hand_Two(self):
        self.BossHandLeft.moveMode = False
        self.BossHandRight.moveMode = False

class BossHand(Boss):
    image = None
    def __init__(self, type, headinfo):
        posX = 0
        posY = 0
        speed = 10
        sizeX = 1.75
        sizeY = 1.75
        Boss.__init__(self, posX, posY, speed, sizeX, sizeY)
        # size
        self.pngSizeX = 85
        self.pngSizeY = 49
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY

        self.angle = 270

        self.moveMode = True
        self.attackMode = False
        self.attackInfoInit = False
        self.attackID = 99

        self.moveLocation = 0
        self.moveT = 0
        self.speedT = 1

        self.shootDelay = 0
        self.shootSpeed = 0
        self.bulletsizeX = 0
        self.bulletsizeY = 0
        self.shootMax = 0
        self.shootCount = 0
        self.shootterm = False
        self.shootAngle = 0
        self.tmpCount = 0

        if BossHand.image == None:
            BossHand.image = {'Left': load_image(os.path.join(os.getcwd(), 'boss', 'Hand_L.png')),
                              'Right': load_image(os.path.join(os.getcwd(), 'boss', 'Hand_R.png'))}

        self.type = type
        self.image = BossHand.image.get(self.type)
        self.headinfo = headinfo

        self.originPosX = []
        self.originPosY = []
        self.startPos   = []
        self.currentPos = []

    def initialize(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
        if self.moveMode == True :
            if self.attackMode == False:
                if self.type == 'Left':
                    self.originPosX = self.headinfo.posX - 160
                    self.originPosY = self.headinfo.posY - 100
                    self.angle += 5

                elif self.type == 'Right':
                    self.originPosX = self.headinfo.posX + 160
                    self.originPosY = self.headinfo.posY - 100
                    self.angle -= 5

                self.startPos = [self.originPosX, self.originPosY]
                self.posX = self.originPosX + math.cos(math.radians(self.angle)) * 4
                self.posY = self.originPosY + math.sin(math.radians(self.angle)) * 4
                self.currentPos = [self.posX, self.posY]

                if self.attackID == 0:
                    check = self.Pattern_Normal()
                    if check == False:
                        self.attackID = 99

            else:
                if self.moveT >= 100:
                    self.attackMode = False
                    self.moveT = 0
                    self.angle = 270
                else:
                    self.moveT += self.speedT * 5
                    self.posX, self.posY = custom_math.move_line([self.startPos[0], self.startPos[1] - 90],
                                                                 self.startPos,
                                                                 self.moveT)
        else:
            if self.attackMode == False:
                if self.moveT >= 100:
                    self.attackMode = True
                    self.moveT = 0
                    self.angle = 270
                else:
                    self.moveT += self.speedT * 5
                    self.posX, self.posY = custom_math.move_line(self.currentPos,
                                                                 [self.startPos[0], self.startPos[1] - 90],
                                                                 self.moveT)
            else:
                check = self.Pattern_Special_One()
                if check == False:
                    self.attackMode = False

    def modify_difficulty(self, difficulty):
        pass

    def Pattern_Normal(self):
        if self.attackInfoInit == False:
            self.shootDelay = random.randint(8, 10)
            self.shootSpeed = 80
            self.bulletsizeX = 2
            self.bulletsizeY = 2
            self.shootMax = 30

            self.time = 0
            self.tmpCount = 0
            self.delayTerm = 0.5

            self.delayCheck = False
            self.attackInfoInit = True

        if self.shootTime > self.shootDelay:
            if self.delayCheck == False:
                self.shootAngle = custom_math.angle_between([self.posX, self.posY],
                                                            [stage_scene.player.x, stage_scene.player.y])
                self.delayCheck = True
            else:
                if self.delayTime > self.delayTerm:
                    game_world.add_object(Bullet(self.posX, self.posY - 10, self.shootAngle,
                                                self.shootSpeed, 'Small_A', '', '',
                                                self.bulletsizeX, self.bulletsizeY), BOSSBULLET)
                    self.shootCount += 1
                    self.tmpCount += 1
                    self.delayTime = 0

                    if self.tmpCount > 2:
                        self.delayCheck = False
                        self.tmpCount = 0

            if self.delayCheck == False:
                self.shootTime = 0
                self.shootDelay = random.randint(8, 10)

        if self.shootCount > self.shootMax:
            self.shootCount = 0
            self.attackInfoInit = False
            return False
        else:
            return True

    def Pattern_Special_One(self):
        if self.attackInfoInit == False:
            self.shootDelay = 0.75
            self.shootSpeed = 50
            self.bulletsizeX = 2
            self.bulletsizeY = 2
            self.shootMax = 100
            self.attackInfoInit = True

        if self.shootTime > self.shootDelay:
            self.shootAngle = random.randint(270 - 60, 270 + 60)

            tmpbullet = Bullet(self.posX, self.posY - 50, self.shootAngle ,
                                    self.shootSpeed, 'Missile', '', 'RotateOnce',
                                    self.bulletsizeX, self.bulletsizeY)
            tmpbullet.rotAngle = self.shootAngle - 270
            game_world.add_object(tmpbullet, BOSSBULLET)

            self.shootTime = 0
            self.shootCount += 1

        if self.shootCount > self.shootMax:
            self.shootCout = 0
            self.attackInfoInit = False
            return False
        else:
            return True