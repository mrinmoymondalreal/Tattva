# from pyray import get_char_pressed, get_key_pressed
# import pyray
from Tattva import App, Div, Style

i = 0

def inc():
  global i
  i += 1
  return i

def root():

  btn_style = Style(
    padding=20,
    background_color=(255, 0, 0, 255),
    justify_content="center",
    align_items="stretch",
    min_width = 300,
    min_height = 300,
    flex_direction="column"
  )

  def on_enter():
      btn_style.background_color = (0, 0, 255, 255)

  def on_leave():
      btn_style.background_color = (200, 200, 200, 255)

  return Div(
    style=btn_style,
    id="main_div",
    on_click=lambda: print("Main Div Clicked!", inc()),
    on_mouse_enter=on_enter,
    on_mouse_leave=on_leave,
    children=[
      Div(
        style=Style(
          width=50,
          height=25,
          background_color=(0, 0, 255, 255),
          # padding=5,
          # margin=5,
          min_width=190, min_height=95,
          justify_content="flex-end",
          align_items="center",
          flex_direction="column",
          gap=20
        ),
        id="main_child_div",
        children=[
          Div(
            id="inner_child",
            style=Style(
              width=25,
              height=25,
              background_color=(255, 255, 0, 255),
            ),
          ),
          Div(
            id="inner_child",
            style=Style(
              width=25,
              height=25,
              background_color=(255, 255, 0, 255),
            ),
          )
        ]
      ),
      Div(
        style=Style(
          width=50,
          height=75,
          background_color=(25, 0, 0, 255),
        ),
        id="second_child_div",
      ),
      Div(
        style=Style(
          width=50,
          height=50,
          background_color=(0, 255, 0, 255),
        ),
      ),
    ]
  )

App((800, 450), "Demo App", root)
