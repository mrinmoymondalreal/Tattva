from .Layout import Layout
from ..utils.draw import rect, get_mouse_position, get_mouse_button_pressed, get_mouse_button_released, get_key_pressed
from .StyleSheet import Style

class Div(Layout):
    def __init__(self, width, height, children=None, styles=None, **args):
        self.children = children if children is not None else []
        styles = styles or Style(background_color=(0, 0, 0, 255))
        super().__init__(x=0, y=0, width=width, height=height, styles=styles, **args)
        
        self.__type__ = "DIV"
        
        # --- State Tracking ---
        self.is_hovered = False
        self.is_focused = False
        self.is_active = False # True while mouse is held down on this element

        # --- Event Callbacks ---
        # Mouse
        self.onMouseDown = args.get("onMouseDown", None)
        self.onMouseUp = args.get("onMouseUp", None)
        self.onMouseMove = args.get("onMouseMove", None)
        self.onMouseStart = args.get("onMouseStart", None) # Mouse Enter
        self.onMouseEnd = args.get("onMouseEnd", None)     # Mouse Leave
        self.onClick = args.get("onClick", None)
        self.onHover = args.get("onHover", None)
        
        # Keyboard (Only fires if is_focused is True)
        self.onKeyDown = args.get("onKeyDown", None)
        self.onKeyUp = args.get("onKeyUp", None)

    def update(self):
        """
        Updates state and fires events. 
        Returns True if this element consumed the input.
        """
        # 1. Update Children First (Reverse order for Z-index bubbling)
        for child in reversed(self.children):
            if child.update():
                return True # Child consumed the event

        # 2. Geometry & Input Data
        mouse_pos = get_mouse_position()
        x, y = self.getPos()
        w, h = self.getSize()
        
        # Hit Test
        is_inside = (x <= mouse_pos.x <= x + w) and (y <= mouse_pos.y <= y + h)
        
        # --- Mouse Enter / Leave Logic ---
        if is_inside and not self.is_hovered:
            self.is_hovered = True
            if self.onMouseStart: self.onMouseStart(self)
            
        elif not is_inside and self.is_hovered:
            self.is_hovered = False
            if self.onMouseEnd: self.onMouseEnd(self)

        # --- Mouse Move ---
        if self.is_hovered:
            # You might want to check if mouse actually moved here
            if self.onMouseMove: self.onMouseMove(self, mouse_pos)
            if self.onHover: self.onHover(self, True, mouse_pos) # onHover can be used for continuous hover effects
        else:
            if self.onHover: self.onHover(self, False, mouse_pos)
        # --- Mouse Down / Up / Click ---
        if is_inside:
            if get_mouse_button_pressed(): # Left Click Down
                self.is_active = True
                self.is_focused = True  # GAIN FOCUS
                if self.onMouseDown: self.onMouseDown(self)
                
            if get_mouse_button_released() and self.is_active: # Left Click Up
                self.is_active = False
                if self.onMouseUp: self.onMouseUp(self)
                if self.onClick: self.onClick(self) # Full Click (Down+Up inside)
        else:
            # If clicked OUTSIDE, lose focus
            if get_mouse_button_pressed():
                self.is_focused = False

        # --- Keyboard Events (Only if Focused) ---
        if self.is_focused:
            key = get_key_pressed()
            if key != 0: # 0 means no key pressed
                if self.onKeyDown: self.onKeyDown(self, key)
            
            # Note: Raylib doesn't have a perfect "KeyReleased" event for all keys 
            # without checking every key code, but you can check specific keys if needed.

        return self.is_hovered or self.is_focused

    def computeLayout(self, parent=None, index=0):
        # 1. Get base layout from parent
        my_x, my_y, my_w, my_h = super().computeLayout(parent, index)

        pt, pl, pb, pr = self.styles.padding
        
        # Cursor starts at top-left of CONTENT area (inside padding)
        currX = my_x + pl
        currY = my_y + pt
        
        currWidth, currHeight = 0, 0

        for index, child in enumerate(self.children):
            c_mt, c_ml, c_mb, c_mr = child.styles.margin

            # Apply Child's Margin before placing
            if self.styles.direction == "row":
                currX += c_ml
            else:
                currY += c_mt

            # 2. Set Child Absolute Position
            child.setPos(currX, currY)
            
            # 3. Recursively compute child layout
            x, y, w, h = child.computeLayout(self, index)
            
            # 4. Advance Cursor
            if self.styles.direction == "row":
                currX += w + c_mr
                currHeight = max(currHeight, h + c_mt + c_mb) # Track tallest child
                currWidth += w + c_ml + c_mr
            else:
                currY += h + c_mb
                currWidth = max(currWidth, w + c_ml + c_mr)   # Track widest child
                currHeight += h + c_mt + c_mb

        # 5. Set final container size
        self.setSize(currWidth, currHeight)
        
        return self.getPos() + self.getSize()

    def onClick(self, func):
        self.clickFunc = func

    def draw(self):
        # 1. Draw Self
        # Optional: You can now use self.is_hovered to change color!
        draw_color = self.styles.background_color
        # if self.is_hovered: draw_color = self.styles.hover_color

        rect(
            self.getPos(), 
            self.getSize(), 
            color=draw_color, 
            border_color=self.styles.border_color, 
            border_width=self.styles.border_width, 
            border_radius=self.styles.border_radius
        )

        # 2. Draw Children (Normal Order)
        for child in self.children:
            child.draw()