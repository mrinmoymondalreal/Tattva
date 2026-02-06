import os

cwd = os.path.abspath(os.getcwd())

def joinPath(*args):
  return os.path.join(*args)

def getfontPath(path):
  return os.path.join(cwd, "fonts", path)

def generateId(prefix):
  import random
  import string
  suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
  return f"{prefix}_{suffix}"

def normalize_quad(value):
    # Case 1: Single Integer -> All 4 sides same
    if isinstance(value, (int, float)):
        return (value, value, value, value)
    
    # Case 2: Tuple/List handling
    if isinstance(value, (tuple, list)):
        # (Top/Bottom, Left/Right) -> (Top, Right, Bottom, Left)
        if len(value) == 2:
            return (value[0], value[1], value[0], value[1])
        
        # (Top, Right, Bottom, Left) -> Returns as is
        elif len(value) == 4:
            return tuple(value)

    # Fallback (optional)
    return (0, 0, 0, 0)

# print(os.path.join(cwd, "fonts", "TIMES.TTF"))