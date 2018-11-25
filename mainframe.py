class GameScene:
    def __init__(self, scene):
        self.initialize = scene.initialize
        self.handle_events = scene.handle_events
        self.update = scene.update
        self.draw = scene.draw
        self.pause = scene.pause
        self.resume = scene.resume
        self.exit = scene.exit

class TestGameScene:
    def __init__(self, name):
        self.name = name

    def initialize(self):
        print("Scene  [%s] initialized" % self.name)

    def handle_events(self):
        print("Scene  [%s] handle_events" % self.name)

    def update(self):
        print("Scene  [%s] update" % self.name)

    def draw(self):
        print("Scene  [%s] draw" % self.name)

    def pause(self):
        print("Scene  [%s] Paused" % self.name)

    def resume(self):
        print("Scene  [%s] Resumed" % self.name)

    def exit(self):
        print("Scene  [%s] Exited" % self.name)

running = None
stack = None

def isLenEmpty(stack):
    if (len(stack) > 0):
        return False
    else:
        return True

def change_state(scene):
    global stack
    if(isLenEmpty(stack) == False):
        stack[-1].exit()
        stack.pop()
    stack.append(scene)
    scene.initialize()

def push_state(scene):
    global stack
    if(len(stack) > 0):
        stack[-1].pause()
    stack.append(scene)
    scene.initialize()

def pop_state():
    global stack
    if(isLenEmpty(stack) == False):
        stack[-1].exit()
        stack.pop()

    if(isLenEmpty(stack) == False):
        stack[-1].resume()

def quit():
    global running
    running = False

import time
frame_time = 0.0

def run(start_scene):
    global running, stack
    running = True
    stack = [start_scene]
    start_scene.initialize()

    global frame_time
    current_time = time.time()
    while(running):
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        #frame_rate = 1.0 / frame_time
        current_time += frame_time

    while(isLenEmpty(stack) == False):
        stack[-1].exit()
        stack.pop()

def game_mainframe():
    start_scene = TestGameScene('StartScene')
    run(start_scene)

if __name__ == '__main__':
    game_mainframe()
