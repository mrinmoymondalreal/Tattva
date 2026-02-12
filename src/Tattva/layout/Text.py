from Tattva.layout.Container import Container
from Tattva.utils.draw import measureText, text

class Text(Container):
  def __init__(self, text, **args):
    super().__init__(**args)
    self.set_text(text)
    self.__type__ = "TEXT"

  def set_text(self, text):
    self.text = text
    size = measureText(text, font_size=self.style.font_size, font=self.style.font_family, spacing=self.style.letter_spacing)
    self.set_dimensions(int(size.x), int(size.y))

  def render(self):
    left, top, width, height = self.get_draw_bounds()
    text(
        self.text,
        (left, top),
        font_size=self.style.font_size,
        color=self.style.color,
    )
