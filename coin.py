import mainframe
from static import *
from pico2d import *
import game_world
from effect import Effect

# Action Speed
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Coin:
    image = None
    sound = None
    def __init__(self, x, y, sizeX, sizeY, coinAmount):
        self.posX, self.posY = x, y
        self.speed = 40

        if Coin.image == None:
            Coin.image = load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Ingame', 'coin.png'))
        if Coin.sound == None:
            Coin.sound = load_wav(os.path.join(os.getcwd(), 'resources', 'sound', 'effect', 'coin.wav'))
            Coin.sound.set_volume(25)
        # size
        self.pngSizeX = 24
        self.pngSizeY = 23

        rectSizeX = self.pngSizeX // 2
        rectSizeY = self.pngSizeY // 2

        self.originSizeX = sizeX
        self.originSizeY = sizeY

        self.rectSizeX = rectSizeX * self.originSizeX
        self.rectSizeY = rectSizeY * self.originSizeY

        self.sizeX = self.pngSizeX * self.originSizeX
        self.sizeY = self.pngSizeY * self.originSizeY

        # Anim
        self.frame = 0
        self.maxFrame = 4

        self.time = 0
        self.collideCheck = False

        self.coinAmount = coinAmount
        self.attackDamage = 0

        self.modify_abilities()


    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def collideActive(self, opponent):
        self.collideCheck = True
        game_world.add_object(Effect(self.posX, self.posY, '', 'HitEffect02', self.originSizeX, self.originSizeY),
                              EFFECT)
        opponent.parsingMoneyBar(self.coinAmount)
        Coin.sound.play()
        # 돈 증가

    def update(self):
        # Anim
        TimeToFrameQuantity = self.maxFrame * ACTION_PER_TIME * mainframe.frame_time
        self.frame = (self.frame + TimeToFrameQuantity) % self.maxFrame

        self.speed -= 50 * mainframe.frame_time
        self.modify_abilities()
        # speed
        # self.posX += self.speedPixelPerSecond * mainframe.frame_time
        self.posY += self.speedPixelPerSecond * mainframe.frame_time

        # 충돌하면 없앤다.
        if self.collideCheck == True:
            # 이펙트?
            return True

        # 맵 밖을 나가면 없앤다.
        if (self.posX < 0 - self.sizeX) or (self.posX > canvas_width + self.sizeX):
            return True
        elif (self.posY < 0 - self.sizeY):
            return True
        else:
            return False

    def draw_rect(self):
        draw_rectangle(*self.get_rect())

    def draw(self):
        Coin.image.clip_draw(int(self.frame) * self.pngSizeX, 0,
                             self.pngSizeX, self.pngSizeY,
                             self.posX, self.posY,
                             self.sizeX, self.sizeY)

    def modify_abilities(self):
        self.speedMeterPerMinute = (self.speed * 1000.0 / 60.0)
        self.speedMterPerSecond = (self.speedMeterPerMinute / 60.0)
        self.speedPixelPerSecond = (self.speedMterPerSecond * PIXEL_PER_METER)
