from pico2d import *
import mainframe
import title_scene
import stage_scene

class UI:
    def __init__(self):
        self.x, self.y = 0, 0
        self.sizeX, self.sizeY = 0, 0
        self.rectSizeX, self.rectSizeY = 0, 0
        self.collideCheck = False
        self.uiID = 0

    def get_rect(self):
        return self.posX - self.rectSizeX, self.posY - self.rectSizeY, \
               self.posX + self.rectSizeX, self.posY + self.rectSizeY

    def collideActive(self, opponent):
        pass

    def update(self):
        pass

    def draw(self):
        pass