from pico2d import *
from static import *
import random
import static
import mainframe

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Effect:
    image = None
    size = None
    others = None
    index = None
    rectSize = None
    def __init__(self, posX, posY, effectType, imageType, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        # image
        self.imgType = imageType
        self.effectType = effectType

        #
        if Effect.image == None:
            self.initialize_image()
        #
        if Effect.size == None:
            self.initialize_size()

        if Effect.index == None:
            self.initialize_index()

        if Effect.others == None:
            self.initialize_others()

        if effectType == 'random_effect':
            tempNum = random.randint(0, 2)
            self.imgType = Effect.index[tempNum]

        self.image = Effect.image.get(self.imgType)

        self.pngSizeX = Effect.size.get(self.imgType)[0]
        self.pngSizeY = Effect.size.get(self.imgType)[1]

        sizeX *= Effect.others.get(self.imgType)[1]
        sizeY *= Effect.others.get(self.imgType)[1]

        self.sizeX = self.pngSizeX * sizeX
        self.sizeY = self.pngSizeY * sizeY

        self.rectSizeX = 0
        self.rectSizeY = 0

        # frame
        self.frame = 0
        self.maxFrame = Effect.size.get(self.imgType)[2]

        # speed anim
        self.timePerAction = Effect.others.get(self.imgType)[0]
        self.actionPerTime = 1.0 / self.timePerAction
    def initialize_image(self):
        Effect.image = {
            #'Effect01': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'Effect1.png')),
            'Effect02': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'Effect2.png')),
            'Effect03': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'Effect3.png')),
            'Effect04': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'Effect4.png')),
            'HitEffect01': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'HitEffect1.png')),
            'HitEffect02': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'HitEffect2.png')),
            'BombEffect': load_image(os.path.join(os.getcwd(), 'resources', 'effect', 'BombEffect.png')),
        }


    def initialize_size(self):
        Effect.size = {
            #'Effect01':              [300 // 12, 22, 12],
            'Effect02':              [1462 // 15, 98, 15],
            'Effect03':              [1930 // 15, 104, 15],
            'Effect04':              [975 // 15, 65, 15],
            'HitEffect01':           [390 // 13, 30, 13],
            'HitEffect02':           [120 // 3, 40, 3],
            'BombEffect':            [2300 // 23, 200, 23],
        }

    def initialize_index(self):
        Effect.index = [#'Effect01',
                        'Effect02',
                        'Effect03',
                        'Effect04']

    def initialize_others(self):
        Effect.others = {
            #'Effect01':              [0.5, 4],
            'Effect02':              [0.5, 1],
            'Effect03':              [0.5, 1],
            'Effect04':              [0.5, 2],
            'HitEffect01':           [0.3, 1],
            'HitEffect02':           [0.15, 1],
            'BombEffect':            [0.5,  1],
        }

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def update(self):
        TimeToFrameQuantity = self.maxFrame * self.actionPerTime * mainframe.frame_time
        self.frame = (self.frame + TimeToFrameQuantity)

        if self.frame >= self.maxFrame:
            return True

        return False

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.pngSizeX, 0,
                             self.pngSizeX, self.pngSizeY,
                             self.posX, self.posY,
                             self.sizeX, self.sizeY)

    def draw_rect(self):
        draw_rectangle(*self.get_rect())