import mainframe
from pico2d import *
import title_scene

name = "StartScene"
image = None
logo_time = 0.0

def initialize():
    global image
    image = load_image(os.path.join(os.getcwd(),'scene', 'kpu_credit.png'))

def handle_events():
    events = get_events()

def update():
    global logo_time
    if(logo_time > 1.0) :
        logo_time = 0
        mainframe.change_state(title_scene)
    delay(0.01)
    logo_time += 0.01

def draw():
    global image
    clear_canvas()
    image.draw(275, 350)
    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    global image
    del(image)