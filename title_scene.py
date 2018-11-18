import mainframe
from pico2d import *
import stage_scene
from mouse import Mouse

name = "TitleScene"
image = None
mouse = None

def initialize():
    global image
    global mouse
    image = load_image(os.path.join(os.getcwd(), 'resources', 'scene', 'title2.png'))
    mouse = Mouse()
    hide_cursor()

def handle_events():
    global mouse
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) :
            mainframe.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                mainframe.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                mainframe.change_state(stage_scene)
        mouse.handle_event(event)

def update():
    mouse.update()

def draw():
    clear_canvas()
    image.draw(250, 350)
    mouse.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    global image
    global mouse
    del(image)
    mouse.free()
    del(mouse)