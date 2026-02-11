
from .StyleSheet import LAYOUT_MODES
from ..utils.basic import generateId


class Layout:
  def __init__(self, x, y, **args):
    self.x = x
    self.y = y
    self.width = args.get("width", float("inf"))
    self.height = args.get("height", float("inf"))

    self.min_width = args.get("min_width", 0)
    self.min_height = args.get("min_height", 0)
    self.max_width = args.get("max_width", float("inf"))
    self.max_height = args.get("max_height", float("inf"))

    self.parent = None

    self.styles = args.get("styles", None)
    self.__ID__ =  args.get("id", generateId(""))

    self.saved_width = self.width
    self.saved_height = self.height

    self.__type__ = None

  def computeLayout(self, parent=None, index = 0):
    self.parent = parent
    self.index = index

    return self.getPos() + self.getSize()
  
  def getPos(self):
    x, y =  self.x, self.y
    my_w, my_h = self.getSize()

    if self.parent:
      parent_x, parent_y = self.parent.getPos()
      parent_w, parent_h = self.parent.getSize()
      pt, pl, pb, pr = self.parent.styles.padding
      parentFlexDirection = self.parent.styles.direction
      justifyContent = self.parent.styles.justify_content
      # align-self overrides align-items for individual items
      alignItems = self.styles.align_self or self.parent.styles.align_items

      # justify-content controls distribution along the MAIN axis (flow direction)
      # align-items controls alignment along the CROSS axis (perpendicular to flow)
      
      if parentFlexDirection == "row":
        # Main axis = X (horizontal), Cross axis = Y (vertical)
        
        # justify-content controls X positioning (main axis)
        if justifyContent == "center":
          x = x + ((parent_w // 2) - (self.parent.saved_width // 2))
        elif justifyContent == "flex-end":
          x = x + (parent_w - self.parent.saved_width) - pl - pr
        elif justifyContent == "space-between":
          if len(self.parent.children) > 1:
            x = x + (self.index * ((parent_w - self.parent.saved_width - pl - pr) // (len(self.parent.children) - 1)))
        
        # align-items controls Y positioning (cross axis)
        if alignItems == "center":
          y = parent_y + (parent_h - my_h) // 2
        elif alignItems == "flex-end":
          y = parent_y + (parent_h - my_h) - pb
        elif alignItems == "flex-start":
          y = parent_y + pt
          
      else:  # column
        # Main axis = Y (vertical), Cross axis = X (horizontal)
        
        # justify-content controls Y positioning (main axis)
        if justifyContent == "center":
          y = y + ((parent_h // 2) - (self.parent.saved_height // 2))
        elif justifyContent == "flex-end":
          y = y + (parent_h - self.parent.saved_height) - pt - pb
        elif justifyContent == "space-between":
          if len(self.parent.children) > 1:
            y = y + (self.index * ((parent_h - self.parent.saved_height - pt - pb) // (len(self.parent.children) - 1)))
        
        # align-items controls X positioning (cross axis)
        if alignItems == "center":
          x = parent_x + (parent_w - my_w) // 2
        elif alignItems == "flex-end":
          x = parent_x + (parent_w - my_w) - pr
        elif alignItems == "flex-start":
          x = parent_x + pl

    return (x, y)
  
  def getSize(self):
    pt, pl, pb, pr = self.styles.padding
    height = self.height + pt + pb
    width = self.width + pl + pr

    if self.parent:
      parentFlexDirection = self.parent.styles.direction
      alignItems = self.parent.styles.align_items
      alignItems = self.styles.align_self or alignItems if parentFlexDirection == "row" else alignItems
      if alignItems == "stretch":
        if parentFlexDirection == "row": height = self.parent.height
        else: width = self.parent.width

    return (width, height)

  def setPos(self, x, y):
    if x:
      self.x = x
    if y:
      self.y = y
  
  def setSize(self, width = None, height = None):
    self.saved_width = width
    self.saved_height = height

    if self.styles.mode == LAYOUT_MODES["FIXED"]:
      return
    
    if width:
      self.width = min(max(width, self.min_width), self.max_width)
    if height:
      self.height = min(max(height, self.min_height), self.max_height)

  def update(self):
    pass