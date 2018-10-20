from pico2d import *

class Bullet:
    image = None
    size = None
    def __init__(self, posX, posY, speed, type, rootType, sizeX, sizeY):
        self.posX = posX
        self.posY = posY
        self.speed = speed
        self.type = type
        self.rootType = rootType
        self.sizeX = sizeX
        self.sizeY = sizeY
        # image
        if Bullet.image == None:
            self.initialize_image()
        self.image = Bullet.image.get(self.type)
        # size of png
        if Bullet.size == None:
            self.initialize_size()
        self.pngSizeX = Bullet.size.get(self.type)[0]
        self.pngSizeY = Bullet.size.get(self.type)[1]
        # frame type
        self.frame = 0
        self.maxFrame = 0

    def initialize_image(self):
        Bullet.image = { # player bullet
                        'BlueCircle':   load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'BlueCircle.png')),
                        'Eagle':        load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'Eagle.png')),
                        'ExplodeMiss':  load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'ExplodeMiss.png')),
                        'GreenWeak':    load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'GreenWeak.png')),
                        'GreenNormal':  load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'GreenNormal.png')),
                        'GreenStrong':  load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'GreenStrong.png')),
                        'PurpleWeak':   load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleWeak.png')),
                        'PurpleNormal': load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleNormal.png')),
                        'PurpleStrong': load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleStrong.png')),
                        'PurpleMax':    load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'PurpleMax.png')),
                        'Rug':          load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'Rug.png')),
                        'SmallCircle':  load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'SmallCircle.png')),
                        'SmallMiss':    load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'SmallMiss.png')),
                        'Thunder':      load_image(os.path.join(os.getcwd(), 'bullet', 'player', 'Thunder.png'))
                         # monster bullet
                        }
    def initialize_size(self):
        Bullet.size  = {'BlueCircle':   [36, 36],
                        'Eagle':        [75, 49],
                        'ExplodeMiss':  [48, 22],
                        'GreenWeak':    [36, 36],
                        'GreenNormal':  [28, 28],
                        'GreenStrong':  [32, 32],
                        'PurpleWeak':   [26, 26],
                        'PurpleNormal': [26, 26],
                        'PurpleStrong': [32, 32],
                        'PurpleMax':    [48, 48],
                        'Rug':          [24, 24],
                        'SmallCircle':  [8, 8],
                        'SmallMiss':    [16, 16],
                        'Thunder':      [100, 200]}

    def update(self):
        pass

    def draw(self):
        pass