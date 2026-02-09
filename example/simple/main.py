# from pyray import get_char_pressed, get_key_pressed
# import pyray
from Tattva import App, Div, Root, Text, LAYOUT_MODES, Style

def Menu():
  arr = []
  items = ["Home", "About", "Contact", "Blog", "Careers"]

  def onClick(self, item, b = True):
    self.styles.border_radius = (20, 20, 20, 20) if b else (0, 0, 0, 0)
    if b: print(f"Clicked on {item}", self.parent.__ID__)

  col = (186, 143, 187, 255)

  def onHover(self, is_hovered, mouse_pos):
    self.styles.background_color = (186, 203, 187, 255) if is_hovered else col

  for i in range(len(items)):
    arr.append(Div(200, 25,
      styles=Style(
        mode=LAYOUT_MODES["FIXED"],
        background_color=col,
        justify_content="space-between",
        padding=10,
        margin=(0, 0, 10 if i < len(items) - 1 else 0, 0),
        align_items="center"
      ),
      onMouseDown=lambda self, item=items[i]: onClick(self, item),
      onMouseUp=lambda self, item=items[i]: onClick(self, item, False),
      onHover=onHover,
      children=[
        Text(items[i], styles=Style(font_size=30, color=(255, 255, 255, 255))),
        Div(25, 25, styles=Style(background_color=(255, 0, 0, 255), mode=LAYOUT_MODES["FIXED"]))
      ],
    ))
  return arr

def root():
  return Root(children=[
  Div(
    width=800, height=450,
    styles=Style(
      background_color=(255, 200, 200, 100),
      mode=LAYOUT_MODES["FIXED"],
      justify_content="center",
      align_items="center"
    ),
    children=[
      Div(
        width=400, height=200,
        styles=Style(
          background_color=(247, 193, 24, 255),
          padding=10,
          direction="column",
          border_radius=(400 + 200) // 2,
          border_width=10,
          border_color=(0, 0, 255, 255)
        ),
        children=Menu()
      ),
      Div(
        width=400, height=200,
        styles=Style(
          background_color=(247, 193, 24, 255),
          padding=10,
          direction="column",
          margin=(0, 20, 0, 0)
        ),
        children=Menu()
      )
    ]
  )
])

App((800, 450), "Demo App", root)