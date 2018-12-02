from pico2d import *
from static import *

import stage_scene
import mainframe
from bullet import Bullet
from effect import Effect
from ui import *
import game_world

# Action Speed
TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

# Move Speed
# 추후 변경 가능하도록 해야함

class Player:
    image = None
    data = None
    sound = None
    def __init__(self):
        # position
        self.x = 250
        self.y = 50
        self.dirX = 0
        self.dirY = 0
        self.velocityX = 0
        self.velocityY = 0
        # status
        self.deadcheck = False
        self.turncheck = False
        # key
        self.pushLcheck = False
        self.pushRcheck = False
        self.pushAttcheck = False
        self.pushBombcheck = False
        # collider
        self.collideCheck = False
        # frame
        self.frameID = 0
        self.frame = 0
        self.reformframe = 0
        # bullet
        #self.bullet = []
        # time
        self.BulletTime = 0
        self.BulletDelay = 0.15
        self.BombTime = 0
        self.BombDelay = 5
        self.TickTime = 0
        self.TickDelay = 0.4
        # speed
        self.moveSpeed = 30
        # image
        if Player.image == None:
            Player.image = load_image(os.path.join(os.getcwd(), 'resources', 'player', 'player.png'))
        if Player.data == None:
            self.initializeData()
        if Player.sound == None:
            self.iniializeSound()
        # player abilities
        self.hp = 150
        self.score = 0
        self.money = 0
        self.attackDamage = 10
        self.bomb = None
        self.bombCount = 3
        self.bombDamage = 2
        self.parsingID = '1'

        # modify
        self.hpBar = None
        self.scoreBar = None
        self.moneyBar = None
        self.bombBar = None
        self.initPlayerUI()
        self.parsingAttData(self.parsingID)
        self.Modify_Abilities()

        # sound
        self.bomb_sound = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'bomb.wav'))
        self.bomb_sound.set_volume(110)


    def initPlayerUI(self):
        uiHpCheck = 0
        uiScoreCheck = 0
        uiMoneyCheck = 0
        uiBombCheck = 0
        uiLayer = game_world.get_layer(UIINGAME)

        for ui in uiLayer:
            if ui.uiID == 'hpbar':
                self.hpBar = ui
                uiHpCheck = 1
            elif ui.uiID == 'score':
                self.scoreBar = ui
                uiScoreCheck = 1
            elif ui.uiID == 'money':
                self.moneyBar = ui
                uiMoneyCheck = 1
            elif ui.uiID == 'bomb':
                self.bombBar = ui
                uiBombCheck = 1

        if uiHpCheck == 0:
            self.hpBar = HPBar(470, 30, self.hp)
            game_world.add_object(self.hpBar, UIINGAME)

        if uiBombCheck == 0:
            self.bombBar = BombBar(470, 80, self.bombCount)
            game_world.add_object(self.bombBar, UIINGAME)

        if uiScoreCheck == 0:
            self.scoreBar = Score(120, 680, self.score)
            game_world.add_object(self.scoreBar, UIINGAME)

        if uiMoneyCheck == 0:
            self.moneyBar = Money(480, 680, 1, 100, 2, 17, self.money)
            game_world.add_object(self.moneyBar, UIINGAME)

    def initializeData(self):
        Player.data = {
            # bullet
            # 불렛 갯수 사이각 각도, 속도, 이미지 타입, 불릿 타입, 사이즈
            # 나중에 데미지도 (맨 뒤에)
            '1': [3, 110, 'SmallCircle', 'RotateOnce', 2, 2, 1],
            '2': [3, 100, 'SmallMiss', 'RotateOnce', 2.7, 2.7, 2],
            '3': [3, 130, 'Rug', 'Rotate', 2, 2, 3],
            '4': [3, 90, 'GreenWeak', 'RotateOnce', 2, 2, 4],
            '5': [3, 90, 'PurpleWeak', 'RotateOnce', 2.5, 2.5, 4],
            '6': [5, 80, 'GreenNormal', 'RotateOnce', 2, 2, 5],
            '7': [5, 80, 'PurpleNormal', 'RotateOnce', 1.75, 1.75, 5],
            '8': [3, 100, 'GreenStrong', 'RotateOnce', 2, 2, 6],
            '9': [3, 100, 'PurpleStrong', 'RotateOnce', 1.75, 1.75, 6],
            '10': [1, 150, 'PurpleMax', 'RotateOnce', 3, 3, 7],
            '11': [3, 90, 'ExplodeMiss', 'Anim', 4, 4, 8],
            '12': [5, 100, 'BlueCircle', '', 1.25, 1.25, 7],
            '13': [1, 175, 'Eagle', 'RotateOnce', 3, 3, 15]
        }
    def iniializeSound(self):
        lazer = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer.wav'))
        lazer.set_volume(10)
        lazer2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer2.wav'))
        lazer2.set_volume(15)
        lazer3 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer3.wav'))
        lazer3.set_volume(25)
        lazer4 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'lazer4.wav'))
        lazer4.set_volume(25)
        shoot = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'shoot.wav'))
        shoot.set_volume(5)
        shoot2 = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'shoot2.wav'))
        shoot2.set_volume(20)
        hit = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'player', 'hit.WAV'))
        hit.set_volume(20)
        Player.sound = {
            # bullet
            '1': shoot2,
            '2': shoot,
            '3': shoot,
            '4': lazer,
            '5': lazer2,
            '6': lazer3,
            '7': lazer4,
            '8': lazer,
            '9': lazer2,
            '10': lazer3,
            '11': lazer4,
            '12': lazer3,
            '13': lazer2,

            # hit
            'hit' : hit
        }

    def get_rect(self):
        return self.x - 10, self.y - 20, self.x + 10, self.y + 20

    def handle_events(self, event):
        # 이동 구현
        # 키를 눌렀다면?
        if event.type == SDL_KEYDOWN:
            self.Move_State_DownKey(event.key)
            self.Attack_State_DownKey(event.key)
        # 키를 떼었다면?
        elif event.type == SDL_KEYUP:
            self.Move_State_UpKey(event.key)
            self.Attack_State_UpKey(event.key)

        # 동시에 눌렸을때는 그자리에 있는 스프라이트를 재생한다.
        if(self.pushLcheck == True) and (self.pushRcheck == True):
            self.turncheck = False

    # Key Input process
    # Move DownKey
    def Move_State_DownKey(self, key_state):
        if key_state == SDLK_UP:
            self.velocityY += self.moveSpeedPixelPerSecond
        elif key_state == SDLK_DOWN:
            self.velocityY -= self.moveSpeedPixelPerSecond
        # 좌
        elif key_state == SDLK_LEFT:
            # pushRcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
            # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushRcheck == False:
                self.turncheck = False
                self.frameID = 1
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            #
            self.velocityX -= self.moveSpeedPixelPerSecond
            self.pushLcheck = True
        # 우
        elif key_state == SDLK_RIGHT:
            # pushLcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
            # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushLcheck == False:
                self.turncheck = False
                self.frameID = 2
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            #
            self.velocityX += self.moveSpeedPixelPerSecond
            self.pushRcheck = True

        self.dirX = clamp(-1, self.velocityX, 1)
    # Move UpKey
    def Move_State_UpKey(self, key_state):
        if key_state == SDLK_UP:
            self.velocityY -= self.moveSpeedPixelPerSecond
        elif key_state == SDLK_DOWN:
            self.velocityY += self.moveSpeedPixelPerSecond
        # 좌
        elif key_state == SDLK_LEFT:
            # pushRcheck가 켜져있다는 뜻은 키를 뗌과 동시에 반대키가 눌리고 있다는 뜻이므로
            # 뗀 키의 반대쪽 키가 눌리고 있을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushRcheck == True:
                self.turncheck = True
                self.frameID = 2
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            else:
                self.turncheck = False
            #
            self.velocityX += self.moveSpeedPixelPerSecond
            self.dirX += 1
            self.pushLcheck = False
        # 우
        elif key_state == SDLK_RIGHT:
            # pushLcheck가 켜져있다는 뜻은 키를 뗌과 동시에 반대키가 눌리고 있다는 뜻이므로
            # 뗀 키의 반대쪽 키가 눌리고 있을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushLcheck == True:
                self.turncheck = True
                self.frameID = 1
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            else:
                self.turncheck = False
            #
            self.velocityX -= self.moveSpeedPixelPerSecond
            self.dirX -= 1
            self.pushRcheck = False
    # Att DownKey
    def Attack_State_DownKey(self, key_state):
        if key_state == SDLK_s:
            self.pushAttcheck = True
        elif key_state == SDLK_a:
            # 필살기
            if self.pushBombcheck == False:
                game_world.add_object(Bullet(100, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                game_world.add_object(Bullet(250, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                game_world.add_object(Bullet(400, 150, 90, 60, 'Thunder', 0, 'Anim_Stop', 6, 6, self.attackDamage * 2), BULLET_PLAYER)
                self.bomb_sound.play()
                self.bombCount -= 1
                self.bombBar.setBombImage(self.bombCount)
                self.pushBombcheck = True

    # Att UpKey
    def Attack_State_UpKey(self, key_state):
        if key_state == SDLK_s:
            self.pushAttcheck = False

    def parsingAttData(self, parsingID):
        # 불렛 갯수 /사이각 각도/, 속도, 이미지 타입, 불릿 타입, 사이즈
        if int(parsingID) >= 13 and self.parsingID == parsingID:
            return False

        self.parsingID = parsingID
        self.bulletCount = Player.data.get(parsingID)[0]
        self.bulletSpeed = Player.data.get(parsingID)[1]
        self.bulletImage = Player.data.get(parsingID)[2]
        self.bulletType = Player.data.get(parsingID)[3]
        self.bulletSizeX = Player.data.get(parsingID)[4]
        self.bulletSizeY = Player.data.get(parsingID)[5]
        self.attackDamage = Player.data.get(parsingID)[6]
        return True

    def parsingHPBar(self, healAmount):
        if (self.hp + healAmount) >= 500:
            return False

        self.hp += healAmount
        self.hpBar.setHPImage(self.hp)

        return True

    def parsingBombBar(self, bombAmount):
        if self.bombCount + bombAmount > 10:
            return False

        self.bombCount += bombAmount
        self.bombBar.setBombImage(self.bombCount)

        return True

    def parsingScoreBar(self, scoreAmount):
         self.score += scoreAmount
         self.scoreBar.setScore(self.score)

    def parsingMoneyBar(self, moneyAmount):
        if (self.money + moneyAmount) < 0:
            return False

        self.money += moneyAmount
        self.moneyBar.setMoney(self.money)

        return True

    def Modify_Abilities(self):
        # speed
        self.moveSpeedMeterPerMinute = (self.moveSpeed * 1000.0 / 60.0)
        self.moveSpeedMterPerSecond = (self.moveSpeedMeterPerMinute / 60.0)
        self.moveSpeedPixelPerSecond = (self.moveSpeedMterPerSecond * PIXEL_PER_METER)

    def collideActive(self, opponent):
        if self.hp - opponent.attackDamage <= 0:
            self.hp = 0
        else:
            self.hp -= opponent.attackDamage
            self.hpBar.setHPImage(self.hp)
            if opponent.attackDamage > 0:
                Player.sound.get('hit').play()

    def update(self):
        # dead
        if (self.hp <= 0):
            game_world.add_object(Effect(self.x, self.y, 'random_effect', '', 70 * 3, 70 * 3),
                                  EFFECT)
            stage_scene.score = self.score
            stage_scene.money = self.money
            return True

        #player_time
        self.BulletTime += mainframe.frame_time

        TimeToFrameQuantity = FRAMES_PER_ACTION * ACTION_PER_TIME * mainframe.frame_time

        if self.turncheck == True:
            # 회전 이동 상태일때
            # 회전 스프라이트 끝 장면에 프레임을 고정
            if self.frame < 6:
               # self.frame = (self.frame + 1) % 7
               self.frame = (self.frame + TimeToFrameQuantity) % 7
        else:
            # 만약 회전 이동 상태가 아니라면 IDLE 상태로 돌아오는
            # 스프라이트를 재생한다.(프레임을 거꾸로 돌린다)
            if self.reformframe < 0:
                self.frameID = 0
                # self.frame = (self.frame + 1) % 7
                self.frame = (self.frame + TimeToFrameQuantity) % 7
            else:
                self.reformframe = self.reformframe - TimeToFrameQuantity
                self.frame = self.reformframe


        # print('Vel X = ', self.velocityX, '  Vel Y = ', self.velocityY)

        # 이동 계산
        self.y += self.velocityY * mainframe.frame_time
        self.x += self.velocityX * mainframe.frame_time

        self.block_player()

        # 화면 내 이동
        # boy.x = clamp(25, boy.x, 1600 - 25)


        # 공격
        if self.pushAttcheck == True :
            if self.BulletTime > self.BulletDelay:
                Player.sound.get(self.parsingID).play()
                angleTerm = 0
                angle = 90
                for cnt in range(0, self.bulletCount):
                    bullet = Bullet(self.x + 5, self.y + 20, angle + angleTerm, self.bulletSpeed, self.bulletImage, 0, self.bulletType
                           , self.bulletSizeX, self.bulletSizeY, self.attackDamage)
                    bullet.set_rotation(angle)
                    game_world.add_object(bullet, BULLET_PLAYER)
                    if angleTerm == 0:
                        angleTerm += 10
                    elif angleTerm > 0:
                        angleTerm *= -1
                    elif angleTerm < 0:
                        angleTerm *= -1
                        angleTerm += 10


                self.BulletTime = 0

        # 폭탄
        if self.pushBombcheck == True:
            self.BombTime += mainframe.frame_time
            self.TickTime += mainframe.frame_time
            # 지속 시간동안
            # 모든 몬스터 보스 총알을 무효화시키며
            # 지속적인 피해를 입힘
            game_world.clear_layer(BULLET)
            game_world.clear_layer(BOSS_BULLET)

            if self.TickTime > self.TickDelay:
                monsterLayer = game_world.get_layer(MONSTER)
                for monster in monsterLayer:
                    if monster.posY <= 700:
                        monster.hp -= self.bombDamage
                bossLayer = game_world.get_layer(BOSS)
                for boss in bossLayer:
                    if boss.posY <= 700:
                        boss.hp -= self.bombDamage
                self.TickTime = 0

            if self.BombTime > self.BombDelay:
                self.BombTime = 0
                self.TickTime = 0
                self.pushBombcheck = False

        return False

    def draw(self):
        Player.image.clip_draw(int(self.frame) * 70, self.frameID * 70, 70, 70, self.x, self.y)


        # DEBUG
        # print(str(self.pushLcheck) + " " + str(self.pushRcheck))
        # print(len(stage_scene.bullets))
        # print(self.frame)
        # print

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

    def block_player(self):
       left, bottom, right, top = self.get_rect()

       if left < 0:
           self.x -= self.velocityX * mainframe.frame_time

       if right > 500:
           self.x -= self.velocityX * mainframe.frame_time

       if top > 700:
           self.y -= self.velocityY * mainframe.frame_time

       if bottom < 0:
           self.y -= self.velocityY * mainframe.frame_time
