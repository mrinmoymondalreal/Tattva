import math
from .basic import getfontPath, normalize_quad, map_value
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

# def rect(position, size, color = DEFAULTS["color"], border_radius = (0, 0, 0, 0), border_width=0, border_color=ry.BLACK):
#   rtl, rtr, rbl, rbr = border_radius

#   x, y = position
#   w, h = size

#   seg = 100
#   points = []

#   # Top Left Arc
#   topLeft = []
#   startAngle = math.radians(180)
#   endAngle = math.radians(270)
#   for i in range(seg + 1):
#     a = map_value(i, 0, seg, startAngle, endAngle)
#     cx = (math.sin(a) * rtl/2) + (x + rtl/2)
#     cy = (math.cos(a) * rtl/2) + (y + rtl/2)
#     topLeft.append((cx, cy))

#     # Top Right Arc
#   topRight = []
#   startAngle = math.radians(90)
#   endAngle = math.radians(180)
#   for i in range(seg + 1):
#     a = map_value(i, 0, seg, startAngle, endAngle)
#     cx = (math.sin(a) * rtr/2) + (x + w - rtr/2)
#     cy = (math.cos(a) * rtr/2) + (y + rtr/2)
#     topRight.append((cx, cy))
  
#   # Bottom Left Arc
#   bottomLeft = []
#   startAngle = math.radians(270)
#   endAngle = math.radians(360)
#   for i in range(seg + 1):
#     a = map_value(i, 0, seg, startAngle, endAngle)
#     cx = (math.sin(a) * rbl/2) + (x + rbl/2)
#     cy = (math.cos(a) * rbl/2) + (y + h - rbl/2)
#     bottomLeft.append((cx, cy))

#   # Bottom Right Arc
#   bottomRight = []
#   startAngle = math.radians(0)
#   endAngle = math.radians(90)
#   for i in range(seg + 1):
#     a = map_value(i, 0, seg, startAngle, endAngle)
#     cx = (math.sin(a) * rbr/2) + (x + w - rbr/2)
#     cy = (math.cos(a) * rbr/2) + (y + h - rbr/2)
#     bottomRight.append((cx, cy))

#   points = [
#     *topLeft,
#     *bottomLeft,
#     *bottomRight,
#     *topRight,
#   ]

#   points.append(points[0]) # Ensure we end at the starting point for a closed shape
#   if color and color[3] > 0:
#     ry.draw_triangle_fan(points, len(points), color)

#   for j in range(len(points) - 1):
#     ry.draw_line_ex(points[j], points[j+1], border_width, border_color)

def rect(position, size, color = DEFAULTS["color"], border_radius = (0, 0, 0, 0), border_width=0, border_color=ry.BLACK):
  rtl, rtr, rbl, rbr = border_radius

  x, y = position
  w, h = size

  seg = 100
  points = []

  # Top Left Arc
  topLeft = []
  startAngle = math.radians(180)
  endAngle = math.radians(270)
  for i in range(seg + 1):
    a = map_value(i, 0, seg, startAngle, endAngle)
    cx = (math.sin(a) * rtl/2) + (x + rtl/2)
    cy = (math.cos(a) * rtl/2) + (y + rtl/2)
    topLeft.append((cx, cy))

    # Top Right Arc
  topRight = []
  startAngle = math.radians(90)
  endAngle = math.radians(180)
  for i in range(seg + 1):
    a = map_value(i, 0, seg, startAngle, endAngle)
    cx = (math.sin(a) * rtr/2) + (x + w - rtr/2)
    cy = (math.cos(a) * rtr/2) + (y + rtr/2)
    topRight.append((cx, cy))
  
  # Bottom Left Arc
  bottomLeft = []
  startAngle = math.radians(270)
  endAngle = math.radians(360)
  for i in range(seg + 1):
    a = map_value(i, 0, seg, startAngle, endAngle)
    cx = (math.sin(a) * rbl/2) + (x + rbl/2)
    cy = (math.cos(a) * rbl/2) + (y + h - rbl/2)
    bottomLeft.append((cx, cy))

  # Bottom Right Arc
  bottomRight = []
  startAngle = math.radians(0)
  endAngle = math.radians(90)
  for i in range(seg + 1):
    a = map_value(i, 0, seg, startAngle, endAngle)
    cx = (math.sin(a) * rbr/2) + (x + w - rbr/2)
    cy = (math.cos(a) * rbr/2) + (y + h - rbr/2)
    bottomRight.append((cx, cy))

  points = [
    *topLeft,
    # Left
    (x, y + h - rbl),
    (x, y + rtl),
    *bottomLeft,
    # Bottom
    (x + w - rbr, y + h),
    (x + rbl, y + h),
    *bottomRight,
    # Right
    (x + w, y + rtr),
    (x + w, y + h - rbr),
    *topRight,
    # Top
    (x + rtl, y),
    (x + w - rtr, y),
  ]

  points.append(points[0]) # Ensure we end at the starting point for a closed shape
  if color and color[3] > 0:
    ry.draw_triangle_fan(points, len(points), color)

  for j in range(len(points) - 1):
    ry.draw_line_ex(points[j], points[j+1], border_width, border_color)

def measureText(text, font_size = DEFAULTS["font_size"], font = None, spacing = DEFAULTS["spacing"]):
  font = font or initFontSizes(font_size)
  return ry.measure_text_ex(font, text, font_size, spacing)

def get_mouse_position():
  return ry.get_mouse_position()

def get_mouse_pressed():
  return ry.is_mouse_button_pressed(ry.MOUSE_BUTTON_LEFT)