from logging import root
from pyray import *

from utils.draw import initDefaults, rect

def App(size, title, root):
    width, height = get_screen_width(), get_screen_height()
    w, h = size
    init_window(w, h, title)
    set_target_fps(60)
    initDefaults()
    Render(root())

def Render(root):
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)

        if root:
            root.draw()
            
        end_drawing()

    close_window()
# unload_font(font)
