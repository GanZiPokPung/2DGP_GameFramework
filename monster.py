from pico2d import *
from static import *
import game_world
import stage_scene
from bullet import Bullet
from effect import Effect
from coin import Coin
import custom_math
import static
import mainframe

import player

import random

# monster pattern
# 몬스터가 나오는 방식을 랜덤으로 가져오는 클래스이다.
# 무한히 계속되는 게임이기 때문에 이것이 필요함
class Monster_Pattern:
    monster_list = None
    difficulty = None

    def __init__(self):
        if Monster_Pattern.difficulty == None:
            Monster_Pattern.difficulty = 1
        self.spawnDelay = 7
        self.spawnTime = self.spawnDelay * 0.5

    def update(self):
        self.spawnTime += mainframe.frame_time
        if self.spawnTime > (self.spawnDelay / (1 + Monster_Pattern.difficulty / 3)):
            self.get_monster()
            self.spawnTime = 0
            return True
        return False

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
                    game_world.add_object(monster, MONSTER)
            # 오른쪽위치에서 오른쪽 방향
            elif subselect == 1:
                warrior_pattern_right = [Warrior(300, 800, i, 'Right', 'warrior')
                                         for i in range(warrior_count)]
                warrior_pattern_right.append(Warrior(300, 800,
                                                     len(warrior_pattern_right) + 1, 'Right', 'warrior_other'))

                for monster in warrior_pattern_right :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    game_world.add_object(monster, MONSTER)
            # 중앙 방향
            elif subselect == 2:
                warrior_pattern_center = [Warrior(300 + random.randint(-200, 200), 800, i, '', 'warrior')
                                          for i in range(warrior_count)]
                warrior_pattern_center.append(Warrior(300 + random.randint(-200, 200), 800,
                                                      len(warrior_pattern_center) + 1, '', 'warrior_other'))

                for monster in warrior_pattern_center :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    game_world.add_object(monster, MONSTER)
            # 오른쪽위치에서 왼쪽 방향
            elif subselect == 3:
                warrior_pattern_left_other = [Warrior(400, 800, i,'Left', 'warrior')
                                        for i in range(warrior_count)]
                warrior_pattern_left_other.append(Warrior(400, 800,
                                                    len(warrior_pattern_left_other) + 1, 'Left', 'warrior_other'))

                for monster in warrior_pattern_left_other :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    game_world.add_object(monster, MONSTER)
            # 왼쪽위치에서 오른쪽 방향
            elif subselect == 4:
                warrior_pattern_right_other = [Warrior(100, 800, i, 'Right', 'warrior')
                                               for i in range(warrior_count)]
                warrior_pattern_right_other.append(Warrior(100, 800,
                                            len(warrior_pattern_right_other) + 1, 'Right', 'warrior_other'))

                for monster in warrior_pattern_right_other :
                    monster.modify_difficulty(Monster_Pattern.difficulty)
                    game_world.add_object(monster, MONSTER)
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
                    game_world.add_object(monster[0], MONSTER)
                    game_world.add_object(monster[1], MONSTER)
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
                    game_world.add_object(monster[0], MONSTER)
                    game_world.add_object(monster[1], MONSTER)
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
                    game_world.add_object(monster[0], MONSTER)
                    game_world.add_object(monster[1], MONSTER)
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
                    game_world.add_object(monster[0], MONSTER)
                    game_world.add_object(monster[1], MONSTER)
        # warrior가 아닌 네임드급 몬스터들
        else:
            subselect = random.randint(0, 2)
            # debug
            # subselect = random.randint(2, 2)
            # Bird
            if subselect == 0:
                bird = Bird(300 + random.randint(-70, 70), 800)
                bird.modify_difficulty(Monster_Pattern.difficulty)
                game_world.add_object(bird, MONSTER)
            # Dragon
            elif subselect == 1:
                dragon = Dragon(200, 800)
                dragon.modify_difficulty(Monster_Pattern.difficulty)
                game_world.add_object(dragon, MONSTER)
            # Dragon_Strong
            elif subselect == 2:
                dragon_strong = Dragon_Strong(50, 800)
                dragon_strong.modify_difficulty(Monster_Pattern.difficulty)
                game_world.add_object(dragon_strong, MONSTER)

##########################################################################################

# Monster Classes
class Monster:
    sound = None
    def __init__(self, posX, posY, moveSpeed, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        self.moveSpeed = moveSpeed
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.rectSizeX = 0
        self.rectSizeY = 0
        self.frame = 0
        self.shootTime = 0
        self.shootDelay = 0
        self.shootCheck = False
        self.collideCheck = False
        self.hp = 0
        self.attackDamage = 0
        self.time = 0
        self.difficulty = 1

        if Monster.sound == None:
            self.initialize_sound()

        # 부모
        self.player = None
        if len(game_world.get_layer(PLAYER)) > 0:
            self.player = game_world.curtain_object(PLAYER, 0)
            self.playerAttackDamage = self.player.attackDamage

    def initialize_sound(self):
        hit = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'hit.wav'))
        hit.set_volume(15)
        explode = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'explode.wav'))
        explode.set_volume(6)
        explode2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'bigexplode.wav'))
        explode2.set_volume(25)
        Monster.sound = {
                'hit': hit,
                # explode
                '1': explode,
                '2': explode2
        }

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY,\
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def Modify_Abilities(self):
        pass

    def collideActive(self, opponent):
        if opponent.bulletType == 'Anim_Stop':
            return

        if self.posY <= 700:
            self.hp -= opponent.attackDamage
            game_world.curtain_object(PLAYER, 0).parsingScoreBar(opponent.attackDamage * random.randint(1, 5))
            Monster.sound.get('hit').play()

    def update(self):
        self.time += mainframe.frame_time

        if self.shootCheck == True:
            self.shootTime += mainframe.frame_time

        # update
        self.update_AI()
        self.update_anim()

        # 맵 밖을 나가면 몬스터를 없앤다.
        if (self.posX < 0 - self.sizeX) or (self.posX > static.canvas_width + self.sizeX):
            return True
        elif (self.posY < 0 - self.sizeY):
            return True
        # 체력이 다되면 몬스터를 없앤다.
        elif (self.hp <= 0):
            game_world.add_object(Effect(self.posX, self.posY, 'random_effect', '', self.originSizeX, self.originSizeY),
                                  EFFECT)
            game_world.curtain_object(PLAYER, 0).parsingScoreBar(random.randint(100, 500) * self.difficulty)
            game_world.add_object(Coin(self.posX, self.posY, 1.5, 1.5, random.randint(1, 5) * (self.difficulty * 3) * 500), COIN)
            Monster.sound.get(str(random.randint(1, 2))).play()
            return True
        else:
            return False

    def draw(self):
        pass

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

    def update_anim(self):
        pass

    def update_AI(self):
        pass

    def modify_difficulty(self, difficulty):
        pass

    def modify_abilities(self):
        pass

class Warrior(Monster):
    image = None
    size = None
    rectsize = None
    def __init__(self, posX, posY, term, LRtype, imageType):
        # 초기 난이도 능력치
        moveSpeed = 30
        sizeX = 0.5
        sizeY = 0.5
        Monster.__init__(self, posX, posY, moveSpeed, sizeX, sizeY)
        # types
        self.LRtype = LRtype
        self.imageType = imageType
        # image
        if Warrior.image == None:
            self.initialize_image()
        self.image = Warrior.image.get(self.imageType)
        # png size
        if Warrior.size == None:
            self.initialize_size()
        self.pngSizeX = Warrior.size.get(self.imageType)[0]
        self.pngSizeY = Warrior.size.get(self.imageType)[1]

        rectSizeX = Warrior.rectSize.get(self.imageType)[0]
        rectSizeY = Warrior.rectSize.get(self.imageType)[1]
        # size
        self.rectSizeX = (rectSizeX // 2) * self.sizeX
        self.rectSizeY = (rectSizeY // 2) * self.sizeY

        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY

        # 아래를 바라보는게 기본
        self.angle = 270
        # 타입에 따라 다른 행동을 하도록 초기화
        self.initialize_type()
        # 한꺼번에 나오지 않게 해준다. 줄지어 나올수 있도록 도와주는 변수
        self.term = term / 3

        # abilities
        self.hp = 5
        self.attackDamage = 2
        # modify
        self.modify_abilities()

    def initialize_image(self):
        Warrior.image = {'warrior': load_image(os.path.join(os.getcwd(), 'resources', 'monster', 'warrior.png')),
                         'warrior_other': load_image(os.path.join(os.getcwd(), 'resources', 'monster', 'warrior_other.png'))
                         }

    def initialize_size(self):
        Warrior.size = {'warrior': [163, 173],
                         'warrior_other': [147, 142]
                         }
        Warrior.rectSize = {'warrior': [100, 100],
                        'warrior_other': [147, 142]
                        }

    # 타입별 어떤 행동을 할지 결정
    def initialize_type(self):
        if self.LRtype == 'Right':
            # 나가는 오른쪽으로 점을 찍음
            self.anglespeed = 0.2
        elif self.LRtype == 'Left':
            # 나가는 왼쪽으로 점을 찍음
            self.anglespeed = -0.2
        else:
            # 돌진
            self.anglespeed = 0
        if self.imageType == 'warrior':
            self.originShootDelay = random.randint(7, 10)
            self.shootSpeed = 20
            self.bulletsizeX = 1
            self.bulletsizeY = 1
        if self.imageType == 'warrior_other':
            self.originShootDelay = random.randint(4, 10)
            self.shootSpeed = 40
            self.bulletsizeX = 2
            self.bulletsizeY = 2

    # 바꿔야함, 각도를 따라 이미지가 회전하도록
    def draw(self):
        #self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY, self.posX, self.posY, self.sizeX, self.sizeY)
        self.image.clip_composite_draw(0, 0,
                                       self.pngSizeX, self.pngSizeY,
                                       math.radians(self.angle - 270), '',
                                       self.posX, self.posY,
                                       self.sizeX, self.sizeY)
    def update_anim(self):
        pass

    def update_AI(self):
        # 아직 나올 텀이 아닐때에는 AI를 update하지 않음
        if self.time < self.term:
            return 1

        self.angle += self.anglespeed
        self.posX += math.cos(math.radians(self.angle)) * self.moveSpeedPixelPerSecond * mainframe.frame_time
        self.posY += math.sin(math.radians(self.angle)) * self.moveSpeedPixelPerSecond * mainframe.frame_time

        if self.player == None:
            return 1

        if self.player.y > self.posY:
            self.shootCheck = False
        else:
            self.shootCheck = True

        if self.shootTime > self.shootDelay:
            angle = custom_math.angle_between([self.posX, self.posY], [stage_scene.player.x, stage_scene.player.y])
            if self.imageType == 'warrior':
                game_world.add_object(Bullet(self.posX, self.posY, angle, self.shootSpeed, 'Small_A', '', '',
                                             self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            if self.imageType == 'warrior_other':
                game_world.add_object(Bullet(self.posX, self.posY, angle,self.shootSpeed, 'Small_B', '', '',
                                             self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootTime = 0

    def modify_difficulty(self, difficulty):
        difficulty -= 1
        self.originShootDelay /= (1 + difficulty / 3)
        self.shootSpeed *= (1 + difficulty / 10)
        self.moveSpeed  *= (1 + difficulty / 3)
        self.hp *= (1 + difficulty / 3)
        self.attackDamage *= (1 + difficulty / 10)
        difficulty += 1
        self.difficulty = difficulty
        self.Modify_Abilities()

    def modify_abilities(self):
        # speed
        self.moveSpeedMeterPerMinute = (self.moveSpeed * 1000.0 / 60.0)
        self.moveSpeedMterPerSecond = (self.moveSpeedMeterPerMinute / 60.0)
        self.moveSpeedPixelPerSecond = (self.moveSpeedMterPerSecond * PIXEL_PER_METER)
        # delay
        self.shootDelay = self.originShootDelay / 5

class Bird(Monster):
    image = None
    def __init__(self, posX, posY):
        moveSpeed = 0
        sizeX = 2
        sizeY = 2
        Monster.__init__(self, posX, posY, moveSpeed, sizeX, sizeY)
        # image
        if Bird.image == None:
            Bird.image = load_image(os.path.join(os.getcwd(), 'resources', 'monster', 'bird.png'))
        # size of png
        self.pngSizeX = 100
        self.pngSizeY = 100

        rectSizeX = self.pngSizeX
        rectSizeY = self.pngSizeY
        # size
        self.rectSizeX = (rectSizeX // 3) * self.sizeX
        self.rectSizeY = (rectSizeY // 4) * self.sizeY

        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.bulletsizeX = 0.4
        self.bulletsizeY = 0.4
        # anim
        self.animSpeed = 50
        self.frameMax = 4
        # angle
        self.angle = 270
        # AI를 위해 초기 자리를 저장해둠
        self.originPos = [self.posX, self.posY]
        # AI Check
        self.moveMode = True
        self.firstMode = True
        # 와리가리할 포지션을 정해둠
        tempPosY = random.randint(500, 600)
        self.movePattern = [[posX, tempPosY], [posX + random.randint(100, 200), tempPosY]]
        self.moveLocation = 0
        self.moveT = 0
        self.speedT = 20
        # shoot
        self.originShootDelay = 15
        self.shootCount = 0
        self.shootSpeed = 40

        # abilities
        self.hp = 75
        self.attackDamage = 5

        self.modify_abilities()

    def draw(self):
        Bird.image.clip_draw(int(self.frame) * self.pngSizeX, 3 * self.pngSizeY, self.pngSizeX, self.pngSizeY,
                             self.posX, self.posY,
                             self.sizeX, self.sizeY)

    def update_anim(self):
        TimeToFrameQuantity = self.frameMax * self.actionPerTime * mainframe.frame_time
        self.frame = (self.frame + TimeToFrameQuantity) % 4

    def update_AI(self):
        #self.angle += self.anglespeed
        self.modify_abilities()
        # 이동 중일때
        if self.moveMode == True:
            self.animSpeed = 50
            # 처음 등장시
            if self.firstMode == True:
                self.spawn_move()
            # 이후
            else:
                self.move()
        #공격시
        elif self.shootCheck == True:
            self.animSpeed = 50 * 0.5
            self.attack()

    def spawn_move(self):
        if self.moveT >= 100:
            self.firstMode = False
            self.moveMode = False
            self.moveT = 0
            self.shootCheck = True
        else:
            self.moveT += self.speedT * mainframe.frame_time
            self.posX, self.posY = custom_math.move_line(self.originPos,
                                                         self.movePattern[self.moveLocation],
                                                         self.moveT)
    def move(self):
        if self.moveT >= 100:
            self.moveMode = False
            self.shootCheck = True
            self.moveT = 0
            if self.moveLocation == 1:
                self.moveLocation = 0
            else:
                self.moveLocation = 1
        else:
            self.moveT += self.speedT * mainframe.frame_time
            if self.moveLocation == 1:
                self.posX, self.posY = custom_math.move_line(self.movePattern[1],
                                                             self.movePattern[0],
                                                             self.moveT)
            else:
                self.posX, self.posY = custom_math.move_line(self.movePattern[0],
                                                             self.movePattern[1],
                                                             self.moveT)

    def attack(self):
        startShootPos = 15
        if self.shootCount == 0 and self.shootTime > self.shootDelay:
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 - 20, self.shootSpeed, 'RedSun', '', '',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(Bullet(self.posX, self.posY - startShootPos, 270, self.shootSpeed, 'RedSun', '', '',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 + 20, self.shootSpeed, 'RedSun', '', '',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif self.shootCount == 1 and self.shootTime > self.shootDelay * 1.25:
            game_world.add_object(
                Bullet(self.posX - 5, self.posY - startShootPos, 270 - 10, self.shootSpeed, 'RedSun', '', '',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX + 5, self.posY - startShootPos, 270 + 10, self.shootSpeed, 'RedSun', '', '',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif self.shootCount == 2 and self.shootTime > self.shootDelay * 1.5:
            self.shootTime = 0
            self.shootCount = 0
            self.moveMode = True
            self.shootCheck = False

    def modify_difficulty(self, difficulty):
        difficulty -= 1
        self.originShootDelay /= (1 + difficulty / 10)
        self.shootSpeed *= (1 + difficulty / 10)
        self.speedT     *= (1 + difficulty / 2)
        self.hp *= (1 + difficulty / 3)
        self.attackDamage *= (1 + difficulty / 10)
        difficulty += 1
        self.difficulty = difficulty
        self.modify_abilities()

    def modify_abilities(self):
        # speed
        self.timePerAction = 1.0 - self.animSpeed / 100
        self.actionPerTime = 1.0 / self.timePerAction
        # delay
        self.shootDelay = self.originShootDelay / 5

class Dragon(Monster):
    image = None
    def __init__(self, posX, posY):
        speed = 0
        sizeX = 2
        sizeY = 2
        Monster.__init__(self, posX, posY, speed, sizeX, sizeY)
        # image
        if Dragon.image == None:
            Dragon.image = load_image(os.path.join(os.getcwd(), 'resources', 'monster', 'dragon.png'))
        # size of png
        self.pngSizeX = 128
        self.pngSizeY = 128

        rectSizeX = self.pngSizeX
        rectSizeY = self.pngSizeY
        # size
        self.rectSizeX = (rectSizeX // 4) * self.sizeX
        self.rectSizeY = (rectSizeY // 3) * self.sizeY

        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        # angle
        self.angle = 270
        self.bulletsizeX = 0.5
        self.bulletsizeY = 0.5
        #
        self.animSpeed = 40
        self.frameMax = 4
        # AI를 위해 초기 위치를 저장
        self.originPos = [self.posX, self.posY]
        self.movePattern = [[100, 670], [400, 500], [400, 670], [100, 500]]
        self.moveLocation = 0
        # AI
        self.firstMode = True
        self.moveT = 0
        self.speedT = 50
        # shoot
        self.originShootDelay = 20
        self.shootCount = 0
        self.shootSpeed = 40
        self.shootterm = False

        # abilities
        self.hp = 100
        self.attackDamage = 6

        self.modify_abilities()

    def draw(self):
        Dragon.image.clip_draw(int(self.frame) * self.pngSizeX, 3 * self.pngSizeY, self.pngSizeX, self.pngSizeY, self.posX,
                               self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        TimeToFrameQuantity = self.frameMax * self.actionPerTime * mainframe.frame_time
        self.frame = (self.frame + TimeToFrameQuantity) % 4

    def update_AI(self):
        #self.angle += self.anglespeed
        self.modify_abilities()
        # 처음 등장시
        if self.firstMode == True:
            self.spawn_move()
        # 이후
        else:
            self.move()

        self.attack()
        # print(self.shootCount)

    def spawn_move(self):
        self.animSpeed = 60
        if self.moveT >= 100:
            self.firstMode = False
            self.moveT = 0
            self.shootCheck = True
        else:
            self.moveT += self.speedT * mainframe.frame_time
            self.posX, self.posY = custom_math.move_line(self.originPos,
                                                         self.movePattern[2],
                                                         self.moveT)

    def move(self):
        if self.moveT >= 100:
            self.moveT = 0
            if self.moveLocation == 3:
                self.moveLocation = 0
            else:
                self.moveLocation += 1
        else:
            self.moveT += self.speedT * mainframe.frame_time
            if self.moveLocation == 3:
                dstLocation = 0
            else:
                dstLocation = self.moveLocation + 1
            self.posX, self.posY = custom_math.move_curve(self.movePattern[self.moveLocation - 3],
                                                          self.movePattern[self.moveLocation - 2],
                                                          self.movePattern[self.moveLocation - 1],
                                                          self.movePattern[self.moveLocation],
                                                          self.moveT)

    def attack(self):
        startShootPos = (self.pngSizeY / 2 + 15)
        if (self.shootTime > self.shootDelay - self.shootDelay) \
                and (self.shootTime < self.shootDelay - self.shootDelay + 0.1) \
                and (self.shootCount == 0):
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 - 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 + 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif (self.shootTime > self.shootDelay - (self.shootDelay * 0.8) - 0.1) \
                and (self.shootTime < self.shootDelay - (self.shootDelay * 0.8) + 0.1) \
                and (self.shootCount == 1):
            game_world.add_object(
                Bullet(self.posX - 5, self.posY - startShootPos, 270 - 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX + 5, self.posY - startShootPos, 270 + 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif (self.shootTime > self.shootDelay - (self.shootDelay * 0.6) - 0.1) \
                and (self.shootTime < self.shootDelay - (self.shootDelay * 0.6) + 0.1) \
                and (self.shootCount == 2):
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 - 40, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 + 40, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif (self.shootTime > self.shootDelay - (self.shootDelay * 0.4) - 0.1) \
                and (self.shootTime < self.shootDelay - (self.shootDelay * 0.4) + 0.1) \
                and (self.shootCount == 3):
            game_world.add_object(
                Bullet(self.posX - 5, self.posY - startShootPos, 270 - 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX + 5, self.posY - startShootPos, 270 + 5, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif (self.shootTime > self.shootDelay - (self.shootDelay * 0.2) - 0.1) \
                and (self.shootTime < self.shootDelay - (self.shootDelay * 0.2) + 0.1) \
                and (self.shootCount == 4):
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 - 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 + 30, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif (self.shootTime > self.shootDelay - 0 - 0.1) \
                and (self.shootTime < self.shootDelay - 0) \
                and (self.shootCount == 5):
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 - 40, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            game_world.add_object(
                Bullet(self.posX, self.posY - startShootPos, 270 + 40, self.shootSpeed, 'RedCircle', '', 'Rotate',
                       self.bulletsizeX, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootCount += 1
        elif self.shootCount == 6:
            self.shootCount = 0

        if self.shootTime > self.shootDelay * 1.15:
            self.shootTime = 0

    def modify_difficulty(self, difficulty):
        difficulty -= 1
        self.originShootDelay /= (1 + difficulty / 5)
        self.shootSpeed *= (1 + difficulty / 10)
        self.speedT     *= (1 + difficulty / 2)
        self.hp *= (1 + difficulty / 3)
        self.attackDamage *= (1 + difficulty / 10)
        difficulty += 1
        self.difficulty = difficulty
        self.modify_abilities()

    def modify_abilities(self):
        # speed
        self.timePerAction = 1.0 - self.animSpeed / 100
        self.actionPerTime = 1.0 / self.timePerAction
        # delay
        self.shootDelay = self.originShootDelay / 5

class Dragon_Strong(Monster):
    image = None

    def __init__(self, posX, posY):
        moveSpeed = 50
        sizeX = 2
        sizeY = 2
        Monster.__init__(self, posX, posY, moveSpeed, sizeX, sizeY)
        # image
        if Dragon_Strong.image == None:
            Dragon_Strong.image = load_image(os.path.join(os.getcwd(), 'resources', 'monster', 'dragon_other.png'))
        # size of png
        self.pngSizeX = 75
        self.pngSizeY = 70

        rectSizeX = self.pngSizeX
        rectSizeY = self.pngSizeY
        # size
        self.rectSizeX = (rectSizeX // 4) * self.sizeX
        self.rectSizeY = (rectSizeY // 4) * self.sizeY

        # size
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.bulletsizeX = 2
        self.bulletsizeY = 2
        # anim
        self.frameMax = 10
        self.animSpeed = 50
        self.animID = 5

        self.angle = 270
        self.originPosY = self.posY
        self.firstMode = True

        self.anglespeed = 150
        self.bulletAngle = 0
        self.bulletAngleSpeed = 50
        #
        self.originShootDelay = 2

        # difficulty
        self.shootSpeed = 45

        # abilities
        self.hp = 125
        self.attackDamage = 10

        self.modify_abilities()

    def draw(self):
        Dragon_Strong.image.clip_draw(int(self.frame) * self.pngSizeX, self.animID * self.pngSizeY, self.pngSizeX, self.pngSizeY, self.posX,
                               self.posY, self.sizeX, self.sizeY)

    def update_anim(self):
        TimeToFrameQuantity = self.frameMax * self.actionPerTime * mainframe.frame_time
        self.frame = (self.frame + TimeToFrameQuantity) % 10

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
        self.angle += self.anglespeed * mainframe.frame_time
        if self.angle >= 360:
            self.angle = 0
        if self.firstMode == True:
            if self.originPosY > 550:
                self.posX += math.cos(math.radians(self.angle)) * self.moveSpeedPixelPerSecond * mainframe.frame_time
                self.posY += math.sin(math.radians(self.angle)) * self.moveSpeedPixelPerSecond * mainframe.frame_time - 2
                self.originPosY += -2
            else:
                self.firstMode = False
                self.shootCheck = True
                self.originPosY = 550
        else:
            self.posX += math.cos(math.radians(self.angle)) * self.moveSpeedPixelPerSecond * mainframe.frame_time
            self.posY += math.sin(math.radians(self.angle)) * self.moveSpeedPixelPerSecond * mainframe.frame_time


        self.bulletAngle += self.bulletAngleSpeed * mainframe.frame_time
        if self.shootTime > self.shootDelay:
            game_world.add_object(Bullet(self.posX, self.posY,  self.bulletAngle, self.shootSpeed, 'YellowCircle_Anim', '', 'Anim'
                                        , self.bulletsizeY, self.bulletsizeY, self.attackDamage), BULLET)
            self.shootTime = 0

    def modify_difficulty(self, difficulty):
        difficulty -= 1
        self.originShootDelay /= (1 + difficulty / 10)
        self.shootSpeed *= (1 + difficulty / 10)
        self.hp *= (1 + difficulty / 3)
        self.attackDamage *= (1 + difficulty / 10)
        difficulty += 1
        self.difficulty = difficulty
        self.modify_abilities()

    def modify_abilities(self):
        # speed
        self.moveSpeedMeterPerMinute = (self.moveSpeed * 1000.0 / 60.0)
        self.moveSpeedMterPerSecond = (self.moveSpeedMeterPerMinute / 60.0)
        self.moveSpeedPixelPerSecond = (self.moveSpeedMterPerSecond * PIXEL_PER_METER)
        # speed
        self.timePerAction = 1.0 - self.animSpeed / 100
        self.actionPerTime = 1.0 / self.timePerAction
        # delay
        self.shootDelay = self.originShootDelay / 5