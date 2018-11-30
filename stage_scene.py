import mainframe
import shop_state
from pico2d import *
from static import *

from map import Map
from player import Player
from monster import *
from boss import *
from coin import Coin

import game_world
import collision_manager

# default
name = "StageScene"
image = None
stage_time = 0.0
stage = 0

# mouse
mouse = None

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
monsterSpawnCheck = False

# boss
bossCheck = False

#stage
stage = 1
stageCount = 0
stageCountMax = 10

# debug
rectCheck = True


def initialize():
    global mouse
    #map
    global totalmap
    global map1
    global map2
    #player
    global player
    global monsterpattern

    # mouse
    mouse = game_world.curtain_object(MOUSE, 0)
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
    global mouse
    global monsterSpawnCheck
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            mainframe.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            monsterSpawnCheck = True
            Monster_Pattern.difficulty += 1
            for map in totalmap.get(2):
                map.speed += 50
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            monsterSpawnCheck = True
            Monster_Pattern.difficulty -= 1
            for map in totalmap.get(2):
                map.speed -= 50
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            game_world.add_object(BossHead(), BOSS)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_e):
            game_world.clear_layer(MONSTER)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_m):
            # money
            game_world.add_object(Coin(250, 350, 1.5, 1.5, 1000), COIN)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_l):
            mainframe.push_state(shop_state)
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
        #mouse
        mouse.handle_events(event)

def updateStage():
    global stage
    global stageCount
    global stageCountMax
    global bossCheck
    # stage
    if stageCount > stageCountMax:
        monsterSpawnCheck = False

    # monster spawn
    if monsterSpawnCheck == True:
        spawnCheck = monsterpattern.update()
        if spawnCheck == True:
            stageCount += 1
    else:
        # 몬스터를 모두 잡았으면?
        monsterLayer = game_world.get_layer(MONSTER)

        if len(monsterLayer) == 0 and bossCheck == False:
            # 보스 등장
            game_world.add_object(BossHead(), BOSS)
            bossCheck = True
        else:
            # if 보스를 잡으면
            # 코인이 쏟아지며
            # 코인이 없어지면
            bossLayer = game_world.get_layer(BOSS)
            if len(bossLayer) == 0:
                # 상점 등장
                mainframe.push_state(shop_state)

def update():
    # map
    # 현재 스테이지 리스트를 딕셔너리에서 가져옴

    currentmaplist = totalmap.get(currentmap)
    # list loop
    for map in currentmaplist:
        erase = map.update(currentmaplist)
        if erase == True :
            currentmaplist.remove(map)

    # stage
    updateStage()

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
    # restart 후
    # 몬스터 난이도 증가, 맵 이동속도 증가
    global stage
    global stageCount
    global stageCountMax
    global monsterSpawnCheck

    monsterSpawnCheck = True
    stage += 1
    stageCount = 0
    stageCountMax += 5
    Monster_Pattern.difficulty += 1
    for map in totalmap.get(2):
        map.speed += 50

def exit():
    game_world.clear()
