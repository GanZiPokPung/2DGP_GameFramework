from pico2d import *

import game_world

# player Event
UPKEY_DOWN, UPKEY_UP, DOWNKEY_DOWN, DOWNKEY_UP,\
RIGHTKEY_DOWN, RIGHTKEY_UP, LEFTKEY_DOWN, LEFTKEY_UP,\
AKEY_DOWN, AKEY_UP, SKEY_DOWN, SKEY_UP, DKEY_DOWN, DKEY_UP,\
SHIFTKEY_DOWN, SHIFTKEY_UP = range(16)

key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_a): AKEY_DOWN,
    (SDL_KEYDOWN, SDLK_s): SKEY_DOWN,
    (SDL_KEYDOWN, SDLK_d): DKEY_DOWN,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFTKEY_DOWN,
    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHTKEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFTKEY_UP,
    (SDL_KEYUP, SDLK_a): AKEY_UP,
    (SDL_KEYUP, SDLK_s): SKEY_UP,
    (SDL_KEYUP, SDLK_d): DKEY_UP,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFTKEY_UP
}

# player State

class IdleState:

    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class MoveState:

    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class SemiMoveState:

    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

next_state_table = {
    IdleState:{},
    MoveState:{},
    SemiMoveState:{}
}

class Player:
    MoveSpeed = 50 / 10
    BulletTime = 0
    AnimTime = 0
    def __init__(self):
        self.x = 250
        self.y = 50
        self.dirX = 0
        self.dirY = 0
        #status
        self.deadcheck = False
        self.turncheck = False
        #key
        self.pushLcheck = False
        self.pushRcheck = False
        self.pushAttcheck = False
        #frame
        self.frameID = 0
        self.frame = 0
        self.reformframe = 0
        #image
        self.image = load_image(os.path.join(os.getcwd(), 'player', 'player.png'))

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
