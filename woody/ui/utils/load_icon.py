from PIL import Image
import customtkinter as ctk

def load_icon(path, size):
    """
    Load an icon and return a CTkImage ready for use in CustomTkinter widgets
    
    Args:
        path: Path to the image file
        size: Target size (will maintain aspect ratio)
        
    Returns:
        CTkImage object
    """
    image = Image.open(path)
    original_width, original_height = image.size
    
    if original_width > original_height:
        new_width = size
        new_height = int((original_height * size) / original_width)
    else:
        new_height = size
        new_width = int((original_width * size) / original_height)
    

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    return ctk.CTkImage(
        light_image=resized_image,
        dark_image=resized_image,
        size=(new_width, new_height) 
    )