from logging import root
from pyray import *

from utils.draw import initDefaults, rect

init_window(800, 450, "Hello")
set_target_fps(60)

initDefaults()

def Render(root):
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)


        if root:
            root.draw()
            
        w = 50 * 4

        # rect(((500//2) - (w//2), (60 - (50//2))), (w, 50), (0, 0, 0, 120))

        end_drawing()

    close_window()
# unload_font(font)
