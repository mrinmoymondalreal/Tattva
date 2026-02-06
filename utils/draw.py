from .basic import getfontPath
import pyray as ry

print("fontPath", getfontPath("TIMES.TTF"))

DEFAULTS = {
  "font": None,
  "font_size": 20,
  "spacing": 0,
  "color": ry.BLACK
}

def initDefaults():
  DEFAULTS["font"] = ry.load_font_ex(getfontPath("TIMES.TTF"), 20, None, 0)

def text(text, position, font_size = DEFAULTS["font_size"], color = DEFAULTS["color"], font = None, spacing = DEFAULTS["spacing"]):
  if font is None:
    font = DEFAULTS["font"]
  ry.draw_text_ex(font, text, position, font_size, spacing, color)

def rect(position, size, color = DEFAULTS["color"]):
  ry.draw_rectangle(position[0], position[1], size[0], size[1], color)

def measureText(text, font_size = DEFAULTS["font_size"], font = None, spacing = DEFAULTS["spacing"]):
  if font is None:
    font = DEFAULTS["font"]
  return ry.measure_text_ex(font, text, font_size, spacing)