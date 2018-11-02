from pico2d import *
from static import *
import game_world
import stage_scene
from bullet import Bullet
import custom_math
import static

import random

class Monster:
    def __init__(self, posX, posY, speed, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        self.speed = speed / 10
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.frame = 0
        self.shootTime = 0
        self.shootDelay = 0

    def initialize(self):
        pass

    def update(self):
        self.shootTime += 0.1

        self.update_AI()
        self.update_anim()

        # 맵 밖을 나가면 몬스터를 없앤다.
        if (self.posX < 0 - self.sizeX) or (self.posX > static.canvas_width + self.sizeX):
            return True
        elif (self.posY < 0 - self.sizeY):
            return True
        else:
            return False

    def draw(self):
        pass

    def update_anim(self):
        pass

    def update_AI(self):
        pass


class Warrior(Monster):
    image = None
    size = None
    def __init__(self, posX, posY, speed, sizeX, sizeY, LRtype, imageType):
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.LRtype = LRtype
        self.imageType = imageType
        #
        if Warrior.image == None:
            self.initialize_image()
        self.image = Warrior.image.get(self.imageType)
        if Warrior.size == None:
            self.initialize_size()
        self.pngSizeX = Warrior.size.get(self.imageType)[0]
        self.pngSizeY = Warrior.size.get(self.imageType)[1]
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        #
        self.initialize()
        #

    def initialize_image(self):
        Warrior.image = {'warrior': load_image(os.path.join(os.getcwd(), 'monster', 'warrior.png')),
                         'warrior_other': load_image(os.path.join(os.getcwd(), 'monster', 'warrior_other.png'))
                         }

    def initialize_size(self):
        Warrior.size = {'warrior': [163, 173],
                         'warrior_other': [147, 142]
                         }

    def initialize(self):
        if self.LRtype == 'Right' :
            # 나가는 오른쪽으로 점을 찍음
            self.anglespeed = 0.2
        elif self.LRtype == 'Left' :
            # 나가는 왼쪽으로 점을 찍음
            self.anglespeed = -0.2
        else :
            # 돌진
            self.anglespeed = 0

        if self.imageType == 'warrior':
            self.shootDelay = 8
        if self.imageType == 'warrior_other':
            self.shootDelay = 6

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX, self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
        self.angle += self.anglespeed
        self.posX += math.cos(math.radians(self.angle)) * self.speed
        self.posY += math.sin(math.radians(self.angle)) * self.speed

        if self.shootTime > self.shootDelay:
            angle = custom_math.angle_between([self.posX, self.posY], [stage_scene.player.x, stage_scene.player.y])
            if self.imageType == 'warrior':
                game_world.add_object(Bullet(self.posX, self.posY, angle, 20, 'Small_A', '', 1, 1), BULLET)
            if self.imageType == 'warrior_other':
                game_world.add_object(Bullet(self.posX, self.posY, angle, 40, 'Small_B', '', 2, 2), BULLET)
            self.shootTime = 0

    def modify_difficulty(self):
        pass

class Bird(Monster):
    image = None
    def __init__(self, posX, posY, speed, sizeX, sizeY):
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 100
        self.pngSizeY = 100
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        #
        self.animTime = 0
        self.animSpeed = 0.1

        if Bird.image == None:
            Bird.image = load_image(os.path.join(os.getcwd(), 'monster', 'bird.png'))

        self.originPos = [self.posX, self.posY]
        self.moveMode = True
        self.firstMode = True
        tmpPosY = random.randint(500, 600)
        self.movePattern = [[posX, tmpPosY],[posX + random.randint(100, 200), tmpPosY]]
        self.moveLocation = 0
        self.moveT = 0

        self.shootDelay = 15
        self.shootterm = False

    def draw(self):
        Bird.image.clip_draw(self.frame * self.pngSizeX, 3 * self.pngSizeY, self.pngSizeX, self.pngSizeY, self.posX, self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        self.animTime += self.animSpeed
        if self.animTime > 0.8:
            self.frame = (self.frame + 1) % 4
            self.animTime = 0

    def update_AI(self):
        #self.angle += self.anglespeed
        if self.moveMode == True:
            self.animSpeed = 0.15
            if self.firstMode == True:
                if self.moveT >= 100:
                    self.animSpeed = 0.1
                    self.firstMode = False
                    self.moveMode = False
                    self.moveT = 0
                else:
                    self.moveT += 1
                    self.posX, self.posY = custom_math.move_line(self.originPos,
                                                             self.movePattern[self.moveLocation],
                                                             self.moveT)
            else:
                if self.moveT >= 100:
                    self.animSpeed = 0.1
                    self.moveMode = False
                    self.moveT = 0
                    if self.moveLocation == 1:
                        self.moveLocation = 0
                    else:
                        self.moveLocation = 1
                else:
                    self.moveT += 1
                    if self.moveLocation == 1:
                        self.posX, self.posY = custom_math.move_line(self.movePattern[1],
                                                                     self.movePattern[0],
                                                                     self.moveT)
                    else:
                        self.posX, self.posY = custom_math.move_line(self.movePattern[0],
                                                                     self.movePattern[1],
                                                                     self.moveT)
        elif self.shootTime > self.shootDelay:
            if  self.shootterm == False:
                stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 - 10, 30, 'BlueCircle', '', 0.75, 0.75))
                stage_scene.bullets.append(Bullet(self.posX, self.posY, 270, 30, 'BlueCircle', '', 0.75, 0.75))
                stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 + 10, 30, 'BlueCircle', '', 0.75, 0.75))
                self.shootterm = True
            if self.shootTime > self.shootDelay + 3:
                stage_scene.bullets.append(Bullet(self.posX - 5, self.posY, 270 - 5, 30, 'BlueCircle', '', 0.75, 0.75))
                stage_scene.bullets.append(Bullet(self.posX + 5, self.posY, 270 + 5, 30, 'BlueCircle', '', 0.75, 0.75))
                self.shootTime = 0
                self.shootterm = False
                self.moveMode = True

    def modify_difficulty(self):
        pass

class Dragon(Monster):
    image = None
    def __init__(self, posX, posY, speed, sizeX, sizeY):
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 128
        self.pngSizeY = 128
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        #
        self.animTime = 0
        self.animSpeed = 0.1

        if Dragon.image == None:
            Dragon.image = load_image(os.path.join(os.getcwd(), 'monster', 'dragon.png'))

        self.originPos = [self.posX, self.posY]
        self.firstMode = True
        self.movePattern = [[100, 670], [400, 500], [400, 670], [100, 500]]
        self.moveLocation = 0
        self.moveT = 0

        self.shootDelay = 30
        self.shootterm = False

    def draw(self):
        Dragon.image.clip_draw(self.frame * self.pngSizeX, 3 * self.pngSizeY, self.pngSizeX, self.pngSizeY, self.posX,
                               self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        self.animTime += self.animSpeed
        if self.animTime > 0.55:
            self.frame = (self.frame + 1) % 4
            self.animTime = 0

    def update_AI(self):
        #self.angle += self.anglespeed
        if self.firstMode == True:
            if self.moveT >= 100:
                self.firstMode = False
                self.moveT = 0
            else:
                self.moveT += 1
                self.posX, self.posY = custom_math.move_line(self.originPos,
                                                             self.movePattern[2],
                                                             self.moveT)
        else:
            if self.moveT >= 100:
                self.moveT = 0
                if self.moveLocation == 3:
                    self.moveLocation = 0
                else:
                    self.moveLocation += 1
            else:
                self.moveT += 1
                if self.moveLocation == 3:
                    dstLocation = 0
                else:
                    dstLocation = self.moveLocation + 1
                self.posX, self.posY = custom_math.move_curve(self.movePattern[self.moveLocation - 3],
                                                              self.movePattern[self.moveLocation - 2],
                                                              self.movePattern[self.moveLocation - 1],
                                                              self.movePattern[self.moveLocation],
                                                              self.moveT)
        self.shootTime += 0.01
        if (self.shootTime > self.shootDelay - 10 - 0.1) and (self.shootTime < self.shootDelay - 10 + 0.1)\
                and (self.shootterm == False):
            stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 - 30, 40, 'BlueCircle', '', 1, 1))
            stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 + 30, 40, 'BlueCircle', '', 1, 1))
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 8 - 0.1) and (self.shootTime < self.shootDelay - 8 + 0.1) \
                and (self.shootterm == False):
            stage_scene.bullets.append(Bullet(self.posX - 5, self.posY, 270 - 5, 40, 'BlueCircle', '', 1, 1))
            stage_scene.bullets.append(Bullet(self.posX + 5, self.posY, 270 + 5, 40, 'BlueCircle', '', 1, 1))
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 6 - 0.1) and (self.shootTime < self.shootDelay - 6 + 0.1) \
                and (self.shootterm == False):
            stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 - 30, 40, 'BlueCircle', '', 1, 1))
            stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 + 30, 40, 'BlueCircle', '', 1, 1))
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 4 - 0.1) and (self.shootTime < self.shootDelay - 4 + 0.1) \
                and (self.shootterm == False):
            stage_scene.bullets.append(Bullet(self.posX - 5, self.posY, 270 - 5, 40, 'BlueCircle', '', 1, 1))
            stage_scene.bullets.append(Bullet(self.posX + 5, self.posY, 270 + 5, 40, 'BlueCircle', '', 1, 1))
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 2 - 0.1) and (self.shootTime < self.shootDelay - 2 + 0.1) \
                and (self.shootterm == False):
            stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 - 30, 40, 'BlueCircle', '', 1, 1))
            stage_scene.bullets.append(Bullet(self.posX, self.posY, 270 + 30, 40, 'BlueCircle', '', 1, 1))
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 0 - 0.1) and (self.shootTime < self.shootDelay - 0 + 0.1) \
                and (self.shootterm == False):
            stage_scene.bullets.append(Bullet(self.posX - 5, self.posY, 270 - 5, 40, 'BlueCircle', '', 1, 1))
            stage_scene.bullets.append(Bullet(self.posX + 5, self.posY, 270 + 5, 40, 'BlueCircle', '', 1, 1))
            self.shootterm = True
        else:
            self.shootterm = False

        if self.shootTime > self.shootDelay:
            self.shootTime = 0

    def modify_difficulty(self):
        pass

class Dragon_Strong(Monster):
    image = None

    def __init__(self, posX, posY, speed, sizeX, sizeY):
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 75
        self.pngSizeY = 70
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        #
        self.animTime = 0
        self.animID = 5
        if Dragon.image == None:
            Dragon.image = load_image(os.path.join(os.getcwd(), 'monster', 'dragon_other.png'))
        #
        self.originPosY = self.posY
        self.firstMode = True

        self.anglespeed = 2
        #
        self.bulletTime = 0
        self.bulletDelay = 2
        self.bulletAngle = 0

    def draw(self):
        Dragon.image.clip_draw(self.frame * self.pngSizeX, self.animID * self.pngSizeY, self.pngSizeX, self.pngSizeY, self.posX,
                               self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        self.animTime += 0.1
        if self.animTime > 0.2:
            self.frame = (self.frame + 1) % 10
            self.animTime = 0

        if (self.angle > 0) and (self.angle < 0 + 22):
            self.animID = 1
        elif (self.angle > 45) and (self.angle < 45 + 22):
            self.animID = 2
        elif (self.angle > 90) and (self.angle < 90 + 22):
            self.animID = 3
        elif (self.angle > 90 + 45) and (self.angle < 90 + 45 + 22):
            self.animID = 4
        elif (self.angle > 180) and (self.angle < 180 + 22):
            self.animID = 5
        elif (self.angle > 180 + 45) and (self.angle < 180 + 45 + 22):
            self.animID = 6
        elif (self.angle > 180 + 90) and (self.angle < 180 + 90 + 22):
            self.animID = 7
        elif (self.angle > 180 + 90 + 45) and (self.angle < 180 + 90 + 45 + 22):
            self.animID = 0

    def update_AI(self):
        self.angle += self.anglespeed
        if self.angle >= 360:
            self.angle = 0
        if self.firstMode == True:
            if self.originPosY > 550:
                self.posX += math.cos(math.radians(self.angle)) * self.speed
                self.posY += math.sin(math.radians(self.angle)) * self.speed - 2
                self.originPosY += -2
            else:
                self.firstMode = False
                self.originPosY = 550
        else:
            self.posX += math.cos(math.radians(self.angle)) * self.speed
            self.posY += math.sin(math.radians(self.angle)) * self.speed

        self.bulletTime += 0.1
        self.bulletAngle += 1
        if self.bulletTime > self.bulletDelay:
            stage_scene.bullets.append(Bullet(self.posX, self.posY,  self.bulletAngle, 100, 'BlueCircle', '', 0.5, 0.5))
            self.bulletTime = 0

    def modify_difficulty(self):
        pass