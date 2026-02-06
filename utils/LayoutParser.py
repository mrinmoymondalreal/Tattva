from html.parser import HTMLParser
import re

# ==========================================
# 1. Helpers for Value Conversion
# ==========================================

def parse_color(value):
    """Converts hex, rgb, or common names to (r, g, b, a)."""
    value = value.strip().lower()
    
    # Hex: #RRGGBB or #RGB
    if value.startswith("#"):
        hex_code = value.lstrip('#')
        if len(hex_code) == 3:
            hex_code = "".join([c*2 for c in hex_code])
        if len(hex_code) == 6:
            r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
            return (r, g, b, 255)
    
    # RGB/RGBA: rgb(255, 0, 0)
    if value.startswith("rgb"):
        nums = re.findall(r'\d+', value)
        if len(nums) >= 3:
            r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
            a = int(nums[3]) if len(nums) > 3 else 255
            return (r, g, b, a)
            
    # Basic Names (Extend as needed)
    colors = {
        "red": (255, 0, 0, 255), "green": (0, 255, 0, 255), "blue": (0, 0, 255, 255),
        "white": (255, 255, 255, 255), "black": (0, 0, 0, 255), "transparent": (0, 0, 0, 0)
    }
    return colors.get(value, (0, 0, 0, 255))

def parse_value(value):
    """
    Smart parser:
    - "10px" -> 10 (int)
    - "10px 20px" -> (10, 20) (tuple)
    - "row" -> "row" (string)
    """
    if not isinstance(value, str): return value
    value = value.strip()
    
    # Check if it's a space-separated list (for padding/margin)
    if " " in value:
        parts = value.split()
        parsed_parts = [parse_value(p) for p in parts]
        # Return tuple if all parts are valid numbers, else keep string
        if all(isinstance(p, (int, float)) for p in parsed_parts):
            return tuple(parsed_parts)
    
    # Check for numbers (remove px, pt, etc)
    clean_val = re.sub(r'[a-zA-Z%]+$', '', value)
    try:
        if "." in clean_val: return float(clean_val)
        return int(clean_val)
    except ValueError:
        return value # Return original string if not a number

def parse_inline_style(style_str):
    """Parses 'color: red; margin: 10px' into a dictionary."""
    styles = {}
    if not style_str: return styles
    
    for item in style_str.split(';'):
        if ':' in item:
            key, val = item.split(':', 1)
            # CSS uses hyphens (background-color), Python uses underscores (background_color)
            py_key = key.strip().replace('-', '_')
            
            # Special check for colors vs numbers
            if "color" in py_key: 
                styles[py_key] = parse_color(val)
            else:
                styles[py_key] = parse_value(val)
    return styles


# ==========================================
# 2. The HTML Parser
# ==========================================

class LayoutParser(HTMLParser):
    def __init__(self, root_cls, div_cls, text_cls, style_cls):
        super().__init__()
        self.root_cls = root_cls
        self.div_cls = div_cls
        self.text_cls = text_cls
        self.style_cls = style_cls
        
        # Keys that belong to Layout/Div __init__, not Style
        self.layout_keys = {
            "width", "height", "min_width", "min_height", 
            "max_width", "max_height", "id", "x", "y"
        }
        
        self.stack = []
        self.root = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        # 1. Extract Styles
        # Get styles from 'style' attribute and merge with any direct style attributes
        style_args = parse_inline_style(attr_dict.pop('style', ''))
        
        # 2. Extract Layout Args
        layout_args = {}
        
        # Check explicit attributes (e.g. <div width="500">)
        for key in list(attr_dict.keys()):
            val = parse_value(attr_dict[key])
            py_key = key.replace('-', '_')
            
            if py_key in self.layout_keys:
                layout_args[py_key] = val
            elif py_key in style_args: 
                # If explicit attribute exists (e.g. direction="row"), overwrite CSS
                style_args[py_key] = val
            else:
                # FUTURE PROOFING: 
                # If we don't know this key, assume it's a Style property
                style_args[py_key] = val

        # 3. Handle CSS Width/Height mapping to Layout Width/Height
        # (CSS width usually overrides attribute width in standard web, 
        # but here they map to the same constructor arg)
        if 'width' in style_args: layout_args['width'] = style_args.pop('width')
        if 'height' in style_args: layout_args['height'] = style_args.pop('height')

        # 4. Create Object
        # Defaults for mandatory args in Div
        w = layout_args.pop("width", 0) # Default to 0 if not found
        h = layout_args.pop("height", 0)
        
        style_obj = self.style_cls(**style_args)
        
        node = None
        if tag == 'root':
            node = self.root_cls(children=[], **layout_args)
            self.root = node
        elif tag == 'div':
            node = self.div_cls(w, h, children=[], styles=style_obj, **layout_args)
        elif tag == 'text' or tag == 'span':
            # Temporary holder, usually text is handled in handle_data
            # But if someone does <Text id="...">
            node = self.div_cls(w, h, children=[], styles=style_obj, **layout_args)
            # We treat spans as Divs in this engine mostly, 
            # unless specific Text class logic is needed for containers.

        if node:
            if self.stack:
                self.stack[-1].children.append(node)
            self.stack.append(node)

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        text_content = data.strip()
        if text_content and self.stack:
            # Create a Text object
            # Note: Text inherits parent style colors usually, but here we pass defaults
            # or you can implement inheritance logic here.
            text_node = self.text_cls(text_content, styles=self.style_cls())
            self.stack[-1].children.append(text_node)

    def parse(self, html_string):
        self.feed(html_string)
        return self.root