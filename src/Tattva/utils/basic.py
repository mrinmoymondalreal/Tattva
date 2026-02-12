import os

cwd = os.path.abspath(os.getcwd())

def joinPath(*args):
  return os.path.join(*args)

def getfontPath(path):
  return os.path.join(cwd, "src", "Tattva", "fonts", path)

def generateId(prefix):
  import random
  import string
  suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
  return f"{prefix}_{suffix}"

def normalize_quad(value, to = 4):
    if isinstance(value, (int, float)):
        return (value,) * to
    elif isinstance(value, (list, tuple)):
        if len(value) == 1:
            return value * to
        elif len(value) == 2:
            return (value[0], value[1], value[0], value[1])
        elif len(value) == 3:
            return (value[0], value[1], value[2], value[1])
        elif len(value) >= 4:
            return tuple(value[:to])
    else:
        raise ValueError("Invalid input for normalize_quad")

def map_value(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
