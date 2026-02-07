from .Layout import Layout
from utils.draw import rect
from .StyleSheet import Style

class Div(Layout):
  def __init__(self, width, height, children = [], styles = None, **args):
    # Ensure styles is initialized if None
    styles = styles or Style(background_color=(0, 0, 0, 255))
    super().__init__(x=0, y=0, width=width, height=height, styles=styles, **args)
    self.children = children
    self.__type__ = "DIV"

  def computeLayout(self, parent=None, index=0):
      my_x, my_y, my_w, my_h = super().computeLayout(parent, index)

      # 1. Get our absolute position to calculate total size later (if needed)
      # But for placing children, we only need RELATIVE coordinates (0,0 is top-left of this div)
      
      pt, pl, pb, pr = self.styles.padding
      mt, ml, mb, mr = self.styles.margin
      
      # Initialize cursor RELATIVE to self (0,0)
      # We do NOT add my_x or parent_x here.
      currX = my_x + pl
      currY = my_y + pt
      
      currWidth, currHeight = 0, 0
      
      # REMOVED: The block that added parent_x/parent_y. 
      # We want child.setPos() to store local coordinates (e.g., x=10), 
      # so getPos() can later do (Parent(100) + Child(10) = 110).

      for index, child in enumerate(self.children):
        c_mt, c_ml, c_mb, c_mr = child.styles.margin

        # Apply Child's Left/Top Margin before placing
        if self.styles.direction == "row":
            currX += c_ml
        else:
            currY += c_mt

        # 2. Place child at current cursor (Relative Coordinate)
        child.setPos(currX, currY)
        
        # 3. Compute child's layout
        x, y, w, h = child.computeLayout(self, index)
        
        # 4. Update Cursor for the NEXT loop iteration
        if self.styles.direction == "row":
            # Move X cursor: Child Width + Margin Right
            currX += w + c_mr
            # Track max height for container size
            currHeight = max(currHeight, h + c_mt + c_mb)
            currWidth += w + c_ml + c_mr # Accumulate width
        else:
            # Move Y cursor: Child Height + Margin Bottom
            currY += h + c_mb
            # Track max width for container size
            currWidth = max(currWidth, w + c_ml + c_mr)
            currHeight += h + c_mt + c_mb # Accumulate height

      # Finally, set the size of this container (Inner content + Padding)
      self.setSize(currWidth, currHeight)
      
      return self.getPos() + self.getSize()
  

  def draw(self):
    if self.__ID__ == "div1": print(self.getPos())
    rect(self.getPos(), self.getSize(), self.styles.background_color)
    for child in self.children:
      child.draw()