import mainframe
from pico2d import *
from static import *
import stage_scene
from mouse import Mouse
import game_world
import collision_manager
from ui import Button


name = "TitleScene"
image = None

def initialize():
    global image
    global mouse
    image = load_image(os.path.join(os.getcwd(), 'resources', 'scene', 'title2.png'))
    mouse = Mouse()
    game_world.add_object(mouse, MOUSE)
    game_world.add_object(Button(250, 200, 1.5, 1.5, 'start'), UI)
    hide_cursor()

def handle_events():
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) :
            mainframe.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                mainframe.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                mainframe.change_state(stage_scene)
        mouse.handle_events(event)

def update():
    collision_manager.collide_update()

    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()
    image.draw(250, 350)

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    global image
    global mouse
    del(image)
    game_world.clear_layer(UI)
