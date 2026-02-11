from .Layout import Layout
from ..utils.draw import text, measureText
from .StyleSheet import Style

class Text(Layout):
  def __init__(self, text, styles = None, **args):
    styles = styles or Style()
    self.styles = styles
    self.setText(text)
    # self.text = text
    # size = measureText(text, font_size=styles.font_size, font=styles.font, spacing=styles.spacing)
    # width, height = (int(size.x), int(size.y))
    super().__init__(x=0, y=0, width=self.width, height=self.height, styles=styles, **args)
    self.__type__ = "TEXT"

  def setText(self, text):
    self.text = text
    size = measureText(text, font_size=self.styles.font_size, font=self.styles.font, spacing=self.styles.spacing)
    self.width, self.height = (int(size.x), int(size.y))
    
  def draw(self):
    text(
        self.text,
        self.getPos(),
        font_size=self.styles.font_size,
        color=self.styles.color,
    )

