from .basic import getfontPath
import pyray as ry

DEFAULTS = {
  "font": None,
  "font_size": 20,
  "spacing": 0,
  "color": ry.BLACK
}

font_sizes = {}

def initDefaults():
  # DEFAULTS["font"] = ry.load_font_ex(getfontPath("TIMES.TTF"), 20, None, 0)
  pass

def initFontSizes(font_size=20):
  font = None
  if font is None:
    font = DEFAULTS["font"]
  if font_size not in font_sizes:
    font = ry.load_font_ex(getfontPath("TIMES.TTF"), font_size, None, 0)
    font_sizes[font_size] = font
  return font_sizes[font_size]

def text(text, position, font_size = DEFAULTS["font_size"], color = DEFAULTS["color"], font = None, spacing = DEFAULTS["spacing"]):
  font = font or initFontSizes(font_size)
  ry.draw_text_ex(font, text, position, font_size, spacing, color)

def rect(position, size, color = DEFAULTS["color"]):
  ry.draw_rectangle(position[0], position[1], size[0], size[1], color)

def measureText(text, font_size = DEFAULTS["font_size"], font = None, spacing = DEFAULTS["spacing"]):
  font = font or initFontSizes(font_size)
  return ry.measure_text_ex(font, text, font_size, spacing)