import mainframe
from pico2d import *

# default
name = "StageScene"
image = None
stage_time = 0.0
stage = 0

# map
totalmap = None
currentmap = 1
map1 = None
map1_posy = 0
map2 = None
map2_posy = 0
mapSpeed = 150

#player
player = None

class Player:
    def __init__(self):
        self.x = 250
        self.y = 50
        self.dirX = 0
        self.dirY = 0
        #status
        self.deadcheck = False
        self.turncheck = False
        #key
        self.pushLcheck = False
        self.pushRcheck = False
        #frame
        self.frameID = 0
        self.frame = 0
        self.reformframe = 0
        #image
        self.image = load_image(os.path.join(os.getcwd(), 'player', 'player.png'))

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                self.dirY += 1
            elif event.key == SDLK_DOWN:
                self.dirY -= 1
            elif event.key == SDLK_LEFT:
                if self.pushRcheck == False:
                    self.turncheck = False
                    self.frameID = 1
                    self.frame = 0
                    self.reformframe = 6
                    self.turncheck = True
                self.dirX -= 1
                self.pushLcheck = True
            elif event.key == SDLK_RIGHT:
                if self.pushLcheck == False:
                    self.turncheck = False
                    self.frameID = 2
                    self.frame = 0
                    self.reformframe = 6
                    self.turncheck = True
                self.dirX += 1
                self.pushRcheck = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                self.dirY -= 1
            if event.key == SDLK_DOWN:
                self.dirY += 1
            elif event.key == SDLK_LEFT:
                if self.pushRcheck == True:
                    self.turncheck = True
                    self.frameID = 2
                    self.frame = 0
                    self.reformframe = 6
                    self.turncheck = True
                else:
                    self.turncheck = False
                self.dirX += 1
                self.pushLcheck = False
            elif event.key == SDLK_RIGHT:
                if self.pushLcheck == True:
                    self.turncheck = True
                    self.frameID = 1
                    self.frame = 0
                    self.reformframe = 6
                    self.turncheck = True
                else:
                    self.turncheck = False
                self.dirX -= 1
                self.pushRcheck = False

        if(self.pushLcheck == True) and (self.pushRcheck == True):
            self.turncheck = False


    def update(self):
        global stage_time
        stage_time += 0.1
        if self.turncheck == True:
            if self.frame < 6:
                self.frame = (self.frame + 1) % 7
        else:
            if self.reformframe == 0:
                self.frameID = 0
                self.frame = (self.frame + 1) % 7
            else:
                self.reformframe = self.reformframe - 2
                self.frame = self.reformframe

        self.y += self.dirY * 5
        self.x += self.dirX * 5

    def draw(self):
        self.image.clip_draw(self.frame * 70, self.frameID * 70, 70, 70, self.x, self.y)
        print(str(self.pushLcheck) + " " + str(self.pushRcheck))
class Map:
    def __init__(self, name, subname, posy):
        self.name = name
        self.subname = subname
        self.width = 500
        self.height = 4000
        # 250
        self.x = self.width / 2
        # 2000
        self.y = posy
        self.pushcheck = False
        self.endCheck = False
        self.image = load_image(os.path.join(os.getcwd(), 'map', 'Stage' + str(name) + '_' + str(subname) + '.png'))

    def update(self, mapList):
        self.y = self.y - (mapSpeed / 100)
        # 맵 이동 구간 체크
        # self.height / 2 = 2000
        # self.width + 2000 => 4000 + 2000 = 6000
        if(self.pushcheck == False) and (self.y < 2000):
            mapList.append(Map(self.name, 1, 6000))
            self.pushcheck = True
        else:
            if self.y < -2500:
                mapList.pop(0)

    def draw(self):
            self.image.draw(self.x, self.y)
            #print(self.y)


def initialize():
    #map
    global totalmap
    global map1
    global map2
    #player
    global player

    #map
    map1 = [Map(1, 0, 2000)]
    map2 = [Map(2, 0, 2000)]
    totalmap = {1:map1, 2:map2}
    #player
    player = Player()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            mainframe.quit()
        #player
        player.handle_events(event)

def update():
    # map
    currentmaplist = totalmap.get(currentmap)
    for map in currentmaplist:
        map.update(currentmaplist)

    #player
    player.update()

    delay(0.015)

def draw():
    clear_canvas()
    # map
    for map in totalmap.get(currentmap):
        map.draw()

    #player
    player.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    pass
