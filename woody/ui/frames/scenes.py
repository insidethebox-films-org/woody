from .. import style
from ...tool.event_bus import event_bus
from ..widgets import CTkListbox

from .operations.scenes import get_blends_list, get_blend_versions_list
from .operations.scenes import open_blend_file

import customtkinter as ctk

class ScenesFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
        self.element_id = None
        
        self.open_blend_button.configure(state="disabled")
        
        event_bus.subscribe('browser_selection_changed', self.get_blends)
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
            height=200
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(3, weight=2)
        self.frame.grid_propagate(False)
    
    def get_blends(self, new_browser_selection):

        self.blends_list_box.delete(0, "END")
        self.blend_version_list_box.delete(0, "END")
        
        self.open_blend_button.configure(state="disabled")
        
        # Get data
        blends, self.element_id = get_blends_list(new_browser_selection)

        if not blends:
            self.blends_list_box.insert("END", "No scenes found")
            self.blends_list_box.configure(state="disabled")
            return
        
        self.blends_list_box.configure(state="normal")
        
        # Populate the listbox
        for i, name in enumerate(blends):
            self.blends_list_box.insert(i, name)
            
    
    def get_blend_versions(self, selected):
        
        self.blend_version_list_box.delete(0, "END")
        
        self.open_blend_button.configure(state="disabled")
        
        # Get data
        versions_sorted = get_blend_versions_list(self.element_id, selected)
        
        # Populate the listbox
        for i, version in enumerate(versions_sorted):
            self.blend_version_list_box.insert(i, version) 
     
    def on_version_selected(self, selected):
        if selected:
            self.open_blend_button.configure(state="normal")
        else:
            self.open_blend_button.configure(state="disabled")
            
    def on_open_blend_file(self):
        open_blend_file(self.blends_list_box, self.blend_version_list_box)
            
    def create_widgets(self):
    
        # Header
        self.header_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.header_frame.grid(row=0, columnspan=2, pady=(7, 3), padx=7, sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Scenes:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, pady=7, padx=12, sticky="w")
        
        # Blends listbox
        self.blends_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.get_blend_versions
            )
        self.blends_list_box.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(3,5), padx=5)
        
        # Blend versions title
        self.blend_versions_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.blend_versions_title_frame.grid(row=2, padx=(7,3), pady=(0, 5), sticky="ew")
        self.blend_versions_title_frame.grid_propagate(False)
        
        self.blend_versions_title_label = ctk.CTkLabel(
            self.blend_versions_title_frame,
            text="Scene Versions:",
            **style.SUB_HEADER_LABEL
        )
        self.blend_versions_title_label.grid(row=0, padx=12, sticky="w")
        
        # Blend options title
        self.blend_options_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.blend_options_title_frame.grid(row=2, column=1, padx=(0,7), pady=(0, 5), sticky="ew")
        self.blend_options_title_frame.grid_propagate(False)
        
        self.blend_options_title_label = ctk.CTkLabel(
            self.blend_options_title_frame,
            text="Scene Options:",
            **style.SUB_HEADER_LABEL
        )
        self.blend_options_title_label.grid(row=0, padx=12, sticky="w")
        
        # Blend versions listbox
        self.blend_version_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_version_selected
            )
        self.blend_version_list_box.grid(row=3, column=0, sticky="nsew", pady=(0,5), padx=5)
        
        # Scene options frame
        self.blend_options_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            border_width=2,
            fg_color="transparent",
            height=30
        )
        self.blend_options_frame.grid(row=3, column=1, padx=(0,7), pady=(0, 5), sticky="nsew")
        self.blend_options_frame.grid_propagate(False)
        self.blend_options_frame.grid_columnconfigure(0, weight=1)
        
        # Open scene button
        self.open_blend_button = ctk.CTkButton(
            self.blend_options_frame,
            text="Open Scene",
            **style.BUTTON_STYLE,
            
            command=self.on_open_blend_file
        )
        self.open_blend_button.grid(row=0, padx=7, pady=8, sticky="ew")