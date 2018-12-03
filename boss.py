from pico2d import *
from static import *
from bullet import Bullet
from effect import Effect
from coin import Coin
import static
import mainframe
import custom_math
import game_world
import random
import stage_scene

class Boss:
    sound = None
    def __init__(self, posX, posY, movespeed, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        self.moveSpeed = movespeed
        #
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.originSizeX = sizeX
        self.originSizeY = sizeY
        self.rectSizeX = 0
        self.rectSizeY = 0
        #
        self.frame = 0
        # shoot
        self.shootCheck = False
        self.shootTime = 0
        self.shootDelay = 0
        # default time
        self.time = 0
        # delayTerm
        self.delayCheck = False
        self.delayTerm = 0
        self.delayTime = 0
        self.hp = 0
        self.attackDamage = 0
        self.difficulty = 1

        self.deadCheck = False

        if Boss.sound == None:
            self.initialize_sound()

        # ability
    def initialize_sound(self):
        hit = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'hit.wav'))
        hit.set_volume(15)
        explode = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'explode.wav'))
        explode.set_volume(8)
        explode2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'bigexplode.wav'))
        explode2.set_volume(70)
        laughing = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'laughing.wav'))
        laughing.set_volume(100)
        laughing2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'laughing2.wav'))
        laughing2.set_volume(100)
        god = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'god.wav'))
        god.set_volume(120)
        hell = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'hell.wav'))
        hell.set_volume(120)
        shoot = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'shoot.wav'))
        shoot.set_volume(3)
        lazer = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'lazer.wav'))
        lazer.set_volume(10)
        lazer2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'lazer2.wav'))
        lazer2.set_volume(10)
        dying = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'dying.wav'))
        dying.set_volume(30)
        bossexplode = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'boss', 'bossExplode.wav'))
        bossexplode.set_volume(30)
        Boss.sound = {
                'hit': hit,
                # explode
                '1': explode,
                '2': explode2,
                # att
                'shoot': shoot,
                'lazer': lazer,
                'lazer2': lazer2,
                # laughing
                'laughing': laughing,
                'laughing2': laughing2,
                # speak
                'god': god,
                'hell': hell,
                # dying
                'dying': dying,
                # deadExplode
                'bossexplode': bossexplode
        }

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY,\
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def collideActive(self, opponent):
        if opponent.bulletType == 'Anim_Stop':
            return

        if self.posY <= 700:
            self.hp -= opponent.attackDamage
            game_world.curtain_object(PLAYER, 0).parsingScoreBar(opponent.attackDamage * random.randint(2, 5))
            Boss.sound.get('hit').play()

    def update(self):

        self.time += mainframe.frame_time

        if self.shootCheck == True:
            self.shootTime += mainframe.frame_time
        if self.delayCheck == True:
            self.delayTime += mainframe.frame_time

        if self.deadCheck == False:
            self.update_AI()
            self.update_anim()

        if (self.hp <= 0):
            if self.deadCheck == False:
                Boss.sound.get('dying').play()
                self.deadCheck = True
            check = self.deadProcess()
            if check == True:
                game_world.add_object(
                    Effect(self.posX, self.posY, 'random_effect', '', self.originSizeX * 3, self.originSizeY * 3),
                    EFFECT)
                game_world.curtain_object(PLAYER, 0).parsingScoreBar(random.randint(1000, 5000) * self.difficulty)
                Boss.sound.get('bossexplode').play()
                return True
            else:
                return False

    def deadProcess(self):
        return True

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

class BossHead(Boss):
    image = None
    def __init__(self):
        posX = 250
        posY = 950
        moveSpeed = 10
        sizeX = 1.75
        sizeY = 1.75
        Boss.__init__(self, posX, posY, moveSpeed, sizeX, sizeY)
        if BossHead.image == None:
            BossHead.image = load_image(os.path.join(os.getcwd(), 'resources', 'boss', 'head.png'))
        # size of png
        self.pngSizeX = 259
        self.pngSizeY = 125
        # size
        self.rectSizeX = (self.pngSizeX // 6) * self.sizeX
        self.rectSizeY = (self.pngSizeY // 2) * self.sizeY
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.bulletsizeX = 0
        self.bulletsizeY = 0
        # AI를 위한 위치들
        self.originPos = [self.posX, self.posY]
        self.startPos = [250, 570]
        self.currentPos = []
        self.movePattern = [self.startPos,
                            [self.startPos[0] - 5, self.startPos[1] - 5],
                            [self.startPos[0] + 5, self.startPos[1] + 5],
                            [self.startPos[0] + 5, self.startPos[1] - 5],
                            [self.startPos[0] - 5, self.startPos[1] + 5]]
        # for AI check
        self.firstMode = True
        self.moveMode = False
        self.attackMode = False
        self.attacking = False
        self.attackInfoInit = False
        # for attack type
        self.attackID = 99
        self.attackOtherID = 99
        # for attack term
        self.attackingTime = 0
        self.attackDelay = 0
        # for AI move
        self.moveT_Curv = 0
        self.moveLocation = 2
        self.moveT = 0
        self.speedT = 20
        self.curvSpeedT = 100
        # for AI shooting
        self.originShootDelay = 0
        self.shootDelay = 0
        self.shootSpeed = 0
        self.shootMax = 0
        self.shootCount = 0
        self.shootterm = False
        self.shootAngle = 0
        self.LR_decision = 0
        self.handOnceCheck = False

        #hand
        self.initializeHands()
        self.modify_abilities()

        #
        self.explodeTime = 0
        self.explodeDelay = 0.25

        #abilities
        self.hp = 200
        self.attackDamage = 10


        self.patternDelay = 7
        self.patternHandDelay = 10

        self.patternTime = self.patternDelay - 3
        self.patternHandTime = 0

        # coin
        self.coinTime = 0
        self.coinDelay = 0.15
        self.coinCount = 0

    def initializeHands(self):
        self.BossHandLeft = BossHand('Left', self)
        self.BossHandRight = BossHand('Right', self)
        game_world.add_object(self.BossHandLeft, BOSS)
        game_world.add_object(self.BossHandRight, BOSS)

    def draw(self):
        BossHead.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
       if self.hp < (self.hp * 0.3):
            self.almost_die(1)
        # move
       if self.firstMode == True:
            self.spawn_move()
       else:
           if self.moveMode == True:
                self.move()

           self.attack()

    def spawn_move(self):
        if self.moveT >= 100:
            self.firstMode = False
            self.moveMode = True
            self.moveT = 0
        else:
            self.moveT += self.speedT * mainframe.frame_time
            self.posX, self.posY = custom_math.move_line(self.originPos,
                                                         self.startPos,
                                                         self.moveT)
    def move(self):
        if self.moveT_Curv >= 100:
            self.moveT_Curv = 0
            if self.moveLocation == 4:
                self.moveLocation = 0
            else:
                self.moveLocation += 1
        else:
            self.moveT_Curv += self.curvSpeedT * mainframe.frame_time
            self.posX, self.posY = custom_math.move_curve(self.movePattern[self.moveLocation - 3],
                                                          self.movePattern[self.moveLocation - 2],
                                                          self.movePattern[self.moveLocation - 1],
                                                          self.movePattern[self.moveLocation],
                                                          self.moveT_Curv)
    def attack(self):
        self.pattern_check()
        # head
        if self.attackID == 1:
            check = self.Pattern_Normal()
            if check == False:
                self.attackID = 99
        elif self.attackID == 2:
            check = self.Pattern_Lazer_One()
            if check == False:
                self.attackID = 99
        elif self.attackID == 3:
            check = self.Pattern_Lazer_Two()
            if check == False:
                self.attackID = 99

        # hand
        if self.attackOtherID == 1:
            check = self.Pattern_Hand_Normal()
            if check == False:
                self.attackOtherID = 99
        elif self.attackOtherID == 2:
            check = self.Pattern_Hand_One()
            if check == False:
                self.attackOtherID = 99
        elif self.attackOtherID == 3:
            check = self.Pattern_Hand_Two()
            if check == False:
                self.attackOtherID = 99
        elif self.attackOtherID == 4:
            check = self.Pattern_Hand_Three()
            if check == False:
                self.attackOtherID = 99

    def pattern_check(self):
        self.patternTime += mainframe.frame_time
        self.patternHandTime += mainframe.frame_time

        if self.patternTime > self.patternDelay:
            if self.attackID != 99:
                return
            else:
                check = random.randint(0, 10)
                if check < 6:
                    self.attackID = 1
                else:
                    self.attackID = random.randint(2, 3)

            self.patternTime = 0

        if self.patternHandTime > self.patternHandDelay:
            if self.attackOtherID != 99:
                return
            else:
                self.attackOtherID = random.randint(1, 4)
            self.patternHandTime = 0

    def modify_difficulty(self, difficulty):
        difficulty -= 1
        self.hp *= (1 + difficulty / 2)
        self.attackDamage *= (1 + difficulty / 2)
        self.patternHandDelay /= (1 + difficulty / 2)
        self.patternDelay /= (1 + difficulty / 2)
        difficulty += 1
        self.difficulty = difficulty
        self.BossHandLeft.modify_difficulty(self.difficulty)
        self.BossHandRight.modify_difficulty(self.difficulty)

    def modify_abilities(self):
        # delay
        self.shootDelay = self.originShootDelay / 5

    def deadProcess(self):
        self.coinTime += mainframe.frame_time

        if self.BossHandLeft != None:
            self.BossHandLeft.hp = 0
        if self.BossHandRight != None:
            self.BossHandRight.hp = 0

        self.almost_die(3)

        if self.coinTime > self.coinDelay:
            game_world.add_object(Coin(random.randint(int(self.posX - self.sizeX // 2), int(self.posX + self.sizeX // 2)),
                                        random.randint(int(self.posY - self.sizeY // 3), int(self.posY + self.sizeY // 3)),
                                        1.5, 1.5, random.randint(3, 5) * self.difficulty * 100), COIN)
            self.coinTime = 0
            self.coinCount += 1

        if self.coinCount > 50:
            return True
        else:
            return False

    def almost_die(self, size):
        self.explodeTime += mainframe.frame_time
        if self.explodeTime > self.explodeDelay:
            game_world.add_object(Effect(random.randint(int(self.posX - self.sizeX // 2), int(self.posX + self.sizeX // 2)),
                                         random.randint(int(self.posY - self.sizeY // 3), int(self.posY + self.sizeY // 3)),
                                  'random_effect', '', (self.originSizeX / 2) * size, (self.originSizeY / 2) * size),
                                  EFFECT)
            Boss.sound.get(str(random.randint(1, 2))).play()
            self.explodeTime = 0

    def Pattern_Normal(self):
        if self.attackInfoInit == False:
            self.originShootDelay = 0.5
            self.shootSpeed = 50
            self.bulletsizeX = 1
            self.bulletsizeY = 1
            self.shootMax = 30
            self.modify_abilities()
            self.shootCheck = True
            self.attackInfoInit = True

        if self.shootTime > self.shootDelay:
            self.shootAngle = random.randint(270 - 40, 270 + 40)

            game_world.add_object(Bullet(self.posX, self.posY - 50, self.shootAngle ,
                                    self.shootSpeed, 'Small_A', '', '',
                                    self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)

            self.shootTime = 0
            self.shootCount += 1

        if self.shootCount > self.shootMax:
            self.shootCount = 0
            self.shootTime = 0
            self.shootCheck = False
            self.attackInfoInit = False
            return False
        else:
            return True

    def Pattern_Lazer_One(self):
        if self.attackInfoInit == False:
            self.originShootDelay = 0.5
            self.shootSpeed = 100
            self.bulletsizeX = 0.7
            self.bulletsizeY = 0.7
            self.shootCheck = True
            self.LR_decision = random.randint(0, 1)

            if self.LR_decision == 0:
                self.shootAngle = 270 - 80
            else:
                self.shootAngle = 270 + 80

            self.time = 0
            self.attackingTime = 0.75
            self.delayTerm = 0.5

            self.delayCheck = False

            self.modify_abilities()
            Boss.sound.get('god').play()
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
                                             self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
                game_world.add_object(Bullet(self.posX + 40, self.posY + 5, self.shootAngle,
                                             self.shootSpeed, 'Y', '', 'Anim',
                                             self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
                Boss.sound.get('lazer').play()
            self.shootTime = 0

        if self.LR_decision == 0:
            if self.shootAngle > 270 + 80:
                self.shootTime = 0
                self.shootCheck = False
                self.attackInfoInit = False
                return False
        else:
            if self.shootAngle < 270 - 80:
                self.shootTime = 0
                self.shootCheck = False
                self.attackInfoInit = False
                return False

        return True

    def Pattern_Lazer_Two(self):
        if self.attackInfoInit == False:
            self.originShootDelay = 0.5
            self.shootSpeed = 100
            self.bulletsizeX = 1.5
            self.bulletsizeY = 1.5
            self.shootAngle = 0
            self.modify_abilities()
            Boss.sound.get('laughing').play()
            self.shootCheck = True
            self.attackInfoInit = True

        self.shootAngle += 0.4

        if self.shootTime > self.shootDelay:
            game_world.add_object(Bullet(self.posX - 40, self.posY, 180 + self.shootAngle,
                                         self.shootSpeed, 'BlueCircle_Anim', '', 'Anim',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
            game_world.add_object(Bullet(self.posX + 40, self.posY, 360 - self.shootAngle,
                                         self.shootSpeed, 'BlueCircle_Anim', '', 'Anim',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
            Boss.sound.get('lazer2').play()
            self.shootTime = 0


        if self.shootAngle > 85:
            self.shootTime = 0
            self.shootCheck = False
            self.attackInfoInit = False
            return False

        return True

    def Pattern_Hand_Normal(self):
        if self.handOnceCheck == False:
            if  self.BossHandLeft != None:
                self.BossHandLeft.attackID = 0
            if self.BossHandRight != None:
                self.BossHandRight.attackID = 0

            self.handOnceCheck = True

            # 끝나는 체크
        if self.BossHandLeft == None:
            doCheckR = self.BossHandRight.attackID
            if doCheckR == 99:
                self.handOnceCheck = False
                return False
        elif self.BossHandRight == None:
            doCheckL = self.BossHandLeft.attackID
            if doCheckL == 99:
                self.handOnceCheck = False
                return False
        else:
            doCheckL = self.BossHandLeft.attackID
            doCheckR = self.BossHandRight.attackID
            if doCheckL == 99 and doCheckR == 99:
                self.handOnceCheck = False
                return False

        return True

    def Pattern_Hand_One(self):

        if self.handOnceCheck == False:
            if self.BossHandLeft != None:
                self.BossHandLeft.moveMode = False
                self.BossHandLeft.attackID = 1
            if self.BossHandRight != None:
                self.BossHandRight.moveMode = False
                self.BossHandRight.attackID = 1
            Boss.sound.get('god').play()
            self.handOnceCheck = True

        # 끝나는 체크
        if self.BossHandLeft == None:
            doCheckR = self.BossHandRight.attackID
            if doCheckR == 99:
                self.handOnceCheck = False
                return False
        elif self.BossHandRight == None:
            doCheckL = self.BossHandLeft.attackID
            if doCheckL == 99:
                self.handOnceCheck = False
                return False
        else:
            doCheckL = self.BossHandLeft.attackID
            doCheckR = self.BossHandRight.attackID
            if doCheckL == 99 and doCheckR == 99:
                self.handOnceCheck = False
                return False

        return True

    def Pattern_Hand_Two(self):

        if self.handOnceCheck == False:
            LRCheck = random.randint(0, 1)

            if LRCheck == 0:
                if self.BossHandLeft != None:
                    self.BossHandLeft.moveMode = False
                    self.BossHandLeft.attackID = 2
            else:
                if self.BossHandRight != None:
                    self.BossHandRight.moveMode = False
                    self.BossHandRight.attackID = 2
            #Boss.sound.get('laughing2').play()
            self.handOnceCheck = True

        # 끝나는 체크
        if self.BossHandLeft == None:
            doCheckR = self.BossHandRight.attackID
            if doCheckR == 99:
                self.handOnceCheck = False
                return False
        elif self.BossHandRight == None:
            doCheckL = self.BossHandLeft.attackID
            if doCheckL == 99:
                self.handOnceCheck = False
                return False
        else:
            doCheckL = self.BossHandLeft.attackID
            doCheckR = self.BossHandRight.attackID
            if doCheckL == 99 and doCheckR == 99:
                self.handOnceCheck = False
                return False

        return True

    def Pattern_Hand_Three(self):
        if self.handOnceCheck == False:
            LRCheck = random.randint(0, 1)

            if LRCheck == 0:
                if self.BossHandLeft != None:
                    self.BossHandLeft.specialMoveMode = True
            else:
                if self.BossHandRight != None:
                    self.BossHandRight.specialMoveMode = True
            Boss.sound.get('hell').play()
            self.handOnceCheck = True

        #끝나는 체크
        if self.BossHandLeft == None:
            checkR = self.BossHandRight.specialMoveMode
            if checkR == False:
                self.handOnceCheck = False
                return False
        elif self.BossHandRight == None:
            checkL = self.BossHandLeft.specialMoveMode
            if checkL == False:
                self.handOnceCheck = False
                return False
        else:
            checkL = self.BossHandLeft.specialMoveMode
            checkR = self.BossHandRight.specialMoveMode
            if checkL == False and checkR == False:
                self.handOnceCheck = False
                return False

        return True


class BossHand(Boss):
    image = None
    def __init__(self, type, headinfo):
        posX = 0
        posY = 0
        moveSpeed = 10
        sizeX = 1.75
        sizeY = 1.75
        Boss.__init__(self, posX, posY, moveSpeed, sizeX, sizeY)
        #image
        if BossHand.image == None:
            BossHand.image = {'Left': load_image(os.path.join(os.getcwd(),'resources', 'boss', 'Hand_L.png')),
                              'Right': load_image(os.path.join(os.getcwd(),'resources', 'boss', 'Hand_R.png'))}
        self.type = type
        self.image = BossHand.image.get(self.type)
        # 부모
        self.headinfo = headinfo
        # size of png
        self.pngSizeX = 85
        self.pngSizeY = 49
        # size
        self.rectSizeX = (self.pngSizeX // 2) * self.sizeX
        self.rectSizeY = (self.pngSizeY // 2) * self.sizeY
        self.sizeX = self.pngSizeX * self.sizeX
        self.sizeY = self.pngSizeY * self.sizeY
        self.bulletsizeX = 0
        self.bulletsizeY = 0
        #
        self.angle = 270
        self.angleSpeed = 350
        # for AI check
        self.moveMode = True
        self.attackMode = False
        self.specialMoveMode = False
        self.specialAttMode = False
        self.attackInfoInit = False
        self.attackID = 99
        # for AI move
        self.moveLocation = 0
        self.moveT = 0
        self.speedT = 50
        self.moveT_Curv = 0
        self.curvSpeedT = 200
        # for AI shoot
        self.originShootDelay = 0
        self.shootDelay = 0
        self.shootSpeed = 0

        self.shootMax = 0
        self.shootCount = 0
        self.shootterm = False
        self.shootAngle = 0

        self.tmpCount = 0

        # for AI pos
        self.originPosX = []
        self.originPosY = []
        self.startPos   = []
        self.currentPos = []
        self.curvPos = []
        self.initialize_course()

        # 부모
        self.player = None
        if len(game_world.get_layer(PLAYER)) > 0:
            self.player = game_world.curtain_object(PLAYER, 0)

        # abilities
        self.hp = 100
        self.attackDamage = 10

        self.modify_abilities()

    def initialize_course(self):
        if self.type == 'Left':
            self.curvPos = [[470, 200], self.currentPos, self.currentPos, self.currentPos, [0 + 20, 360]]
        elif self.type == 'Right':
            self.curvPos = [[30, 200], self.currentPos, self.currentPos, self.currentPos, [500 - 20, 360]]

    def draw(self):
        self.image.clip_draw(0, 0, self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def update_anim(self):
        pass

    def update_AI(self):
        if self.specialMoveMode == True:
            self.special_move_attack()
            return

        if self.moveMode == True :
            if self.attackMode == False:
                # 보스를 따라 움직일때
                self.move_and_norm_attack()
            # 팔 접기
            else:
                self.end_special_attack()
        else:
            # 팔 뻗기
            if self.attackMode == False:
                self.start_special_attack()
            # 공격
            else:
                self.special_attack()


    def special_move_attack(self):
        self.initialize_course()
        if self.moveT_Curv >= 100:
            self.moveT_Curv = 0
            if self.moveLocation == 3:
                self.moveLocation = 0
                self.specialMoveMode = False
                self.shootCount = 0
                self.shootTime = 0
                self.shootCheck = False
                self.attackInfoInit = False
            else:
                self.moveLocation += 1
        else:
            self.moveT_Curv += self.curvSpeedT * mainframe.frame_time
            if self.moveLocation == 0:
                self.curvSpeedT = 50
            elif self.moveLocation == 1:
                self.curvSpeedT = 300
                self.Pattern_Normal_For_Special()
            else:
                self.curvSpeedT = 150

            self.posX, self.posY = custom_math.move_curve(self.curvPos[self.moveLocation - 3],
                                                          self.curvPos[self.moveLocation - 2],
                                                          self.curvPos[self.moveLocation - 1],
                                                          self.curvPos[self.moveLocation],
                                                          self.moveT_Curv)

    def move_and_norm_attack(self):
        if self.type == 'Left':
            self.originPosX = self.headinfo.posX - 160
            self.originPosY = self.headinfo.posY - 100
            self.angle += self.angleSpeed * mainframe.frame_time
        elif self.type == 'Right':
            self.originPosX = self.headinfo.posX + 160
            self.originPosY = self.headinfo.posY - 100
            self.angle -= self.angleSpeed * mainframe.frame_time

        self.startPos = [self.originPosX, self.originPosY]
        self.posX = self.originPosX + math.cos(math.radians(self.angle)) * 400 * mainframe.frame_time
        self.posY = self.originPosY + math.sin(math.radians(self.angle)) * 400 * mainframe.frame_time
        self.currentPos = [self.posX, self.posY]

        if self.attackID == 0:
            check = self.Pattern_Normal()
            if check == False:
                self.attackID = 99

    def start_special_attack(self):
        if self.moveT >= 100:
            self.attackMode = True
            self.moveT = 0
            self.angle = 270
        else:
            self.moveT += self.speedT * 5 * mainframe.frame_time
            self.posX, self.posY = custom_math.move_line(self.currentPos,
                                                         [self.startPos[0], self.startPos[1] - 90],
                                                         self.moveT)
    def special_attack(self):
        if self.attackID == 1:
            check = self.Pattern_Special_One()
            if check == False:
                self.moveMode = True
                self.attackID = 99
        elif self.attackID == 2:
            check = self.Pattern_Special_Two()
            if check == False:
                self.moveMode = True
                self.attackID = 99

    def end_special_attack(self):
        if self.moveT >= 100:
            self.attackMode = False
            self.moveT = 0
            self.angle = 270
        else:
            self.moveT += self.speedT * 5 * mainframe.frame_time
            self.posX, self.posY = custom_math.move_line([self.startPos[0], self.startPos[1] - 90],
                                                         self.startPos,
                                                         self.moveT)

    def modify_difficulty(self, difficulty):
        difficulty -= 1
        self.hp *= (1 + difficulty / 2)
        self.attackDamage *= (1 + difficulty / 2)
        difficulty += 1
        self.difficulty = difficulty

    def modify_abilities(self):
        self.shootDelay = self.originShootDelay / 5

    def Pattern_Normal_For_Special(self):
        if self.attackInfoInit == False:
            self.originShootDelay = 0.25
            self.shootSpeed = 20
            self.bulletsizeX = 2
            self.bulletsizeY = 2
            self.time = 0
            self.delayCheck = False
            self.shootCheck = True
            self.modify_abilities()
            self.attackInfoInit = True

        if self.shootTime > self.shootDelay:
            game_world.add_object(Bullet(self.posX, self.posY - 10, 270,
                                                self.shootSpeed, 'Y', '', 'Anim',
                                                self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
            Boss.sound.get('lazer').play()
            self.shootTime = 0

        return True

    def Pattern_Normal(self):
        if self.attackInfoInit == False:
            self.originShootDelay = random.randint(2, 3)
            self.shootSpeed = 55
            self.bulletsizeX = 2
            self.bulletsizeY = 2
            self.shootMax = 8

            self.time = 0
            self.tmpCount = 0
            self.delayTerm = 0.15

            self.delayCheck = False
            self.shootCheck = True
            self.modify_abilities()
            self.shootTime = self.shootDelay
            self.attackInfoInit = True

        if self.shootTime > self.shootDelay:
            if self.delayCheck == False:
                if self.player != None:
                    self.shootAngle = custom_math.angle_between([self.posX, self.posY],
                                                                [self.player.x, self.player.y])
                self.delayCheck = True
            else:
                if self.delayTime > self.delayTerm:
                    game_world.add_object(Bullet(self.posX, self.posY - 10, self.shootAngle,
                                                self.shootSpeed, 'Small_A', '', '',
                                                self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
                    self.shootCount += 1
                    self.tmpCount += 1
                    self.delayTime = 0
                    Boss.sound.get('shoot').play()
                    if self.tmpCount > 2:
                        self.delayCheck = False
                        self.tmpCount = 0

            if self.delayCheck == False:
                self.shootTime = 0
                self.shootDelay = random.randint(5, 7)

        if self.shootCount > self.shootMax:
            self.shootCount = 0
            self.shootTime = 0
            self.shootCheck = False
            self.attackInfoInit = False
            return False

        return True

    def Pattern_Special_One(self):
        if self.attackInfoInit == False:
            self.originShootDelay = 0.025
            self.shootSpeed = 80
            self.bulletsizeX = 2
            self.bulletsizeY = 2
            self.shootMax = 70
            self.modify_abilities()
            self.shootCheck = True
            self.attackInfoInit = True

        if self.shootTime > self.originShootDelay:
            self.shootAngle = random.randint(270 - 40, 270 + 40)

            tmpbullet = Bullet(self.posX, self.posY - 50, self.shootAngle,
                                    self.shootSpeed, 'Missile', '', 'RotateOnce',
                                    self.bulletsizeX, self.bulletsizeY, self.attackDamage)
            tmpbullet.set_rotation(270)
            game_world.add_object(tmpbullet, BOSS_BULLET)
            Boss.sound.get('shoot').play()
            self.shootTime = 0
            self.shootCount += 1

        if self.shootCount > self.shootMax:
            self.shootCount = 0
            self.shootTime = 0
            self.shootCheck = False
            self.attackInfoInit = False

            return False

        return True

    def Pattern_Special_Two(self):
        # 손에서 나가게 할 예정
        if self.attackInfoInit == False:
            self.originShootDelay = 0.2
            self.shootSpeed = 40
            self.bulletsizeX = 1
            self.bulletsizeY = 1
            self.shootAngle = 0
            self.shootMax = 100
            self.modify_abilities()
            self.shootCheck = True
            self.attackInfoInit = True

        if self.type == 'Left':
            self.shootAngle += 300 * mainframe.frame_time
        else:
            self.shootAngle -= 300 * mainframe.frame_time

        if self.shootTime > self.shootDelay:
            game_world.add_object(Bullet(self.posX, self.posY - 50, self.shootAngle,
                                         self.shootSpeed, 'Small_A', '', '',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
            game_world.add_object(Bullet(self.posX, self.posY - 50, self.shootAngle + 90,
                                         self.shootSpeed, 'Small_A', '', '',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
            game_world.add_object(Bullet(self.posX, self.posY - 50, self.shootAngle + 180,
                                         self.shootSpeed, 'Small_A', '', '',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)
            game_world.add_object(Bullet(self.posX, self.posY - 50, self.shootAngle + 270,
                                         self.shootSpeed, 'Small_A', '', '',
                                         self.bulletsizeX, self.bulletsizeY, self.attackDamage), BOSS_BULLET)

            self.shootCount += 1
            self.shootTime = 0


        if self.shootCount > self.shootMax:
            self.shootCount = 0
            self.shootTime = 0
            self.shootCheck = False
            self.attackInfoInit = False
            return False

        return True