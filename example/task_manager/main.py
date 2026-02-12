from Tattva import App, Div, Text, Style

# --- DESIGN SYSTEM (The Palette) ---
# Modern UI relies on subtle variations of grey, not just Black/White
THEME = {
    "bg_app":      (248, 250, 252, 255), # Very light blue-grey
    "bg_sidebar":  (255, 255, 255, 255), # White
    "bg_card":     (255, 255, 255, 255), # White
    "text_main":   (15, 23, 42, 255),    # Dark Slate
    "text_muted":  (100, 116, 139, 255), # Medium Slate
    "primary":     (79, 70, 229, 255),   # Indigo
    "border":      (226, 232, 240, 255), # Light border
    "success_bg":  (220, 252, 231, 255), # Pastel Green
    "success_txt": (22, 101, 52, 255),   # Dark Green
    "urgent_bg":   (254, 226, 226, 255), # Pastel Red
    "urgent_txt":  (153, 27, 27, 255),   # Dark Red
}

# --- REUSABLE COMPONENTS ---

def SidebarItem(label, is_active=False):
    """A single link in the sidebar"""
    bg = (241, 245, 249, 255) if is_active else (255, 255, 255, 0)
    text_col = THEME["primary"] if is_active else THEME["text_muted"]
    weight = "bold" if is_active else "normal"

    return Div(
        style=Style(
            padding=(10, 15, 10, 15),
            margin=(0, 0, 5, 0),
            border_radius=8,
            background_color=bg,
            width=200,
        ),
        children=[
            Text(label, style=Style(font_size=16, color=text_col, font_weight=weight))
        ]
    )

def Badge(text, type="normal"):
    """A status pill"""
    if type == "urgent":
        bg, col = THEME["urgent_bg"], THEME["urgent_txt"]
    elif type == "success":
        bg, col = THEME["success_bg"], THEME["success_txt"]
    else:
        bg, col = THEME["bg_app"], THEME["text_muted"]

    return Div(
        style=Style(
            padding=(6, 12, 6, 12),
            background_color=bg,
            border_radius=20,
        ),
        children=[
            Text(text, style=Style(font_size=12, color=col, font_weight="bold"))
        ]
    )

def TaskCard(title, subtitle, tag, tag_type="normal", is_checked=False):
    """A beautiful card for a single task"""

    # Visual state for checked items
    opacity = 100 if is_checked else 255
    # Since we don't have opacity prop, we might fake it with text color
    title_col = THEME["text_muted"] if is_checked else THEME["text_main"]

    # The Checkbox visual
    check_bg = THEME["primary"] if is_checked else (0,0,0,0)
    check_border = THEME["primary"] if is_checked else THEME["border"]

    return Div(
        style=Style(
            background_color=THEME["bg_card"],
            padding=20,
            margin=(0, 0, 15, 0),
            border_radius=12,
            border_width=1,
            border_color=THEME["border"],
            flex_direction="row",
            align_items="center",
            justify_content="space-between"
        ),
        children=[
            # Left Group (Checkbox + Texts)
            Div(
                style=Style(flex_direction="row", align_items="center", gap=15),
                children=[
                    # Custom Checkbox
                    Div(
                        style=Style(
                            width=24, height=24,
                            border_width=2,
                            border_color=check_border,
                            border_radius=8,
                            background_color=check_bg,
                            justify_content="center",
                            align_items="center"
                        ),
                        # Render a simple white dot or check if checked
                        children=[Div(style=Style(width=10, height=10, background_color=(255,255,255,255), border_radius=5))] if is_checked else []
                    ),
                    # Text Column
                    Div(
                        style=Style(flex_direction="column", gap=4),
                        children=[
                            Text(title, style=Style(font_size=16, color=title_col, font_weight="bold")),
                            Text(subtitle, style=Style(font_size=13, color=THEME["text_muted"]))
                        ]
                    )
                ]
            ),
            # Right Group (Badge)
            Badge(tag, tag_type)
        ]
    )

# --- MAIN LAYOUT ---

def Sidebar():
    return Div(
        style=Style(
            width=250,
            min_height=600, # Full height
            background_color=THEME["bg_sidebar"],
            padding=30,
            border_width=1,
            # Border right hack: usually border is all around,
            # if your lib supports distinct sides, use border_right_width.
            # If not, we just live with a border or use margin to separate.
            border_color=THEME["border"],
            flex_direction="column"
        ),
        children=[
            Text("Tattva Tasks", style=Style(font_size=22, color=THEME["text_main"], font_weight="bold", margin=(0,0,40,0))),

            Text("MENU", style=Style(font_size=12, color=THEME["text_muted"], margin=(0,0,10,10), letter_spacing=1)),
            SidebarItem("My Day", is_active=True),
            SidebarItem("Important"),
            SidebarItem("Planned"),
            SidebarItem("Assigned to me"),

            Div(style=Style(height=30)), # Spacer

            Text("LISTS", style=Style(font_size=12, color=THEME["text_muted"], margin=(0,0,10,10), letter_spacing=1)),
            SidebarItem("Personal"),
            SidebarItem("Work"),
            SidebarItem("Groceries")
        ]
    )

def MainContent():
    return Div(
        style=Style(
            flex_direction="column",
            padding=40,
            background_color=THEME["bg_app"],
            # Flex grow replacement: ensure it fills remaining width manually for now
            min_width=600
        ),
        children=[
            # Header
            Div(
                style=Style(margin=(0,0,30,0)),
                children=[
                    Text("My Day", style=Style(font_size=32, font_weight="bold", color=THEME["text_main"])),
                    Text("Thursday, October 5th", style=Style(font_size=16, color=THEME["text_muted"], margin=(5,0,0,0)))
                ]
            ),

            # Task List
            TaskCard("Finish the UI Library", "The native render engine needs optimization", "High Priority", "urgent"),
            TaskCard("Design System Meeting", "Sync with the design team at 2 PM", "Work", "normal"),
            TaskCard("Buy Coffee", "We are completely out of beans", "Done", "success", is_checked=True),
            TaskCard("Update Documentation", "Add docstrings to the Style class", "Dev", "normal"),

            # Floating Action Button (New Task)
            Div(
                style=Style(
                    position="absolute",
                    bottom=40, right=40,
                    width=60, height=60,
                    background_color=THEME["text_main"], # Dark button
                    border_radius=20,
                    justify_content="center",
                    align_items="center",
                    # A trick to make it look 3D: a thick bottom border of a darker shade
                    border_width=0,
                ),
                children=[
                    Text("+", style=Style(font_size=30, color=(255,255,255,255)))
                ]
            )
        ]
    )

def root():
    return Div(
        style=Style(
            min_width=900, min_height=600,
            flex_direction="row", # Horizontal Layout for Sidebar + Content
            background_color=THEME["bg_app"]
        ),
        children=[
            Sidebar(),
            MainContent()
        ]
    )

App((900, 600), "Tattva Tasks", root)
