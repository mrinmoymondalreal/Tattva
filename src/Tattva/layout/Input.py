from Tattva.layout.Div import Div
from Tattva.layout.Text import Text
from Tattva.layout.Style import Style
from Tattva.utils.draw import rect
import time

class Input(Div):
    def __init__(self, **kwargs):
        # 1. Initialize the container (Div) look
        super().__init__(**kwargs)
        self.__type__ = "INPUT"
        
        # 2. Input State
        self.value = ""
        self.placeholder = kwargs.get("placeholder", "")
        self.is_focused = False
        self.cursor_visible = True
        self.last_blink_time = time.time()
        
        # 3. Callbacks
        self.on_submit = kwargs.get("on_submit", None)
        self.on_change = kwargs.get("on_change", None)

        # 4. Child Text Element (This renders the actual text)
        # We create a style for the text that inherits useful props
        text_style = Style(
            color=self.style.color or (0, 0, 0, 255),
            font_size=self.style.font_size,
            font_family=self.style.font_family
        )
        
        # If value is empty, show placeholder (usually gray)
        display_text = self.placeholder if not self.value else self.value
        if not self.value:
            text_style.color = (150, 150, 150, 255) # Placeholder Grey

        self.text_element = Text(display_text, style=text_style)
        
        # Add the text element as a child so 'Div' renders it automatically
        self.add_child(self.text_element)

        # 5. Bind internal click to handle focus
        # We save the user's on_click to call it later if needed
        self._user_on_click = self.on_click
        self.on_click = self._handle_click
        self._user_on_blur = self.on_blur
        self.on_blur = self._handle_blur

    def _handle_click(self):
        """Sets focus to this input when clicked."""
        self.is_focused = True
        if self._user_on_click:
            self._user_on_click()

    def _handle_blur(self):
        """Called when user clicks somewhere else"""
        self.is_focused = False
        if self._user_on_blur:
            self._user_on_blur()

    def handle_key(self, key, char):
        """
        Main Logic: Updates text based on key press.
        key: The key constant (e.g., 'BACKSPACE', 'RETURN')
        char: The actual typed character (e.g., 'a', 'B', '1')
        """
        if not self.is_focused:
            return

        # Handle Backspace
        if key == "BACKSPACE":
            if len(self.value) > 0:
                self.value = self.value[:-1]

        # Handle Enter
        elif key == "RETURN":
            if self.on_submit:
                self.on_submit(self.value)
            # Optional: Clear focus on enter?
            # self.is_focused = False 

        # Handle Typing
        elif char and len(char) == 1:
            # Simple filter to ensure we only type printable characters
            if char.isprintable():
                self.value += char

        # Update the Visuals
        self._update_text_element()
        
        # Trigger external change event
        if self.on_change:
            self.on_change(self.value)

    def _update_text_element(self):
        """Updates the child text node to match the current state"""
        if not self.value:
            # Show Placeholder
            self.text_element.set_text(self.placeholder)
            self.text_element.style.color = (150, 150, 150, 255)
        else:
            # Show Value
            self.text_element.set_text(self.value)
            self.text_element.style.color = self.style.color or (0, 0, 0, 255)

    def render(self):
        # 1. Render the background Box (Super logic)
        # Optional: Change border color if focused
        original_border = self.style.border_color
        if self.is_focused:
            # Highlight border when focused (e.g., Blue)
            self.style.border_color = (0, 120, 215, 255) 
        
        super().render()
        
        # Restore border color so we don't permanently change it
        self.style.border_color = original_border

        # 2. Render the Cursor (Blinking Line)
        if self.is_focused:
            current_time = time.time()
            if current_time - self.last_blink_time > 0.5: # Blink every 500ms
                self.cursor_visible = not self.cursor_visible
                self.last_blink_time = current_time

            if self.cursor_visible:
                # Calculate Cursor Position
                # We put the cursor right after the text
                txt_left, txt_top, txt_w, txt_h = self.text_element.get_draw_bounds()
                
                # Start cursor at the end of the text
                cursor_x = txt_left + txt_w + 2 # +2px padding
                cursor_y = txt_top
                cursor_h = txt_h if txt_h > 0 else self.style.font_size
                
                # Draw the cursor as a thin rectangle
                rect(
                    (cursor_x, cursor_y), 
                    (2, cursor_h), 
                    color=(0, 0, 0, 255) # Black Cursor
                )