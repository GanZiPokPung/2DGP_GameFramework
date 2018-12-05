import mainframe
from pico2d import *
from static import *
import game_world
import collision_manager
from ui import *
from mouse import Mouse

score = 0
money = 0
name = "ResultScene"
image = None
mouse = None
bgm = None

def initialize():
    global image
    global mouse
    global bgm
    image = load_image(os.path.join(os.getcwd(), 'resources', 'scene', 'result.png'))

    # mouse
    mouse = Mouse()
    game_world.add_object(mouse, MOUSE)
    # restart button
    game_world.add_object(Button(250, 100, 0.8, 0.8, 'confirm', 'confirm'), UIDEFAULT)
    # money
    game_world.add_object(Money(320, 450, 1.8, 205, 3, 27, money), UIDEFAULT)
    # score
    game_world.add_object(Numbers(320, 350, 3, 3, 27, score), UIDEFAULT)
    # bgm
    bgm = load_music(os.path.join(os.getcwd(), 'resources', 'sound', 'back', 'result.mp3'))
    bgm.set_volume(40)
    bgm.repeat_play()

def handle_events():
    global mouse
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

    # ui
    for ui in game_world.get_layer(UIDEFAULT):
        ui.update()

    mouse.update()

def draw():
    clear_canvas()
    image.draw(250, 350)

    for game_object in game_world.all_objects():
        game_object.draw()

    mouse.draw()

    update_canvas()

def pause():
    pass

def resume():
    pass

def exit():
    bgm.stop()
    game_world.clear()