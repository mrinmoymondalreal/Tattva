from pyray import *

from .utils.draw import initDefaults, rect

width, height = 0, 0

def App(size, title, root):
    global width, height
    w, h = size
    # get_window_scale_dpi()
    # set_config_flags(ConfigFlags.FLAG_WINDOW_HIGHDPI)
    init_window(w, h, title)
    width, height = get_screen_width(), get_screen_height()
    set_target_fps(60)
    initDefaults()
    Render(root())

def handle_mouse_click(root, mouse_x, mouse_y):
    # 1. Ask the root element to find what was clicked
    # 'root' is your top-level Div
    target_element = root.find_element_under_mouse(mouse_x, mouse_y)
    is_mouse_pressed = is_mouse_button_pressed(MOUSE_BUTTON_LEFT)
    is_mouse_released = is_mouse_button_released(MOUSE_BUTTON_LEFT)

    # 2. If we found something, fire the event
    if is_mouse_released and target_element and target_element.on_click:
        target_element.on_click()

# GLOBAL VARIABLE
_last_hovered_element = None

def handle_mouse_move(root, mouse_x, mouse_y, window_width, window_height):
    global _last_hovered_element

    # 1. SANITY CHECK: Is mouse actually inside the window?
    if not (0 <= mouse_x <= window_width and 0 <= mouse_y <= window_height):
        # Mouse is outside. If we were hovering something, leave it.
        if _last_hovered_element and _last_hovered_element.on_mouse_leave:
            _last_hovered_element.on_mouse_leave()

        _last_hovered_element = None
        return # STOP HERE

    # 2. Who is under the mouse?
    current_element = root.find_element_under_mouse(mouse_x, mouse_y)

    # 3. Handle Transitions
    if current_element != _last_hovered_element:

        # LEAVE old
        if _last_hovered_element and _last_hovered_element.on_mouse_leave:
            _last_hovered_element.on_mouse_leave()

        # ENTER new
        if current_element and current_element.on_mouse_enter:
            current_element.on_mouse_enter()

        _last_hovered_element = current_element

def Render(root):
    # Calculate layout once before rendering
    root.calculate_layout()

    while not window_should_close():
      begin_drawing()
      clear_background(WHITE)

      if root:
          root.render()

      end_drawing()

      handle_mouse_click(root, get_mouse_x(), get_mouse_y())
      handle_mouse_move(root, get_mouse_x(), get_mouse_y(), width, height)

    close_window()
# unload_font(font)
