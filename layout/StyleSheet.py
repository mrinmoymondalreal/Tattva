from utils.basic import normalize_quad


LAYOUT_MODES = {
  "GROW": 0,
  "FIXED": 1,
}

class Style:
  def __init__(self, **args):
    self.font = args.get("font", None)
    self.font_size = args.get("font_size", 20)
    self.color = args.get("color", (0, 0, 0, 255))  # Default
    self.spacing = args.get("spacing", 0)
    self.background_color = args.get("background_color", (255, 255, 255, 255))  # Default white background
    self.border_color = args.get("border_color", (0, 0, 0, 255))  # Default black border
    self.border_width = args.get("border_width", 0)
    self.align_self = args.get("align_self", None)

    padding = args.get("padding", (0, 0, 0, 0))
    margin = args.get("margin", (0, 0, 0, 0))
    direction = args.get("direction", "row")
    mode = args.get("mode", LAYOUT_MODES["GROW"])
    justify_content = args.get("justify_content", "flex-start")
    align_items = args.get("align_items", "flex-start")


    # margin = (top, right, bottom, left)
    self.margin = normalize_quad(margin)

    # top, right, bottom, left
    self.padding = normalize_quad(padding)

    self.direction = direction
    self.mode = mode

    self.justify_content = justify_content
    self.align_items = align_items
    