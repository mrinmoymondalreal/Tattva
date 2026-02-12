from typing import Tuple
from Tattva.utils.basic import normalize_quad


class Style():
  border_color: Tuple[4]

  def __init__(self, **kwargs):
    self.min_width = kwargs.get("min_width", 0)
    self.max_width = kwargs.get("max_width", float("inf"))
    self.min_height = kwargs.get("min_height", 0)
    self.max_height = kwargs.get("max_height", float("inf"))
    self.width = min(max(kwargs.get("width", 0), self.min_width), self.max_width)
    self.height = min(max(kwargs.get("height", 0), self.min_height), self.max_height)
    self.background_color = kwargs.get("background_color", None)
    self.color = kwargs.get("color", None)
    self.font_size = kwargs.get("font_size", 20)
    self.font_family = kwargs.get("font_family", None)
    self.font_weight = kwargs.get("font_weight", None)
    self.letter_spacing = kwargs.get("letter_spacing", 0)
    self.text_align = kwargs.get("text_align", None)
    self.padding = normalize_quad(kwargs.get("padding", 0))
    self.margin = normalize_quad(kwargs.get("margin", 0))
    self.border_width: Tuple[4] = kwargs.get("border_width", None)
    self.border_color = kwargs.get("border_color", (0, 0, 0, 255))
    self.border_radius = normalize_quad(kwargs.get("border_radius", 0))
    self.flex_direction = kwargs.get("flex_direction", "row")
    self.justify_content = kwargs.get("justify_content", None)
    self.align_items = kwargs.get("align_items", None)
    self.gap = normalize_quad(kwargs.get("gap", 0), 2)
    self.flex_wrap = kwargs.get("flex_wrap", None)
    self.position = kwargs.get("position", "relative")
    self.top = kwargs.get("top", None)
    self.left = kwargs.get("left", None)
    self.right = kwargs.get("right", None)
    self.bottom = kwargs.get("bottom", None)
    self.z_index = kwargs.get("z_index", None)
