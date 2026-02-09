import math
from .basic import getfontPath, map_value
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
    print(f"Loading font size: {font_size} {getfontPath('TIMES.TTF')}")
    font = ry.load_font_ex(getfontPath("TIMES.TTF"), font_size, None, 0)
    font_sizes[font_size] = font
  return font_sizes[font_size]

def text(text, position, font_size = DEFAULTS["font_size"], color = DEFAULTS["color"], font = None, spacing = DEFAULTS["spacing"]):
  font = font or initFontSizes(font_size)
  ry.draw_text_ex(font, text, position, font_size, spacing, color)

# def rect(position, size, color=DEFAULTS["color"], border_radius=(0, 0, 0, 0), border_width=0, border_color=ry.BLACK):
#     # 1. Setup Geometry
#     x, y = position
#     w, h = size
#     rtl, rtr, rbl, rbr = border_radius
    
#     # Calculate Center (Hub of the fan)
#     center = (x + w / 2, y + h / 2)
    
#     seg = 8 

#     # 2. Helper: Generate points for one corner
#     def get_corner_points(start_deg, end_deg, radius, corner_center):
#         p = []
#         if radius == 0: return [corner_center]
        
#         for i in range(seg + 1):
#             deg = map_value(i, 0, seg, start_deg, end_deg)
#             rad = math.radians(deg)
#             cx = (math.cos(rad) * radius) + corner_center[0]
#             cy = (math.sin(rad) * radius) + corner_center[1]
#             p.append((cx, cy))
#         return p

#     # 3. Generate Perimeter (Counter-Clockwise Order to fix visibility)
#     # Order: Bottom-Left -> Bottom-Right -> Top-Right -> Top-Left
#     perimeter = []
    
#     # Bottom-Left (180 to 90 degrees) - NOTE: Angles reversed for CCW
#     perimeter.extend(get_corner_points(180, 90, rbl, (x + rbl, y + h - rbl)))
    
#     # Bottom-Right (90 to 0 degrees)
#     perimeter.extend(get_corner_points(90, 0, rbr, (x + w - rbr, y + h - rbr)))

#     # Top-Right (360 to 270 degrees)
#     perimeter.extend(get_corner_points(360, 270, rtr, (x + w - rtr, y + rtr)))

#     # Top-Left (270 to 180 degrees)
#     perimeter.extend(get_corner_points(270, 180, rtl, (x + rtl, y + rtl)))

#     # Close the loop
#     perimeter.append(perimeter[0])

#     # 4. Draw Fill (Triangle Fan)
#     # Ensure color has Alpha channel and is valid
#     if color and len(color) >= 4 and color[3] > 0:
#         # Fan structure: [Center, P1, P2, ... P1]
#         fill_points = [center, *perimeter]
#         ry.draw_triangle_fan(fill_points, len(fill_points), color)

#     # 5. Draw Border
#     if border_width > 0:
#         for i in range(len(perimeter) - 1):
#             ry.draw_line_ex(
#                 perimeter[i], 
#                 perimeter[i+1], 
#                 border_width, 
#                 border_color
#             )

def rect(position, size, color=DEFAULTS["color"], border_radius=(0, 0, 0, 0), border_width=0, border_color=ry.BLACK):
    x, y = position
    w, h = size
    rtl, rtr, rbl, rbr = border_radius

    rtl = max(0, min(rtl, w/2, h/2))
    rtr = max(0, min(rtr, w/2, h/2))
    rbl = max(0, min(rbl, w/2, h/2))
    rbr = max(0, min(rbr, w/2, h/2))

    # --- 1. Draw Fill (Inner Body) ---
    # We use the previous logic for the fill because it works well for solid shapes
    # (re-using the logic from before for the 'fill_points' fan)
    if color and len(color) >= 4 and color[3] > 0:
        center = (x + w / 2, y + h / 2)
        seg = 8
        
        def get_fill_corner(start_deg, end_deg, r, c):
            p = []
            if r == 0: return [c]
            for i in range(seg + 1):
                rad = math.radians(start_deg + (end_deg - start_deg) * (i / seg))
                p.append((c[0] + math.cos(rad) * r, c[1] + math.sin(rad) * r))
            return p

        # Generate perimeter for fill (Counter-Clockwise)
        perimeter = [
            *get_fill_corner(180, 90, rbl, (x + rbl, y + h - rbl)),   # BL
            *get_fill_corner(90, 0, rbr, (x + w - rbr, y + h - rbr)), # BR
            *get_fill_corner(360, 270, rtr, (x + w - rtr, y + rtr)),  # TR
            *get_fill_corner(270, 180, rtl, (x + rtl, y + rtl)),      # TL
            # Close loop
        ]
        perimeter.append(perimeter[0])
        
        ry.draw_triangle_fan([center, *perimeter], len(perimeter) + 1, color)

    # --- 2. Draw Border (Thick & Smooth) ---
    if border_width > 0:
        half_w = border_width / 2
        
        # Raylib draw_ring uses standard degrees (0=Right, 90=Down)
        # We draw 4 rings for the corners and 4 lines for the edges.
        
        # --- A. Draw Corners (Rings) ---
        # Note: draw_ring(center, inner_radius, outer_radius, start_angle, end_angle, segments, color)
        
        # Top-Left (180 to 270)
        if rtl > 0:
            ry.draw_ring((x + rtl, y + rtl), rtl - half_w, rtl + half_w, 180, 270, 16, border_color)
        else:
            # Draw a square corner block if radius is 0
            ry.draw_rectangle(int(x - half_w), int(y - half_w), int(border_width), int(border_width), border_color)

        # Top-Right (270 to 360) (or 270 to 0)
        if rtr > 0:
            ry.draw_ring((x + w - rtr, y + rtr), rtr - half_w, rtr + half_w, 270, 360, 16, border_color)
        else:
            ry.draw_rectangle(int(x + w - half_w), int(y - half_w), int(border_width), int(border_width), border_color)

        # Bottom-Right (0 to 90)
        if rbr > 0:
            ry.draw_ring((x + w - rbr, y + h - rbr), rbr - half_w, rbr + half_w, 0, 90, 16, border_color)
        else:
            ry.draw_rectangle(int(x + w - half_w), int(y + h - half_w), int(border_width), int(border_width), border_color)

        # Bottom-Left (90 to 180)
        if rbl > 0:
            ry.draw_ring((x + rbl, y + h - rbl), rbl - half_w, rbl + half_w, 90, 180, 16, border_color)
        else:
            ry.draw_rectangle(int(x - half_w), int(y + h - half_w), int(border_width), int(border_width), border_color)

        # --- B. Draw Straight Edges ---
        # We connect the "ends" of the rings.
        # draw_line_ex draws a rectangle centered on the line, so it matches the ring thickness perfectly.

        # Top Edge
        ry.draw_line_ex(
            (x + rtl, y), 
            (x + w - rtr, y), 
            border_width, border_color
        )
        
        # Bottom Edge
        ry.draw_line_ex(
            (x + rbl, y + h), 
            (x + w - rbr, y + h), 
            border_width, border_color
        )
        
        # Left Edge
        ry.draw_line_ex(
            (x, y + rtl), 
            (x, y + h - rbl), 
            border_width, border_color
        )
        
        # Right Edge
        ry.draw_line_ex(
            (x + w, y + rtr), 
            (x + w, y + h - rbr), 
            border_width, border_color
        )

def measureText(text, font_size = DEFAULTS["font_size"], font = None, spacing = DEFAULTS["spacing"]):
  font = font or initFontSizes(font_size)
  return ry.measure_text_ex(font, text, font_size, spacing)

def get_mouse_position():
  return ry.get_mouse_position()

def get_mouse_button_pressed():
  return ry.is_mouse_button_pressed(ry.MOUSE_BUTTON_LEFT)

def get_mouse_button_released():
  return ry.is_mouse_button_released(ry.MOUSE_BUTTON_LEFT)

def is_mouse_button_down():
  return ry.is_mouse_button_down(ry.MOUSE_BUTTON_LEFT)

def get_key_pressed():
  return ry.get_key_pressed()

def get_char_pressed():
  return ry.get_char_pressed()

def get_mouse_button_pressed():
  return ry.is_mouse_button_pressed(ry.MOUSE_BUTTON_LEFT)

def get_mouse_button_released():
  return ry.is_mouse_button_released(ry.MOUSE_BUTTON_LEFT)
