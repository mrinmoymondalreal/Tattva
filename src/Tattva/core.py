from pyray import *

from .utils.draw import initDefaults, rect
from raylib import KEY_KP_ENTER, KEY_BACKSPACE, KEY_ENTER, MOUSE_BUTTON_LEFT

width, height = 0, 0

def App(size, title, root):
    global width, height
    w, h = size
    init_window(w, h, title)
    width, height = get_screen_width(), get_screen_height()
    set_target_fps(60)
    initDefaults()
    Render(root())

focused_element = None

def handle_mouse_click(root, mouse_x, mouse_y):
    global focused_element
    # 1. Ask the root element to find what was clicked
    # 'root' is your top-level Div
    target_element = root.find_element_under_mouse(mouse_x, mouse_y)
    # is_mouse_pressed = is_mouse_button_pressed(MOUSE_BUTTON_LEFT)
    is_mouse_released = is_mouse_button_released(MOUSE_BUTTON_LEFT)

    # 1. Handle Blur (Unfocus old element)
    if focused_element and focused_element != target_element:
        if hasattr(focused_element, "on_blur"):
            print("Blurring", focused_element.__dict__)
            focused_element.on_blur()
        focused_element = None

    # 2. Handle Focus (Focus new element)
    if target_element and target_element.__type__ == "INPUT":
        focused_element = target_element

    # 2. If we found something, fire the event
    if is_mouse_released and target_element and target_element.on_click:
        target_element.on_click()

def handle_keyboard(key, char):
    global focused_element
    if focused_element:
        # Pass the key to the input component!
        focused_element.handle_key(key, char)

# GLOBAL VARIABLE
_last_hovered_element = None

def handle_mouse_move(root, mouse_x, mouse_y):
    global _last_hovered_element

    if not is_cursor_on_screen():
        return

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
        # 1. Mouse Events
        handle_mouse_click(root, get_mouse_x(), get_mouse_y())
        handle_mouse_move(root, get_mouse_x(), get_mouse_y())

        # 2. Keyboard Events (Text Input)
        # Raylib queues characters. We loop until the queue is empty.
        char_code = get_char_pressed()
        while char_code > 0:
            # Convert integer code (e.g., 65) to string (e.g., "A")
            char_str = chr(char_code)
            # Pass to your handler
            handle_keyboard(None, char_str)
            # Get next char
            char_code = get_char_pressed()

        # 3. Keyboard Events (Special Keys)
        # We check specific control keys that your Input component needs
        if is_key_pressed(KEY_BACKSPACE):
            handle_keyboard("BACKSPACE", None)
        
        if is_key_pressed(KEY_ENTER) or is_key_pressed(KEY_KP_ENTER):
            handle_keyboard("RETURN", None)
            
        # Optional: Add arrows or tabs here later if needed
        # if is_key_pressed(KEY_TAB): handle_keyboard("TAB", None)

    close_window()
# unload_font(font)
