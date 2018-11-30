from static import *

import game_world
import mainframe

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_rect()
    left_b, bottom_b, right_b, top_b = b.get_rect()

    if left_a   > right_b  : return False
    if right_a  < left_b   : return False
    if top_a    < bottom_b : return False
    if bottom_a > top_b    : return False

    return True


def collide_check(groupA, groupB):
    for objA in groupA:
        for objB in groupB:
            if collide(objA, objB) == True:
                objA.collideActive(objB)
                objB.collideActive(objA)

def collide_check_other(groupA, groupB):
    for objA in groupA:
        for objB in groupB:
            if collide(objA, objB) == True:
                objA.collideActive(objB)
                objB.collideActive(objA)
            else:
                objA.collideInactive(objB)
                objB.collideInactive(objA)

def collide_update():
    # player, bullet
    monsterLayer = game_world.get_layer(MONSTER)
    bulletplayerLayer = game_world.get_layer(BULLET_PLAYER)
    playerLayer = game_world.get_layer(PLAYER)
    bulletLayer = game_world.get_layer(BULLET)
    bossLayer = game_world.get_layer(BOSS)
    coinLayer = game_world.get_layer(COIN)
    bulletbossLayer = game_world.get_layer(BOSS_BULLET)
    uiLayer = game_world.get_layer(UIDEFAULT)
    mouseLayer = game_world.get_layer(MOUSE)

    # 몬스터, 플레이어탄환
    collide_check(monsterLayer, bulletplayerLayer)
    # 플레이어, 몬스터탄환
    collide_check(playerLayer, bulletLayer)
    # 플레이어, 코인
    collide_check(playerLayer, coinLayer)
    # 보스, 플레이어탄환
    collide_check(bossLayer, bulletplayerLayer)
    # 플레이어, 보스탄환
    collide_check(playerLayer, bulletbossLayer)
    # ui, 마우스
    collide_check_other(uiLayer, mouseLayer)
    # monster, bullet


