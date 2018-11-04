from pico2d import *

import math
import static

import stage_scene
import custom_math

class Bullet:
    image = None
    size = None
    def __init__(self, posX, posY, angle, speed, imageType, rootType, bulletType, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        self.angle = angle
        self.rotAngle = 0
        self.speed = speed / 10
        self.type = imageType
        self.rootType = rootType
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
        #size
        self.sizeX = self.pngSizeX * sizeX
        self.sizeY = self.pngSizeY * sizeY
        # frame type
        self.frame = 0
        if self.bulletType == 'Anim':
            self.maxFrame = Bullet.size.get(self.type)[2]
        else:
            self.maxFrame = 0

    def initialize_image(self):
        Bullet.image = { # player bullet
                'BlueCircle':       load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'BlueCircle.png')),
                'Eagle':            load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'Eagle.png')),
                'ExplodeMiss':      load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'ExplodeMiss.png')),
                'GreenWeak':        load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'GreenWeak.png')),
                'GreenNormal':      load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'GreenNormal.png')),
                'GreenStrong':      load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'GreenStrong.png')),
                'PurpleWeak':       load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleWeak.png')),
                'PurpleNormal':     load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleNormal.png')),
                'PurpleStrong':     load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleStrong.png')),
                'PurpleMax':        load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleMax.png')),
                'Rug':              load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'Rug.png')),
                'SmallCircle':      load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'SmallCircle.png')),
                'SmallMiss':        load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'SmallMiss.png')),
                'Thunder':          load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'Thunder.png')),
                 # monster bulletmonster
                'Small_A':          load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'Small_A.png')),
                'Small_B':          load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'Small_B.png')),
                'Small_Anim':       load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'Small_Anim.png')),
                'BlueCircle_M':     load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'BlueCircle.png')),
                'BlueCircle_Anim':  load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'BlueCircle_Anim.png')),
                'RedCircle':        load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'RedCircle.png')),
                'RedSun':           load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'RedSun.png')),
                'Missile':          load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'Missile.png')),
                'YellowCircle_Anim':load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'YellowCircle_Anim.png')),
                'Y':                load_image(os.path.join(os.getcwd(), 'bullet', 'monster', 'Y2.png'))
                        }
    def initialize_size(self):
        Bullet.size  = {
                        # player
                        'BlueCircle':           [36, 36],
                        'Eagle':                [75, 49],
                        'ExplodeMiss':          [48, 22],
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
                        'Thunder':              [100, 200],
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

    def update(self):
        self.posX += math.cos(math.radians(self.angle)) * self.speed
        self.posY += math.sin(math.radians(self.angle)) * self.speed

        if self.maxFrame != 0:
            self.frame = (self.frame + 1) % self.maxFrame

        if self.bulletType == 'Rotate':
            self.rotAngle += 20

        # 맵 밖을 나가면 총알을 없앤다.
        if (self.posX < 0 - self.sizeX) or (self.posX > static.canvas_width + self.sizeX):
            return True
        elif (self.posY < 0 - self.sizeY) or (self.posY > static.canvas_height + self.sizeY):
            return True
        else:
            return False

    def draw(self):

        if self.bulletType == 'Rotate' or self.bulletType == 'RotateOnce':
            self.image.clip_composite_draw(self.frame * self.pngSizeX, 0,
                                           self.pngSizeX, self.pngSizeY,
                                           math.radians(self.rotAngle), '',
                                           self.posX, self.posY,
                                           self.sizeX, self.sizeY)
        else:
            # No Sprite
            self.image.clip_draw(self.frame * self.pngSizeX, 0,
                                 self.pngSizeX, self.pngSizeY,
                                 self.posX, self.posY,
                                 self.sizeX, self.sizeY)