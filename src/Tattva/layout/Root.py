from .Layout import Layout

class Root(Layout):
  def __init__(self, children = []):
    self.children = children
    Layout.__init__(self, x=0, y=0, width=float("inf"), height=float("inf"))

  def draw(self):
    for child in self.children:
      child.computeLayout()

    for child in self.children:
      if hasattr(child, "update"):
        child.update()
      child.draw()