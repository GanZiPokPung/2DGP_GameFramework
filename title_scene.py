import mainframe
from pico2d import *
import stage_scene

name = "TitleScene"
image = None

def initialize():
    global image
    image = load_image(os.path.join(os.getcwd(), 'scene', 'title2.png'))

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

def update():
    delay(0.01)

def draw():
    global image
    clear_canvas()
    image.draw(250, 350)
    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    global image
    del(image)