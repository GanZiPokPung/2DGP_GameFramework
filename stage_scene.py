import mainframe
import shop_state
from pico2d import *
from static import *

from map import Map
from player import Player
from monster import *
from boss import *

import game_world
import collision_manager
import result_scene

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

# player
player = None

# monster pattern
monsterpattern = None
monsterSpawnCheck = True

# boss
bossCheck = False

# stage
stage = 1
stageCount = 0
stageCountMax = 5

# debug
rectCheck = False
score = 0
money = 0
bgm = None
bossbgm = None

def initialize():
    global mouse
    # stage
    global stage
    global stageCount
    global stageCountMax
    # spawn
    global monsterSpawnCheck
    global bossCheck
    # map
    global totalmap
    global map1
    global map2
    # player
    global player
    global monsterpattern
    # bgm
    global bgm
    global bossbgm
    # mouse
    mouse = game_world.curtain_object(MOUSE, 0)

    # stage
    stage = 1
    stageCount = 0
    stageCountMax = 5
    # spawn
    monsterpattern = None
    monsterSpawnCheck = True
    bossCheck = False


    # map
    # stage 별로 리스트에 보관
    map1 = [Map(1, 0, 2000, mapSpeed)]
    map2 = [Map(2, 0, 2000, mapSpeed)]
    # 리스트 별로 딕셔너리에 스테이지 번호와 함께 보관
    totalmap = {1: map1, 2: map2}
    # player
    player = Player()
    # monster
    monsterpattern = Monster_Pattern()
    game_world.add_object(player, PLAYER)

    # bgm
    bgm = load_music(os.path.join(os.getcwd(), 'resources', 'sound', 'back', 'stage.mp3'))
    bgm.set_volume(60)
    bgm.repeat_play()

    bossbgm = load_music(os.path.join(os.getcwd(), 'resources', 'sound', 'back', 'boss.mp3'))
    bossbgm.set_volume(30)

def handle_events():
    # 치트키 필요
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            mainframe.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            mainframe.quit()
        # cheats
        cheat_key(event)
        # player
        player.handle_events(event)
        # mouse
        mouse.handle_events(event)

def cheat_key(event):
    global monsterSpawnCheck
    global rectCheck

    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
        monsterSpawnCheck = True
        Monster_Pattern.difficulty += 1
        for map in totalmap.get(2):
            map.speed += 50
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
        mainframe.push_state(shop_state)
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_b):
        game_world.add_object(BossHead(), BOSS)
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_e):
        game_world.clear_layer(MONSTER)
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_m):
        player.hp = 0
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
        game_world.curtain_object(BOSS, 2).attackID = 1
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
        game_world.curtain_object(BOSS, 2).attackID = 2
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
        game_world.curtain_object(BOSS, 2).attackOtherID = 3
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4):
        game_world.curtain_object(BOSS, 2).attackOtherID = 4
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_5):
        game_world.curtain_object(BOSS, 2).attackID = 4
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
        if rectCheck == False:
            rectCheck = True
        else:
            rectCheck = False

def updateStage():
    global stage
    global stage_time
    global stageCount
    global stageCountMax
    global monsterSpawnCheck
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
            boss = BossHead()
            boss.modify_difficulty(Monster_Pattern.difficulty)
            game_world.add_object(boss, BOSS)
            #
            bgm.stop()
            bossbgm.repeat_play()
            bossCheck = True

        elif bossCheck == True:
            # if 보스를 잡으면
            bossLayer = game_world.get_layer(BOSS)
            if len(bossLayer) == 0:
                # 코인이 쏟아지며
                # 코인이 없어지면
                coinLayer = game_world.get_layer(COIN)
                # 상점 등장
                if len(coinLayer) == 0:
                    stage_time += mainframe.frame_time
                    if stage_time > 1.5:
                        bossCheck = False
                        mainframe.push_state(shop_state)
                        stage_time = 0.0

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

    # end check
    if len(game_world.get_layer(PLAYER)) == 0:
        mainframe.change_state(result_scene)

    # update game obj
    for game_object in game_world.all_objects():
        erase = game_object.update()
        if erase == True :
            game_world.remove_object(game_object)



def draw():
    clear_canvas()
    # map
    for map in totalmap.get(currentmap):
        map.draw()

    # game obj
    for game_object in game_world.all_objects():
        game_object.draw()
        # debug
        if rectCheck == True:
            game_object.draw_rect()

    update_canvas()

def pause():
    bgm.stop()

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

    # 맵 이동 속도 증가
    for map in totalmap.get(2):
        map.speed += 50

    # 플레이어 버그
    player.dirX = 0
    player.dirY = 0
    player.velocityX = 0
    player.velocityY = 0

    bgm.play()

def exit():
    bgm.stop()
    # score, money parsing
    result_scene.score = score
    result_scene.money = money
    game_world.clear()
