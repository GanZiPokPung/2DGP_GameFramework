from pico2d import *
import mainframe
import static

class Mouse:
    images = None
    frames = None
    def __init__(self):
        self.posX, self.posY = 0, 0
        if Mouse.images == None:
            self.initialize_images()
        if Mouse.frames == None:
            self.initialize_frames()
        self.pngSizeX, self.pngSizeY = 32, 32
        sizeX, sizeY = 1, 1

        self.sizeX = self.pngSizeX * sizeX
        self.sizeY = self.pngSizeY * sizeY

        self.rectSizeX = self.sizeX / 4
        self.rectSizeY = self.sizeY / 4

        self.collideCheck = False
        self.mouseID = 'normal'

        self.frame = 0
        self.frameMax = Mouse.frames.get(self.mouseID)[0]

        self.timePerAction = Mouse.frames.get(self.mouseID)[1]
        self.actionPerTime = 1.0 / self.timePerAction

        self.time = 0
        self.hideTime = 2.0

        self.drawCheck = True
        self.ui = None

    def initialize_images(self):
        Mouse.images = {
            'normal' : [load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Mouse', 'Normal',
                                                'Normal_'+ str(number) + '.png')) for number in range(0, 12 + 1)],
            'click'  : [load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Mouse', 'Click',
                                                'Click' + str(number) + '.png')) for number in range(0, 1 + 1)],
            'gate': [load_image(os.path.join(os.getcwd(), 'resources', 'ui', 'Mouse', 'Gate',
                                              'Gate' + str(number) + '.png')) for number in range(0, 3 + 1)]
        }

    def initialize_frames(self):
        Mouse.frames = {
            'normal' : [13, 1.0],
            'click'  : [2, 0.2],
            'gate'   : [4, 0.5]
        }

    def change_ID(self, id):
        self.mouseID = id
        self.frameMax = Mouse.frames.get(self.mouseID)[0]
        self.timePerAction = Mouse.frames.get(self.mouseID)[1]
        self.actionPerTime = 1.0 / self.timePerAction
        self.frame = 0

    def get_rect(self):
        return (self.posX - self.pngSizeX / 2) - self.rectSizeX, (self.posY + self.pngSizeY / 2) - self.rectSizeY, \
               (self.posX - self.pngSizeX / 2) + self.rectSizeX, (self.posY + self.pngSizeY / 2) + self.rectSizeY

    def collideActive(self, opponent):
        if opponent.uiID == 'button':
            self.ui = opponent

    def collideInactive(self, opponent):
        pass

    def update(self):
        self.time += mainframe.frame_time

        if self.time > self.hideTime:
            self.drawCheck = False
        else:
            self.drawCheck = True

        if self.mouseID == 'click' :
            if int(self.frame) >= self.frameMax - 1:
                self.change_ID('normal')
        else:
            TimeToFrameQuantity = self.frameMax * self.actionPerTime * mainframe.frame_time
            self.frame = (self.frame + TimeToFrameQuantity) % self.frameMax


    def handle_events(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.time = 0
            self.posX, self.posY = event.x,  static.canvas_height - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN :
            self.time = 0
            if event.button == SDL_BUTTON_LEFT:
                self.change_ID('click')
                if self.ui != None:
                    self.ui.click()
            if event.button == SDL_BUTTON_RIGHT:
                self.change_ID('gate')
        elif event.type == SDL_MOUSEBUTTONUP:
            self.time = 0
            if event.button == SDL_BUTTON_LEFT:
                self.frame = 1
                if self.ui != None:
                    self.ui.unclick()
            if event.button == SDL_BUTTON_RIGHT:
                self.change_ID('normal')
        #elif event.type == SDL_MOUSEBUTTONDOWN

    def draw(self):
        if self.drawCheck == True:
            Mouse.images[self.mouseID][int(self.frame)].draw(self.posX, self.posY, self.sizeX, self.sizeY)

    def draw_rect(self):
        if self.drawCheck == True:
            draw_rectangle(*self.get_rect())

    def free(self):
        for k in Mouse.images.keys():
            for image in Mouse.images.get(k):
                del image
