from .Layout import Layout
from utils.draw import rect, text, measureText
from .StyleSheet import Style

class Text(Layout):
  def __init__(self, text, styles = None, **args):
    styles = styles or Style()
    size = measureText(text, font_size=styles.font_size, font=styles.font, spacing=styles.spacing)
    width, height = (int(size.x), int(size.y))
    super().__init__(x=0, y=0, width=width, height=height, styles=styles, **args)
    self.text = text
    self.__type__ = "TEXT"
    
  def draw(self):
    text(
        self.text,
        self.getPos(),
        font_size=self.styles.font_size,
        color=self.styles.color,
    )

