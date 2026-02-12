from Tattva import App, Div, Text, Style

def Menu():
  arr = []
  items = ["Home", "About", "Contact", "Blog", "Careers"]

  col = (186, 143, 187, 255)

  for i in range(len(items)):
    arr.append(Div(
      style=Style(
        min_width=200, min_height=25,
        background_color=col,
        justify_content="space-between",
        padding=10,
        align_items="center"
      ),
      children=[
        Text(items[i], style=Style(font_size=30, color=(255, 255, 255, 255))),
        Div(style=Style(min_height=25, min_width=25, background_color=(255, 0, 0, 255)))
      ],
    ))
  return arr

def root():
  return Div(
    style=Style(
      min_width=800, min_height=450,
      background_color=(255, 200, 200, 100),
      justify_content="center",
      align_items="center",
      gap=20,
    ),
    children=[
      Div(
        style=Style(
          background_color=(247, 193, 24, 255),
          padding=10,
          flex_direction="column",
          border_radius=(400 + 200) // 2,
          # border_width=10,
          # border_color=(0, 0, 255, 255)
        ),
        children=Menu()
      ),
      Div(
        style=Style(
          background_color=(247, 193, 24, 255),
          padding=10,
          flex_direction="column",
          margin=(0, 20, 0, 0)
        ),
        children=Menu()
      )
    ]
  )

App((800, 450), "Demo App", root)
