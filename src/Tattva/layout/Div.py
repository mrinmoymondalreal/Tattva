from Tattva.layout.Container import Container
from Tattva.utils.draw import rect


class Div(Container):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.__type__ = "DIV"

  def render(self):
    left, top, width, height = self.get_draw_bounds()
    border_color = self.style.border_color or (0, 0, 0, 255)
    rect((left, top), (width, height), self.style.background_color or (0, 0, 0, 0), border_color=border_color, border_width=(self.style.border_width or 0), border_radius=self.style.border_radius)
    super().render()
