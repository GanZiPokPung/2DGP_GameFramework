from pico2d import *
from static import *
import game_world
import stage_scene
from bullet import Bullet
import custom_math
import static

import random

# monster pattern
class Monster_Pattern:
    monster_list = None
    difficulty = None

    def __init__(self):
        if Monster_Pattern.difficulty == None:
            Monster_Pattern.difficulty = 0

    def get_monster(self):

        select = random.randint(1, 10)

        if select < 8:
            subselect = random.randint(0, 8)
            warrior_count = random.randint(4, 7 + Monster_Pattern.difficulty)
            # warrior
            # 왼쪽위치에서 왼쪽 방향
            if subselect == 0:
                warrior_pattern_left = [Warrior(200, 800, i,'Left', 'warrior')
                                        for i in range(warrior_count)]
                warrior_pattern_left.append(Warrior(200, 800,
                                                    len(warrior_pattern_left) + 1, 'Left', 'warrior_other'))

                for monster in warrior_pattern_left :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    yield monster
            # 오른쪽위치에서 오른쪽 방향
            elif subselect == 1:
                warrior_pattern_right = [Warrior(300, 800, i, 'Right', 'warrior')
                                         for i in range(warrior_count)]
                warrior_pattern_right.append(Warrior(300, 800,
                                                     len(warrior_pattern_right) + 1, 'Right', 'warrior_other'))

                for monster in warrior_pattern_right :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    yield monster
            # 중앙 방향
            elif subselect == 2:
                warrior_pattern_center = [Warrior(300 + random.randint(-200, 200), 800, i, '', 'warrior')
                                          for i in range(warrior_count)]
                warrior_pattern_center.append(Warrior(300 + random.randint(-200, 200), 800,
                                                      len(warrior_pattern_center) + 1, '', 'warrior_other'))

                for monster in warrior_pattern_center :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    yield monster
            # 오른쪽위치에서 왼쪽 방향
            elif subselect == 3:
                warrior_pattern_left_other = [Warrior(400, 800, i,'Left', 'warrior')
                                        for i in range(warrior_count)]
                warrior_pattern_left_other.append(Warrior(400, 800,
                                                    len(warrior_pattern_left_other) + 1, 'Left', 'warrior_other'))

                for monster in warrior_pattern_left_other :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    yield monster
            # 왼쪽위치에서 오른쪽 방향
            elif subselect == 4:
                warrior_pattern_right_other = [Warrior(100, 800, i, 'Right', 'warrior')
                                               for i in range(warrior_count)]
                warrior_pattern_right_other.append(Warrior(100, 800,
                                            len(warrior_pattern_right_other) + 1, 'Right', 'warrior_other'))

                for monster in warrior_pattern_right_other :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    yield monster
            # 양쪽에서 바깥쪽 방향
            elif subselect == 5:
                warrior_pattern_left = [Warrior(200, 800, i, 'Left', 'warrior')
                                        for i in range(warrior_count)]
                warrior_pattern_left.append(Warrior(200, 800,
                                                    len(warrior_pattern_left) + 1, 'Left', 'warrior_other'))
                warrior_pattern_right = [Warrior(300, 800, i, 'Right', 'warrior')
                                         for i in range(warrior_count)]
                warrior_pattern_right.append(Warrior(300, 800,
                                                     len(warrior_pattern_right) + 1, 'Right', 'warrior_other'))

                warrior_pattern_both_out = [[warrior_pattern_left[i], warrior_pattern_right[i]]
                                               for i in range(warrior_count + 1)]

                for monster in warrior_pattern_both_out:
                    monster[0].modify_difficulty(Monster_Pattern.difficulty)
                    monster[1].modify_difficulty(Monster_Pattern.difficulty)
                    yield  monster[0]
                    yield  monster[1]
            # 양쪽에서 안쪽 방향
            elif subselect == 6:
                warrior_pattern_left_other = [Warrior(400, 800, i, 'Left', 'warrior')
                                              for i in range(warrior_count)]
                warrior_pattern_left_other.append(Warrior(400, 800,
                                                          len(warrior_pattern_left_other) + 1, 'Left', 'warrior_other'))
                warrior_pattern_right_other = [Warrior(100, 800, i, 'Right', 'warrior')
                                               for i in range(warrior_count)]
                warrior_pattern_right_other.append(Warrior(100, 800,
                                                           len(warrior_pattern_right_other) + 1, 'Right',
                                                           'warrior_other'))

                warrior_pattern_both_in = [[warrior_pattern_left_other[i], warrior_pattern_right_other[i]]
                                              for i in range(warrior_count + 1)]

                for monster in warrior_pattern_both_in:
                    monster[0].modify_difficulty(Monster_Pattern.difficulty)
                    monster[1].modify_difficulty(Monster_Pattern.difficulty)
                    yield monster[0]
                    yield monster[1]
            # 양쪽에서 왼쪽 방향
            elif subselect == 7:
                warrior_pattern_left = [Warrior(200, 800, i, 'Left', 'warrior')
                                        for i in range(warrior_count)]
                warrior_pattern_left.append(Warrior(200, 800,
                                                    len(warrior_pattern_left) + 1, 'Left', 'warrior_other'))
                warrior_pattern_left_other = [Warrior(400, 800, i, 'Left', 'warrior')
                                              for i in range(warrior_count)]
                warrior_pattern_left_other.append(Warrior(400, 800,
                                                          len(warrior_pattern_left_other) + 1, 'Left', 'warrior_other'))

                warrior_pattern_both_left = [[warrior_pattern_left[i], warrior_pattern_left_other[i]]
                                               for i in range(warrior_count + 1)]

                for monster in warrior_pattern_both_left:
                    monster[0].modify_difficulty(Monster_Pattern.difficulty)
                    monster[1].modify_difficulty(Monster_Pattern.difficulty)
                    yield  monster[0]
                    yield  monster[1]
            # 양쪽에서 오른쪽 방향
            elif subselect == 8:
                warrior_pattern_right = [Warrior(300, 800, i, 'Right', 'warrior')
                                         for i in range(warrior_count)]
                warrior_pattern_right.append(Warrior(300, 800,
                                                     len(warrior_pattern_right) + 1, 'Right', 'warrior_other'))
                warrior_pattern_right_other = [Warrior(100, 800, i, 'Right', 'warrior')
                                               for i in range(warrior_count)]
                warrior_pattern_right_other.append(Warrior(100, 800,
                                                           len(warrior_pattern_right_other) + 1, 'Right',
                                                           'warrior_other'))

                warrior_pattern_both_right = [[warrior_pattern_right[i], warrior_pattern_right_other[i]]
                                              for i in range(warrior_count + 1)]

                for monster in warrior_pattern_both_right:
                    monster[0].modify_difficulty(Monster_Pattern.difficulty)
                    monster[1].modify_difficulty(Monster_Pattern.difficulty)
                    yield monster[0]
                    yield monster[1]
        # warrior가 아닌 네임드급 몬스터들
        else:
            subselect = random.randint(0, 2)
            # Bird
            if subselect == 0:
                bird = Bird(300 + random.randint(-150, 150), 800)
                bird.modify_difficulty(Monster_Pattern.difficulty)
                yield bird
            # Dragon
            elif subselect == 1:
                dragon = Dragon(200, 800)
                dragon.modify_difficulty(Monster_Pattern.difficulty)
                yield dragon
            # Dragon_Strong
            elif subselect == 2:
                dragon_strong = Dragon_Strong(100, 800)
                dragon_strong.modify_difficulty(Monster_Pattern.difficulty)
                yield dragon_strong


##########################################################################################

# Monster Classes
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
        self.time = 0

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

    def modify_difficulty(self, difficulty):
        pass

class Warrior(Monster):
    image = None
    size = None
    def __init__(self, posX, posY, term, LRtype, imageType):
        speed = 50
        sizeX = 0.5
        sizeY = 0.5
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
        self.term = term

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
            self.shootDelay = random.randint(10, 20)
            self.shootSpeed = 20
            self.bulletsizeX = 1
            self.bulletsizeY = 1
        if self.imageType == 'warrior_other':
            self.shootDelay = random.randint(5, 10)
            self.shootSpeed = 40
            self.bulletsizeX = 2
            self.bulletsizeY = 2

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX, self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
        self.time += 0.1
        if self.time < self.term:
            return 1

        self.angle += self.anglespeed
        self.posX += math.cos(math.radians(self.angle)) * self.speed
        self.posY += math.sin(math.radians(self.angle)) * self.speed

        if self.shootTime > self.shootDelay:
            angle = custom_math.angle_between([self.posX, self.posY], [stage_scene.player.x, stage_scene.player.y])
            if self.imageType == 'warrior':
                game_world.add_object(Bullet(self.posX, self.posY, angle, self.shootSpeed, 'Small_A', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
            if self.imageType == 'warrior_other':
                game_world.add_object(Bullet(self.posX, self.posY, angle,self.shootSpeed, 'Small_B', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootTime = 0

    def modify_difficulty(self, difficulty):
        self.shootDelay /= (1 + difficulty / 10)
        self.shootSpeed *= (1 + difficulty / 10)
        self.speed      *= (1 + difficulty / 10)

class Bird(Monster):
    image = None
    def __init__(self, posX, posY):
        speed = 5
        sizeX = 2
        sizeY = 2
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 100
        self.pngSizeY = 100
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        self.bulletsizeX = 0.4
        self.bulletsizeY = 0.4
        #
        self.animTime = 0
        self.animSpeed = 0.1

        if Bird.image == None:
            Bird.image = load_image(os.path.join(os.getcwd(), 'monster', 'bird.png'))

        self.originPos = [self.posX, self.posY]
        self.moveMode = True
        self.firstMode = True
        tmpPosY = random.randint(500, 600)
        self.movePattern = [[posX, tmpPosY], [posX + random.randint(100, 200), tmpPosY]]
        self.moveLocation = 0
        self.moveT = 0
        self.speedT = 1

        self.shootDelay = 15
        self.shootterm = False

        self.shootSpeed = 100

    def draw(self):
        Bird.image.clip_draw(self.frame * self.pngSizeX, 3 * self.pngSizeY, self.pngSizeX, self.pngSizeY,
                             self.posX, self.posY,
                             self.sizeX, self.sizeY)

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
                    self.moveT += self.speedT
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
                    self.moveT += self.speedT
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
                game_world.add_object(Bullet(self.posX, self.posY, 270 - 20, self.shootSpeed, 'RedSun', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
                game_world.add_object(Bullet(self.posX, self.posY, 270, self.shootSpeed, 'RedSun', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
                game_world.add_object(Bullet(self.posX, self.posY, 270 + 20, self.shootSpeed, 'RedSun', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
                self.shootterm = True
            if self.shootTime > self.shootDelay + 3:
                game_world.add_object(Bullet(self.posX - 5, self.posY, 270 - 10, self.shootSpeed, 'RedSun', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
                game_world.add_object(Bullet(self.posX + 5, self.posY, 270 + 10, self.shootSpeed, 'RedSun', '', '',
                                             self.bulletsizeX, self.bulletsizeY), BULLET)
                self.shootTime = 0
                self.shootterm = False
                self.moveMode = True

    def modify_difficulty(self, difficulty):
        self.shootDelay /= (1 + difficulty / 10)
        self.shootSpeed *= (1 + difficulty / 10)
        self.speedT     += difficulty // 2

class Dragon(Monster):
    image = None
    def __init__(self, posX, posY):
        speed = 5
        sizeX = 2
        sizeY = 2
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 128
        self.pngSizeY = 128
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        self.bulletsizeX = 0.5
        self.bulletsizeY = 0.5
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
        self.speedT = 1

        self.shootDelay = 30
        self.shootSpeed = 40
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
                self.moveT += self.speedT
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
                self.moveT += self.speedT
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
            game_world.add_object(Bullet(self.posX, self.posY, 270 - 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX, self.posY, 270 + 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 8 - 0.1) and (self.shootTime < self.shootDelay - 8 + 0.1) \
                and (self.shootterm == False):
            game_world.add_object(Bullet(self.posX - 5, self.posY, 270 - 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX + 5, self.posY, 270 + 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 6 - 0.1) and (self.shootTime < self.shootDelay - 6 + 0.1) \
                and (self.shootterm == False):
            game_world.add_object(Bullet(self.posX, self.posY, 270 - 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX, self.posY, 270 + 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 4 - 0.1) and (self.shootTime < self.shootDelay - 4 + 0.1) \
                and (self.shootterm == False):
            game_world.add_object(Bullet(self.posX - 5, self.posY, 270 - 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX + 5, self.posY, 270 + 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 2 - 0.1) and (self.shootTime < self.shootDelay - 2 + 0.1) \
                and (self.shootterm == False):
            game_world.add_object(Bullet(self.posX, self.posY, 270 - 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX, self.posY, 270 + 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootterm = True
        elif (self.shootTime > self.shootDelay - 0 - 0.1) and (self.shootTime < self.shootDelay - 0 + 0.1) \
                and (self.shootterm == False):
            game_world.add_object(Bullet(self.posX - 5, self.posY, 270 - 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            game_world.add_object(Bullet(self.posX + 5, self.posY, 270 + 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                                         self.bulletsizeX, self.bulletsizeY), BULLET)
            self.shootterm = True
        else:
            self.shootterm = False

        if self.shootTime > self.shootDelay:
            self.shootTime = 0

    def modify_difficulty(self, difficulty):
        self.shootDelay /= (1 + difficulty / 10)
        self.shootSpeed *= (1 + difficulty / 10)
        self.speedT     += difficulty // 2

class Dragon_Strong(Monster):
    image = None

    def __init__(self, posX, posY):
        speed = 50
        sizeX = 2
        sizeY = 2
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        self.pngSizeX = 75
        self.pngSizeY = 70
        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.angle = 270
        self.bulletsizeX = 2
        self.bulletsizeY = 2
        #
        self.animTime = 0
        self.animID = 5
        if Dragon_Strong.image == None:
            Dragon_Strong.image = load_image(os.path.join(os.getcwd(), 'monster', 'dragon_other.png'))
        #
        self.originPosY = self.posY
        self.firstMode = True

        self.anglespeed = 2
        #
        self.bulletTime = 0
        self.bulletDelay = 2
        self.bulletAngle = 0

        # difficulty
        self.shootSpeed = 90

    def draw(self):
        Dragon_Strong.image.clip_draw(self.frame * self.pngSizeX, self.animID * self.pngSizeY, self.pngSizeX, self.pngSizeY, self.posX,
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
        self.bulletAngle += 2
        if self.bulletTime > self.bulletDelay:
            game_world.add_object(Bullet(self.posX, self.posY,  self.bulletAngle, self.shootSpeed, 'YellowCircle_Anim', '', 'Anim'
                                              , self.bulletsizeX, self.bulletsizeY), BULLET)
            self.bulletTime = 0

    def modify_difficulty(self, difficulty):
        self.shootDelay /= (1 + difficulty / 10)
        self.shootSpeed *= (1 + difficulty / 10)
        self.anglespeed *= (1 + difficulty / 10)