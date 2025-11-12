from .ui import *

import customtkinter
import os

class WoodyApp:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        
        self.mainWindow = customtkinter.CTk()
        self.mainWindow.geometry("1300x800")
        self.mainWindow.title("Woody")
        self.mainWindow.configure
        
        # Create icon
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "woodyIcon.ico")
        self.mainWindow.iconbitmap(icon_path)
        
        # Create ui
        self.setup_ui()
    
    def setup_ui(self):
        
        self.mainWindow.grid_rowconfigure(0, weight=0)  
        self.mainWindow.grid_rowconfigure(1, weight=1)
        self.mainWindow.grid_rowconfigure(2, weight=3)
        self.mainWindow.grid_rowconfigure(3, weight=0)

        self.mainWindow.grid_columnconfigure(0, weight=0)
        self.mainWindow.grid_columnconfigure(1, weight=1)
        self.mainWindow.grid_columnconfigure(2, weight=3)
        self.mainWindow.grid_columnconfigure(3, weight=3)
        
        # Header
        self.header_frame = HeaderFrame(self.mainWindow)
        self.header_frame.frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=3, pady=(3, 1))

        # Tools
        self.tools_frame = ToolsFrame(self.mainWindow)
        self.tools_frame.frame.grid(row=1, column=0, rowspan=2, sticky="nswe", padx=(3, 1), pady=3)
        
        # Asset Browser
        self.asset_browser_frame = AssetBrowserFrame(self.mainWindow)
        self.asset_browser_frame.frame.grid(row=1, column=1, columnspan=3, sticky="nswe", padx=3, pady=3)
        
        # Asset Details
        self.asset_details_frame = AssetDetailsFrame(self.mainWindow)
        self.asset_details_frame.frame.grid(row=2, column=1, sticky="nswe", padx=(3, 0), pady=(0, 3))
        
        # Scenes
        self.scenes_frame = ScenesFrame(self.mainWindow)
        self.scenes_frame.frame.grid(row=2, column=2, sticky="nswe", padx=(3, 0), pady=(0, 3))
        
        # Publishes
        self.publishes_frame = PublishesFrame(self.mainWindow)
        self.publishes_frame.frame.grid(row=2, column=3, sticky="nswe", padx=3, pady=(0, 3))

        # Status Bar
        self.status_bar_frame = StatusBarFrame(self.mainWindow)
        self.status_bar_frame.frame.grid(row=3, column=0, columnspan=4, sticky="nswe", padx=3, pady=(0, 3))

    def run(self):
        self.mainWindow.mainloop()
        
__all__ = ['WoodyApp']