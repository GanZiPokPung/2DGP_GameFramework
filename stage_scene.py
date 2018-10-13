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

#################################################################################################################
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
        # 이동 구현

        # 키를 눌렀다면?
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                self.dirY += 1
            elif event.key == SDLK_DOWN:
                self.dirY -= 1
            elif event.key == SDLK_LEFT:
                # pushRcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
                # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
                if self.pushRcheck == False:
                    self.turncheck = False
                    self.frameID = 1
                    self.frame = 0
                    self.reformframe = 6
                    self.turncheck = True
                #
                self.dirX -= 1
                self.pushLcheck = True
            elif event.key == SDLK_RIGHT:
                # pushLcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
                # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
                if self.pushLcheck == False:
                    self.turncheck = False
                    self.frameID = 2
                    self.frame = 0
                    self.reformframe = 6
                    self.turncheck = True
                #
                self.dirX += 1
                self.pushRcheck = True

        # 키를 떼었다면?
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                self.dirY -= 1
            if event.key == SDLK_DOWN:
                self.dirY += 1
            elif event.key == SDLK_LEFT:
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
                self.dirX += 1
                self.pushLcheck = False

            elif event.key == SDLK_RIGHT:
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
                self.dirX -= 1
                self.pushRcheck = False

        # 동시에 눌렸을때는 그자리에 있는 스프라이트를 재생한다.
        if(self.pushLcheck == True) and (self.pushRcheck == True):
            self.turncheck = False


    def update(self):
        #global stage_time
        #stage_time += 0.1
        if self.turncheck == True:
            # 회전 이동 상태일때
            # 회전 스프라이트 끝 장면에 프레임을 고정
            if self.frame < 6:
                self.frame = (self.frame + 1) % 7
        else:
            # 만약 회전 이동 상태가 아니라면 IDLE 상태로 돌아오는
            # 스프라이트를 재생한다.(프레임을 거꾸로 돌린다)
            if self.reformframe == 0:
                self.frameID = 0
                self.frame = (self.frame + 1) % 7
            else:
                self.reformframe = self.reformframe - 1
                self.frame = self.reformframe

        #이동 계산
        self.y += self.dirY * 5
        self.x += self.dirX * 5

    def draw(self):
        self.image.clip_draw(self.frame * 70, self.frameID * 70, 70, 70, self.x, self.y)
        # print(str(self.pushLcheck) + " " + str(self.pushRcheck))

#################################################################################################################
class Map:
    def __init__(self, name, subname, posy):
        self.name = name
        self.subname = subname
        self.width = 500
        self.height = 4000
        # 250
        self.x = self.width / 2
        # 맵 시작위치 2000
        self.y = posy
        self.pushcheck = False
        self.endCheck = False
        self.image = load_image(os.path.join(os.getcwd(), 'map', 'Stage' + str(name) + '_' + str(subname) + '.png'))

    def update(self, mapList):
        # 스피드에 따라 맵 이동
        self.y = self.y - (mapSpeed / 100)
        # 맵 이동 구간 체크
        # self.height / 2 = 2000
        # self.width + 2000 => 4000 + 2000 = 6000
        # 일정 구간에 다다르면 다음 맵을 리스트에 넣는다.
        if(self.pushcheck == False) and (self.y < 2000):
            mapList.append(Map(self.name, 1, 6000))
            self.pushcheck = True
        else:
        # 캔버스에 벗어난 맵은 리스트에서 제거한다.
            if self.y < -2500:
                mapList.pop(0)

    def draw(self):
        self.image.draw(self.x, self.y)
        #print(self.y)

#################################################################################################################


def initialize():
    #map
    global totalmap
    global map1
    global map2
    #player
    global player

    # map
    # stage 별로 리스트에 보관
    map1 = [Map(1, 0, 2000)]
    map2 = [Map(2, 0, 2000)]
    # 리스트 별로 딕셔너리에 스테이지 번호와 함께 보관
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
    # 현재 스테이지 리스트를 딕셔너리에서 가져옴
    currentmaplist = totalmap.get(currentmap)
    # list loop
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
