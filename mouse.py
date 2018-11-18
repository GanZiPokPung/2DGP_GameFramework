from pico2d import *
import mainframe
import static

class Mouse:
    images = None
    frames = None
    def __init__(self):
        self.x, self.y = 0, 0
        if Mouse.images == None:
            self.initialize_images()
        if Mouse.frames == None:
            self.initialize_frames()
        self.pngSizeX, self.pngSizeY = 32, 32
        sizeX, sizeY = 1, 1

        self.sizeX = self.pngSizeX * sizeX
        self.sizeY = self.pngSizeY * sizeY

        self.collideCheck = False
        self.mouseID = 'normal'

        self.frame = 0
        self.frameMax = Mouse.frames.get(self.mouseID)[0]

        self.timePerAction = Mouse.frames.get(self.mouseID)[1]
        self.actionPerTime = 1.0 / self.timePerAction

        self.time = 0

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

    def update(self):
        # self.time += mainframe.frame_time

        if self.mouseID == 'click' :
            if int(self.frame) >= self.frameMax - 1:
                self.change_ID('normal')
        else:
            TimeToFrameQuantity = self.frameMax * self.actionPerTime * mainframe.frame_time
            self.frame = (self.frame + TimeToFrameQuantity) % self.frameMax


    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.x, self.y = event.x,  static.canvas_height - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN :
            if event.button == SDL_BUTTON_LEFT:
                self.change_ID('click')
            if event.button == SDL_BUTTON_RIGHT:
                self.change_ID('gate')
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                self.frame = 1
        #elif event.type == SDL_MOUSEBUTTONDOWN

    def draw(self):
        Mouse.images[self.mouseID][int(self.frame)].draw(self.x, self.y, self.sizeX, self.sizeY)

    def free(self):
        for k in Mouse.images.keys():
            for image in Mouse.images.get(k):
                del image
