import mainframe
from pico2d import *
from static import *
import stage_scene
from mouse import Mouse
import game_world
import collision_manager
from ui import Button
from ui import Number
from ui import Numbers

name = "TitleScene"
image = None
bgm = None

def initialize():
    global image
    global mouse
    global bgm
    image = load_image(os.path.join(os.getcwd(), 'resources', 'scene', 'title2.png'))
    bgm = load_music(os.path.join(os.getcwd(), 'resources', 'sound', 'back', 'title.mp3'))
    bgm.set_volume(40)
    bgm.repeat_play()
    mouse = Mouse()
    game_world.add_object(mouse, MOUSE)
    game_world.add_object(Button(250, 250, 0.4, 0.38, 'start', 'start'), UIDEFAULT)
    game_world.add_object(Button(250, 160, 0.4, 0.38, 'quit', 'quit'), UIDEFAULT)
    hide_cursor()

def handle_events():
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) :
            mainframe.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                mainframe.quit()
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
    bgm.stop()
    game_world.clear_layer(UIDEFAULT)
