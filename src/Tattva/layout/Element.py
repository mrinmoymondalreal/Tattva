from Tattva.layout.Style import Style

class Element:
  def __init__(self, **kwargs):
    # Using .get() is safe, but ensure style is always a Style object
    self.style = kwargs.get("style", Style(top=0, left=0, width=0, height=0))
    self.bounds = {"x": 0, "y": 0, "width": 0, "height": 0}
    self.__id__ = kwargs.get("id", None)
    self.parent = None  # Initialize parent to None
    self.index = 0  # Initialize index to 0

    # Mouse
    self.on_click = kwargs.get("on_click", None)
    self.on_mouse_enter = kwargs.get("on_mouse_enter", None) # Hover start
    self.on_mouse_leave = kwargs.get("on_mouse_leave", None) # Hover end
    self.on_scroll = kwargs.get("on_scroll", None)

    # Keyboard / Focus
    self.on_focus = kwargs.get("on_focus", None)
    self.on_blur = kwargs.get("on_blur", None)
    self.on_key_down = kwargs.get("on_key_down", None)
    self.on_input = kwargs.get("on_input", None) # Specifically for text typing

  def calculate_layout(self, parent=None, index=0):
    """Processes the geometry based on parent constraints."""
    self.parent = parent
    self.index = index

    return self.get_position() + self.get_dimensions()

  def get_parent(self):
    """Returns the parent element, if any."""
    return self.parent

  def get_id(self):
    """Returns the element's unique identifier."""
    return self.__id__

  def get_dimensions(self):
    """Returns the current width and height."""
    width, height = self.style.width, self.style.height
    width += self.style.padding[1] + self.style.padding[3]  # left + right padding
    height += self.style.padding[0] + self.style.padding[2]  # top + bottom padding
    return (width, height)

  def set_dimensions(self, width, height):
    """Updates the element's size."""
    self.bounds["width"] = width
    self.bounds["height"] = height
    if width:
      self.style.width = min(max(width, self.style.min_width), self.style.max_width)
    if height:
      self.style.height = min(max(height, self.style.min_height), self.style.max_height)

  def set_position(self, x, y):
    """Moves the element to a specific coordinate."""
    if self.style.position == "static":
      return  # Static elements don't have explicit positions
    self.style.left = x
    self.style.top = y

  def get_position(self):
    """Returns the current (x, y) coordinates."""
    x, y = self.style.left or 0, self.style.top or 0
    return (x, y)

  def update(self):
    """Internal logic/state updates per frame."""
    pass

  def render(self):
    """Outputs the element to the display/canvas."""
    pass
