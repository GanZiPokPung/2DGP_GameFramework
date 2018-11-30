from pico2d import *
from static import *
from effect import Effect
import math
import static
import mainframe
import random
import stage_scene
import custom_math
import game_world

# Action Speed
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

TIME_FOR_BOMB = 5

class Bullet:
    image = None
    size = None
    rectSize = None
    def __init__(self, posX, posY, angle, speed, imageType, rootType, bulletType, sizeX, sizeY, damage):
        self.posX = posX
        self.posY = posY
        self.angle = angle
        self.speed = speed
        # image
        self.type = imageType
        #
        self.rootType = rootType
        # 총알 타입 회전(보는 각도, 지속), 스프라이트, 등등
        self.bulletType = bulletType

        # image
        if Bullet.image == None:
            self.initialize_image()
        self.image = Bullet.image.get(self.type)
        # size of png
        if Bullet.size == None:
            self.initialize_size()
        self.pngSizeX = Bullet.size.get(self.type)[0]
        self.pngSizeY = Bullet.size.get(self.type)[1]

        rectSizeX = Bullet.rectSize.get(self.type)[0]
        rectSizeY = Bullet.rectSize.get(self.type)[1]
        #size
        self.originSizeX = sizeX
        self.originSizeY = sizeY

        self.rectSizeX = rectSizeX * self.originSizeX
        self.rectSizeY = rectSizeY * self.originSizeY

        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY


        # frame type
        self.frame = 0
        if self.bulletType == 'Anim':
            self.maxFrame = Bullet.size.get(self.type)[2]
        elif self.bulletType == 'Anim_Stop':
            self.maxFrame = Bullet.size.get(self.type)[2]
            self.frame = random.randint(0, self.maxFrame)
        else:
            self.maxFrame = 0

        self.rotAngle = 0

        self.time = 0

        self.attackDamage = damage

        self.collideCheck = False
        self.modify_abilities()

    def initialize_image(self):
        Bullet.image = { # player bullet
                'BlueCircle':       load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'BlueCircle.png')),
                'Eagle':            load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'Eagle.png')),
                'ExplodeMiss':      load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'ExplodeMiss.png')),
                'GreenWeak':        load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'GreenWeak.png')),
                'GreenNormal':      load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'GreenNormal.png')),
                'GreenStrong':      load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'GreenStrong.png')),
                'PurpleWeak':       load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleWeak.png')),
                'PurpleNormal':     load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleNormal.png')),
                'PurpleStrong':     load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleStrong.png')),
                'PurpleMax':        load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'PurpleMax.png')),
                'Rug':              load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'Rug.png')),
                'SmallCircle':      load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'SmallCircle.png')),
                'SmallMiss':        load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'SmallMiss.png')),
                'Thunder':          load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'player', 'Thunder.png')),
                 # monster bulletmonst,
                'Small_A':          load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'Small_A.png')),
                'Small_B':          load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'Small_B.png')),
                'Small_Anim':       load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'Small_Anim.png')),
                'BlueCircle_M':     load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'BlueCircle.png')),
                'BlueCircle_Anim':  load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'BlueCircle_Anim.png')),
                'RedCircle':        load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'RedCircle.png')),
                'RedSun':           load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'RedSun.png')),
                'Missile':          load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'Missile.png')),
                'YellowCircle_Anim':load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'YellowCircle_Anim.png')),
                'Y':                load_image(os.path.join(os.getcwd(), 'resources', 'bullet', 'monster', 'Y2.png'))
                        }
    def initialize_size(self):
        Bullet.size  = {
                        # player
                        'BlueCircle':           [36, 36],
                        'Eagle':                [75, 49],
                        'ExplodeMiss':          [48 // 3, 22, 3],
                        'GreenWeak':            [36, 36],
                        'GreenNormal':          [28, 28],
                        'GreenStrong':          [32, 32],
                        'PurpleWeak':           [26, 26],
                        'PurpleNormal':         [26, 26],
                        'PurpleStrong':         [32, 32],
                        'PurpleMax':            [48, 48],
                        'Rug':                  [24, 24],
                        'SmallCircle':          [8, 8],
                        'SmallMiss':            [16, 16],
                        'Thunder':              [100 // 5, 200, 5],
                        # monster
                        'Small_A':              [16, 16],
                        'Small_B':              [12, 12],
                        'Small_Anim':           [142 // 8, 10, 8],
                        'BlueCircle_M':         [92, 98],
                        'BlueCircle_Anim':      [108 // 3, 38, 3],
                        'RedCircle':            [91, 92],
                        'RedSun':               [91, 92],
                        'Missile':              [24, 24],
                        'YellowCircle_Anim':    [336 // 6, 61, 6],
                        'Y':                    [270 // 3, 90, 3]
        }

        Bullet.rectSize = {
                        # player
                        'BlueCircle':           [36 // 2, 36 //2],
                        'Eagle':                [75 // 2, 49 // 2],
                        'ExplodeMiss':          [(48 // 3)//6, 22 // 2],
                        'GreenWeak':            [36 // 10, 36 // 2],
                        'GreenNormal':          [28 // 6, 28 // 2],
                        'GreenStrong':          [32 // 4, 32 // 2],
                        'PurpleWeak':           [26 // 6, 26 // 2],
                        'PurpleNormal':         [26 // 4, 26 // 2],
                        'PurpleStrong':         [32 // 3, 32 // 2],
                        'PurpleMax':            [48 // 4, 48 // 2],
                        'Rug':                  [24 // 5, 24 // 3],
                        'SmallCircle':          [8 // 2, 8 // 2],
                        'SmallMiss':            [16 // 5, 16 // 3],
                        'Thunder':              [(100 // 5) // 4, 200 // 2],
                        # monster
                        'Small_A':              [16 // 2, 16 // 2],
                        'Small_B':              [12 // 2, 12 // 2],
                        'Small_Anim':           [(142 // 8) // 2, 10 // 2],
                        'BlueCircle_M':         [92 // 2, 98 // 2],
                        'BlueCircle_Anim':      [(108 // 3) // 2, 38 // 2],
                        'RedCircle':            [91 // 2, 92 // 2],
                        'RedSun':               [91 // 2, 92 // 2],
                        'Missile':              [24 // 2, 24 // 2],
                        'YellowCircle_Anim':    [(336 // 6) // 3, 61 // 3],
                        'Y':                    [(270 // 3) // 2, 90 // 2]
        }

    def set_rotation(self, degree):
        self.rotAngle = self.angle - degree

    def get_rect(self):
        # 기울기에 따른 렉트 회전(해결 X, 다른 충돌처리 함수가 필요)
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def collideActive(self, opponent):
        self.collideCheck = True

    def update(self):
        if self.bulletType == 'Anim_Stop':
            self.time += mainframe.frame_time
            if self.time > TIME_FOR_BOMB:
                return True
        else:
            self.posX += math.cos(math.radians(self.angle)) * self.speedPixelPerSecond * mainframe.frame_time
            self.posY += math.sin(math.radians(self.angle)) * self.speedPixelPerSecond * mainframe.frame_time

        if self.bulletType == 'Anim' or self.bulletType == 'Anim_Stop':
            TimeToFrameQuantity = self.maxFrame * ACTION_PER_TIME * mainframe.frame_time
            self.frame = (self.frame + TimeToFrameQuantity) % self.maxFrame

        elif self.bulletType == 'Rotate':
            self.rotAngle += 20

        # 충돌하면 총알을 없앤다.
        if self.collideCheck == True:
            game_world.add_object(Effect(self.posX, self.posY, '', 'HitEffect01',
                                         self.originSizeX * 0.8, self.originSizeY * 0.8), EFFECT)
            return True

        # 맵 밖을 나가면 총알을 없앤다.
        if (self.posX < 0 - self.sizeX) or (self.posX > static.canvas_width + self.sizeX):
            return True
        elif (self.posY < 0 - self.sizeY) or (self.posY > static.canvas_height + self.sizeY):
            return True
        else:
            return False



    def draw(self):
        if self.bulletType == 'Rotate' or self.bulletType == 'RotateOnce':
            self.image.clip_composite_draw(int(self.frame) * self.pngSizeX, 0,
                                           self.pngSizeX, self.pngSizeY,
                                           math.radians(self.rotAngle), '',
                                           self.posX, self.posY,
                                           self.sizeX, self.sizeY)
        else:
            # No Sprite
            self.image.clip_draw(int(self.frame) * self.pngSizeX, 0,
                                 self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

    def modify_abilities(self):
        self.speedMeterPerMinute = (self.speed * 1000.0 / 60.0)
        self.speedMterPerSecond = (self.speedMeterPerMinute / 60.0)
        self.speedPixelPerSecond = (self.speedMterPerSecond * PIXEL_PER_METER)