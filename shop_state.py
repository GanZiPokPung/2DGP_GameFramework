import mainframe
import stage_scene
from pico2d import *
from static import *

import game_world
import collision_manager

from ui import *

mouse = None

def initialize():
    global mouse
    # background
    game_world.add_object(Others(250, 350, 1, 1, 'shop_back', 0.7), UITYPE)
    # shop logo
    game_world.add_object(Others(250, 650, 1, 1, 'shop_logo', 1.0), UITYPE)
    # money cap
    game_world.add_object(Others(400, 570, 1.3, 1.3, 'money_capacity', 1.0), UITYPE)
    # default button
    game_world.add_object(Button(200, 400, 1, 1, 'default'), UITYPE)
    game_world.add_object(Number(200, 400, 1, 1, 10), UITYPE)
    mouse = game_world.curtain_object(MOUSE, 0)

def handle_events():
    global mouse
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) :
            mainframe.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                mainframe.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_l):
                mainframe.pop_state()

        mouse.handle_events(event)
def update():
    collision_manager.collide_update()

    for ui in game_world.get_layer(UITYPE):
        ui.update()

    mouse.update()

def draw():
    clear_canvas()

    for map in stage_scene.totalmap.get(stage_scene.currentmap):
        map.draw()

    for game_object in game_world.all_objects():
        game_object.draw()

    mouse.draw()

    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    game_world.clear_layer(UITYPE)