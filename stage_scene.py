import mainframe
from pico2d import *

from map import Map
from player import Player

# default
name = "StageScene"
image = None
stage_time = 0.0
stage = 0

# map
totalmap = None
currentmap = 1
map1 = None
map2 = None
mapSpeed = 150

#player
player = None


def initialize():
    #map
    global totalmap
    global map1
    global map2
    #player
    global player

    # map
    # stage 별로 리스트에 보관
    map1 = [Map(1, 0, 2000, mapSpeed)]
    map2 = [Map(2, 0, 2000, mapSpeed)]
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
