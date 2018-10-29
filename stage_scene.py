import mainframe
from pico2d import *

from map import Map
from player import Player
from monster import *

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

#bullet
bullets = []

#monster
monsterpatterns = []
monsters = []

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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            # monsters.append((Warrior(200, 800, 50, 0.5, 0.5, 'Left', 'warrior_other')))
            monsters.append((Bird(200, 800, 5, 2, 2)))
            # monsters.append(Dragon(200, 800, 5, 2, 2))
            # monsters.append(Dragon_Strong(100, 800, 50, 2, 2))
        #player
        player.handle_events(event)

def update():
    # map
    # 현재 스테이지 리스트를 딕셔너리에서 가져옴
    currentmaplist = totalmap.get(currentmap)
    # list loop
    for map in currentmaplist:
        map.update(currentmaplist)

    # player
    player.update()

    # monster
    for monster in monsters:
        erasecheck = monster.update()
        if erasecheck == True:
            monsters.remove(monster)

    # bullet
    for bullet in bullets:
        erasecheck = bullet.update()
        if erasecheck == True:
            bullets.remove(bullet)

    delay(0.015)

def draw():
    clear_canvas()
    # map
    for map in totalmap.get(currentmap):
        map.draw()

    #player
    player.draw()

    # monster
    for monster in monsters:
        monster.draw()

    # bullet
    for bullet in bullets:
        bullet.draw()

    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    pass
