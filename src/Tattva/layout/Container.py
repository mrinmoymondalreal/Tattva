from Tattva.layout.Element import Element

class Container(Element):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = kwargs.get("children", [])

  def add_child(self, child):
    self.children.append(child)
    child.parent = self
    child.index = len(self.children) - 1

  def calculate_layout(self, parent=None, index=0):
    pt, pl, pb, pr = self.style.padding
    my_left, my_top, curr_width, curr_height = super().calculate_layout(parent, index)
    curr_pos = (pl, pt)

    my_width, my_height = 0, 0
    _gap_x, _gap_y = self.style.gap

    child_count = len(self.children)

    for index, child in enumerate(self.children):
      is_last_child = index == child_count - 1
      gap_x = 0 if is_last_child else _gap_x
      gap_y = 0 if is_last_child else _gap_y

      child.set_position(*curr_pos)
      left, top, width, height = child.calculate_layout(self, index)
      mt, ml, mb, mr = child.style.margin
      x, y = curr_pos
      if self.style.flex_direction == "row":
        x = x + width + ml + mr + gap_x  # Move right by width + horizontal margins
        my_width += width + ml + mr + gap_x  # Update container width
        my_height = max(my_height, height + mt + mb)  # Update container height
      else:
        y = y + height + mt + mb + gap_y  # Move down by height + vertical margins
        my_height += height + mt + mb + gap_y  # Update container height
        my_width = max(my_width, width + ml + mr)  # Update container width
      curr_pos = (x, y)

    self.set_dimensions(my_width, my_height)  # Account for padding
    return self.get_draw_bounds()

  def get_draw_position(self):
    left, top = super().get_position()

    parent = self.get_parent()

    if not parent: return left, top

    justify = parent.style.justify_content
    align = parent.style.align_items

    direction = parent.style.flex_direction

    parent_left, parent_top = parent.get_draw_position()
    parent_width, parent_height = parent.get_draw_dimensions()

    parent_pt, parent_pl, parent_pb, parent_pr = parent.style.padding
    parent_bound_width, parent_bound_height = parent.bounds["width"], parent.bounds["height"]

    if justify == "center":
      if direction == "row":
        left = left + (parent_width//2 - parent_bound_width//2) - parent_pl  # Center horizontally
      else:
        top = top + (parent_height//2 - parent_bound_height//2) - parent_pt  # Center vertically

    if align == "center":
      if direction == "row":
        top = top + (parent_height//2 - parent_bound_height//2) - parent_pt  # Center vertically
      else:
        left = left + (parent_width//2 - parent_bound_width//2) - parent_pl  # Center horizontally

    if justify == "space-between":
      if len(parent.children) > 1:
        if direction == "row":
          left = left + (self.index * ((parent_width - parent_bound_width - parent_pl - parent_pr) // (len(parent.children) - 1)))
        else:
          top = top + (self.index * ((parent_height - parent_bound_height - parent_pt - parent_pb) // (len(parent.children) - 1)))

    if justify == "flex-end":
      if direction == "row":
        left = left + (parent_width - parent_bound_width - parent_pl - parent_pr)
      else:
        top = top + (parent_height - parent_bound_height - parent_pt - parent_pb)

    if align == "flex-end":
      if direction == "row":
        top = top + (parent_height - parent_bound_height - parent_pt - parent_pb)
      else:
        left = left + (parent_width - parent_bound_width - parent_pl - parent_pr)

    return left + parent_left, top + parent_top

  def get_draw_dimensions(self):
    width, height = self.get_dimensions()
    parent = self.get_parent()
    if parent:
      parent_width, parent_height = parent.get_dimensions()
      p_mt, p_ml, p_mb, p_mr = parent.style.padding
      if parent.style.align_items == "stretch":
        if parent.style.flex_direction == "row":
          height = parent_height - p_mt - p_mb
        else:
          width = parent_width - p_ml - p_mr
    return (width, height)

  def get_draw_bounds(self):
    x, y = self.get_draw_position()
    width, height = self.get_draw_dimensions()
    return (x, y, width, height)

  def find_element_under_mouse(self, x, y):
    """
    Recursively finds the top-most element at coordinates (x, y).
    """
    # 1. Check Children First (Reverse order!)
    # We iterate backwards because the last child is drawn on top (highest Z-order).
    for child in reversed(self.children):
      # Recursive call: Ask the child if the mouse is inside it
      found = child.find_element_under_mouse(x, y)
      if found:
        return found

    # 2. Check Self
    # If no child captured the click, check if it hit this container.
    left, top, width, height = self.get_draw_bounds()

    # Check if (x, y) is inside the rectangle
    if (left <= x <= left + width) and (top <= y <= top + height):
      # Only return self if it actually has a click handler (optional optimization)
      # or you can return self regardless and check for the handler later.
      if self.on_click:
          return self

      # If you want empty divs to block clicks from passing through to elements
      # behind them, return self here even if on_click is None.
      # return self

    return None

  def render(self):
    for child in self.children:
      child.render()
