from layout.Root import Root
from layout.Div import Div
from layout.Text import Text
from layout.StyleSheet import Style, LAYOUT_MODES
from main import Render
from utils.LayoutParser import LayoutParser

# root = Root(children=[
#   Div(100, 100, children=[
#     Div(50, 50, min_width=50, min_height=50, styles = Style(background_color=(255, 0, 0, 255)), children=[
#       Div(20, 20, styles = Style(background_color=(255, 255, 0, 255))),
#       Div(30, 30, styles = Style(background_color=(0, 255, 255, 255))),
#     ]),
#     Div(50, 60, styles = Style(background_color=(0, 255, 0, 255))),
#     Div(60, 70, styles = Style(background_color=(0, 0, 255, 255))),
#   ]),
# ])

# root = Root(children=[
#   Div(500, 120, children=[
#     Div(50, 50, min_width=50, min_height=50, styles = Style(background_color=(255, 0, 0, 255), padding=10), children=[
#       Div(20, 20, styles = Style(background_color=(255, 255, 0, 255))),
#       Div(30, 30, styles = Style(background_color=(0, 255, 255, 255))),
#     ]),
#     Div(50, 60, styles = Style(background_color=(0, 255, 0, 255), margin=(0, 10, 5, 5))),
#     Div(60, 70, styles = Style(background_color=(0, 0, 255, 255))),
#     Text("Hello World", styles=Style(color=(0,0,0,255))),
#     Div(10, 10, children=[
#       Text("Hello World 1", id="focus_text", styles=Style(color=(0,0,0,255)))
#     ], id="text_div", styles=Style(direction="column", padding=10, background_color=(200, 0, 0, 255))),
#   ], styles = Style(mode=LAYOUT_MODES["FIXED"], padding=10, background_color=(200, 200, 200, 255), align_items="bottom", justify_content="right")),
# ])

# root = Root(children=[
#   Div(500, 120, children=[
#     Div(50, 50, styles = Style(background_color=(255, 0, 0, 255))),
#     Div(50, 50, styles = Style(background_color=(255, 255, 0, 255))),
#     Div(50, 50, styles = Style(background_color=(0, 255, 255, 255))),
#     Div(50, 50, styles = Style(background_color=(255, 0, 0, 255))),
#     Div(50, 50, styles = Style(background_color=(255, 255, 0, 255))),
#   ], styles = Style(mode=LAYOUT_MODES["FIXED"], padding=10, background_color=(200, 200, 200, 255), align_items="center", justify_content="center")),
# ])

# Render(root)

html_content = """
<root>
    <div width="500px" height="120" 
         style="padding: 10px; background-color: rgb(200, 200, 200); align-items: bottom; justify-content: right;">
        
        <div width="50" height="50" min_width="50" min_height="50" 
             style="background-color: #FF0000; padding: 10;">
             
             <div width="20" height="20" style="background-color: #FFFF00;"></div>
             <div width="30" height="30" style="background-color: #00FFFF;"></div>
        </div>

        <div width="50" height="60" style="background-color: green; margin: 0 10 5 5;"></div>
        
        <div width="60" height="70" style="background-color: blue;"></div>

        <div width="100" height="20">Hello World</div>

        <div id="text_div" width="10" height="10" 
             style="direction: column; padding: 10px; background-color: #C80000;">
            Hello World 1
        </div>
    </div>
</root>
"""

# 3. Run Parser
parser = LayoutParser(root_cls=Root, div_cls=Div, text_cls=Text, style_cls=Style)
root_obj = parser.parse(html_content)

Render(root_obj)