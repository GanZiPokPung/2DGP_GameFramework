import mainframe
from pico2d import *
from static import *

from map import Map
from player import Player
from monster import *
from boss import *

import game_world
import collision_manager

# default
name = "StageScene"
image = None
stage_time = 0.0
stage = 0

# map
totalmap = None
currentmap = 2
map1 = None
map2 = None
mapSpeed = 150

#player
player = None

# #bullet
# bullets = []

#
# #monster
# monsterpatterns = []
# monsters = []
monsterpattern = None

# debug
rectCheck = True


def initialize():
    #map
    global totalmap
    global map1
    global map2
    #player
    global player
    global monsterpattern
    # map
    # stage 별로 리스트에 보관
    map1 = [Map(1, 0, 2000, mapSpeed)]
    map2 = [Map(2, 0, 2000, mapSpeed)]
    # 리스트 별로 딕셔너리에 스테이지 번호와 함께 보관
    totalmap = {1:map1, 2:map2}
    # player
    player = Player()
    # monster
    monsterpattern = Monster_Pattern()

    game_world.add_object(player, PLAYER)

def handle_events():
    global rectCheck
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            mainframe.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            monsterpattern.get_monster()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            game_world.add_object(BossHead(), BOSS)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_e):
            game_world.clear_layer(MONSTER)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            game_world.curtain_object(BOSS, 2).attackID = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            game_world.curtain_object(BOSS, 2).attackID = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            game_world.curtain_object(BOSS, 2).attackID = 2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4):
            game_world.curtain_object(BOSS, 2).attackID = 3
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_5):
            game_world.curtain_object(BOSS, 2).attackID = 4
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            if rectCheck == False:
                rectCheck = True
            else:
                rectCheck = False
        #player
        player.handle_events(event)

def update():
    # map
    # 현재 스테이지 리스트를 딕셔너리에서 가져옴
    currentmaplist = totalmap.get(currentmap)
    # list loop
    for map in currentmaplist:
        map.update(currentmaplist)

    # collider Check
    collision_manager.collide_update()

    for game_object in game_world.all_objects():
        erase = game_object.update()
        if erase == True :
            game_world.remove_object(game_object)



    #delay(0.015)

def draw():
    clear_canvas()
    # map
    for map in totalmap.get(currentmap):
        map.draw()

    for game_object in game_world.all_objects():
        game_object.draw()
        # debug
        if rectCheck == True:
            game_object.draw_rect()

    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    game_world.clear()
