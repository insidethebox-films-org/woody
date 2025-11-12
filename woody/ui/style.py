# Global color palette
COLORS = {
    "theme": "#F5C317",
    "theme_secondary": "#b49530",
    
    "text": "#EBEBEB",
    "foreground": "#414141",
    "hover": "#1F1F1F",
    
    "success": "#72a343",
    "warning": "#e9883f",
    "danger": "#d13b3b",
    

}

FONTS = {
    "title": ("Arial", 14, "bold"),
    "sub_title": ("Arial", 13, "bold"),
    "body": ("Arial", 12),
    "small": ("Arial", 10, "italic")
}

HEADER_LABEL = {
    "font": FONTS["title"]
}

SUB_HEADER_LABEL = {
    "font": FONTS["sub_title"]
}

BODY_LABEL = {
    "font": FONTS["body"]    
}

BODY_DANGER = {
    "font": FONTS["body"], 
    "text_color": COLORS["danger"]
}

BUTTON_STYLE = {
    "fg_color": COLORS["foreground"],
    "hover_color": COLORS["hover"],
    "text_color": COLORS["text"],
    "corner_radius": 5,
    "font": FONTS["body"]
}

INPUT_DIALOG_STYLE = {
    "button_fg_color": COLORS["foreground"],
    "button_hover_color": COLORS["hover"],
    "button_text_color": COLORS["text"]
}

LIST_BOX_STYLE = {
    "highlight_color":"#575757",
    "hover_color":"#3F3F3F",
    "border_width":2
}
