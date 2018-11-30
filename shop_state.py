import collision_manager

from ui import *

mouse = None

def initialize():
    global mouse
    # background
    game_world.add_object(Others(250, 350, 1, 1, 'shop_back', 0.7), UIDEFAULT)
    # shop logo
    game_world.add_object(Others(250, 600, 1, 1, 'shop_logo', 1.0), UIDEFAULT)
    # money cap
    # game_world.add_object(Others(400, 570, 1.3, 1.3, 'money_capacity', 1.0), UIDEFAULT)

    # attUpgrade button
    playerAttID = game_world.curtain_object(PLAYER, 0).parsingID
    attUpgradeButton = Button(150, 440, 1, 1, 'default', 'attUpgrade')
    attUpgradeButton.set_numbers(attUpgradeButton.posX + 30, attUpgradeButton.posY - 25, 2, 2, 17, int(playerAttID))
    attUpgradeButton.set_additionalimage(attUpgradeButton.posX, attUpgradeButton.posY + 10, 1, 1, playerAttID, 1)
    attUpgradeButton.additionalImage.setOtherImageToIndex(int(playerAttID))
    game_world.add_object(attUpgradeButton, UIDEFAULT)
    # 가격
    game_world.add_object(Numbers(175, 370, 1.5, 1.5, 17, 1500), UIDEFAULT)

    # lifeUpgrade button
    lifeUpgradeButton = Button(350, 440, 1, 1, 'default', 'lifeUpgrade')
    lifeUpgradeButton.set_additionalimage(lifeUpgradeButton.posX, lifeUpgradeButton.posY, 1, 1, 'posion', 1)
    game_world.add_object(lifeUpgradeButton, UIDEFAULT)
    # 가격
    game_world.add_object(Numbers(368, 370, 1.5, 1.5, 17, 500), UIDEFAULT)

    # magicaUpgrade button
    magicaUpgradeButton = Button(250, 280, 1, 1, 'default', 'magicaUpgrade')
    magicaUpgradeButton.set_additionalimage(magicaUpgradeButton.posX, magicaUpgradeButton.posY, 1, 1, 'magica', 1)
    game_world.add_object(magicaUpgradeButton, UIDEFAULT)
    # 가격
    game_world.add_object(Numbers(275, 210, 1.5, 1.5, 17, 1000), UIDEFAULT)

    # restart button
    game_world.add_object(Button(250, 140, 0.8, 0.8, 'restart', 'resume'), UIDEFAULT)

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

        mouse.handle_events(event)

def update():
    collision_manager.collide_update()

    # ui만 업데이트
    for ui in game_world.get_layer(UIDEFAULT):
        ui.update()

    for ui in game_world.get_layer(UIINGAME):
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
    game_world.clear_layer(UIDEFAULT)