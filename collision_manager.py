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
                objA.collideCheck = True
                objB.collideCheck = True

def collide_update():
    # player, bullet
    monsterLayer = game_world.get_layer(MONSTER)
    bulletplayerLayer = game_world.get_layer(BULLET_PLAYER)
    playerLayer = game_world.get_layer(MONSTER)
    bulletLayer = game_world.get_layer(BULLET_PLAYER)
    collide_check(monsterLayer, bulletplayerLayer)
    collide_check(playerLayer, bulletLayer)
    # monster, bullet


