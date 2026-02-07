
from layout.StyleSheet import LAYOUT_MODES
from utils.basic import generateId


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
      alignItems = self.parent.styles.align_items
      index = self.index

      changed = []

      justifyContent = self.styles.align_self or justifyContent if parentFlexDirection == "column" else justifyContent
      alignItems = self.styles.align_self or alignItems if parentFlexDirection == "row" else alignItems
      
      if justifyContent == "center":
        if parentFlexDirection == "row": x = x + ((parent_w//2) - (self.parent.saved_width//2))
        else: x = parent_x + (parent_w - my_w) // 2

      if justifyContent == "flex-end":
        if parentFlexDirection == "row": x = x + (parent_w - self.parent.saved_width) - pt - pb
        else: x = parent_x + (parent_w - my_w) - pr

      if justifyContent == "space-between":
        if parentFlexDirection == "row":
          if len(self.parent.children) > 1: x = x + (index * ((parent_w - self.parent.saved_width - pl - pr) // (len(self.parent.children) - 1)))
        else:
          if len(self.parent.children) > 1: y = y + (index * ((parent_h - self.parent.saved_height - pt - pb) // (len(self.parent.children) - 1)))
          changed.append("space-between")

      if alignItems == "center":
        if parentFlexDirection == "column": y = y + ((parent_h//2) - (self.parent.saved_height//2))
        else: y = parent_y + (parent_h - my_h) // 2
        changed.append("align-items-center")

      if alignItems == "flex-end":
        if parentFlexDirection == "column": y = y + (parent_h - self.parent.saved_height) - pt - pb
        else: y = parent_y + (parent_h - my_h) - pb
        changed.append("align-items-flex-end")

    if self.__ID__ == "div1": print(y, changed)

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

