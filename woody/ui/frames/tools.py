from .. import style
from ..windows import SettingsWindow
from ..windows import CreateProjectWindow
from ..windows import CreateElementWindow
from ..windows import CreateGroupWindow
from ..windows import CreateBlendWindow
from ..utils.load_icon import load_icon

import os
import customtkinter as ctk
from PIL import Image

class ToolsFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#b59630",
            width=50
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_propagate(False)
        
    def open_create_project(self):
        create_project = CreateProjectWindow(self.parent.winfo_toplevel())
        create_project.run()
        
    def open_create_group(self):
        create_group = CreateGroupWindow(self.parent.winfo_toplevel())
        create_group.run()
        return
    
    def open_create_element(self):
        create_element = CreateElementWindow(self.parent.winfo_toplevel())
        create_element.run()
        
    def open_create_blend(self):
        create_blend = CreateBlendWindow(self.parent.winfo_toplevel())
        create_blend.run()
    
    def open_settings(self):
        settings = SettingsWindow(self.parent.winfo_toplevel()) 
        settings.run()
    
    def create_widgets(self):

        create_project_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "create_project.png")
        create_project_icon = load_icon(create_project_icon_path, 22)

        self.createProjectButton = ctk.CTkButton(
            self.frame,
            image=create_project_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#b59630",
            **style.BUTTON_STYLE,
            
            command=self.open_create_project
        )
        self.createProjectButton.grid(row=0, column=0, padx=0, pady=(5, 3))
        
        # Create Group Button
        create_group_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "create_group.png")
        create_group_icon = load_icon(create_group_icon_path, 28)

        self.createGroupButton = ctk.CTkButton(
            self.frame,
            image=create_group_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#b34555",
            **style.BUTTON_STYLE,
            
            command=self.open_create_group
        )
        self.createGroupButton.grid(row=1, column=0, padx=0, pady=(0, 3), sticky="n")
        

        # Create Element Button
        create_element_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "create_element.png")
        create_element_icon = load_icon(create_element_icon_path, 25)

        self.createElementButton = ctk.CTkButton(
            self.frame,
            image=create_element_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#4d8242",
            **style.BUTTON_STYLE,
            
            command=self.open_create_element
        )
        self.createElementButton.grid(row=2, column=0, padx=0, pady=(0, 3))
        
        # Create Blend Button
        create_blend_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "blender.png")
        create_blend_icon = load_icon(create_blend_icon_path, 23)

        self.createBlendButton = ctk.CTkButton(
            self.frame,
            image=create_blend_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#e97824",
            **style.BUTTON_STYLE,
            
            command=self.open_create_blend
        )
        self.createBlendButton.grid(row=3, column=0, padx=0, pady=(0, 5), sticky="n")
                
                
        # Settings Button
        settings_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "settings.png")
        settings_icon = load_icon(settings_icon_path, 23)

        self.settingsButton = ctk.CTkButton(
            self.frame,
            image=settings_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#5a5a5a",
            **style.BUTTON_STYLE,
            
            command=self.open_settings
        )
        self.settingsButton.grid(row=4, column=0, padx=0, pady=5, sticky="s")

