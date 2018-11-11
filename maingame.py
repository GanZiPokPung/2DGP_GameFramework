import mainframe
import pico2d

import start_scene
import static

pico2d.open_canvas(static.canvas_width, static.canvas_height, sync = True)
mainframe.run(start_scene)
pico2d.clear_canvas()